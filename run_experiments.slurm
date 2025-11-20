#!/bin/bash
#SBATCH --job-name=experiments
#SBATCH --partition=hype
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=6:00:00
#SBATCH --output=%x_%j.out
#SBATCH --error=%x_%j.err

# Navegar para o diretório do projeto
cd $SLURM_SUBMIT_DIR

# Compilar os códigos de src/ para build/
echo "=== Compilando códigos ==="
mpicc src/mpi_coletiva.c -o build/mpi_coletiva
mpicc src/mpi_p2p_bloqueante.c -o build/mpi_p2p_bloqueante
mpicc src/mpi_p2p_naobloqueante.c -o build/mpi_p2p_naobloqueante

# Verificar se a compilação foi bem-sucedida
if [ $? -ne 0 ]; then
    echo "ERRO: Falha na compilação!"
    exit 1
fi

echo "=== Compilação concluída com sucesso ==="

# Executar os scripts Python na ordem especificada
echo "=== Executando experimental_design.py ==="
python3 scripts/experimental_design.py
if [ $? -ne 0 ]; then
    echo "ERRO: Falha na execução de experimental_design.py!"
    exit 1
fi

echo "=== Executando run_experiments.py ==="
python3 scripts/run_experiments.py
if [ $? -ne 0 ]; then
    echo "ERRO: Falha na execução de run_experiments.py!"
    exit 1
fi

echo "=== Executando generate_graphs.py ==="
python3 scripts/generate_graphs.py
if [ $? -ne 0 ]; then
    echo "ERRO: Falha na execução de generate_graphs.py!"
    exit 1
fi

echo "=== Todos os scripts foram executados com sucesso ==="

