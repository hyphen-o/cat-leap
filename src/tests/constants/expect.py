import sys

sys.path.append("../")
from utils import RecursiveNamespace

MILE_STATS = {
    "length": {
        "bas_to_dev": {
            "list": [14, 4],
            "mean": 9,
        },
        "dev_to_mas": {
            "list": [3, 7],
            "mean": 5,
        },
    },
    "duplication": {
        "bas_to_dev": [
            {
                "Count": 2,
                "Edge": {
                    "StartP": {
                        "Abst": 1,
                        "Para": 1,
                        "Logi": 0,
                        "Sync": 0,
                        "Flow": 1,
                        "User": 1,
                        "Data": 0,
                        "CTScore": 4,
                        "IsRemix": 0,
                        "Level": "BASIC",
                    },
                    "EndP": {
                        "Abst": 1,
                        "Para": 1,
                        "Logi": 0,
                        "Sync": 0,
                        "Flow": 1,
                        "User": 1,
                        "Data": 0,
                        "CTScore": 4,
                        "IsRemix": 0,
                        "Level": "BASIC",
                    },
                },
            },
            {
                "Count": 1,
                "Edge": {
                    "StartP": {
                        "Abst": 1,
                        "Para": 1,
                        "Logi": 0,
                        "Sync": 0,
                        "Flow": 1,
                        "User": 1,
                        "Data": 0,
                        "CTScore": 4,
                        "IsRemix": 0,
                        "Level": "BASIC",
                    },
                    "EndP": "NEXT_LEVEL",
                },
            },
            {
                "Count": 1,
                "Edge": {
                    "StartP": {
                        "Abst": 0,
                        "Para": 0,
                        "Logi": 0,
                        "Sync": 0,
                        "Flow": 0,
                        "User": 0,
                        "Data": 0,
                        "CTScore": 0,
                        "IsRemix": 0,
                        "Level": "BASIC",
                    },
                    "EndP": {
                        "Abst": 1,
                        "Para": 1,
                        "Logi": 3,
                        "Sync": 3,
                        "Flow": 2,
                        "User": 2,
                        "Data": 1,
                        "CTScore": 13,
                        "IsRemix": 1,
                        "Level": "DEVELOPING",
                    },
                },
            },
            {
                "Count": 1,
                "Edge": {
                    "StartP": {
                        "Abst": 1,
                        "Para": 1,
                        "Logi": 3,
                        "Sync": 3,
                        "Flow": 2,
                        "User": 2,
                        "Data": 1,
                        "CTScore": 13,
                        "IsRemix": 1,
                        "Level": "DEVELOPING",
                    },
                    "EndP": "NEXT_LEVEL",
                },
            },
        ]
    },
}
