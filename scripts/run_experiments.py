import csv
import os
import re
import subprocess
from typing import Dict, Tuple, Optional

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSV_PATH = os.path.join(PROJECT_ROOT, "experimental_design.csv")
BUILD_DIR = os.path.join(PROJECT_ROOT, "build")

METHOD_EXECUTABLE = {
    "coletiva": "mpi_coletiva",
    "bloqueante": "mpi_p2p_bloqueante",
    "nao_bloqueante": "mpi_p2p_naobloqueante",
}

RESULT_COLUMNS = [
    "execution_time",
    "communication_time",
    "status",
    "stderr",
]


def run_experiment(method: str, num_processes: int, matrix_size: int) -> Tuple[str, str, int]:
    exe_name = METHOD_EXECUTABLE.get(method)
    if not exe_name:
        return "", f"Unknown mpi_method '{method}'", 127

    exe_path = os.path.join(BUILD_DIR, exe_name)
    if not os.path.isfile(exe_path):
        return "", f"Executable not found: {exe_path}", 127

    cmd = ["mpirun", "-np", str(num_processes), "--oversubscribe", exe_path, str(matrix_size)]
    try:
        completed = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=PROJECT_ROOT,
            check=False,
        )
        return completed.stdout, completed.stderr, completed.returncode
    except Exception as e:
        return "", str(e), 1


def parse_metrics(stdout_text: str) -> Optional[Dict[str, str]]:
    # Expect lines printed by rank 0, e.g.:
    # Execution time: 0.123456
    # Communication time: 0.012345
    exec_time = re.search(r"Execution time:\s*([0-9]*\.?[0-9]+)", stdout_text)
    comm_time = re.search(r"Communication time:\s*([0-9]*\.?[0-9]+)", stdout_text)

    if not (exec_time and comm_time):
        return None

    return {
        "execution_time": exec_time.group(1),
        "communication_time": comm_time.group(1),
    }


def row_has_results(row: Dict[str, str]) -> bool:
    return all(col in row and str(row[col]).strip() != "" for col in RESULT_COLUMNS)


def main():
    if not os.path.isfile(CSV_PATH):
        raise FileNotFoundError(f"CSV not found at {CSV_PATH}")

    with open(CSV_PATH, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        base_fieldnames = list(reader.fieldnames or [])

        out_fieldnames = base_fieldnames[:]
        for col in RESULT_COLUMNS:
            if col not in out_fieldnames:
                out_fieldnames.append(col)

        rows = list(reader)

    updated_rows = []
    counter = 1
    total_rows = len(rows)
    for row in rows:
        repetition = int(row.get("repetition", "1") or "1")
        print(f"Executando experimento {counter} de {total_rows} (repetição {repetition})")
        counter += 1
        method = (row.get("mpi_method") or "").strip()
        num_proc = int(row.get("num_processes", "0"))
        size = int(row.get("matrix_size", "0"))

        #pula se ja tem resultados
        if row_has_results(row):
            row["status"] = row.get("status", "skipped_existing_results")
            updated_rows.append(row)
            continue

        stdout_text, stderr_text, rc = run_experiment(method, num_proc, size)
        if rc == 0:
            if(len(stdout_text) > 200):
                print("Mpi error")
                continue
            metrics = parse_metrics(stdout_text)
            if metrics:
                row.update(metrics)
                row["status"] = "ok"
            else:
                row["status"] = "parse_error"
        else:
            row["status"] = f"rc_{rc}"

        row["stderr"] = (stderr_text or "").strip()[:2000]
        updated_rows.append(row)

    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=out_fieldnames)
        writer.writeheader()
        for row in updated_rows:
            for col in out_fieldnames:
                if col not in row:
                    row[col] = ""
            writer.writerow(row)


if __name__ == "__main__":
    main()


