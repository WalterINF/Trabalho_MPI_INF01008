# Trabalho_MPI_INF01008

#### Regras para a execução do trabalho:

- 1. No dia 30/11/2025 `as 23:59 encerra-se o prazo para a entrega do trabalho. Trabalho atrasado ser´a descontado 10% da nota por dia atrasado.
- 2. O trabalho pode ser realizado em trios.
- 3. Um aluno, em nome do grupo, at´e o prazo final de entrega, dever´a fazer o envio via Moodle de um arquivo contendo o pdf do trabalho.

### Sobre a avaliação do trabalho:

- 1. A nota ser´a composta pela qualidade do relat´orio entregue.
- 2. Trabalho plagiado (com ou sem o uso de IA) ter´a nota zero.

#### Datas:

1. Entrega do trabalho: 30/11/2025 at´e `as 23:59

# Definição:

**Objetivos:** O objetivo deste trabalho é realizar uma análise do desempenho entre comunicações síncronas e assíncronas no contexto de um algoritmo de multiplicação de matrizes em ambiente distribuído. Pretende-se investigar como cada método de comunicação impacta a eficiência geral do algoritmo, medindo métricas de desempenho tais como tempo de execução em diferentes cenários de carga de trabalho.

**Descrição:** Multiplicação de matrizes é uma operação fundamental em muitos campos científicos e de engenharia, sendo frequentemente utilizada para testar a eficácia e eficiência de algoritmos paralelos e distribuídos. O presente trabalho considera a implementação de um algoritmo de multiplicação de matrizes em MPI que utilize tanto comunicações síncronas quanto assíncronas.

## Metodologia:

**Algoritmo:** Utilizar os algoritmos paralelos disponibilizados no moodle da disciplina.

**Configuração do Ambiente de Teste:** Definir um conjunto de matrizes de diferentes tamanhos para os testes, garantindo que sejam suficientemente grandes para demonstrar as diferenças de desempenho.

**Experimentos:** Executar as versões do algoritmo em várias configurações de tamanho de matriz e número de processos MPI. Coletar dados de desempenho, incluindo o tempo total de execução e o tempo gasto em comunicação (inserir funções para medição de tempo).

**Análise de Desempenho:** Analisar os dados coletados para identificar tendências, gargalos e condições sob as quais um método de comunicação pode ser preferível ao outro.

**Entregáveis:** Um relatório técnico contendo a metodologia de teste, os resultados experimentais e a análise de desempenho.