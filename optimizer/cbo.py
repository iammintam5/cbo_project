import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import (CARD_USERS, CARD_POSTS, LENGTH_POST,
                    LENGTH_UID, SELECTIVITY)
import optimizer.plan_a as plan_a
import optimizer.plan_b as plan_b
from optimizer.cost_model import CostComponents


def pick_plan(
    card_users:  int   = CARD_USERS,
    card_posts:  int   = CARD_POSTS,
    length_post: int   = LENGTH_POST,
    length_uid:  int   = LENGTH_UID,
    selectivity: float = SELECTIVITY,
) -> tuple[str, CostComponents, CostComponents]:
    cost_a = plan_a.compute_cost(card_users, card_posts, length_post)
    cost_b = plan_b.compute_cost(card_users, card_posts, length_post,
                                  length_uid, selectivity)

    if cost_a.total <= cost_b.total:
        return cost_a.plan_name, cost_a, cost_b
    else:
        return cost_b.plan_name, cost_b, cost_a


def semi_join_breakeven_posts(
    card_users:  int   = CARD_USERS,
    length_post: int   = LENGTH_POST,
    length_uid:  int   = LENGTH_UID,
    selectivity: float = SELECTIVITY,
) -> float:

    from config import C_TR, C_MSG
    numerator   = C_TR * card_users * length_uid + C_MSG  # extra msg for B
    denominator = C_TR * (1 - selectivity) * length_post
    return numerator / denominator


if __name__ == "__main__":
    name, winner, loser = pick_plan()
    print(winner)
    print(loser)
    print(f"\n  ✓ CBO picks: {name}")
    be = semi_join_breakeven_posts()
    print(f"  Breakeven Card(Posts) ≈ {be:,.0f}  "
          f"(Semi-Join wins above this threshold)")
