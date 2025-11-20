# Trabalho_MPI_INF01008

# Definição:

**Objetivos:** O objetivo deste trabalho é realizar uma análise do desempenho entre comunicações síncronas e assíncronas no contexto de um algoritmo de multiplicação de matrizes em ambiente distribuído. Pretende-se investigar como cada método de comunicação impacta a eficiência geral do algoritmo, medindo métricas de desempenho tais como tempo de execução em diferentes cenários de carga de trabalho.

**Descrição:** Multiplicação de matrizes é uma operação fundamental em muitos campos científicos e de engenharia, sendo frequentemente utilizada para testar a eficácia e eficiência de algoritmos paralelos e distribuídos. O presente trabalho considera a implementação de um algoritmo de multiplicação de matrizes em MPI que utilize tanto comunicações síncronas quanto assíncronas.

## Metodologia:

**Configuração do Ambiente de Teste:** Definir um conjunto de matrizes de diferentes tamanhos para os testes, garantindo que sejam suficientemente grandes para demonstrar as diferenças de desempenho.

**Experimentos:** Executar as versões do algoritmo em várias configurações de tamanho de matriz e número de processos MPI. Coletar dados de desempenho, incluindo o tempo total de execução e o tempo gasto em comunicação (inserir funções para medição de tempo).

**Análise de Desempenho:** Analisar os dados coletados para identificar tendências, gargalos e condições sob as quais um método de comunicação pode ser preferível ao outro.

**Entregáveis:** Um relatório técnico contendo a metodologia de teste, os resultados experimentais e a análise de desempenho.
