import json

with open("entrada/entrada.json", "r") as arquivo:
    dados = json.load(arquivo)

    print(dados)