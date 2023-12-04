import requests
from env import env

# https://store.steampowered.com/api/appdetails?appids=apiId&cc=br general game info

# https://itad.docs.apiary.io/#reference/game/prices isthereanydeal documentation
# https://api.isthereanydeal.com # historical low, prices in other places
# https://api.isthereanydeal.com/v01/game/plain/id/?key={api-key}&shop=steam&ids=app/{game-steam-id} # get game plain
# https://api.isthereanydeal.com/v01/game/overview/?key={api-key}&country=BR&shop=steam&ids=app/{game-steam-id} # overview

# null steam id test on https://www.cheapshark.com/api/1.0/games?title=call%20of%20duty or call of duty

# https://www.cheapshark.com/api/1.0/deals?id={id-of-deal}

class Extractor:

    def __init__(self):
        self.csUrl = "https://www.cheapshark.com/api/1.0/"
        self.stUrl = "https://store.steampowered.com/api/"
        self.adUrl = "https://api.isthereanydeal.com/"

    # main extractor
    def supCheapSharkExtractor(self,path,**kwargs) -> list:
        """
        Comentário teste...
        """ 
        send = self.csUrl + path

        for key,value in kwargs.items():
            if value != None: send += f"{key}={value}"

        return requests.get(send).json()
    
    def supSteamPoweredExtractor(self,path,**kwargs) -> list:
        send = self.Url + path

        for key,value in kwargs.items():
            if value != None: send += f"{key}={value}"

    
    def supIsThereAnyDealExtractor(self,path,**kwargs) -> list: # to do: add key

        send = self.adUrl + path

        for key,value in kwargs.items():
            if value != None: send += f"{key}={value}"
    
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
    def getGameByTheme(self,title:str = None,size:int = 60) -> list:
        """
        Retorna uma lista de jogos baseados em um tema.
        """
        return self.supCheapSharkExtractor(path="games?",title=title,size=size)
    
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
