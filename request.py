import requests

#os.system('clear')
apikey = 'qEbvlDxInweeAIjmOzEl9vKKKMrdkvLV'

url = 'http://stub.2xt.com.br/air/search/{}/POA/MAO/2022-06-12'.format(apikey)
username = 'test'
senha = 'tB7vlD'

r = requests.get(url=url, auth=(username,senha))

data = r.json()
print(data)
