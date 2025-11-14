import sqlite3
from pathlib import Path

DB_PATH = Path("data/results.db")
OUT_YAHOO = Path("data/yahoo.txt")
OUT_LLM = Path("data/llm.txt")

def normalize(s: str) -> str:
    if s is None:
        return ""
    return " ".join(s.strip().split())

def export_column(cursor, col_name: str, out_path: Path) -> int:
    try:
        cursor.execute(f"SELECT {col_name} FROM results")
    except sqlite3.OperationalError as e:
        raise SystemExit(
            f"[ERROR] No pude leer la columna '{col_name}'. "
            f"¿Existe la tabla 'results' y esa columna? Detalle: {e}"
        )
    rows = cursor.fetchall()

    out_path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with out_path.open("w", encoding="utf-8", newline="\n") as f:
        for (val,) in rows:
            text = normalize(val)
            if text:
                f.write(text + "\n")
                count += 1
    return count

def main():
    if not DB_PATH.exists():
        raise SystemExit(f"[ERROR] No existe {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    n_yahoo = export_column(cur, "human_answer", OUT_YAHOO)
    n_llm = export_column(cur, "llm_answer", OUT_LLM)

    conn.close()
    print(f"[OK] Exportado: {n_yahoo} líneas en {OUT_YAHOO}")
    print(f"[OK] Exportado: {n_llm} líneas en {OUT_LLM}")
    if n_yahoo == 0 or n_llm == 0:
        print("Alguno de los archivos quedó vacio.")

if __name__ == "__main__":
    main()