import json
import random
from pathlib import Path

import pandas as pd


random.seed(42)

RISK_MODELS = {
    "Conservative": {
        "Equity": 0.20,
        "Debt": 0.65,
        "Gold": 0.15,
    },
    "Moderately Conservative": {
        "Equity": 0.40,
        "Debt": 0.45,
        "Gold": 0.15,
    },
    "Moderate": {
        "Equity": 0.60,
        "Debt": 0.30,
        "Gold": 0.10,
    },
    "Moderately Aggressive": {
        "Equity": 0.75,
        "Debt": 0.15,
        "Gold": 0.10,
    },
    "Aggressive": {
        "Equity": 0.90,
        "Debt": 0.05,
        "Gold": 0.05,
    },
}


FIRST_NAMES = [
    "Rahul","Amit","Neha","Riya","Sneha",
    "Vikram","Rohan","Ananya","Priya",
    "Karan","Rakesh","Pooja","Meera",
    "Arjun","Nikhil","Suresh","Ankit",
    "Divya","Ayesha","Ritu"
]

LAST_NAMES = [
    "Sharma","Patel","Singh","Verma",
    "Reddy","Pradhan","Das","Mishra",
    "Nair","Joshi","Kapoor","Gupta",
    "Jain","Yadav","Sahoo"
]


clients = []

for i in range(1, 501):

    risk = random.choice(list(RISK_MODELS.keys()))

    target = RISK_MODELS[risk]

    current = {}

    for asset in target:

        noise = random.uniform(-0.08, 0.08)

        current[asset] = round(target[asset] + noise, 2)

    total = sum(current.values())

    current = {
        k: round(v / total, 2)
        for k, v in current.items()
    }

    clients.append({

        "portfolio_id": f"WP-{1000+i}",

        "client_name":
            random.choice(FIRST_NAMES)
            + " "
            + random.choice(LAST_NAMES),

        "risk_category": risk,

        "portfolio_value":
            random.randint(
                500000,
                50000000,
            ),

        "current_allocation": current,

        "target_allocation": target,

    })

Path("data").mkdir(exist_ok=True)

pd.DataFrame(clients).to_csv(
    "data/clients.csv",
    index=False,
)

with open(
    "data/clients.json",
    "w",
) as f:

    json.dump(
        clients,
        f,
        indent=4,
    )

print(
    f"Generated {len(clients)} portfolios."
)