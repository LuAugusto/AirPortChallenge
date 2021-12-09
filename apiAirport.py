from flask import Flask
from flask_restplus import Api, Resource
from flask import Response
from datetime import datetime
from main import server
from request import Request
from haversine import haversine, Unit
from itertools import product
app, api = server.app, server.api

def combineFlights(data):
    if data.get('volta'):
        dataVolta = data.get('volta').get('options')
        dataIda = data.get('ida').get('options')

        all_combines = list(product(dataIda, dataVolta))

        combinesDict = []

        for item in all_combines:
            arrival_time = item[0].get('arrival_time')
            aircraft = item[0].get('aircraft')
            departure_time = item[0].get('departure_time')
            arrival_time1 = item[1].get('arrival_time')
            aircraft1 = item[1].get('aircraft')
            departure_time1 = item[1].get('departure_time')
            fare = item[0].get('price').get('fare') + item[1].get('price').get('fare')
            total = item[0].get('price').get('total') + item[1].get('price').get('total')
            fees = item[0].get('price').get('fees') + item[1].get('price').get('fees')
            price = {'fare':fare, 'total':total, 'fees':fees}

            result = {'Ida':{'arrival_time':arrival_time, 'aircraft':aircraft, 'departure_time':departure_time},
                      'volta':{ 'arrival_time1':arrival_time1, 'aircraft1':aircraft1, 'departure_time1':departure_time1}, 'precoTotal':price}

            combinesDict.append({'combine':result})

        return combinesDict
    else:
        return False

def priceTicket(item):
   if item.get('volta'):
       for itemValue in item.get('volta').get('options'):
           feesValue = itemValue['price'].get('fees')
           fareValue = itemValue['price'].get('fare')

           price = round((fareValue * 10) / 100)
           feesCalc = round(price if price > 40 else price)
           total = round(fareValue + feesCalc)

           result = {'fare': fareValue, 'total': total, 'fees': feesCalc}

           itemValue['price'] = result

       for itemValue in item.get('ida').get('options'):
           feesValue = itemValue['price'].get('fees')
           fareValue = itemValue['price'].get('fare')

           price = round((fareValue * 10) / 100)
           feesCalc = round(price if price > 40 else price)
           total = round(fareValue + feesCalc)

           result = {'fare': fareValue, 'total': total, 'fees': feesCalc}

           itemValue['price'] = result

       return item

   else:
       for itemValue in item.get('ida').get('options'):
           feesValue = itemValue['price'].get('fees')
           fareValue = itemValue['price'].get('fare')

           price = round((fareValue * 10) / 100)
           feesCalc = round(price if price > 40 else price)
           total = round(fareValue + feesCalc)

           result = {'fare': fareValue, 'total': total, 'fees': feesCalc}

           itemValue['price'] = result

       return item

def metaTicket(item):
    if item.get('volta'):
        summary = item.get('volta').get('summary')
        latFrom = summary.get('from').get('lat')
        lonFrom = summary.get('from').get('lon')
        latTo = summary.get('to').get('lat')
        lonTo = summary.get('to').get('lon')

        summaryIda = item.get('ida').get('summary')
        latFromIda = summary.get('from').get('lat')
        lonFromIda = summary.get('from').get('lon')
        latToIda = summary.get('to').get('lat')
        lonToIda = summary.get('to').get('lon')

        for itemValue in item.get('volta').get('options'):
            arrival_time = str(itemValue.get('arrival_time'))
            departure_time = str(itemValue.get('departure_time'))

            date1 = datetime.strptime(arrival_time, '%Y-%m-%dT%H:%M:%S')
            date2 = datetime.strptime(departure_time, '%Y-%m-%dT%H:%M:%S')

            subDate = str(date1 - date2)
            speedCalc = subDate.split(':',1)

            range = round(haversine((latFrom, lonFrom),(latTo, lonTo)))
            cost_per_km = itemValue['price'].get('fare') / range
            cruise_speed_kmh = round(range / int(speedCalc[0]))

            result = {'cost_per_km': cost_per_km, 'range': range, 'cruise_speed_kmh': cruise_speed_kmh}

            itemValue['meta'] = result

        for itemValue in item.get('ida').get('options'):
            arrival_time = str(itemValue.get('arrival_time'))
            departure_time = str(itemValue.get('departure_time'))

            date1 = datetime.strptime(arrival_time, '%Y-%m-%dT%H:%M:%S')
            date2 = datetime.strptime(departure_time, '%Y-%m-%dT%H:%M:%S')

            subDate = str(date1 - date2)
            speedCalc = subDate.split(':',1)

            range = round(haversine((latFrom, lonFrom),(latTo, lonTo)))
            cost_per_km = itemValue['price'].get('fare') / range
            cruise_speed_kmh = round(range / int(speedCalc[0]))

            result = {'cost_per_km': cost_per_km, 'range': range, 'cruise_speed_kmh': cruise_speed_kmh}

            itemValue['meta'] = result

        return item

    else:
        summaryIda = item.get('ida').get('summary')
        latFromIda = summaryIda.get('from').get('lat')
        lonFromIda = summaryIda.get('from').get('lon')
        latToIda = summaryIda.get('to').get('lat')
        lonToIda = summaryIda.get('to').get('lon')

        for itemValue in item.get('ida').get('options'):
            arrival_time = str(itemValue.get('arrival_time'))
            departure_time = str(itemValue.get('departure_time'))

            date1 = datetime.strptime(arrival_time, '%Y-%m-%dT%H:%M:%S')
            date2 = datetime.strptime(departure_time, '%Y-%m-%dT%H:%M:%S')

            subDate = str(date1 - date2)
            speedCalc = subDate.split(':',1)

            range = round(haversine((latFromIda, lonFromIda),(latToIda, lonToIda)))
            cost_per_km = itemValue['price'].get('fare') / range
            cruise_speed_kmh = round(range / int(speedCalc[0]))

            result = {'cost_per_km': cost_per_km, 'range': range, 'cruise_speed_kmh': cruise_speed_kmh}

            itemValue['meta'] = result

        return item

def verifyIata(dataIda, dataVolta):
    date1 = datetime.strptime(dataIda, '%Y-%m-%d').date()
    date2 = datetime.strptime(dataVolta, '%Y-%m-%d').date()

    if date2 <= date1:
        return False

@api.route('/voo/<iataOrigem>/<iataDestino>/<dataIda>', defaults={"dataVolta":None})
@api.route('/voo/<iataOrigem>/<iataDestino>/<dataIda>/<dataVolta>')
class ApiAirport(Resource):
    def get(self, iataOrigem, iataDestino, dataIda, dataVolta):
        origem = str(iataOrigem)
        destino = str(iataDestino)
        ida = str(dataIda)
        volta = str(dataVolta) if dataVolta else None
        verifyData = True

        if volta != None:
            verifyData = verifyIata(ida, volta)

        if origem == destino:
            return ({'error':'Origem e destino iguais'}, 400)

        if verifyData == False:
            return ({'error':'data de ida e volta iguais'}, 400)

        data = Request(origem,destino, ida, volta)

        dataVoo = data.requestApi()

        if dataVoo == False:
            return ({'error': 'iata inexistente'}, 400)

        priceValue = priceTicket(dataVoo)
        responseData = metaTicket(priceValue)

        responseCombine = combineFlights(responseData)
        if responseCombine != False:
            return responseCombine

        return responseData
