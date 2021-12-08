import requests

class Request():
    def __init__(self, iataOrigem, iataDestino, dataIda, dataVolta=None):
        self.apikey = 'qEbvlDxInweeAIjmOzEl9vKKKMrdkvLV'
        self.iataOrigem = iataOrigem
        self.iataDestino = iataDestino
        self.dataIda = dataIda
        self.dataVolta = dataVolta
        self.username = 'test'
        self.senha = 'tB7vlD'

    def buildUrlRequest(self):

        if self.dataVolta == None:
            url = 'http://stub.2xt.com.br/air/search/{}/{}/{}/{}' \
                .format(self.apikey, self.iataOrigem, self.iataDestino, self.dataIda)
            return url
        else:
            reqIda = 'http://stub.2xt.com.br/air/search/{}/{}/{}/{}' \
                .format(self.apikey, self.iataOrigem, self.iataDestino, self.dataIda)

            reqVolta = 'http://stub.2xt.com.br/air/search/{}/{}/{}/{}'\
                .format(self.apikey, self.iataDestino, self.iataOrigem, self.dataVolta)

            return reqIda, reqVolta


    def requestApi(self):

        url = self.buildUrlRequest()

        if self.dataVolta == None:
            result = requests.get(url, auth=(self.username, self.senha))
            data = {'ida': result.json() if result else None}
            return data

        else:
            req1, req2 = url[0], url[1]
            result = requests.get(url[0], auth=(self.username, self.senha))

            result2 = requests.get(url[1], auth=(self.username, self.senha))

            data = {'ida':result.json() if result else None, 'volta':result2.json() if result else None}

            if data.get('ida') == None or data.get('volta') == None:
                data = False

            return data