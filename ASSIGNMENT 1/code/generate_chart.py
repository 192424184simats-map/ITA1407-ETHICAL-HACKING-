"""Generate the assignment's Task 10 comparison chart from supplied scenario values."""
from pathlib import Path
import csv
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "scalability_metrics.csv"
OUT_PATH = ROOT / "images" / "task10-scalability.png"


def main() -> None:
    rows = list(csv.DictReader(CSV_PATH.open(newline="", encoding="utf-8")))
    labels = [r["process"] for r in rows]
    small = [float(r["small_programme"]) for r in rows]
    large = [float(r["large_programme"]) for r in rows]

    fig, ax = plt.subplots(figsize=(10, 5.5))
    x = list(range(len(labels)))
    width = 0.36
    bars1 = ax.bar([i - width / 2 for i in x], small, width, label="Small programme")
    bars2 = ax.bar([i + width / 2 for i in x], large, width, label="Large programme")
    ax.set_title("Task 10 — Governance process measures")
    ax.set_ylabel("Value (unit shown on x-axis)")
    ax.set_xticks(x, labels)
    ax.legend()
    ax.grid(axis="y", alpha=0.25)
    ax.bar_label(bars1, padding=3, fmt="%.0f")
    ax.bar_label(bars2, padding=3, fmt="%.0f")
    fig.tight_layout()
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_PATH, dpi=180)
    print(f"Saved chart: {OUT_PATH}")


if __name__ == "__main__":
    main()
