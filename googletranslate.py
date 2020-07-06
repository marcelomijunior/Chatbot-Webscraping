from googletrans import Translator

def printTranslations(translations):
    for translation in translations:
        print(translation.text)

translator = Translator()
t = translator.translate('안녕하세요.', dest='pt')
print(t.text)
"""
t = translator.translate('안녕하세요.')
print(t)

t = translator.translate('안녕하세요.', dest='ja')
print(t)

t = translations = translator.translate('veritas lux mea', src='la')
print(t)
"""

