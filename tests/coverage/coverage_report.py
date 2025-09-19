"""
Coverage reporting script for the CourtListener SDK.
"""

import os
import sys
import subprocess
from pathlib import Path


def run_coverage_analysis():
    """Run coverage analysis and generate reports."""
    print("Running coverage analysis for CourtListener SDK...")
    
    # Get the project root directory
    project_root = Path(__file__).parent.parent.parent
    os.chdir(project_root)
    
    # Run coverage analysis
    try:
        # Run pytest with coverage
        result = subprocess.run([
            sys.executable, '-m', 'pytest',
            'tests/',
            '--cov=courtlistener',
            '--cov-report=html',
            '--cov-report=term-missing',
            '--cov-report=xml',
            '--cov-fail-under=80'
        ], capture_output=True, text=True)
        
        print("Coverage analysis completed!")
        print(f"Exit code: {result.returncode}")
        print(f"Stdout: {result.stdout}")
        print(f"Stderr: {result.stderr}")
        
        # Check if coverage report was generated
        html_report = project_root / 'htmlcov' / 'index.html'
        if html_report.exists():
            print(f"HTML coverage report generated: {html_report}")
        
        xml_report = project_root / 'coverage.xml'
        if xml_report.exists():
            print(f"XML coverage report generated: {xml_report}")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"Error running coverage analysis: {e}")
        return False


def generate_coverage_summary():
    """Generate a coverage summary report."""
    print("Generating coverage summary...")
    
    try:
        # Run coverage report
        result = subprocess.run([
            sys.executable, '-m', 'coverage', 'report', '--show-missing'
        ], capture_output=True, text=True)
        
        print("Coverage Summary:")
        print(result.stdout)
        
        if result.stderr:
            print("Errors:")
            print(result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"Error generating coverage summary: {e}")
        return False


def check_test_coverage():
    """Check if test coverage meets requirements."""
    print("Checking test coverage requirements...")
    
    try:
        # Run coverage check
        result = subprocess.run([
            sys.executable, '-m', 'coverage', 'report', '--fail-under=80'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Coverage requirements met (>= 80%)")
            return True
        else:
            print("❌ Coverage requirements not met (< 80%)")
            print(result.stdout)
            return False
            
    except Exception as e:
        print(f"Error checking coverage: {e}")
        return False


def main():
    """Main function to run coverage analysis."""
    print("=" * 60)
    print("CourtListener SDK Coverage Analysis")
    print("=" * 60)
    
    # Run coverage analysis
    success = run_coverage_analysis()
    
    if success:
        print("\n" + "=" * 60)
        print("Coverage Analysis Results")
        print("=" * 60)
        
        # Generate summary
        generate_coverage_summary()
        
        # Check requirements
        check_test_coverage()
        
        print("\n" + "=" * 60)
        print("Coverage analysis completed successfully!")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("Coverage analysis failed!")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    main()
