import json as js
import nltk
import numpy as np
import random
import string
import tensorflow as tf
import tflearn as tfl

from nltk.stem.rslp import RSLPStemmer
from audio_utils import TextToSpeech, SpeechToText

# Baixando as ferramentas necessárias do nltk
nltk.download('rslp')
nltk.download('punkt')
nltk.download('stopwords')

# Carregando o arquivo de intents
with open("./webscraping/intents/intents.json", 'r', encoding='utf-8') as file:
    data = js.load(file)


# Preparando os dados
palavras = []
intencoes = []
sentencas = []
saidas = []

# Pega cada intenção
for intent in data["intents"]:

    tag = intent['tag']

    if tag not in intencoes:
        intencoes.append(tag)

    for pattern in intent["patterns"]:
        wrds = nltk.word_tokenize(pattern, language='portuguese')
        palavras.extend(wrds)
        sentencas.append(wrds)
        saidas.append(tag)

# Separando as palavras não desejadas
stopwords = list(string.punctuation) + \
    nltk.corpus.stopwords.words('portuguese')
filteredWords = []

for palavra in palavras:
    if palavra not in stopwords:
        filteredWords.append(palavra)


# Stemming
stemer = RSLPStemmer()

stemmed_words = [stemer.stem(w.lower()) for w in palavras]
stemmed_words = sorted(list(set(stemmed_words)))

# Criando a bag of words
training = []
output = []

outputEmpty = [0 for _ in range(len(intencoes))]

for x, frase in enumerate(sentencas):
    bag = []
    wds = [stemer.stem(k.lower()) for k in frase]
    for w in stemmed_words:
        if w in wds:
            bag.append(1)
        else:
            bag.append(0)

    outputRow = outputEmpty[:]
    outputRow[intencoes.index(saidas[x])] = 1

    training.append(bag)
    output.append(outputRow)

# Criando a rede neural
training = np.array(training)
output = np.array(output)

# Reiniciando os dados
tf.reset_default_graph()

# Camada de entrada
net = tfl.input_data(shape=[None, len(training[0])])
# Oito neuronios por camada oculta
net = tfl.fully_connected(net, 8)
# Camada de saida
net = tfl.fully_connected(net, len(output[0]), activation="softmax")
#
net = tfl.regression(net)

# Criando o modelo
model = tfl.DNN(net)

# Treinando o modelo
model.fit(training, output, n_epoch=80, batch_size=8, show_metric=True)
model.save("model.chatbot")
# model.load("model.chatbot")

# O bot em funcionamento

# Função para checar a accuracy de resposta do bot


def isMisunderstood(answers):
    if (max(answers) < 0.30):
        return True
    return False


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return np.array(bag)


def chat():
    print("Esse é o bot de teste! Converse com ele")
    Online = True
    while Online:
        inp = SpeechToText()
        bag_usuario = bag_of_words(inp, stemmed_words)
        results = model.predict([bag_usuario])
        results_index = np.argmax(results)
        tag = intencoes[results_index]

        if (isMisunderstood(results[0])):
            desculpas = 'Desculpe, não entendi... Você poderia repetir por favor a pergunta?'
            print(desculpas)
            TextToSpeech(desculpas)
        else:
            for tg in data["intents"]:
                if tg['tag'] == tag:
                    responses = tg['responses']

            response = random.choice(responses)
            print(response)
            TextToSpeech(response)

            if tag == "ate-mais":
                Online = False


chat()
