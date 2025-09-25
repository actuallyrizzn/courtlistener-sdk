# GitHub Issues for CourtListener SDK - Code Audit Findings

Copy and paste these issue templates into the GitHub repository issues section.

---

## 🚨 CRITICAL ISSUE #1: PHP Fatal Errors in Dockets.php

**Title:** [CRITICAL BUG] Missing function parameters causing fatal errors in PHP Dockets API

**Labels:** `bug`, `critical`, `php`, `api`

**Priority:** Critical

**Description:**
Multiple methods in `php/src/CourtListener/Api/Dockets.php` are missing required parameters, causing PHP fatal errors when called.

**Affected Methods:**
- `getDocketEntries()` - Line 67
- `getParties()` - Line 81  
- `getAttorneys()` - Line 95
- `getRecapDocuments()` - Line 109
- `getDocketsByCourt()` - Line 147
- `getDocketsByDateRange()` - Line 162
- `getDocketsByCaseType()` - Line 189
- `getDocketsByNatureOfSuit()` - Line 202
- `getDocketsByJudge()` - Line 215
- `getDocketsByStatus()` - Line 228
- `getDocketsWithFinancialDisclosures()` - Line 240
- `getDocketsWithAudio()` - Line 252
- `getDocketsWithRecapDocuments()` - Line 264
- `getDocketsByJurisdictionType()` - Line 277
- `getDocketsByJuryDemand()` - Line 290

**Example Bug:**
```php
// Current broken code:
public function getDocketEntries(array $params = []) {
    return $this->client->makeRequest('GET', "dockets/{$docketId}/docket-entries/", [
        'query' => $params
    ]);
}

// Should be:
public function getDocketEntries($docketId, array $params = []) {
    return $this->client->makeRequest('GET', "dockets/{$docketId}/docket-entries/", [
        'query' => $params
    ]);
}
```

**Impact:**
- All affected methods throw PHP fatal errors when called
- Makes the PHP SDK completely unusable for docket-related operations
- Breaks any application trying to use these methods

**Steps to Reproduce:**
1. Install the PHP SDK
2. Try to call `$client->dockets->getDocketEntries()`
3. Observe fatal error: "Undefined variable: $docketId"

**Expected Behavior:**
Methods should accept required parameters and execute without errors.

**Additional Context:**
This appears to be a copy-paste error where parameter definitions were not updated when the method signatures were created.

---

## 🚨 CRITICAL ISSUE #2: Similar Parameter Issues in Other PHP API Classes

**Title:** [CRITICAL BUG] Missing parameters in multiple PHP API endpoint classes

**Labels:** `bug`, `critical`, `php`, `api`, `systematic`

**Priority:** Critical

**Description:**
The same missing parameter pattern found in Dockets.php likely exists in other PHP API endpoint classes. A systematic review is needed.

**Suspected Affected Files:**
- `php/src/CourtListener/Api/Courts.php`
- `php/src/CourtListener/Api/Judges.php`
- `php/src/CourtListener/Api/Opinions.php`
- `php/src/CourtListener/Api/Audio.php`
- Other API endpoint classes

**Action Required:**
1. Audit all PHP API classes for missing parameters
2. Fix parameter definitions in method signatures
3. Update method implementations to use parameters correctly
4. Add unit tests to prevent regression

**Suggested Solution:**
Create a systematic review script to check all API methods for parameter consistency.

---

## 🔧 HIGH PRIORITY ISSUE #3: Static Analysis Implementation

**Title:** [ENHANCEMENT] Implement static analysis tools in CI/CD pipeline

**Labels:** `enhancement`, `ci/cd`, `code-quality`, `php`, `python`

**Priority:** High

**Description:**
Implement static analysis tools to catch code quality issues before they reach production.

**Proposed Implementation:**

**For PHP:**
- Enable stricter PHPStan rules (currently level 6, should be 8+)
- Remove ignoreErrors exceptions in phpstan.neon
- Add Psalm for additional static analysis
- Run in CI/CD pipeline

**For Python:**
- Add mypy type checking
- Add flake8 linting
- Add black code formatting checks
- Integrate with pytest

**Benefits:**
- Catch parameter mismatches before runtime
- Enforce consistent code style
- Improve overall code quality
- Prevent similar bugs in the future

---

## 🔧 HIGH PRIORITY ISSUE #4: Dependency Version Pinning

**Title:** [SECURITY] Pin dependency versions for security and stability

**Labels:** `security`, `dependencies`, `php`

**Priority:** High

**Description:**
PHP composer.json uses wildcard version constraints which can lead to security vulnerabilities and unexpected behavior.

**Current Issue:**
```json
"require": {
    "php": ">=8.1",
    "guzzlehttp/guzzle": "*",
    "vlucas/phpdotenv": "*"
}
```

**Recommended Fix:**
```json
"require": {
    "php": ">=8.1",
    "guzzlehttp/guzzle": "^7.5",
    "vlucas/phpdotenv": "^5.4"
}
```

**Benefits:**
- Prevents automatic installation of potentially breaking updates
- Improves security by controlling dependency versions
- Ensures consistent behavior across environments
- Follows PHP security best practices

---

## 🔧 MEDIUM PRIORITY ISSUE #5: Inconsistent Error Handling

**Title:** [IMPROVEMENT] Standardize error handling patterns across API modules

**Labels:** `improvement`, `error-handling`, `python`, `php`

**Priority:** Medium

**Description:**
Error handling patterns are inconsistent across different API modules in both Python and PHP implementations.

**Issues Found:**
1. Some modules catch all exceptions, others only specific ones
2. Inconsistent error message formatting
3. Different retry logic implementations
4. Mixed exception types for similar errors

**Proposed Solution:**
1. Create standardized error handling mixins/traits
2. Define consistent error message formats
3. Implement uniform retry logic
4. Document error handling patterns

---

## 🔧 MEDIUM PRIORITY ISSUE #6: Performance Optimization Opportunities

**Title:** [ENHANCEMENT] Implement caching and performance optimizations

**Labels:** `enhancement`, `performance`, `caching`

**Priority:** Medium

**Description:**
Several opportunities exist to improve SDK performance and reduce API calls.

**Optimization Areas:**
1. **Response Caching**: Cache static data like courts, judges
2. **Connection Pooling**: Implement in PHP (already exists in Python)
3. **Batch Operations**: Support bulk API operations where possible
4. **Memory Management**: Implement streaming for large datasets

**Proposed Implementation:**
- Add configurable caching layer with TTL
- Implement PSR-6 compatible cache in PHP
- Add memory-efficient pagination helpers
- Create performance benchmarking tests

---

## 🔧 LOW PRIORITY ISSUE #7: Code Style Consistency

**Title:** [IMPROVEMENT] Improve code style consistency between Python and PHP

**Labels:** `improvement`, `code-style`, `documentation`

**Priority:** Low

**Description:**
While both implementations follow their respective language conventions, some patterns could be more consistent.

**Areas for Improvement:**
1. Method naming conventions
2. Documentation format standardization
3. Comment style consistency
4. Error message formatting

**Proposed Solution:**
- Create style guides for both languages
- Implement automated formatting checks
- Update existing code to match standards
- Add style guide to documentation

---

## 📋 TESTING ISSUE #8: Comprehensive Integration Testing

**Title:** [TESTING] Add comprehensive integration tests for fixed PHP methods

**Labels:** `testing`, `php`, `integration-tests`

**Priority:** High

**Description:**
After fixing the PHP parameter issues, comprehensive integration tests are needed to ensure all methods work correctly.

**Test Requirements:**
1. Test all Dockets API methods with real parameters
2. Verify error handling for invalid inputs
3. Test pagination functionality
4. Verify response format consistency
5. Add mock tests for offline testing

**Implementation:**
- Create dedicated test suite for fixed methods
- Add both live API tests and mock tests
- Ensure tests cover edge cases
- Add performance benchmarks

---

## 📚 DOCUMENTATION ISSUE #9: API Documentation Updates

**Title:** [DOCUMENTATION] Update documentation to reflect bug fixes and improvements

**Labels:** `documentation`, `api-reference`

**Priority:** Medium

**Description:**
After fixing the critical PHP bugs, documentation needs to be updated to reflect the correct method signatures and usage patterns.

**Updates Needed:**
1. Correct method signatures in API reference
2. Add examples for fixed methods
3. Update troubleshooting guide
4. Add migration notes for any breaking changes
5. Update version compatibility information

---

## 🔄 PROCESS ISSUE #10: Code Review and Release Process

**Title:** [PROCESS] Establish mandatory code review and testing process

**Labels:** `process`, `code-review`, `ci/cd`

**Priority:** High

**Description:**
To prevent similar issues in the future, establish a mandatory code review and testing process.

**Proposed Process:**
1. **Code Review**: All changes require review before merge
2. **Automated Testing**: CI/CD must pass all tests
3. **Static Analysis**: PHPStan and mypy must pass
4. **Manual Testing**: Critical paths must be manually verified
5. **Release Checklist**: Formal checklist before releases

**Implementation:**
- Configure GitHub branch protection rules
- Set up automated CI/CD pipeline
- Create pull request templates
- Establish release criteria and process

---

# Instructions for Creating Issues

1. **Go to the GitHub repository**
2. **Click "Issues" tab**
3. **Click "New Issue"**
4. **Copy and paste each issue template above**
5. **Assign appropriate labels and priority**
6. **Tag relevant maintainers if known**

## Recommended Creation Order:
1. Critical Issues (#1, #2) - Fix immediately
2. High Priority Issues (#3, #4, #8, #10) - Fix this sprint
3. Medium Priority Issues (#5, #6, #9) - Next sprint
4. Low Priority Issues (#7) - Future improvement

Each issue is detailed enough to be actionable and includes code examples, expected behavior, and implementation suggestions.