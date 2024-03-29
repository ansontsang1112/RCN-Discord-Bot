import requests
import json


def serverAvailable(serverName=""):
    serverList, count, serverDict = ["HyperCity", "香港伊甸園", "伊織生存伺服器", "創造建築伺服器"], False, {}
    if serverName == "":
        return {"ip": "0.0.0.0", "port": "00000"}
    else:
        if serverName == serverList[0]:
            return {"ip": "10.67.70.25", "port": "64006"}
        elif serverName == serverList[1]:
            return {"ip": "10.67.70.25", "port": "64003"}
        elif serverName == serverList[2]:
            return {"ip": "10.67.70.25", "port": "56010"}
        elif serverName == serverList[3]:
            return {"ip": "194.233.75.62", "port": "20001"}
        else:
            return {"ip": "127.0.0.1", "port": "00000"}


def getServerStatus(serverIP, port):
    if serverIP == "" or port == "":
        return 404
    else:
        params = {"ip": serverIP, "port": port}
        apiUrl = "https://api.hypernology.com/mc/statusChecker.php"
        request = requests.get(apiUrl, params=params)
        if request.status_code == requests.codes.ok:
            data = json.loads(request.text)
            if data["res"]:
                return 200
            else:
                return 502
        else:
            return 500
