import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import (CARD_USERS, CARD_POSTS, LENGTH_POST,
                    LENGTH_UID, SELECTIVITY,
                    NETWORK_BANDWIDTH_BPS, NETWORK_LATENCY_S,
                    DISK_IO_TIME_S, CPU_INST_TIME_S)
from optimizer.cost_model import CostComponents


PLAN_NAME = "Plan B — Semi-Join"


def compute_cost(
    card_users: int  = CARD_USERS,
    card_posts: int  = CARD_POSTS,
    length_post: int = LENGTH_POST,
    length_uid: int  = LENGTH_UID,
    selectivity: float = SELECTIVITY,
) -> CostComponents:
    # Step 1: send uid projection of Users → Site B
    bytes_step1 = card_users * length_uid

    # Step 2: filter Posts at Site B
    posts_filtered = card_posts * selectivity

    # Step 3: send filtered Posts back → Site A
    bytes_step3 = posts_filtered * length_post

    n_bytes = bytes_step1 + bytes_step3
    n_msgs  = 2                               # step1 send + step3 send
    n_ios   = card_posts + posts_filtered     # scan Posts + read filtered
    # hash-join on the filtered set (much cheaper than nested loop)
    n_inst  = card_posts + card_users + posts_filtered

    return CostComponents(
        plan_name = PLAN_NAME,
        n_inst    = n_inst,
        n_ios     = n_ios,
        n_msgs    = n_msgs,
        n_bytes   = n_bytes,
    )


def simulate_time(cost: CostComponents) -> float:
    transfer_time = (cost.n_bytes / NETWORK_BANDWIDTH_BPS) + \
                    (cost.n_msgs  * NETWORK_LATENCY_S)
    io_time  = cost.n_ios  * DISK_IO_TIME_S
    cpu_time = cost.n_inst * CPU_INST_TIME_S
    return transfer_time + io_time + cpu_time


if __name__ == "__main__":
    c = compute_cost()
    print(c)
    print(f"  Simulated exec time    =  {simulate_time(c):.4f} s\n")
