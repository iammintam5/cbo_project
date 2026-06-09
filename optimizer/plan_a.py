import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import (CARD_USERS, CARD_POSTS, LENGTH_POST,
                    NETWORK_BANDWIDTH_BPS, NETWORK_LATENCY_S,
                    DISK_IO_TIME_S, CPU_INST_TIME_S)
from optimizer.cost_model import CostComponents


PLAN_NAME = "Plan A — Ship-Whole-Table"


def compute_cost(
    card_users: int = CARD_USERS,
    card_posts: int = CARD_POSTS,
    length_post: int = LENGTH_POST,
) -> CostComponents:
    n_bytes = card_posts * length_post          # ship ALL posts
    n_msgs  = 1                                 # one bulk message
    n_ios   = card_posts                        # read every post tuple
    n_inst  = card_users * card_posts           # nested-loop join

    return CostComponents(
        plan_name = PLAN_NAME,
        n_inst    = n_inst,
        n_ios     = n_ios,
        n_msgs    = n_msgs,
        n_bytes   = n_bytes,
    )


def simulate_time(cost: CostComponents) -> float:
    """
    Estimate wall-clock execution time (seconds).

    transfer_time = bytes / bandwidth  +  latency_per_msg × msgs
    io_time       = ios  × disk_io_time
    cpu_time      = inst × cpu_inst_time
    """
    transfer_time = (cost.n_bytes / NETWORK_BANDWIDTH_BPS) + \
                    (cost.n_msgs  * NETWORK_LATENCY_S)
    io_time  = cost.n_ios  * DISK_IO_TIME_S
    cpu_time = cost.n_inst * CPU_INST_TIME_S
    return transfer_time + io_time + cpu_time


if __name__ == "__main__":
    c = compute_cost()
    print(c)
    print(f"  Simulated exec time    =  {simulate_time(c):.4f} s\n")
