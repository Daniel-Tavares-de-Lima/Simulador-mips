# Simulador-mips
Projeto voltado a ler as instruções MIPS em hexadecimal, identificar/decodificar cada uma,
executar as instruções (aritmético-lógicas, load/store e desvio) e gerar um JSON de saída
com o estado dos registradores e da memória após cada instrução.

## Atualmente o programa realiza:
Hexadecimal
→ Binário
→ Identificação do formato (R, I ou J)
→ Decodificação dos campos
→ Identificação da instrução
→ Geração do texto da instrução (mnemônico assembly)
→ Execução (registradores, memória, PC)
→ JSON de saída (hex, texto, snapshot de registradores/memória e sinalização de overflow)

Banco de registradores: 32 registradores de uso geral ($0-$31) + PC, HI e LO, inicializados
no padrão MARS ($gp, $sp, $pc) e sobrepostos pelos valores de `config.regs` do JSON de entrada.
PC avança 4 bytes a cada instrução; desvios e saltos sobrescrevem esse valor.

Memória: byte-endereçável (dict esparso endereço→byte), com leitura/escrita de byte e de
word (4 bytes, **big-endian**). `data` e `config.mem` do JSON de entrada são carregados antes
da execução. A saída `mem` mostra o valor por word (agrupado em blocos de 4 bytes alinhados,
igual o visor de memória do MARS), só os endereços com valor diferente de zero.

Instruções executadas:
- Aritméticas/lógicas tipo R: `add`, `addu`, `sub`, `subu`, `and`, `or`, `xor`, `nor`, `slt`
- Deslocamento (shift) tipo R: `sll`, `srl`, `sra`, `sllv`, `srlv`, `srav`
- Multiplicação/divisão (HI/LO) tipo R: `mult`, `multu`, `div`, `divu`, `mfhi`, `mflo`
- Aritméticas/lógicas tipo I (imediato): `addi`, `addiu`, `slti`, `andi`, `ori`, `xori`
- Load/store: `lw`, `sw`, `lb` (com sinal), `lbu` (sem sinal), `sb`, `lui`
- Desvio/salto: `beq`, `bne`, `bltz`, `j`, `jal`, `jr`

Após cada instrução, o JSON de saída mostra apenas os registradores com valor diferente de
zero (`$0..$31`, `pc`, `hi`, `lo`) e sinaliza `stdout: "overflow"` quando `add`/`addi`/`sub`
estouram 32 bits com sinal.

Fora da lista da disciplina (`blez`, `bgtz`, `syscall`): são decodificados (texto assembly
correto) mas não executados, já que não fazem parte do escopo das três entregas.

`entrada/entrada.json` traz um exemplo cobrindo as instruções das Entregas 2 e 3 (aritmética,
load/store, desvio/salto), incluindo overflow e um roundtrip de memória; `saida/saida.json`
é a saída gerada a partir desse exemplo.

## Integrantes: 
- Daniel Tavares de Lima Marcelino
- Rodrigo Silva da Luz
- João Matheus Marques de Oliveira
