from dataclasses import dataclass, field
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import C_CPU, C_IO, C_MSG, C_TR


@dataclass
class CostComponents:
    """Holds the raw counts and the final computed cost."""
    plan_name:  str

    # Raw counts
    n_inst:   float = 0.0   # number of CPU instructions
    n_ios:    float = 0.0   # number of disk I/O operations
    n_msgs:   int   = 0     # number of network messages
    n_bytes:  float = 0.0   # total bytes transferred

    # Derived (computed in __post_init__)
    cost_cpu:  float = field(init=False)
    cost_io:   float = field(init=False)
    cost_msg:  float = field(init=False)
    cost_tr:   float = field(init=False)
    total:     float = field(init=False)

    def __post_init__(self):
        self.cost_cpu = C_CPU * self.n_inst
        self.cost_io  = C_IO  * self.n_ios
        self.cost_msg = C_MSG * self.n_msgs
        self.cost_tr  = C_TR  * self.n_bytes
        self.total    = self.cost_cpu + self.cost_io + self.cost_msg + self.cost_tr

    def breakdown(self) -> dict:
        return {
            "plan":       self.plan_name,
            "n_inst":     self.n_inst,
            "n_ios":      self.n_ios,
            "n_msgs":     self.n_msgs,
            "n_bytes":    self.n_bytes,
            "cost_cpu":   round(self.cost_cpu,  6),
            "cost_io":    round(self.cost_io,   6),
            "cost_msg":   round(self.cost_msg,  6),
            "cost_tr":    round(self.cost_tr,   6),
            "total_cost": round(self.total,     6),
        }

    def __str__(self) -> str:
        b = self.breakdown()
        return (
            f"\n{'='*52}\n"
            f"  Plan : {b['plan']}\n"
            f"{'─'*52}\n"
            f"  #inst  = {b['n_inst']:>15,.0f}   → cost_cpu = ${b['cost_cpu']:>10.4f}\n"
            f"  #ios   = {b['n_ios']:>15,.0f}   → cost_io  = ${b['cost_io']:>10.4f}\n"
            f"  #msgs  = {b['n_msgs']:>15,}   → cost_msg = ${b['cost_msg']:>10.4f}\n"
            f"  #bytes = {b['n_bytes']:>15,.0f}   → cost_tr  = ${b['cost_tr']:>10.4f}\n"
            f"{'─'*52}\n"
            f"  TOTAL COST             = ${b['total_cost']:>10.4f}\n"
            f"{'='*52}"
        )
