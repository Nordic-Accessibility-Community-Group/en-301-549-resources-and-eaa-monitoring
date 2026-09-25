"""Generate the compatibility routing ledger from canonical country deliveries."""
import argparse
import json
from pathlib import Path
import country_records as cr
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--write', action='store_true')
args = parser.parse_args()
root = Path(__file__).resolve().parents[2]
text = json.dumps(cr.routing_projection(root), ensure_ascii=False, indent=2) + '\n'
if args.write:
    (root / '.github/agents/evidence-routing/events.json').write_text(text)
else:
    print(text, end='')
