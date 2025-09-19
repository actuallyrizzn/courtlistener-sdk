"""
Run coverage analysis for the CourtListener SDK.
"""

import os
import sys
import subprocess
from pathlib import Path
from coverage_config import COVERAGE_CONFIG, TEST_CATEGORIES, COVERAGE_THRESHOLDS


def run_coverage():
    """Run coverage analysis."""
    project_root = Path(__file__).parent.parent.parent
    os.chdir(project_root)
    
    print("Running coverage analysis...")
    
    # Run pytest with coverage
    cmd = [
        sys.executable, '-m', 'pytest',
        'tests/',
        '--cov=courtlistener',
        '--cov-report=html',
        '--cov-report=term-missing',
        '--cov-report=xml',
        f'--cov-fail-under={COVERAGE_CONFIG["fail_under"]}'
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    print(f"Exit code: {result.returncode}")
    print(f"Stdout: {result.stdout}")
    if result.stderr:
        print(f"Stderr: {result.stderr}")
    
    return result.returncode == 0


if __name__ == "__main__":
    success = run_coverage()
    sys.exit(0 if success else 1)
