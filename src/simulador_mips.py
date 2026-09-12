import json

with open("entrada/entrada.json", "r") as arquivo:
    dados = json.load(arquivo)

    instrucoes = dados["text"]

    for instrucao in instrucoes:
        print(instrucao)
