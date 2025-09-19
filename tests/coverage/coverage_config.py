"""
Coverage configuration for the CourtListener SDK.
"""

# Coverage configuration
COVERAGE_CONFIG = {
    'source': ['courtlistener'],
    'omit': [
        '*/tests/*',
        '*/test_*',
        '*/__pycache__/*',
        '*/venv/*',
        '*/env/*',
        '*/tmp/*',
        '*/build/*',
        '*/dist/*',
        '*/coverage/*',
        '*/htmlcov/*',
        '*/site-packages/*'
    ],
    'branch': True,
    'parallel': True,
    'concurrency': ['thread'],
    'fail_under': 80,
    'precision': 2,
    'show_missing': True,
    'skip_covered': False,
    'sort': 'Cover'
}

# Test categories
TEST_CATEGORIES = {
    'unit_tests': {
        'path': 'tests/test_api/',
        'description': 'Unit tests for API modules',
        'target_coverage': 90
    },
    'model_tests': {
        'path': 'tests/test_models/',
        'description': 'Unit tests for data models',
        'target_coverage': 90
    },
    'integration_tests': {
        'path': 'tests/integration/',
        'description': 'Integration tests for endpoints',
        'target_coverage': 80
    },
    'e2e_tests': {
        'path': 'tests/e2e/',
        'description': 'End-to-end tests',
        'target_coverage': 70
    },
    'live_tests': {
        'path': 'tests/live/',
        'description': 'Live API tests',
        'target_coverage': 60
    }
}

# Coverage thresholds
COVERAGE_THRESHOLDS = {
    'overall': 80,
    'api_modules': 85,
    'models': 90,
    'client': 80,
    'exceptions': 100,
    'utils': 80
}
