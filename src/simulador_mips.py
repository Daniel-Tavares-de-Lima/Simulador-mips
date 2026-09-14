import json
import os

##----Resultado Final
resultado_final = []

with open("entrada/entrada.json", "r") as arquivo:
    dados = json.load(arquivo)


##---------Mapa de indenficação de instruções---------##
INSTRUCOES_R = {
    0x20: "add",
    0x21: "addu",
    0x22: "sub",
    0x23: "subu",
    0x24: "and",
    0x25: "or",
    0x26: "xor",
    0x27: "nor",
    0x2A: "slt",
    0x00: "sll",
    0x02: "srl",
    0x03: "sra",
    0x04: "sllv",
    0x06: "srlv",
    0x07: "srav",
    0x08: "jr",
    0x10: "mfhi",
    0x12: "mflo",
    0x18: "mult",
    0x19: "multu",
    0x1A: "div",
    0x1B: "divu"
}


INSTRUCOES_I = {
    0x04: "beq",
    0x05: "bne",
    0x08: "addi",
    0x09: "addiu",
    0x0A: "slti",
    0x0C: "andi",
    0x0D: "ori",
    0x0E: "xori",
    0x0F: "lui",
    0x23: "lw",
    0x24: "lbu",
    0x28: "sb",
    0x2B: "sw"
}


INSTRUCOES_J = {
    0x02: "j",
    0x03: "jal"
}


#----- Mapa de identificação de registradores-----#
REGISTRADORES = {
    0: "$zero",
    1: "$at",
    2: "$v0",
    3: "$v1",
    4: "$a0",
    5: "$a1",
    6: "$a2",
    7: "$a3",
    8: "$t0",
    9: "$t1",
    10: "$t2",
    11: "$t3",
    12: "$t4",
    13: "$t5",
    14: "$t6",
    15: "$t7",
    16: "$s0",
    17: "$s1",
    18: "$s2",
    19: "$s3",
    20: "$s4",
    21: "$s5",
    22: "$s6",
    23: "$s7",
    24: "$t8",
    25: "$t9",
    26: "$k0",
    27: "$k1",
    28: "$gp",
    29: "$sp",
    30: "$fp",
    31: "$ra"

}


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

## Idenfica a instrução com base no formato e no campo relevante
def identificar_instrucao(formato, campo):
    if formato == "R":
        return INSTRUCOES_R.get(campo["opPlus"], "Instrução desconhecida")

    elif formato == "I":
        return INSTRUCOES_I.get(campo["opcode"], "Instrução desconhecida")

    elif formato == "J":
        return INSTRUCOES_J.get(campo["opcode"], "Instrução desconhecida")

    else:
        return "Formato desconhecido"



# Conversão de hexadecimal para binário
def hexadecimal_para_binario(hexa):
    numero = int(hexa, 16)
    return format(numero, "032b")


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

# Função para gerar o texto da instrução do formato R
def gerar_texto_r(nome, campos):
    rs = campos["rs"]
    rt = campos["rt"]
    rd = campos["rd"]
    shift = campos["shift"]

    if nome in ["sll", "srl", "sra"]:
        return f"{nome} ${rd}, ${rt}, {shift}"

    if nome in ["jr"]:
        return f"{nome} ${rs}"

    if nome in ["mfhi", "mflo"]:
        return f"{nome} ${rd}"

    if nome in ["mult", "multu", "div", "divu"]:
        return f"{nome} ${rs}, ${rt}"
    
    if nome in ["sllv", "srlv", "srav"]:
        return f"{nome} ${rd}, ${rt}, ${rs}"
    return f"{nome} ${rd}, ${rs}, ${rt}"



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


# Função para gerar o texto da instrução do formato I
def gerar_texto_i(nome, campos):

    rs = campos["rs"]
    rt = campos["rt"]
    immediate = campos["immediate"]

    if nome == "lui":
        return f"{nome} ${rt}, {immediate}"

    if nome in ["lw", "lbu", "sb", "sw"]:
        return f"{nome} ${rt}, {immediate}(${rs})"

    if nome in ["beq", "bne"]:
        return f"{nome} ${rs}, ${rt}, {immediate}"

    return f"{nome} ${rt}, ${rs}, {immediate}"

# Função para decodificar instruções do formato J
def decodificar_formato_j(binario):
    opcode = int(binario[0:6], 2)
    address = int(binario[6:32], 2)

    return {
        "opcode": opcode,
        "address": address
    }

# Função para gerar o texto da instrução do formato J
def gerar_texto_j(nome, campos):
    address = campos["address"]
    return f"{nome} {address}"


# Função principal para decodificar a instrução
def decodificar_instrucao(hexadecimal):
    binario = hexadecimal_para_binario(hexadecimal)
    formato = idenficar_formato(binario)

    # Decodifica a instrução com base no formato
    if formato == "R":
        campos = decodificar_formato_r(binario)

    # Decodifica a instrução com base no formato
    elif formato == "I":
        campos = decodificar_formato_i(binario)

    # Decodifica a instrução com base no formato
    else:
        campos = decodificar_formato_j(binario)

    # Identifica o nome da instrução com base no formato e nos campos
    nome = identificar_instrucao(formato, campos)

    # Se a instrução não for reconhecida, retorna uma mensagem de erro
    if nome == "Instrução desconhecida":

        return {
            "hex": hexadecimal,
            "text": "instrução desconhecida"
        }

    # Gera o texto da instrução com base no formato e nos campos
    if formato == "R":
        texto = gerar_texto_r(nome, campos)

    # Se a instrução for do formato I, gera o texto correspondente
    elif formato == "I":
        texto = gerar_texto_i(nome, campos)

    # Se a instrução for do formato J, gera o texto correspondente
    else:
        texto = gerar_texto_j(nome, campos)

    return {
        "hex": hexadecimal,
        "text": texto
    }


#Lista de instruções
instrucoes = dados["text"]


# Gerar saida

def gerar_saida(hexadecimal):
    resultado = decodificar_instrucao(hexadecimal)

    return {
        "hex": resultado["hex"],
        "text": resultado["text"],
        "regs": {},
        "mem": {},
        "stdout": ""
    }



# percorre a lista de instruções e converte cada uma para binário
for instrucao in instrucoes:
    resultado_final.append(gerar_saida(instrucao))

os.makedirs("saida", exist_ok=True)

with open("saida/saida.json", "w") as arquivo:
    json.dump(resultado_final, arquivo, indent=4)