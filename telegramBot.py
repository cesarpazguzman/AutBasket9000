import requests

def telegram_bot_send_text(bot_message, token, chat_id):
    send_text = 'https://api.telegram.org/bot' + token + '/sendMessage?chat_id=' + \
                chat_id + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()


def send_matches_telegram(matches, token, chat_id):
    for match in matches:
        telegram_bot_send_text(get_mensaje(match), token, chat_id)


def get_mensaje(a):
    def get_val(d, key1, key2):
        if key1 not in d: return -1

        return d[key1][key2]

    return """
 ** {0} vs {1} ** 
```
Resultado:{3}, {2}
cuotaPreL:{4}, cuotaPreV:{5}
cuotaLiveL:{6}, cuotaLiveV:{7}
```""" \
        .format(a["Local"], a["Vis"], a["Estado"].replace(" ", ""), a["Resultado"].replace(" ", ""),
                a["cuotaPreviaL"], a["cuotaPreviaV"], a["cuotaVivoL"], a["cuotaVivoV"])