import json
import os

resultado_final = []

with open("entrada/entrada.json", "r") as arquivo:
    dados = json.load(arquivo)


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
    0x1B: "divu",
    0x0C: "syscall"
}


INSTRUCOES_I = {
    0x01: "bltz",
    0x04: "beq",
    0x05: "bne",
    0x06: "blez",
    0x07: "bgtz",
    0x08: "addi",
    0x09: "addiu",
    0x0A: "slti",
    0x0C: "andi",
    0x0D: "ori",
    0x0E: "xori",
    0x0F: "lui",
    0x20: "lb",
    0x23: "lw",
    0x24: "lbu",
    0x28: "sb",
    0x2B: "sw"
}


INSTRUCOES_J = {
    0x02: "j",
    0x03: "jal"
}


# opcode nos 6 bits mais altos decide o formato: R, J ou I
def idenficar_formato(instrucao):
    opcode = int(instrucao[0:6], 2)

    if opcode == 0:
        return "R"

    if opcode == 2 or opcode == 3:
        return "J"

    return "I"


# busca o mnemônico no dicionário certo pra cada formato
def identificar_instrucao(formato, campo):
    if formato == "R":
        return INSTRUCOES_R.get(campo["opPlus"], "Instrução desconhecida")

    elif formato == "I":
        return INSTRUCOES_I.get(campo["opcode"], "Instrução desconhecida")

    elif formato == "J":
        return INSTRUCOES_J.get(campo["opcode"], "Instrução desconhecida")

    else:
        return "Formato desconhecido"



# hex de 32 bits vira string binária de 32 caracteres
def hexadecimal_para_binario(hexa):
    numero = int(hexa, 16)
    return format(numero, "032b")


# quebra a instrução R em opcode, rs, rt, rd, shift e funct
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

# monta o assembly da instrução R (os operandos mudam conforme a instrução)
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

    if nome == "syscall":
        return "syscall"

    if nome in ["mult", "multu", "div", "divu"]:
        return f"{nome} ${rs}, ${rt}"

    if nome in ["sllv", "srlv", "srav"]:
        return f"{nome} ${rd}, ${rt}, ${rs}"
    return f"{nome} ${rd}, ${rs}, ${rt}"



# quebra a instrução I em opcode, rs, rt e immediate
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


# monta o assembly da instrução I (os operandos mudam conforme a instrução)
def gerar_texto_i(nome, campos):

    rs = campos["rs"]
    rt = campos["rt"]
    immediate = campos["immediate"]
    immediate_signed = para_signed_16(immediate)  # offset/imediato com sinal pra exibição

    if nome == "lui":
        return f"{nome} ${rt}, {immediate}"

    if nome in ["lw", "lbu", "sb", "sw", "lb"]:
        return f"{nome} ${rt}, {immediate_signed}(${rs})"

    if nome in ["beq", "bne"]:
        return f"{nome} ${rs}, ${rt}, {immediate_signed}"

    if nome in ["bltz", "blez", "bgtz"]:
        return f"{nome} ${rs}, {immediate_signed}"

    if nome in ["andi", "ori", "xori"]:
        return f"{nome} ${rt}, ${rs}, {immediate}"  # andi/ori/xori usam zero-extend, mostram sem sinal

    return f"{nome} ${rt}, ${rs}, {immediate_signed}"

# quebra a instrução J em opcode e endereço
def decodificar_formato_j(binario):
    opcode = int(binario[0:6], 2)
    address = int(binario[6:32], 2)

    return {
        "opcode": opcode,
        "address": address
    }

# monta o assembly da instrução J
def gerar_texto_j(nome, campos):
    address = campos["address"]
    return f"{nome} {address}"


# decodifica um hex completo: formato, campos, nome e texto assembly
def decodificar_instrucao(hexadecimal):
    binario = hexadecimal_para_binario(hexadecimal)
    formato = idenficar_formato(binario)

    if formato == "R":
        campos = decodificar_formato_r(binario)
    elif formato == "I":
        campos = decodificar_formato_i(binario)
    else:
        campos = decodificar_formato_j(binario)

    nome = identificar_instrucao(formato, campos)

    if nome == "Instrução desconhecida":
        return {
            "hex": hexadecimal,
            "text": "instrução desconhecida",
            "formato": formato,
            "nome": nome,
            "campos": campos
        }

    if formato == "R":
        texto = gerar_texto_r(nome, campos)
    elif formato == "I":
        texto = gerar_texto_i(nome, campos)
    else:
        texto = gerar_texto_j(nome, campos)

    return {
        "hex": hexadecimal,
        "text": texto,
        "formato": formato,
        "nome": nome,
        "campos": campos
    }


# monta o banco de registradores com os defaults do MARS e aplica config.regs por cima
def inicializar_registradores(regs_config):
    banco = {
        "regs": [0] * 32,   # $0 a $31
        "pc": 0x00400000,
        "hi": 0,
        "lo": 0
    }

    banco["regs"][28] = 0x10008000  # $gp, padrão MARS
    banco["regs"][29] = 0x7fffeffc  # $sp, padrão MARS

    if regs_config:
        for nome, valor in regs_config.items():
            if nome == "pc":
                banco["pc"] = valor & 0xFFFFFFFF
            elif nome == "hi":
                banco["hi"] = valor & 0xFFFFFFFF
            elif nome == "lo":
                banco["lo"] = valor & 0xFFFFFFFF
            else:
                indice = int(nome.lstrip("$"))
                if 0 <= indice < 32:  # ignora chave inválida (ex: "$32") em vez de travar o programa
                    escrever_registrador(banco, indice, valor)

    return banco


# lê o valor bruto (sem sinal) de um registrador
def ler_registrador(banco, indice):
    return banco["regs"][indice]


# $0 nunca muda (hardwired a zero, como no MIPS real); valor sempre truncado a 32 bits
def escrever_registrador(banco, indice, valor):
    if indice == 0:
        return
    banco["regs"][indice] = valor & 0xFFFFFFFF


# unsigned 32 bits -> signed (complemento de dois)
def para_signed_32(valor):
    valor = valor & 0xFFFFFFFF
    if valor >= 0x80000000:
        valor -= 0x100000000
    return valor


# mesma ideia de para_signed_32, para o immediate de 16 bits
def para_signed_16(valor):
    valor = valor & 0xFFFF
    if valor >= 0x8000:
        valor -= 0x10000
    return valor


# ordem $0..$31, pc, hi, lo; só valores != 0 (formato exigido na saída)
def gerar_snapshot_registradores(banco):
    snapshot = {}

    for indice in range(32):
        valor = banco["regs"][indice]
        if valor != 0:
            snapshot[f"${indice}"] = para_signed_32(valor)

    if banco["pc"] != 0:
        snapshot["pc"] = para_signed_32(banco["pc"])
    if banco["hi"] != 0:
        snapshot["hi"] = para_signed_32(banco["hi"])
    if banco["lo"] != 0:
        snapshot["lo"] = para_signed_32(banco["lo"])

    return snapshot


banco_registradores = inicializar_registradores(dados.get("config", {}).get("regs", {}))


# lê um byte (0-255); endereço sem dado ainda vale 0
def ler_byte(memoria, endereco):
    return memoria.get(endereco, 0)


# escreve um byte, truncado a 8 bits
def escrever_byte(memoria, endereco, valor):
    memoria[endereco] = valor & 0xFF


# lê uma word de 4 bytes a partir do endereço, little endian (igual ao MARS)
def ler_word(memoria, endereco):
    b0 = ler_byte(memoria, endereco)
    b1 = ler_byte(memoria, endereco + 1)
    b2 = ler_byte(memoria, endereco + 2)
    b3 = ler_byte(memoria, endereco + 3)
    return b0 | (b1 << 8) | (b2 << 16) | (b3 << 24)


# escreve uma word de 4 bytes a partir do endereço, little endian (igual ao MARS)
def escrever_word(memoria, endereco, valor):
    valor &= 0xFFFFFFFF
    escrever_byte(memoria, endereco, valor & 0xFF)
    escrever_byte(memoria, endereco + 1, (valor >> 8) & 0xFF)
    escrever_byte(memoria, endereco + 2, (valor >> 16) & 0xFF)
    escrever_byte(memoria, endereco + 3, (valor >> 24) & 0xFF)


# carrega .data e config.mem (ambos em words) na memória, antes de qualquer instrução rodar
def inicializar_memoria(data_config, mem_config):
    memoria = {}

    for endereco_str, valor in data_config.items():
        escrever_word(memoria, int(endereco_str), int(valor))

    for endereco_str, valor in mem_config.items():
        escrever_word(memoria, int(endereco_str), int(valor))

    return memoria


# snapshot da saída: por word (não por byte), endereços crescentes, só valores != 0
def gerar_snapshot_memoria(memoria):
    enderecos_palavra = sorted({endereco - (endereco % 4) for endereco in memoria})

    snapshot = {}
    for endereco in enderecos_palavra:
        valor = ler_word(memoria, endereco)
        if valor != 0:
            snapshot[str(endereco)] = para_signed_32(valor)

    return snapshot


memoria = inicializar_memoria(dados.get("data", {}), dados.get("config", {}).get("mem", {}))


# Executa a instrução R já decodificada. Retorna True se add/sub estourou 32 bits com sinal.
def executar_r(nome, campos, banco):
    rs = campos["rs"]
    rt = campos["rt"]
    rd = campos["rd"]
    shift = campos["shift"]

    overflow = False

    if nome == "add":
        val_rs = para_signed_32(ler_registrador(banco, rs))
        val_rt = para_signed_32(ler_registrador(banco, rt))
        resultado = val_rs + val_rt
        # overflow: mesmo sinal nos operandos e resultado truncado com sinal diferente
        # (o inteiro do Python não estoura sozinho, por isso comparamos o valor já truncado)
        resultado_signed = para_signed_32(resultado)
        if (val_rs >= 0) == (val_rt >= 0) and (resultado_signed >= 0) != (val_rs >= 0):
            overflow = True
        else:
            escrever_registrador(banco, rd, resultado)  # com overflow o MARS não escreve

    elif nome == "sub":
        val_rs = para_signed_32(ler_registrador(banco, rs))
        val_rt = para_signed_32(ler_registrador(banco, rt))
        resultado = val_rs - val_rt
        resultado_signed = para_signed_32(resultado)
        if (val_rs >= 0) != (val_rt >= 0) and (resultado_signed >= 0) != (val_rs >= 0):
            overflow = True
        else:
            escrever_registrador(banco, rd, resultado)

    elif nome == "addu":
        escrever_registrador(banco, rd, ler_registrador(banco, rs) + ler_registrador(banco, rt))

    elif nome == "subu":
        escrever_registrador(banco, rd, ler_registrador(banco, rs) - ler_registrador(banco, rt))

    elif nome == "and":
        escrever_registrador(banco, rd, ler_registrador(banco, rs) & ler_registrador(banco, rt))

    elif nome == "or":
        escrever_registrador(banco, rd, ler_registrador(banco, rs) | ler_registrador(banco, rt))

    elif nome == "xor":
        escrever_registrador(banco, rd, ler_registrador(banco, rs) ^ ler_registrador(banco, rt))

    elif nome == "nor":
        escrever_registrador(banco, rd, ~(ler_registrador(banco, rs) | ler_registrador(banco, rt)))

    elif nome == "slt":
        val_rs = para_signed_32(ler_registrador(banco, rs))
        val_rt = para_signed_32(ler_registrador(banco, rt))
        escrever_registrador(banco, rd, 1 if val_rs < val_rt else 0)

    elif nome == "sll":
        escrever_registrador(banco, rd, ler_registrador(banco, rt) << shift)

    elif nome == "srl":
        escrever_registrador(banco, rd, ler_registrador(banco, rt) >> shift)

    elif nome == "sra":
        val_rt = para_signed_32(ler_registrador(banco, rt))
        escrever_registrador(banco, rd, val_rt >> shift)  # >> do Python já é aritmético em negativo

    elif nome == "sllv":
        quantidade = ler_registrador(banco, rs) & 0x1F  # 5 bits menos significativos de rs
        escrever_registrador(banco, rd, ler_registrador(banco, rt) << quantidade)

    elif nome == "srlv":
        quantidade = ler_registrador(banco, rs) & 0x1F
        escrever_registrador(banco, rd, ler_registrador(banco, rt) >> quantidade)

    elif nome == "srav":
        quantidade = ler_registrador(banco, rs) & 0x1F
        val_rt = para_signed_32(ler_registrador(banco, rt))
        escrever_registrador(banco, rd, val_rt >> quantidade)

    elif nome == "mfhi":
        escrever_registrador(banco, rd, banco["hi"])

    elif nome == "mflo":
        escrever_registrador(banco, rd, banco["lo"])

    elif nome == "mult":
        val_rs = para_signed_32(ler_registrador(banco, rs))
        val_rt = para_signed_32(ler_registrador(banco, rt))
        produto = val_rs * val_rt
        banco["hi"] = (produto >> 32) & 0xFFFFFFFF
        banco["lo"] = produto & 0xFFFFFFFF

    elif nome == "multu":
        val_rs = ler_registrador(banco, rs)
        val_rt = ler_registrador(banco, rt)
        produto = val_rs * val_rt
        banco["hi"] = (produto >> 32) & 0xFFFFFFFF
        banco["lo"] = produto & 0xFFFFFFFF

    elif nome == "div":
        val_rs = para_signed_32(ler_registrador(banco, rs))
        val_rt = para_signed_32(ler_registrador(banco, rt))
        if val_rt != 0:
            # trunca em direção a zero (divisão à la C); "//" do Python arredonda para
            # baixo e erra quando os sinais são diferentes
            quociente = abs(val_rs) // abs(val_rt)
            if (val_rs < 0) != (val_rt < 0):
                quociente = -quociente
            resto = val_rs - quociente * val_rt
            banco["lo"] = quociente & 0xFFFFFFFF
            banco["hi"] = resto & 0xFFFFFFFF
        # divisão por zero é indefinida no MIPS real: não mexe em HI/LO

    elif nome == "divu":
        val_rs = ler_registrador(banco, rs)
        val_rt = ler_registrador(banco, rt)
        if val_rt != 0:
            banco["lo"] = (val_rs // val_rt) & 0xFFFFFFFF
            banco["hi"] = (val_rs % val_rt) & 0xFFFFFFFF

    elif nome == "jr":
        banco["pc"] = ler_registrador(banco, rs)

    # syscall fica pra depois: nada acontece aqui

    return overflow


# Executa a instrução I já decodificada. Retorna True se addi estourou 32 bits com sinal.
def executar_i(nome, campos, banco, memoria):
    rs = campos["rs"]
    rt = campos["rt"]
    immediate = campos["immediate"]  # 16 bits sem sinal, 0-65535
    endereco = (ler_registrador(banco, rs) + para_signed_16(immediate)) & 0xFFFFFFFF  # usado por lw/sw/lb/lbu/sb

    overflow = False

    if nome == "addi":
        val_rs = para_signed_32(ler_registrador(banco, rs))
        imm_signed = para_signed_16(immediate)
        resultado = val_rs + imm_signed
        resultado_signed = para_signed_32(resultado)
        if (val_rs >= 0) == (imm_signed >= 0) and (resultado_signed >= 0) != (val_rs >= 0):
            overflow = True
        else:
            escrever_registrador(banco, rt, resultado)

    elif nome == "addiu":
        val_rs = para_signed_32(ler_registrador(banco, rs))
        imm_signed = para_signed_16(immediate)  # addiu também faz sign-extend, só não gera overflow
        escrever_registrador(banco, rt, val_rs + imm_signed)

    elif nome == "slti":
        val_rs = para_signed_32(ler_registrador(banco, rs))
        imm_signed = para_signed_16(immediate)
        escrever_registrador(banco, rt, 1 if val_rs < imm_signed else 0)

    elif nome == "andi":
        escrever_registrador(banco, rt, ler_registrador(banco, rs) & immediate)  # zero-extend, diferente de addi/slti

    elif nome == "ori":
        escrever_registrador(banco, rt, ler_registrador(banco, rs) | immediate)

    elif nome == "xori":
        escrever_registrador(banco, rt, ler_registrador(banco, rs) ^ immediate)

    elif nome == "lui":
        escrever_registrador(banco, rt, immediate << 16)  # zero-extend, sem sinal

    elif nome == "lw":
        escrever_registrador(banco, rt, ler_word(memoria, endereco))

    elif nome == "sw":
        escrever_word(memoria, endereco, ler_registrador(banco, rt))

    elif nome == "lb":
        byte = ler_byte(memoria, endereco)
        escrever_registrador(banco, rt, byte - 0x100 if byte >= 0x80 else byte)  # sign-extend

    elif nome == "lbu":
        escrever_registrador(banco, rt, ler_byte(memoria, endereco))  # zero-extend

    elif nome == "sb":
        escrever_byte(memoria, endereco, ler_registrador(banco, rt))

    elif nome == "beq":
        if ler_registrador(banco, rs) == ler_registrador(banco, rt):
            banco["pc"] = (banco["pc"] + (para_signed_16(immediate) << 2)) & 0xFFFFFFFF

    elif nome == "bne":
        if ler_registrador(banco, rs) != ler_registrador(banco, rt):
            banco["pc"] = (banco["pc"] + (para_signed_16(immediate) << 2)) & 0xFFFFFFFF

    elif nome == "bltz":
        if para_signed_32(ler_registrador(banco, rs)) < 0:
            banco["pc"] = (banco["pc"] + (para_signed_16(immediate) << 2)) & 0xFFFFFFFF

    return overflow


# executa j/jal: salto absoluto dentro da região de 256MB do PC+4 atual
def executar_j(nome, campos, banco):
    alvo = (banco["pc"] & 0xF0000000) | (campos["address"] << 2)

    if nome == "jal":
        escrever_registrador(banco, 31, banco["pc"])  # $ra = próxima instrução (sem delay slot)

    banco["pc"] = alvo


# decodifica, executa e monta o objeto de saída de uma instrução
def gerar_saida(hexadecimal):
    resultado = decodificar_instrucao(hexadecimal)

    # PC sempre avança 4 bytes na busca da próxima instrução; desvios/saltos
    # (Entrega 3) sobrescrevem esse valor dentro de executar_r/executar_i/executar_j
    banco_registradores["pc"] = (banco_registradores["pc"] + 4) & 0xFFFFFFFF

    overflow = False
    if resultado.get("formato") == "R":
        overflow = executar_r(resultado["nome"], resultado["campos"], banco_registradores)
    elif resultado.get("formato") == "I":
        overflow = executar_i(resultado["nome"], resultado["campos"], banco_registradores, memoria)
    elif resultado.get("formato") == "J":
        executar_j(resultado["nome"], resultado["campos"], banco_registradores)

    return {
        "hex": resultado["hex"],
        "text": resultado["text"],
        "regs": gerar_snapshot_registradores(banco_registradores),
        "mem": gerar_snapshot_memoria(memoria),
        "stdout": "overflow" if overflow else ""
    }


instrucoes = dados["text"]

for instrucao in instrucoes:
    resultado_final.append(gerar_saida(instrucao))

os.makedirs("saida", exist_ok=True)

with open("saida/saida.json", "w") as arquivo:
    json.dump(resultado_final, arquivo, indent=4)
