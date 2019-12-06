import requests
import json

with open("info.json", "r") as info_file:
    info = json.load(info_file)
    headers = dict()
    for key in info["HEADERS"]:
        value = info["HEADERS"][key]
        headers[key] = value if value != "Bearer " else value + \
            info["SECRET_TOKEN"]


def addPlayer(newPlayer):
    fileContent = getLoadedInfo("player-info.json", all_info=True)

    for i, player in enumerate(fileContent):
        if player["tag"] == newPlayer["tag"]:
            fileContent[i] = newPlayer
            break
    else:
        fileContent.append(newPlayer)

    with open("player-info.json", "w") as playerFile:
        json.dump(fileContent, playerFile, indent=2)


def getURL(sublevel, name, **kwargs):
    with open("links.json", "r") as links_file:
        links = json.load(links_file)
    url = ""
    url += links["base_url"]
    url += links[sublevel]["main"]
    url += links[sublevel][name]
    for argument in links[sublevel]["arguments"]:
        url = url.replace(f"<{argument}>", kwargs[argument])

    return url


def getLoadedInfo(fileName, tag=None, all_info=False):
    with open(fileName, "r") as file:
        fileContent = json.load(file)
    if tag:
        for player in fileContent:
            if player['tag'] == tag:
                return player
        raise NameError("no such tag in file")

    if all_info:
        return fileContent

    return fileContent[0]


def getNewInfo(sublevel, name, headers, **kwargs):
    url = getURL(sublevel, name, **kwargs)
    res = requests.get(url, headers=headers)
    return res.json()


def getPlayerInfo(tag):
    try:
        player = getLoadedInfo("player-info.json", tag=tag)
    except:
        playertag = tag.replace("#", "%23")
        player = getNewInfo("player", "player-info",
                            headers, playertag=playertag)
        addPlayer(player)

    return player


if __name__ == '__main__':
    # res = requests.get(getURL("player", "player-info",
    #                           playertag="%232LCUL2JR"), headers=headers)

    # player = res.json()
    # print(player)

    # player = getNewInfo("player", "player-info",
    #                     headers, playertag="%232LCUL2JR")

    # print(player)

    print(getPlayerInfo("#2LCUL2JR"))
