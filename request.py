import requests

class Request():
    def __init__(self):
        self.apikey = 'qEbvlDxInweeAIjmOzEl9vKKKMrdkvLV'
        self.url = 'http://stub.2xt.com.br/air/search/{}/POA/MAO/2022-06-12'.format(apikey)
        self.username = 'test'
        self.senha = 'tB7vlD'

    def requestApi(self):
        result = requests.get(url=self.url, auth=(self.username, self.senha))
        data = result.json()
        return data