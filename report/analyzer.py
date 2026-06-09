import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from simulation.executor import run_comparison, sensitivity_analysis


# ── 1. Formatted cost breakdown ──────────────────────────────

def print_cost_breakdown():
    r = run_comparison()
    pa = r["plan_a"]["breakdown"]
    pb = r["plan_b"]["breakdown"]

    header = f"{'Metric':<22} {'Plan A (Ship)':>18} {'Plan B (Semi-Join)':>20}"
    sep    = "─" * len(header)

    print(f"\n{'='*len(header)}")
    print("  COST BREAKDOWN  —  Card(Users)=10k | Card(Posts)=1M")
    print(f"{'='*len(header)}")
    print(header)
    print(sep)

    rows = [
        ("#inst (CPU)",         f"{pa['n_inst']:>18,.0f}",  f"{pb['n_inst']:>20,.0f}"),
        ("#ios  (Disk)",        f"{pa['n_ios']:>18,.0f}",   f"{pb['n_ios']:>20,.0f}"),
        ("#msgs (Network)",     f"{pa['n_msgs']:>18,}",      f"{pb['n_msgs']:>20,}"),
        ("#bytes (Transfer)",   f"{pa['n_bytes']:>18,.0f}",  f"{pb['n_bytes']:>20,.0f}"),
        ("",                    "",                           ""),
        ("cost_cpu  ($)",       f"{pa['cost_cpu']:>17.4f}", f"{pb['cost_cpu']:>19.4f}"),
        ("cost_io   ($)",       f"{pa['cost_io']:>17.4f}",  f"{pb['cost_io']:>19.4f}"),
        ("cost_msg  ($)",       f"{pa['cost_msg']:>17.4f}", f"{pb['cost_msg']:>19.4f}"),
        ("cost_tr   ($)",       f"{pa['cost_tr']:>17.4f}",  f"{pb['cost_tr']:>19.4f}"),
        (sep,                   "",                           ""),
        ("TOTAL COST ($)",      f"{pa['total_cost']:>17.4f}",f"{pb['total_cost']:>19.4f}"),
        ("Sim. Time (s)",
         f"{r['plan_a']['sim_time_s']:>18.4f}",
         f"{r['plan_b']['sim_time_s']:>20.4f}"),
        ("Data (MB)",
         f"{r['plan_a']['bytes_MB']:>18.2f}",
         f"{r['plan_b']['bytes_MB']:>20.2f}"),
    ]

    for label, val_a, val_b in rows:
        if label == sep:
            print(sep)
        else:
            print(f"  {label:<20} {val_a} {val_b}")

    print(f"\n  ✓  CBO selects: {r['winner']}  "
          f"(cost ratio {r['cost_ratio']}×, time ratio {r['time_ratio']}×)\n")


# ── 2. Sensitivity table ─────────────────────────────────────

def print_sensitivity_table():
    rows = sensitivity_analysis()
    print(f"\n{'='*76}")
    print("  SENSITIVITY ANALYSIS  —  varying Card(Posts)")
    print(f"{'='*76}")
    print(f"  {'Card(Posts)':>12} {'Cost A':>12} {'Cost B':>12} "
          f"{'Time A (s)':>12} {'Time B (s)':>12} {'Winner':>10}")
    print("─" * 76)
    for row in rows:
        winner_mark = "◀ A" if row["winner"] == "Plan A" else "◀ B"
        print(f"  {row['card_posts']:>12,} {row['cost_a']:>12.4f} "
              f"{row['cost_b']:>12.4f} {row['time_a_s']:>12.4f} "
              f"{row['time_b_s']:>12.4f} {winner_mark:>10}")
    print()


# ── 3. Chart (matplotlib) ────────────────────────────────────

def plot_charts(output_dir: str = "report"):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.ticker as mticker
        import numpy as np
    except ImportError:
        print("  [warn] matplotlib not installed — skipping chart generation.")
        return

    rows  = sensitivity_analysis()
    posts = [r["card_posts"] for r in rows]
    ca    = [r["cost_a"]     for r in rows]
    cb    = [r["cost_b"]     for r in rows]
    ta    = [r["time_a_s"]   for r in rows]
    tb    = [r["time_b_s"]   for r in rows]

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle("CBO Prototype — Social Media\n"
                 "Cost & Execution Time vs Card(Posts)",
                 fontsize=13, fontweight="bold")

    COLOR_A = "#E8593C"
    COLOR_B = "#378ADD"

    for ax, y_a, y_b, ylabel, title in [
        (axes[0], ca, cb, "Estimated Total Cost ($)", "Estimated Cost"),
        (axes[1], ta, tb, "Simulated Execution Time (s)", "Simulated Time"),
    ]:
        ax.plot(posts, y_a, "o-", color=COLOR_A, linewidth=2,
                markersize=6, label="Plan A — Ship-Whole-Table")
        ax.plot(posts, y_b, "s-", color=COLOR_B, linewidth=2,
                markersize=6, label="Plan B — Semi-Join")
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlabel("Card(Posts)  [log scale]", fontsize=10)
        ax.set_ylabel(ylabel, fontsize=10)
        ax.set_title(title, fontsize=11)
        ax.legend(fontsize=9)
        ax.grid(True, which="both", linestyle="--", alpha=0.4)
        ax.xaxis.set_major_formatter(
            mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))

    # Shade the region where each plan wins on the cost chart
    axes[0].fill_between(posts, ca, cb,
                          where=[a <= b for a, b in zip(ca, cb)],
                          alpha=0.12, color=COLOR_A, label="A cheaper zone")
    axes[0].fill_between(posts, ca, cb,
                          where=[b < a for a, b in zip(ca, cb)],
                          alpha=0.12, color=COLOR_B, label="B cheaper zone")

    plt.tight_layout()
    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, "cost_comparison.png")
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    print(f"  Chart saved → {out_path}")
    plt.close()


if __name__ == "__main__":
    print_cost_breakdown()
    print_sensitivity_table()
    plot_charts()
