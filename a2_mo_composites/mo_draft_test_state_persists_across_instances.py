# Extracted from C:/!ass-ade/tests/test_phase_engines.py:252
# Component id: mo.source.ass_ade.test_state_persists_across_instances
from __future__ import annotations

__version__ = "0.1.0"

def test_state_persists_across_instances(self, tmp_path):
    from ass_ade.agent.tca import TCAEngine
    cfg = {"tca": {"state_file": str(tmp_path / "tca_reads.json"), "freshness_hours": 24.0}}
    tca1 = TCAEngine(cfg)
    tca1.record_read("/persistent.py")
    tca2 = TCAEngine(cfg)
    assert tca2.ncb_contract("/persistent.py") is True
