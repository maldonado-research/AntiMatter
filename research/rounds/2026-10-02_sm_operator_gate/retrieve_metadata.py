"""Bounded citation/recent-metadata checks, not exhaustive web review."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, HTTPRedirectHandler, build_opener

root = Path(__file__).resolve().parent / 'literature'
root.mkdir(exist_ok=True)
class RestrictedRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if urlsplit(newurl).hostname != 'inspirehep.net':
            raise RuntimeError('Unexpected redirect host')
        return super().redirect_request(req, fp, code, msg, headers, newurl)

queries = [('classic_conversion', 'doi:10.1103/PhysRevD.42.3344'),
           ('recent_sources', 'date 2026 and "spontaneous baryogenesis"'),
           ('recent_wilson', 'date 2026 and ("Wilson line" or clockwork) and baryogenesis')]
def retrieve(item):
    label, query = item
    url = 'https://inspirehep.net/api/literature?' + urlencode(
        {'q': query, 'size': 10, 'sort': 'mostrecent',
         'fields': 'titles,authors,dois,arxiv_eprints,preprint_date,earliest_date,publication_info'})
    receipt = {'label': label, 'query': query, 'url': url,
               'review_depth': 'bibliographic metadata only; no full-text inference'}
    try:
        opener = build_opener(RestrictedRedirect)
        with opener.open(Request(url, headers={'User-Agent': 'Antimatter-bounded-citation-check/1.0'}), timeout=40) as response:
            raw = response.read()
            receipt.update(http_status=response.status, response_sha256=hashlib.sha256(raw).hexdigest())
        data = json.loads(raw)
        receipt['reported_total'] = data.get('hits', {}).get('total')
        for hit in data.get('hits', {}).get('hits', []):
            hit['metadata']['authors'] = [{'full_name': a.get('full_name')} for a in hit['metadata'].get('authors', [])]
        receipt['records'] = [{'inspire_id': hit['id'], 'metadata': hit['metadata']}
                              for hit in data.get('hits', {}).get('hits', [])]
    except Exception as error:
        receipt['error'] = type(error).__name__ + ': ' + str(error)
    return receipt

with ThreadPoolExecutor(max_workers=3) as pool:
    results = list(pool.map(retrieve, queries))
report = {'retrieved_utc': datetime.now(timezone.utc).isoformat(),
          'scope': 'Three bounded INSPIRE queries, at most ten metadata records each; previous selected full-text review is separately recorded',
          'queries': results}
(root / 'METADATA_RECEIPTS.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps([{'label': r['label'], 'http_status': r.get('http_status'),
                   'records': len(r.get('records', [])), 'error': r.get('error')}
                  for r in results]))
