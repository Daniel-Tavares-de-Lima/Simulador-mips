# Simulador-mips
Projeto voltado a ler as instruções MIPS em hexadecimal, identificar/decodificar cada uma,
executar as instruções aritmético-lógicas e gerar um JSON de saída com o estado dos
registradores após cada instrução.

## Atualmente o programa realiza:
Hexadecimal
→ Binário
→ Identificação do formato (R, I ou J)
→ Decodificação dos campos
→ Identificação da instrução
→ Geração do texto da instrução (mnemônico assembly)
→ Execução das instruções aritmético-lógicas (Entrega 2), atualizando o banco de registradores
→ JSON de saída (hex, texto, snapshot de registradores, memória e sinalização de overflow)

Banco de registradores: 32 registradores de uso geral ($0-$31) + PC, HI e LO, inicializados
no padrão MARS ($gp, $sp, $pc) e sobrepostos pelos valores de `config.regs` do JSON de entrada.

Instruções executadas nesta etapa (Entrega 2 — tipos R e I):
- Aritméticas/lógicas tipo R: `add`, `addu`, `sub`, `subu`, `and`, `or`, `xor`, `nor`, `slt`
- Deslocamento (shift) tipo R: `sll`, `srl`, `sra`, `sllv`, `srlv`, `srav`
- Multiplicação/divisão (HI/LO) tipo R: `mult`, `multu`, `div`, `divu`, `mfhi`, `mflo`
- Aritméticas/lógicas tipo I (imediato): `addi`, `addiu`, `slti`, `andi`, `ori`, `xori`

Após cada instrução, o JSON de saída mostra apenas os registradores com valor diferente de
zero (`$0..$31`, `pc`, `hi`, `lo`) e sinaliza `stdout: "overflow"` quando `add`/`addi` (ou
`sub`) estouram 32 bits com sinal.

## Entrega 3 (load, store e desvio) — implementada
- Memória de 8 bits (dicionário endereço → byte, little-endian como o MARS), cobrindo os
  segmentos `data` (0x10010000), `sp` (0x7fffeffc) e `text` (0x00400000). Carrega `config.mem`
  e `data` antes da execução; a saída lista só words alinhados diferentes de zero, em ordem crescente.
- Load/store: `lw`, `lb` (com extensão de sinal), `lbu`, `sw`, `sb`; também `lui`.
- Desvios: `beq`, `bne`, `bltz` (e `blez`, `bgtz`): destino = (PC+4) + offset×4.
- Saltos: `j`, `jal` (`$ra` = PC+4) e `jr`.
- O PC avança +4 a cada instrução (antes ficava parado em 0x00400000).
- `add`/`sub`/`addi` com overflow sinalizam `stdout: "overflow"` e **não escrevem** o registrador (como o MARS).
- O campo `text` mostra o imediato com sinal em `addi`, `addiu`, `slti`, loads, stores e desvios (ex.: `addi $30, $14, -1`).

### Como executar
```
python src/simulador_mips.py                                   # entrada/entrada.json -> saida/saida.json
python src/simulador_mips.py entrada/entrada_entrega3.json saida/saida_entrega3.json
python src/simulador_mips.py entrada.json saida.json --seguir-pc
```
Por padrão as instruções são processadas na ordem do array `text` (como diz o enunciado).
Com `--seguir-pc` o simulador segue o PC de verdade, obedecendo desvios e saltos.

`entrada/entrada.json` traz um exemplo cobrindo as 27 instruções da Entrega 2, incluindo
casos com registradores negativos e um caso de overflow; `saida/saida.json` é a saída
gerada a partir desse exemplo.

## Integrantes: 
- Daniel Tavares de Lima Marcelino
- Rodrigo Silva da Luz
- João Matheus Marques de Oliveira
