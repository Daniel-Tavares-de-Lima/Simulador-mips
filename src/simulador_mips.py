import json

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
        return INSTRUCOES_R.get(campo, "Instrução desconhecida")
    elif formato == "I":
        return INSTRUCOES_I.get(campo, "Instrução desconhecida")
    elif formato == "J":
        return INSTRUCOES_J.get(campo, "Instrução desconhecida")
    else:
        return "Formato desconhecido"


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

