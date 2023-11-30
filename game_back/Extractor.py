import requests
from env import env

class Extractor:

    def __init__(self):
        self.url = "https://www.cheapshark.com/api/1.0/"

    # main extractor
    def supCheapSharkExtractor(self,path,**kwargs) -> list:
        """
        Comentário teste...
        """ 
        send = self.url + path

        for key,value in kwargs.items():
            if value != None: send += f"{key}={value}"

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
