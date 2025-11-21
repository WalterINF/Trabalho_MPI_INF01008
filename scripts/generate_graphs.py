import csv
import os
from collections import defaultdict
from statistics import mean
from typing import Dict, List
import shutil
import matplotlib.pyplot as plt


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(PROJECT_ROOT, "experimental_design.csv")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "graphs")

MPI_METHODS = ["coletiva", "bloqueante", "nao_bloqueante"]
MATRIX_SIZES = [2048, 1024, 512, 128]
EXECUTION_OUTPUT_TEMPLATE = "execution_time_methods_{matrix_size}.png"
COMMUNICATION_OUTPUT_TEMPLATE = "communication_percentage_{matrix_size}.png"
SPEEDUP_OUTPUT_TEMPLATE = "speedup_{matrix_size}.png"

if os.path.exists(OUTPUT_DIR):
    shutil.rmtree(OUTPUT_DIR)


def ensure_output_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def load_rows(csv_path: str) -> List[Dict[str, str]]:
    with open(csv_path, "r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]


def aggregate_execution_times(rows: List[Dict[str, str]], matrix_size: int) -> Dict[str, Dict[int, float]]:
    per_method: Dict[str, Dict[int, List[float]]] = {
        method: defaultdict(list) for method in MPI_METHODS
    }

    for row in rows:
        try:
            method = (row.get("mpi_method") or "").strip()
            size = int(row.get("matrix_size", "0"))
            num_proc = int(row.get("num_processes", "0"))
            exec_time = float(row.get("execution_time", "nan"))
        except ValueError:
            continue

        if method not in per_method or size != matrix_size:
            continue

        if exec_time > 0:
            per_method[method][num_proc].append(exec_time)

    aggregated: Dict[str, Dict[int, float]] = {}
    for method, per_process in per_method.items():
        aggregated[method] = {
            proc: mean(times) for proc, times in per_process.items() if times
        }
    return aggregated


def plot_execution_time(per_method: Dict[str, Dict[int, float]], matrix_size: int) -> None:
    plt.figure(figsize=(8, 5))
    plotted_any = False

    for method in MPI_METHODS:
        per_process = per_method.get(method, {})
        if not per_process:
            continue

        num_processes = sorted(per_process.keys())
        execution_times = [per_process[proc] for proc in num_processes]
        plt.plot(num_processes, execution_times, marker="o", label=method)
        plotted_any = True

    if not plotted_any:
        print(f"Nenhum dado disponível para matriz {matrix_size}")
        plt.close()
        return

    plt.title(f"Tempo de execução x processos (matriz {matrix_size})")
    plt.xlabel("Número de processos")
    plt.ylabel("Tempo de execução (s)")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend(title="Método MPI")

    filename = EXECUTION_OUTPUT_TEMPLATE.format(matrix_size=matrix_size)
    output_path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()
    print(f"Gráfico salvo em: {output_path}")


def aggregate_communication_percentage(rows: List[Dict[str, str]], matrix_size: int) -> Dict[str, Dict[int, float]]:
    per_method: Dict[str, Dict[int, List[float]]] = {
        method: defaultdict(list) for method in MPI_METHODS
    }

    for row in rows:
        try:
            method = (row.get("mpi_method") or "").strip()
            size = int(row.get("matrix_size", "0"))
            num_proc = int(row.get("num_processes", "0"))
            exec_time = float(row.get("execution_time", "nan"))
            comm_time = float(row.get("communication_time", "nan"))
        except ValueError:
            continue

        if method not in per_method or size != matrix_size:
            continue

        if exec_time > 0 and comm_time >= 0:
            percentage = (comm_time / exec_time) * 100
            per_method[method][num_proc].append(percentage)

    aggregated: Dict[str, Dict[int, float]] = {}
    for method, per_process in per_method.items():
        aggregated[method] = {
            proc: mean(times) for proc, times in per_process.items() if times
        }
    return aggregated


def plot_communication_percentage(per_method: Dict[str, Dict[int, float]], matrix_size: int) -> None:
    plt.figure(figsize=(8, 5))
    plotted_any = False

    for method in MPI_METHODS:
        per_process = per_method.get(method, {})
        if not per_process:
            continue

        num_processes = sorted(per_process.keys())
        percentages = [per_process[proc] for proc in num_processes]
        plt.plot(num_processes, percentages, marker="o", label=method)
        plotted_any = True

    if not plotted_any:
        print(f"Nenhum dado de comunicação disponível para matriz {matrix_size}")
        plt.close()
        return

    plt.title(f"% tempo comunicação x processos (matriz {matrix_size})")
    plt.xlabel("Número de processos")
    plt.ylabel("% do tempo gasto em comunicação")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend(title="Método MPI")

    filename = COMMUNICATION_OUTPUT_TEMPLATE.format(matrix_size=matrix_size)
    output_path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()
    print(f"Gráfico salvo em: {output_path}")


def aggregate_speedup(rows: List[Dict[str, str]], matrix_size: int) -> Dict[str, Dict[int, float]]:
    # First, get baseline execution times (num_processes=1) for each method
    baseline_times: Dict[str, List[float]] = defaultdict(list)
    
    for row in rows:
        try:
            method = (row.get("mpi_method") or "").strip()
            size = int(row.get("matrix_size", "0"))
            num_proc = int(row.get("num_processes", "0"))
            exec_time = float(row.get("execution_time", "nan"))
        except ValueError:
            continue

        if method not in MPI_METHODS or size != matrix_size:
            continue

        if num_proc == 1 and exec_time > 0:
            baseline_times[method].append(exec_time)

    # Calculate mean baseline for each method
    baseline_means: Dict[str, float] = {
        method: mean(times) for method, times in baseline_times.items() if times
    }

    # Now aggregate execution times for all processes
    per_method_exec = aggregate_execution_times(rows, matrix_size)

    # Calculate speedup for each method and process count
    speedup_data: Dict[str, Dict[int, float]] = {}
    
    for method in MPI_METHODS:
        baseline = baseline_means.get(method)
        if not baseline or baseline <= 0:
            continue

        speedup_data[method] = {}
        per_process = per_method_exec.get(method, {})
        
        for num_proc, exec_time in per_process.items():
            if num_proc > 0 and exec_time > 0:
                speedup = baseline / exec_time
                speedup_data[method][num_proc] = speedup

    return speedup_data


def plot_speedup(per_method: Dict[str, Dict[int, float]], matrix_size: int) -> None:
    plt.figure(figsize=(8, 5))
    plotted_any = False

    for method in MPI_METHODS:
        per_process = per_method.get(method, {})
        if not per_process:
            continue

        num_processes = sorted(per_process.keys())
        speedups = [per_process[proc] for proc in num_processes]
        plt.plot(num_processes, speedups, marker="o", label=method)
        plotted_any = True

    if not plotted_any:
        print(f"Nenhum dado de speedup disponível para matriz {matrix_size}")
        plt.close()
        return

    plt.title(f"Speedup x processos (matriz {matrix_size})")
    plt.xlabel("Número de processos")
    plt.ylabel("Speedup")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend(title="Método MPI")

    filename = SPEEDUP_OUTPUT_TEMPLATE.format(matrix_size=matrix_size)
    output_path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()
    print(f"Gráfico salvo em: {output_path}")


def main() -> None:
    if not os.path.isfile(CSV_PATH):
        raise FileNotFoundError(f"Arquivo CSV não encontrado em {CSV_PATH}")

    ensure_output_dir(OUTPUT_DIR)
    rows = load_rows(CSV_PATH)

    for matrix_size in MATRIX_SIZES:
        per_method_exec = aggregate_execution_times(rows, matrix_size)
        plot_execution_time(per_method_exec, matrix_size)

        per_method_comm = aggregate_communication_percentage(rows, matrix_size)
        plot_communication_percentage(per_method_comm, matrix_size)

        per_method_speedup = aggregate_speedup(rows, matrix_size)
        plot_speedup(per_method_speedup, matrix_size)


if __name__ == "__main__":
    main()

