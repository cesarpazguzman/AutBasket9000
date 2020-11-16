from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
import scrapper
import concurrent.futures
import rulesManager
import telegramBot

TOKEN = '1097115710:AAGOk1iuEbKtSadxa8sPu8LAdMfnQ7yu-Hk'  # Ponemos nuestro Token generado con el @BotFather
chat_id = "170999676"

# Partidos de baloncesto, con cuota inicial <1.25 y que empiezan perdiendo de >10 en el primer y segundo
# cuarto
if __name__ == '__main__':
    options = Options()
    options.headless = True
    options.add_argument('--blink-settings=imagesEnabled=false')

    driver = webdriver.Chrome("C:/Users/59002272/Downloads/chromedriver_win32/chromedriver.exe", options=options)

    contador = 0
    analizar = scrapper.get_matches_live(driver)
    analizar_eliminar = []
    while True:

        # Cada 30 minutos actualizamos los partidos live
        if contador == 30:
            analizar = scrapper.get_matches_live(driver, analizar_eliminar)
            contador = 0

        partidos = []

        # Recuperamos las estadísticas de los partidos live
        if (len(analizar) == 0): break

        num_workers = int(len(analizar) * 0.1 if len(analizar) > 9 else 1)

        with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
            futures = []
            step = int(len(analizar) / num_workers)
            for i in range(0, len(analizar), step):
                last = i + step if i + step < len(analizar) else len(analizar)
                futures.append(executor.submit(scrapper.get_stats_match_lives, options, analizar[i:last]))

            for future in concurrent.futures.as_completed(futures):
                try:
                    partidos.extend(future.result()[0])
                    analizar_eliminar.extend(future.result()[1])
                except Exception as exc:
                    print('generated an exception: %s' % exc)

        analizar = [x for x in analizar if x not in analizar_eliminar]
        # Aplicamos las reglas

        print(len(analizar_eliminar), analizar_eliminar)
        print(len(analizar), analizar)
        print(len(partidos), partidos)
        # Realizamos el envío al grupo de telegram

        partidos_rules = rulesManager.get_matches_filtered(partidos)

        telegramBot.send_matches_telegram(partidos_rules, TOKEN, chat_id)

        contador += 3
        # time.sleep(180)
