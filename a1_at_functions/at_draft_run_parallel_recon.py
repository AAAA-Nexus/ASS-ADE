# Extracted from C:/!ass-ade/src/ass_ade/recon.py:881
# Component id: at.source.ass_ade.run_parallel_recon
from __future__ import annotations

__version__ = "0.1.0"

def run_parallel_recon(path: str | Path = ".") -> ReconReport:
    """Run all 5 recon agents in parallel and return a consolidated ReconReport.

    Completes in < 5 seconds for repos with < 500 files.
    All analysis is local — no LLM calls, no network requests.
    """
    root = Path(path).resolve()
    t0 = time.monotonic()

    files = _iter_files(root)

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        f_scout = pool.submit(_scout_agent, root, files)
        f_dep   = pool.submit(_dependency_agent, root, files)
        f_tier  = pool.submit(_tier_agent, root, files)
        f_test  = pool.submit(_test_agent, root, files)
        f_doc   = pool.submit(_doc_agent, root, files)

        scout      = f_scout.result()
        dependency = f_dep.result()
        tier       = f_tier.result()
        test       = f_test.result()
        doc        = f_doc.result()

    recs, next_action = _build_recommendations(scout, dependency, tier, test, doc)
    duration_ms = (time.monotonic() - t0) * 1000

    return ReconReport(
        root=str(root),
        duration_ms=duration_ms,
        scout=scout,
        dependency=dependency,
        tier=tier,
        test=test,
        doc=doc,
        recommendations=recs,
        next_action=next_action,
    )
