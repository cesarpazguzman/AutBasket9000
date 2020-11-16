import time
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver

def check_exists_by_xpath(driver, xpath):
    try:
        return driver.find_element_by_xpath(xpath).text
    except:
        return False


def get_stats_match_lives(options, analizar):
    driver = webdriver.Chrome("C:/Users/59002272/Downloads/chromedriver_win32/chromedriver.exe", options=options)
    res = []
    analizar_eliminar = []
    for url in analizar:
        driver.get(url)
        time.sleep(1)

        c = driver.page_source
        soup = BeautifulSoup(c, "html.parser")

        estado = soup.find(id="flashscore").find_all("span", class_="r")

        if estado:
            estado = estado[1].get_text()

        if '1er Cuarto' not in estado and '2º Cuarto' not in estado:
            analizar_eliminar.append(url)
            continue

        resultado = soup.find(id="event_detail_current_result").get_text()

        print(resultado)

        equipos = soup.find_all("div", {"class": "tname__text"})
        local = equipos[0].find('a').get_text()
        visitante = equipos[1].find('a').get_text()

        print(local, visitante)

        try:
            cuotasLive = soup.find(id="default-live-odds").find_all("span", {"class": "odds value"})
        except:
            cuotasLive = None

        cuotasLiveL = cuotasLive and cuotasLive[0].get_text().replace('\n', '') or -1
        cuotasLiveV = cuotasLive and cuotasLive[1].get_text().replace('\n', '') or -1
        print(cuotasLiveL, cuotasLiveV)
        try:
            cuotas = soup.find(id="default-odds").find_all("span", {"class": "odds value"})
            cuotasL = cuotas and cuotas[0].get_text().replace('\n', '') or -1
            cuotasV = cuotas and cuotas[1].get_text().replace('\n', '') or -1
            print(cuotasL, cuotasV)
            stats = {"Estado": estado, "Local": local, "Vis": visitante, "Resultado": resultado,
                     "cuotaPreviaL": cuotasL,
                     "cuotaPreviaV": cuotasV,
                     "cuotaVivoL": cuotasLiveL,
                     "cuotaVivoV": cuotasLiveV,
                     "ID": url.replace("https://www.flashscore.es/partido/", "").replace("/#estadisticas-del-partido;0",
                                                                                         "")}

            res.append(stats)
        except:
            continue

    driver.quit()

    return res, analizar_eliminar


def get_matches_live(driver, analizar_eliminar=[]):
    driver.get("https://www.flashscore.es/baloncesto/")
    time.sleep(3)
    analizar = []

    c = driver.page_source
    soup = BeautifulSoup(c, "html.parser")
    all = soup.find_all("div", {"class": "event__match"})

    for partido in all:
        if partido.find("img"):
            url = "https://www.flashscore.es/partido/{0}/#resumen-del-partido".format(
                partido.get("id").replace("g_3_", ""))
            if url not in analizar_eliminar:
                analizar.append(url)

    print(len(analizar), analizar)

    return analizar
