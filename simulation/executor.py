# ============================================================
# simulation/executor.py — Execution Time Simulator
#
# "Actual simulated execution time" to compare against the
# CBO's estimated cost.  This satisfies the assignment metric:
#   "A breakdown of estimated cost vs actual simulated time."
#
# The simulator models:
#   - Network transfer latency (bandwidth + per-message latency)
#   - Disk I/O time
#   - CPU processing time
# ============================================================

import time
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import (CARD_USERS, CARD_POSTS, LENGTH_POST, LENGTH_UID,
                    SELECTIVITY, NETWORK_BANDWIDTH_BPS, NETWORK_LATENCY_S,
                    DISK_IO_TIME_S, CPU_INST_TIME_S)
from optimizer.cost_model import CostComponents
import optimizer.plan_a as plan_a
import optimizer.plan_b as plan_b


def _sim_time(cost: CostComponents) -> float:
    transfer = (cost.n_bytes / NETWORK_BANDWIDTH_BPS) + \
               (cost.n_msgs  * NETWORK_LATENCY_S)
    io_time  = cost.n_ios  * DISK_IO_TIME_S
    cpu_time = cost.n_inst * CPU_INST_TIME_S
    return transfer + io_time + cpu_time


def run_comparison(
    card_users:  int   = CARD_USERS,
    card_posts:  int   = CARD_POSTS,
    length_post: int   = LENGTH_POST,
    length_uid:  int   = LENGTH_UID,
    selectivity: float = SELECTIVITY,
) -> dict:
    """
    Run both plans, return a result dict with:
      - cost estimates
      - simulated execution times
      - data-transfer breakdown
    """
    cost_a  = plan_a.compute_cost(card_users, card_posts, length_post)
    cost_b  = plan_b.compute_cost(card_users, card_posts, length_post,
                                   length_uid, selectivity)
    time_a  = _sim_time(cost_a)
    time_b  = _sim_time(cost_b)

    return {
        "params": {
            "card_users":  card_users,
            "card_posts":  card_posts,
            "length_post": length_post,
            "selectivity": selectivity,
        },
        "plan_a": {
            "cost":          round(cost_a.total,  6),
            "sim_time_s":    round(time_a,         4),
            "bytes_MB":      round(cost_a.n_bytes / 1e6, 2),
            "breakdown":     cost_a.breakdown(),
        },
        "plan_b": {
            "cost":          round(cost_b.total,  6),
            "sim_time_s":    round(time_b,         4),
            "bytes_MB":      round(cost_b.n_bytes / 1e6, 2),
            "breakdown":     cost_b.breakdown(),
        },
        "winner": "Plan A" if cost_a.total <= cost_b.total else "Plan B",
        "cost_ratio":   round(max(cost_a.total, cost_b.total) /
                               min(cost_a.total, cost_b.total), 2),
        "time_ratio":   round(max(time_a, time_b) /
                               min(time_a, time_b), 2),
    }


def sensitivity_analysis() -> list[dict]:
    """
    Vary Card(Posts) from 1k to 10M to show how the CBO decision
    changes.  Returns a list of result rows for the report table.
    """
    rows = []
    for card_posts in [1_000, 10_000, 50_000, 100_000,
                        500_000, 1_000_000, 5_000_000, 10_000_000]:
        sel = CARD_USERS / card_posts if card_posts > CARD_USERS else 1.0
        r   = run_comparison(card_posts=card_posts, selectivity=sel)
        rows.append({
            "card_posts": card_posts,
            "cost_a":     r["plan_a"]["cost"],
            "cost_b":     r["plan_b"]["cost"],
            "time_a_s":   r["plan_a"]["sim_time_s"],
            "time_b_s":   r["plan_b"]["sim_time_s"],
            "winner":     r["winner"],
        })
    return rows


if __name__ == "__main__":
    r = run_comparison()
    print(f"\n{'='*56}")
    print(f"  EXECUTION SIMULATION  (Card(Posts) = {r['params']['card_posts']:,})")
    print(f"{'='*56}")
    for plan_key, label in [("plan_a", "Plan A — Ship-Whole-Table"),
                             ("plan_b", "Plan B — Semi-Join       ")]:
        p = r[plan_key]
        print(f"\n  {label}")
        print(f"    Estimated cost   : ${p['cost']:.4f}")
        print(f"    Data transferred : {p['bytes_MB']:.2f} MB")
        print(f"    Simulated time   : {p['sim_time_s']:.4f} s")
    print(f"\n  ✓ CBO winner  : {r['winner']}")
    print(f"  Cost ratio    : {r['cost_ratio']}×  (loser/winner)")
    print(f"  Time ratio    : {r['time_ratio']}×")
    print(f"{'='*56}\n")
