import json
import time
import requests
import html
from datetime import datetime

log = ""
log += "{:^10}".format("TIME")
log += "{:^15}".format("SUB")
log += "{:^10}".format("ACCIÓN")
log += "{:^10}".format("ME/CO")
log += "{:^120}".format("NOTICIA")
log += "{:^15}".format("QUIÉN/QUÉ")
log += "{:^15}".format("ESTADO") + "\n"
print(log, end="")
print("-"*200)

last_checked = 0
while True:
    try:
        r = requests.get(f"https://www.meneame.net/backend/sneaker2?time={int(last_checked)}")
        data = json.loads(r.text)
        events = data["events"]
        if len(events) > 0:
            for event in events:
                for k, v in event.items():
                    if type(v) == str:
                        event[k] = html.unescape(v)
                l = ""
                date_time = datetime.fromtimestamp(int(event["ts"]))
                l += date_time.strftime("%H:%M:%S") + " "*3
                l += "{:^15}".format(event["sub_name"].upper())
                l += "{:^10}".format(event["type"])
                l += "{:^10}".format(f'{event["votes"]}/{event["com"]}')
                l += "{:120}".format(event["title"])
                l += "{:^15}".format(event["who"])
                l += "{:^15}".format(event["status"])
                print(l)
                log += l+"\n"
        last_checked = time.time()
    except KeyboardInterrupt:
        print("Writing to log.txt...")
        with open("log.txt", "w") as f:
            f.write(log)
        break
