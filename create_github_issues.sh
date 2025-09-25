#!/bin/bash

# Script to create GitHub issues for CourtListener SDK audit findings
# Prerequisites: 
# 1. Install GitHub CLI: https://cli.github.com/
# 2. Authenticate: gh auth login
# 3. Make sure you're in the correct repository directory

set -e

echo "🚀 Creating GitHub issues for CourtListener SDK audit findings..."
echo "Make sure you're authenticated with GitHub CLI (gh auth login) and in the correct repo directory."
echo ""

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) is not installed. Please install it first:"
    echo "   https://cli.github.com/"
    exit 1
fi

# Check if user is authenticated
if ! gh auth status &> /dev/null; then
    echo "❌ Not authenticated with GitHub CLI. Please run: gh auth login"
    exit 1
fi

echo "✅ GitHub CLI is installed and authenticated"
echo ""

# Issue 1: Critical PHP Fatal Errors
echo "📝 Creating Issue 1: PHP Fatal Errors in Dockets.php..."
gh issue create \
  --title "[CRITICAL BUG] Missing function parameters causing fatal errors in PHP Dockets API" \
  --label "bug,critical,php,api" \
  --body "## Description
Multiple methods in \`php/src/CourtListener/Api/Dockets.php\` are missing required parameters, causing PHP fatal errors when called.

## Affected Methods
- \`getDocketEntries()\` - Line 67
- \`getParties()\` - Line 81  
- \`getAttorneys()\` - Line 95
- \`getRecapDocuments()\` - Line 109
- \`getDocketsByCourt()\` - Line 147
- \`getDocketsByDateRange()\` - Line 162
- \`getDocketsByCaseType()\` - Line 189
- \`getDocketsByNatureOfSuit()\` - Line 202
- \`getDocketsByJudge()\` - Line 215
- \`getDocketsByStatus()\` - Line 228
- \`getDocketsWithFinancialDisclosures()\` - Line 240
- \`getDocketsWithAudio()\` - Line 252
- \`getDocketsWithRecapDocuments()\` - Line 264
- \`getDocketsByJurisdictionType()\` - Line 277
- \`getDocketsByJuryDemand()\` - Line 290

## Example Bug
\`\`\`php
// Current broken code:
public function getDocketEntries(array \$params = []) {
    return \$this->client->makeRequest('GET', \"dockets/{\$docketId}/docket-entries/\", [
        'query' => \$params
    ]);
}

// Should be:
public function getDocketEntries(\$docketId, array \$params = []) {
    return \$this->client->makeRequest('GET', \"dockets/{\$docketId}/docket-entries/\", [
        'query' => \$params
    ]);
}
\`\`\`

## Impact
- All affected methods throw PHP fatal errors when called
- Makes the PHP SDK completely unusable for docket-related operations
- Breaks any application trying to use these methods

## Steps to Reproduce
1. Install the PHP SDK
2. Try to call \`\$client->dockets->getDocketEntries()\`
3. Observe fatal error: \"Undefined variable: \$docketId\"

## Expected Behavior
Methods should accept required parameters and execute without errors.

## Priority
🚨 **CRITICAL** - Must be fixed immediately before any release."

echo "✅ Issue 1 created"

# Issue 2: Systematic Parameter Issues
echo "📝 Creating Issue 2: Systematic Parameter Issues..."
gh issue create \
  --title "[CRITICAL BUG] Missing parameters in multiple PHP API endpoint classes" \
  --label "bug,critical,php,api,systematic" \
  --body "## Description
The same missing parameter pattern found in Dockets.php likely exists in other PHP API endpoint classes. A systematic review is needed.

## Suspected Affected Files
- \`php/src/CourtListener/Api/Courts.php\`
- \`php/src/CourtListener/Api/Judges.php\`
- \`php/src/CourtListener/Api/Opinions.php\`
- \`php/src/CourtListener/Api/Audio.php\`
- Other API endpoint classes

## Action Required
1. Audit all PHP API classes for missing parameters
2. Fix parameter definitions in method signatures
3. Update method implementations to use parameters correctly
4. Add unit tests to prevent regression

## Suggested Solution
Create a systematic review script to check all API methods for parameter consistency.

## Priority
🚨 **CRITICAL** - Systematic issue affecting entire PHP SDK"

echo "✅ Issue 2 created"

# Issue 3: Static Analysis
echo "📝 Creating Issue 3: Static Analysis Implementation..."
gh issue create \
  --title "[ENHANCEMENT] Implement static analysis tools in CI/CD pipeline" \
  --label "enhancement,ci/cd,code-quality,php,python" \
  --body "## Description
Implement static analysis tools to catch code quality issues before they reach production.

## Proposed Implementation

### For PHP:
- Enable stricter PHPStan rules (currently level 6, should be 8+)
- Remove ignoreErrors exceptions in phpstan.neon
- Add Psalm for additional static analysis
- Run in CI/CD pipeline

### For Python:
- Add mypy type checking
- Add flake8 linting
- Add black code formatting checks
- Integrate with pytest

## Benefits
- Catch parameter mismatches before runtime
- Enforce consistent code style
- Improve overall code quality
- Prevent similar bugs in the future

## Priority
🔧 **HIGH** - Prevents future code quality issues"

echo "✅ Issue 3 created"

# Issue 4: Dependency Pinning
echo "📝 Creating Issue 4: Dependency Version Pinning..."
gh issue create \
  --title "[SECURITY] Pin dependency versions for security and stability" \
  --label "security,dependencies,php" \
  --body "## Description
PHP composer.json uses wildcard version constraints which can lead to security vulnerabilities and unexpected behavior.

## Current Issue
\`\`\`json
\"require\": {
    \"php\": \">=8.1\",
    \"guzzlehttp/guzzle\": \"*\",
    \"vlucas/phpdotenv\": \"*\"
}
\`\`\`

## Recommended Fix
\`\`\`json
\"require\": {
    \"php\": \">=8.1\",
    \"guzzlehttp/guzzle\": \"^7.5\",
    \"vlucas/phpdotenv\": \"^5.4\"
}
\`\`\`

## Benefits
- Prevents automatic installation of potentially breaking updates
- Improves security by controlling dependency versions
- Ensures consistent behavior across environments
- Follows PHP security best practices

## Priority
🔧 **HIGH** - Security and stability improvement"

echo "✅ Issue 4 created"

# Issue 5: Error Handling
echo "📝 Creating Issue 5: Error Handling Standardization..."
gh issue create \
  --title "[IMPROVEMENT] Standardize error handling patterns across API modules" \
  --label "improvement,error-handling,python,php" \
  --body "## Description
Error handling patterns are inconsistent across different API modules in both Python and PHP implementations.

## Issues Found
1. Some modules catch all exceptions, others only specific ones
2. Inconsistent error message formatting
3. Different retry logic implementations
4. Mixed exception types for similar errors

## Proposed Solution
1. Create standardized error handling mixins/traits
2. Define consistent error message formats
3. Implement uniform retry logic
4. Document error handling patterns

## Priority
🔧 **MEDIUM** - Code quality improvement"

echo "✅ Issue 5 created"

# Issue 6: Performance Optimization
echo "📝 Creating Issue 6: Performance Optimization..."
gh issue create \
  --title "[ENHANCEMENT] Implement caching and performance optimizations" \
  --label "enhancement,performance,caching" \
  --body "## Description
Several opportunities exist to improve SDK performance and reduce API calls.

## Optimization Areas
1. **Response Caching**: Cache static data like courts, judges
2. **Connection Pooling**: Implement in PHP (already exists in Python)
3. **Batch Operations**: Support bulk API operations where possible
4. **Memory Management**: Implement streaming for large datasets

## Proposed Implementation
- Add configurable caching layer with TTL
- Implement PSR-6 compatible cache in PHP
- Add memory-efficient pagination helpers
- Create performance benchmarking tests

## Priority
🔧 **MEDIUM** - Performance enhancement"

echo "✅ Issue 6 created"

# Issue 7: Code Style
echo "📝 Creating Issue 7: Code Style Consistency..."
gh issue create \
  --title "[IMPROVEMENT] Improve code style consistency between Python and PHP" \
  --label "improvement,code-style,documentation" \
  --body "## Description
While both implementations follow their respective language conventions, some patterns could be more consistent.

## Areas for Improvement
1. Method naming conventions
2. Documentation format standardization
3. Comment style consistency
4. Error message formatting

## Proposed Solution
- Create style guides for both languages
- Implement automated formatting checks
- Update existing code to match standards
- Add style guide to documentation

## Priority
🎨 **LOW** - Code quality improvement"

echo "✅ Issue 7 created"

# Issue 8: Integration Testing
echo "📝 Creating Issue 8: Integration Testing..."
gh issue create \
  --title "[TESTING] Add comprehensive integration tests for fixed PHP methods" \
  --label "testing,php,integration-tests" \
  --body "## Description
After fixing the PHP parameter issues, comprehensive integration tests are needed to ensure all methods work correctly.

## Test Requirements
1. Test all Dockets API methods with real parameters
2. Verify error handling for invalid inputs
3. Test pagination functionality
4. Verify response format consistency
5. Add mock tests for offline testing

## Implementation
- Create dedicated test suite for fixed methods
- Add both live API tests and mock tests
- Ensure tests cover edge cases
- Add performance benchmarks

## Priority
🔧 **HIGH** - Critical for ensuring fixes work correctly"

echo "✅ Issue 8 created"

# Issue 9: Documentation Updates
echo "📝 Creating Issue 9: Documentation Updates..."
gh issue create \
  --title "[DOCUMENTATION] Update documentation to reflect bug fixes and improvements" \
  --label "documentation,api-reference" \
  --body "## Description
After fixing the critical PHP bugs, documentation needs to be updated to reflect the correct method signatures and usage patterns.

## Updates Needed
1. Correct method signatures in API reference
2. Add examples for fixed methods
3. Update troubleshooting guide
4. Add migration notes for any breaking changes
5. Update version compatibility information

## Priority
📚 **MEDIUM** - Keep documentation current with fixes"

echo "✅ Issue 9 created"

# Issue 10: Code Review Process
echo "📝 Creating Issue 10: Code Review Process..."
gh issue create \
  --title "[PROCESS] Establish mandatory code review and testing process" \
  --label "process,code-review,ci/cd" \
  --body "## Description
To prevent similar issues in the future, establish a mandatory code review and testing process.

## Proposed Process
1. **Code Review**: All changes require review before merge
2. **Automated Testing**: CI/CD must pass all tests
3. **Static Analysis**: PHPStan and mypy must pass
4. **Manual Testing**: Critical paths must be manually verified
5. **Release Checklist**: Formal checklist before releases

## Implementation
- Configure GitHub branch protection rules
- Set up automated CI/CD pipeline
- Create pull request templates
- Establish release criteria and process

## Priority
🔄 **HIGH** - Process improvement to prevent future issues"

echo "✅ Issue 10 created"

echo ""
echo "🎉 All 10 GitHub issues have been created successfully!"
echo ""
echo "📋 Summary:"
echo "   • 2 Critical issues (PHP fatal errors)"
echo "   • 4 High priority issues (static analysis, dependencies, testing, process)"
echo "   • 3 Medium priority issues (error handling, performance, documentation)"
echo "   • 1 Low priority issue (code style)"
echo ""
echo "🚨 Recommendation: Address critical and high priority issues first!"
echo ""
echo "View all issues: gh issue list"