import json
from pathlib import Path


class Intents:

    def __init__(self, data):
        self.data = data
        pass

    def createIntents(self):
        newIntents = self.jsonManipulate(self.readIntents())
        print(newIntents)

        with open('./intents/intents.json', 'w', encoding='utf-8') as archive:
            json.dump({"intents": newIntents}, archive,
                      indent=4, ensure_ascii=False)
            pass

    def readIntents(self):
        if self.checkIntentsExists():
            with open('./intents/intents.json', 'r', encoding='utf-8') as archive:
                data = json.load(archive)
                return data['intents']
        else:
            return {"intents": []}

    def checkIntentsExists(self):
        try:
            return Path('./intents/intents.json').resolve(strict=True)
        except IOError as identifier:
            print(identifier)
            pass

    def jsonManipulate(self, intents):
        socialNetworks = self.data['Store']['Acompanhne-nos']
        address = self.data['Store']['Endereço']
        gamesOnSale = ''
        pcGames = ''
        giftCards = ''

        for product in self.data['Products']:
            if product['promotion'] == True:
                gamesOnSale += "\n"+product['name'] + \
                    ", por "+product['price']+" reais."
                pass
            else:
                pcGames += "\n"+product['name']+", por " + \
                    product['price']+" reais."
                pass

            if product['typeProduct'] == "Gift Card":
                giftCards += "\n"+product['name']+", por " + \
                    product['price']+" reais."
                pass
            pass

        for intent in intents:
            if intent['tag'] == "endereço":
                intent['responses'][0] = intent['responses'][0] + address
                pass

            if intent['tag'] == "contato-redesSociais":
                social = ''

                for socialNetwork in socialNetworks:
                    social += "\n"+socialNetwork
                    pass

                intent['responses'][0] = intent['responses'][0] + social
                pass

            if intent['tag'] == "atender-jogosPromocao":
                intent['responses'][0] = intent['responses'][0] + gamesOnSale
                pass

            if intent['tag'] == "atender-jogos":
                intent['responses'][0] = intent['responses'][0] + pcGames
                pass

            if intent['tag'] == "atender-giftCard":
                intent['responses'][0] = intent['responses'][0] + giftCards
                pass

        intentsManipulate = intents
        return intentsManipulate

    def printData(self):
        print(self.data)
        pass
