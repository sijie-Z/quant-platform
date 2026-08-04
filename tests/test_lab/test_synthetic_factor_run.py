"""Tests for the offline synthetic factor runner (P0 validation path)."""

from pathlib import Path

from quant_platform.lab.runs.synthetic_factor_run import (
    available_factors,
    run_synthetic_factor,
)


def test_available_factors_contains_momentum():
    assert "momentum_12m" in available_factors()


def test_run_synthetic_factor_persists_report():
    run_id = run_synthetic_factor("momentum_12m", n_stocks=3, n_days=120, seed=1)
    assert run_id.startswith("run_")
    report = Path("data/reports") / f"{run_id}.md"
    assert report.exists()
