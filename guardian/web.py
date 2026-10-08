"""Dependency-free local demo for public evaluation."""
from __future__ import annotations

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import argparse
import json
from pathlib import Path
from urllib.parse import urlparse

from .verifier import verify_bundle

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "fixtures"

PAGE = r'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Pulse PoPW Guardian</title><style>
:root{color-scheme:dark;--bg:#07110f;--card:#10201c;--ink:#e9fff7;--muted:#92b7aa;--mint:#43f5ad;--red:#ff667a;--amber:#ffc85c}*{box-sizing:border-box}body{margin:0;background:radial-gradient(circle at 20% 0,#163d31 0,transparent 35%),var(--bg);color:var(--ink);font:15px/1.5 ui-sans-serif,system-ui;min-height:100vh}.wrap{max-width:1100px;margin:auto;padding:48px 22px}header{display:flex;justify-content:space-between;gap:30px;align-items:end;margin-bottom:28px}h1{font-size:clamp(35px,7vw,70px);line-height:.95;margin:8px 0;letter-spacing:-.055em}.tag{color:var(--mint);font:700 12px monospace;letter-spacing:.18em}.sub{max-width:610px;color:var(--muted);font-size:17px}.grid{display:grid;grid-template-columns:1.05fr .95fr;gap:18px}.card{background:linear-gradient(145deg,#132722dd,#0b1714ee);border:1px solid #29453d;border-radius:18px;padding:20px;box-shadow:0 20px 60px #0005}textarea{width:100%;height:420px;resize:vertical;background:#07100e;color:#caefe2;border:1px solid #315349;border-radius:12px;padding:14px;font:12px/1.5 ui-monospace,monospace}button,select{border-radius:10px;border:1px solid #416c5e;padding:10px 14px;background:#172e28;color:var(--ink);font-weight:700}button{background:var(--mint);color:#052117;border:0;cursor:pointer}.bar{display:flex;gap:8px;margin-bottom:12px}.verdict{font-size:38px;font-weight:900;letter-spacing:-.03em}.SUCCESS{color:var(--mint)}.FAILURE{color:var(--red)}.INCONCLUSIVE{color:var(--amber)}.metrics{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:18px 0}.metric{padding:11px;border-radius:10px;background:#07110f}.metric b{float:right}.reasons{font:12px monospace;color:var(--amber)}pre{white-space:pre-wrap;word-break:break-word;background:#07110f;padding:12px;border-radius:10px;max-height:220px;overflow:auto;color:#a9d7c8}@media(max-width:800px){.grid{grid-template-columns:1fr}header{display:block}}
</style></head><body><main class="wrap"><header><div><div class="tag">EVIDENCE FIRST · DETERMINISTIC</div><h1>PoPW<br>Guardian</h1></div><p class="sub">An offline verification boundary for physical-work evidence. Inspect provenance, score Konnex-aligned metrics, and issue reproducible audit receipts—without a wallet or hidden model.</p></header><div class="grid"><section class="card"><div class="bar"><select id="fixture"><option value="valid_success">Valid success</option><option value="tampered_failure">Tampered failure</option><option value="incomplete_inconclusive">Incomplete evidence</option></select><button id="verify">Verify bundle</button></div><textarea id="bundle" spellcheck="false"></textarea></section><section class="card"><div class="tag">VERIFICATION RESULT</div><div id="verdict" class="verdict">READY</div><div id="summary" class="sub">Choose a fixture or edit its JSON.</div><div id="metrics" class="metrics"></div><div id="reasons" class="reasons"></div><h3>Audit receipt</h3><pre id="receipt">No receipt yet.</pre></section></div></main><script>
const $=x=>document.getElementById(x);async function load(){const r=await fetch('/api/fixtures/'+$('fixture').value);$('bundle').value=JSON.stringify(await r.json(),null,2)}async function verify(){try{const r=await fetch('/api/verify',{method:'POST',headers:{'content-type':'application/json'},body:$('bundle').value});const x=await r.json();$('verdict').className='verdict '+x.verdict;$('verdict').textContent=x.verdict+' · '+x.final_pct+'%';$('summary').textContent='Confidence '+Math.round(x.confidence*100)+'% · '+x.checks.filter(c=>c.passed).length+'/'+x.checks.length+' checks passed';$('metrics').innerHTML=Object.entries(x.metrics).map(([k,v])=>`<div class="metric">${k.replaceAll('_',' ')} <b>${v}</b></div>`).join('');$('reasons').textContent=x.reason_codes.length?x.reason_codes.join(' · '):'NO FAILURE REASONS';$('receipt').textContent=JSON.stringify(x.audit_receipt,null,2)}catch(e){$('verdict').textContent='INVALID JSON';$('summary').textContent=e.message}}$('fixture').onchange=load;$('verify').onclick=verify;load().then(verify);
</script></body></html>'''

class Handler(BaseHTTPRequestHandler):
    def _send(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path == "/":
            self._send(200, PAGE.encode(), "text/html; charset=utf-8")
            return
        if path.startswith("/api/fixtures/"):
            name = path.rsplit("/", 1)[-1]
            if name in {"valid_success", "tampered_failure", "incomplete_inconclusive"}:
                self._send(200, (FIXTURES / f"{name}.json").read_bytes(), "application/json")
                return
        self._send(404, b'{"error":"not found"}', "application/json")

    def do_POST(self) -> None:  # noqa: N802
        if urlparse(self.path).path != "/api/verify":
            self._send(404, b'{"error":"not found"}', "application/json"); return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length > 2_000_000:
                raise ValueError("request exceeds 2 MB")
            bundle = json.loads(self.rfile.read(length))
            body, status = json.dumps(verify_bundle(bundle), sort_keys=True).encode(), 200
        except (json.JSONDecodeError, ValueError) as exc:
            body, status = json.dumps({"error": str(exc)}).encode(), 400
        self._send(status, body, "application/json")

    def log_message(self, fmt: str, *args: object) -> None:
        print(f"guardian: {fmt % args}")

def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Pulse PoPW Guardian demo")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()
    print(f"Pulse PoPW Guardian: http://{args.host}:{args.port}")
    ThreadingHTTPServer((args.host, args.port), Handler).serve_forever()

if __name__ == "__main__":
    main()
