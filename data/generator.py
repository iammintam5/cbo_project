import random
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import CARD_USERS, CARD_POSTS


def generate_users(n: int = CARD_USERS) -> list[dict]:
    users = []
    for uid in range(1, n + 1):
        users.append({
            "uid":      uid,
            "name":     f"user_{uid}",
            "email":    f"user_{uid}@social.com",
            "age":      random.randint(18, 65),
            "country":  random.choice(["VN", "US", "JP", "FR"]),
            "site":     "A" if uid <= n // 2 else "B",
        })
    return users


def generate_posts(m: int = CARD_POSTS, n_users: int = CARD_USERS) -> list[dict]:
    posts = []
    for pid in range(1, m + 1):
        posts.append({
            "pid":      pid,
            "uid":      random.randint(1, n_users),   # FK → Users
            "content":  f"post_content_{pid}",
            "likes":    random.randint(0, 10_000),
            "site":     "B",
        })
    return posts


def get_site_a_users(users: list[dict]) -> list[dict]:
    return [u for u in users if u["site"] == "A"]


def get_site_b_users(users: list[dict]) -> list[dict]:
    return [u for u in users if u["site"] == "B"]


if __name__ == "__main__":
    print("Generating dataset...")
    users = generate_users()
    posts = generate_posts()
    site_a = get_site_a_users(users)
    site_b = get_site_b_users(users)
    print(f"  Users total : {len(users):>10,}")
    print(f"    Site A    : {len(site_a):>10,}")
    print(f"    Site B    : {len(site_b):>10,}")
    print(f"  Posts total : {len(posts):>10,}")
    print(f"    All on    : {'Site B':>10}")
