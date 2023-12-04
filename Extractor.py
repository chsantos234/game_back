import requests
from env import env

# https://store.steampowered.com/api/appdetails?appids={game-steam-id}d&cc=br general game info (best for overview)

# https://itad.docs.apiary.io/#reference/game/prices isthereanydeal documentation
# https://api.isthereanydeal.com # historical low, prices in other places
# https://api.isthereanydeal.com/v01/game/plain/id/?key={api-key}&shop=steam&ids=app/{game-steam-id} # get game plain
# https://api.isthereanydeal.com/v01/game/overview/?key={api-key}&country=BR&shop=steam&ids=app/{game-steam-id} # overview

# https://api.isthereanydeal.com/v01/game/overview/?key=48cf3848edaf5a53d702c5b056b0dcb4be35df34&country=BR&shop=steam&ids=app/675260

# null steam id test on https://www.cheapshark.com/api/1.0/games?title=call%20of%20duty or call of duty
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

    def supIsThereAnyDealExtractor(self,path,**kwargs) -> list: # to do: add key

        send = self.adUrl + path

        for key,value in kwargs.items():
            if value != None: send += f"{key}={value}&"

        return requests.get(send).json()
    
    # deal path

    #def getDealList(self) -> list:
    #    """
    #    incompleto.
    #    """
    #    return self.supCheapSharkExtractor()

    def getDealById(self,id:str = None) -> list:
        """
        Retorna as informações de uma venda específica.
        """
        return self.supCheapSharkExtractor(path="deals?",id=id)
    
    # game path

    def getGameByTheme(self,title:str = None,size:int = 60) -> list: # função inicial de pesquisa de jogo
        """
        Retorna uma lista de jogos baseados em um tema com steam id.
        """
        response = self.supCheapSharkExtractor(path="games?",title=title,size=size)

        response_id = []

        for i in response: 
            if i['steamAppID'] != None: response_id.append(i)

        return response_id

    def getGameOverview(self,appids:str = None) -> dict:
        response = self.supSteamPoweredExtractor(path="appdetails?",appids=appids,cc="br")
        return response
    
    def getGameLowest(self,gameid:str = None) -> dict:
        response = self.supIsThereAnyDealExtractor(path="v01/game/overview/?",key=env("AnyDealKey"),country="BR",shop="steam",ids=f"app/{gameid}")
        return response

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
        return self.supCheapSharkExtractor(paht="stores")



    # verificar necessidade de stores last change

    # alert path

    # verificar necessidade das funções em alert path
