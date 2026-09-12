import json

with open("entrada/entrada.json", "r") as arquivo:
    dados = json.load(arquivo)


# Idenfica o formato da instrução
def idenficar_formato(instrucao):
    opcode = int(instrucao[0:6], 2)

    #Formato R
    if opcode == 0:
        return "R"

    #Formato J
    if opcode == 2 or opcode == 3:
        return "J"

    #Formato I
    return "I"


#Lista de instruções
instrucoes = dados["text"]

# Conversão de hexadecimal para binário
def hexadecimal_para_binario(hexa):
    numero = int(hexa, 16)
    return format(numero, "032b")

# percorre a lista de instruções e converte cada uma para binário
for instrucao in instrucoes:
    binario = hexadecimal_para_binario(instrucao)

    print(f"Instrução: {instrucao} -> Binário: {binario}")

# Função para decodificar instruções do formato R
def decodificar_formato_r(binario):
    opcode = int(binario[0:6], 2)
    rs = int(binario[6:11], 2)
    rt = int(binario[11:16], 2)
    rd = int(binario[16:21], 2)
    shift = int(binario[21:26], 2)
    opPlus = int(binario[26:32], 2)

    return{
        
        "opcode": opcode,
        "rs": rs,
        "rt": rt,
        "rd": rd,
        "shift": shift,
        "opPlus": opPlus
    }

# Função para decodificar instruções do formato I
def decodificar_formato_i(binario):
    opcode = int(binario[0:6], 2)
    rs = int(binario[6:11], 2)
    rt = int(binario[11:16], 2)
    immediate = int(binario[16:32], 2)

    return {
        "opcode": opcode,
        "rs": rs,
        "rt": rt,
        "immediate": immediate
    }

# Função para decodificar instruções do formato J
def decodificar_formato_j(binario):
    opcode = int(binario[0:6], 2)
    address = int(binario[6:32], 2)

    return {
        "opcode": opcode,
        "address": address
    }