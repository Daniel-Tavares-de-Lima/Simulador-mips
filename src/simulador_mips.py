import json

with open("entrada/entrada.json", "r") as arquivo:
    dados = json.load(arquivo)

#Lista de instruções
instrucoes = dados["text"]

# Conversão de hexadecimal para binário
def hexadecimal_para_binario(hexa):
    numero = int(hexa, 16)
    return format(numero, "032b")

for instrucao in instrucoes:
    binario = hexadecimal_para_binario(instrucao)

    print(f"Instrução: {instrucao} -> Binário: {binario}")
