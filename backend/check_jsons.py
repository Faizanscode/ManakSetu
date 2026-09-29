import json
import glob

for f in glob.glob("rec_*.json"):
    with open(f) as file:
        data = json.load(file)
        for r in data.get("recommendations", []):
            for k in ['score_breakdown', 'relationships', 'explanation', 'evidence', 'sources', 'relevance_score']:
                if k not in r or r[k] is None:
                    print(f"{f}: {k} is missing or None")
            if 'score_breakdown' in r and r['score_breakdown'] is not None:
                for sk in ['semantic', 'product', 'application', 'keyword', 'scope', 'category_sector']:
                    if sk not in r['score_breakdown'] or r['score_breakdown'][sk] is None:
                         print(f"{f}: score_breakdown.{sk} is missing or None")
