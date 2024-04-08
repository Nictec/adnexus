import coverage
import pytest


def test_only():
    pytest.main(['-x', "--html=reports/tests/index.html", "tests"])


def with_coverage():
    cov = coverage.Coverage()
    cov.start()
    test_only()
    cov.stop()
    cov.html_report(directory="./reports/coverage")
