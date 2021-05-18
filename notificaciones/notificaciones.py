import json

import requests

REST_API_KEY = "ODk4NWU1ZDktMTVhNy00ZGU4LTgwYjctYzJmMjliZmJlZTg5"
APP_ID = "ad1d7216-f430-4929-a719-2c31195e798a"

def notificacioInicioSesion(onesignal_id):
    header = {"Content-type":"application/json; charset=utf-8",
              "Authorization":"Basic "+REST_API_KEY}

    print("Onesignal_id >>"+onesignal_id)

    notificacion ={"app_id":APP_ID,
                   "include_player_ids":[onesignal_id],
                   "android-group": "Notificaciones_app",
                   "android_group_message": {"en": "Notificaciones app"},
                   "contents": {"en": "Se ha iniciado session en este dispositivo"},
                   "android_channel_id":"938a5f3d-6796-43b8-9f7d-9340314fe263",
                   "headings":{"en":"Inicio de session"}
                   }
    req = requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(notificacion))
    print(req.status_code, req.reason)
    print(req.content)