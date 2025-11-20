#script que gera o .csv do experimento
import csv
import itertools



def generate_full_factorial_csv(prediction_variables, response_variables, output_file='experimental_design.csv', repetitions=5):
    """
    Gera um arquivo CSV com design experimental fatorial completo.

    Args:
        mpi_method (list): Lista de métodos de MPI
        num_processes (list): Lista de números de processos
        matrix_sizes (list): Lista de tamanhos de matriz
        output_file (str): Nome do arquivo CSV de saída
        repetitions (int): Número de repetições por combinação (default = 5)
    """

    mpi_method = prediction_variables["mpi_method"]
    num_processes = prediction_variables["num_processes"]
    matrix_sizes = prediction_variables["matrix_size"]


    combinations = list(itertools.product(mpi_method, num_processes, matrix_sizes, range(1, repetitions + 1)))

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # Escreve o cabeçalho
        writer.writerow(list(prediction_variables.keys()) + ["repetition"] + list(response_variables.keys()))

        # Escreve cada combinação
        for mpi_method, num_proc, matrix_size, repetition in combinations:
            writer.writerow([mpi_method, num_proc, matrix_size, repetition])

    print(f"Arquivo CSV gerado: {output_file}")
    print(f"Total de combinações: {len(combinations)}")

def main():

    prediction_variables = {
        "mpi_method": ["coletiva", "bloqueante", "nao_bloqueante"],
        "num_processes": [1, 2, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40],
        "matrix_size": [128, 256, 512, 1024],
    }


    response_variables = {
        "execution_time": "Execution time",
        "communication_time": "Communication time",
    }


    generate_full_factorial_csv(prediction_variables, response_variables)

if __name__ == "__main__":
    main()