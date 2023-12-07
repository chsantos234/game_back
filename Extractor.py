import requests
import urllib.parse
from env import env
from datetime import datetime

# https://store.steampowered.com/api/appdetails?appids={game-steam-id}d&cc=br general game info (best for overview)

# https://itad.docs.apiary.io/#reference/game/prices isthereanydeal documentation
# https://api.isthereanydeal.com # historical low, prices in other places
# https://api.isthereanydeal.com/v01/game/plain/id/?key={api-key}&shop=steam&ids=app/{game-steam-id} # get game plain
# https://api.isthereanydeal.com/v01/game/overview/?key={api-key}&country=BR&shop=steam&ids=app/{game-steam-id} # overview

# https://www.cheapshark.com/api/1.0/deals?id={id-of-deal}


class Extractor:

    def __init__(self):
        self.csUrl = "https://www.cheapshark.com/api/1.0/"
        self.stUrl = "https://store.steampowered.com/api/"
        self.adUrl = "https://api.isthereanydeal.com/"

    # main extractors
    def supCheapSharkExtractor(self,path,**kwargs) -> list:
        send = self.csUrl + path

        for key,value in kwargs.items():
            if value != None: send += f"{key}={value}&"

        return requests.get(send).json()
    
    def supSteamPoweredExtractor(self,path,**kwargs) -> list:
        send = self.stUrl + path

        for key,value in kwargs.items():
            if value != None: send += f"{key}={value}&"

        return requests.get(send).json()

    def supIsThereAnyDealExtractor(self,path,**kwargs) -> list:

        send = self.adUrl + path

        for key,value in kwargs.items():
            if value != None: send += f"{key}={value}&"

        return requests.get(send).json()

    def getDealById(self,id:str = None) -> list:
        """
        Retorna as informações de uma venda específica.
        """
        return self.supCheapSharkExtractor(path="deals?",id=id)
    
    # game path

    def getGameByTheme(self,title:str = None) -> list:
        """
        Retorna uma lista de jogos baseados em um tema.
        """
        if title: title = urllib.parse.quote(title)
        response = self.supCheapSharkExtractor(path="games?",title=title,size=60)
        response_id = []
        for i in response: 
            if i['steamAppID'] != None: 
                response_id.append(f"{i['external']} - {i['steamAppID']}")

        return response_id

    def getGameOverview(self,appids:str = None) -> dict: # botão 1
        response = self.supSteamPoweredExtractor(path="appdetails?",appids=appids,cc="br")
        return response[appids]["data"]['detailed_description']
    
    def getGameLowest(self,gameid:str = None):
        response = self.supIsThereAnyDealExtractor(path="v01/game/overview/?",key=env("AnyDealKey"),country="BR",shop="steam",ids=f"app/{gameid}")

        print(type(response['data'][f"app/{gameid}"]))

        try:

            store_today = response['data'][f"app/{gameid}"]['price']['store']
            price_today = response['data'][f"app/{gameid}"]['price']['price_formatted']

        except:
            store_today = None
            price_today = None

        store_hist = response['data'][f"app/{gameid}"]['lowest']['store']
        price_hist = response['data'][f"app/{gameid}"]['lowest']['price_formatted']

        price_url = response['data'][f"app/{gameid}"]['urls']['history']

        data_formatada = datetime.utcfromtimestamp(response['data'][f"app/{gameid}"]['lowest']['recorded']).strftime('%d-%m-%Y') # dia do menor preço histórico

        struct = {
            "store_today":store_today,
            "price_today":price_today,
            "store_hist":store_hist,
            "price_hist":price_hist,
            "price_url":price_url,
            "date":data_formatada
        }

        return struct
    
    # https://api.isthereanydeal.com/v01/game/plain/id/?key={key-here}&shop=steam&ids=app/377160
    
    def getGamePlains(self,gameid:str = None): # função auxiliar de retornar nome plano
        response = self.supIsThereAnyDealExtractor(path="v01/game/plain/id/?",key=env("AnyDealKey"),shop="steam",ids=f"app/{gameid}")
        return response

    # https://api.isthereanydeal.com/v01/game/prices/?key={key-here}&plains={game-plains-here}&country=BR

    def getGamePrices(self,gamePlain:str = None): # botão 3
        response = self.supIsThereAnyDealExtractor(path="v01/game/prices/?",key=env("AnyDealKey"),plains=gamePlain,country="BR")
        return response

    # verificar necessidade:

    def getGameByIds(self,ids:str = None) -> list:
        """
        Retorna todas as vendas dos jogos listados. Máximo de 25 jogos.
        """
        return self.supCheapSharkExtractor(path="games?",ids=ids)
    
    # store path

    def getStoreInfo(self) -> list:
        """
        Retorna as informções das lojas presentes na api.
        """
        return self.supCheapSharkExtractor(path="stores")
