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
→ JSON de saída (hex, texto, snapshot de registradores e sinalização de overflow)

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

Ainda **não implementados** (previstos para a Entrega 3): memória (segmentos `data`/`text`
de 8 bits), instruções de load/store (`lw`, `sw`, `lb`, `lbu`, `sb`) e desvios/saltos
(`beq`, `bne`, `bltz`, `blez`, `bgtz`, `j`, `jal`, `jr`). Essas instruções já são
identificadas/decodificadas, mas ainda não alteram registradores ou memória.

`entrada/entrada.json` traz um exemplo cobrindo as 27 instruções da Entrega 2, incluindo
casos com registradores negativos e um caso de overflow; `saida/saida.json` é a saída
gerada a partir desse exemplo.

## Integrantes: 
- Daniel Tavares de Lima Marcelino
- Rodrigo Silva da Luz
- João Matheus Marques de Oliveira
