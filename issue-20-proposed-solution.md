# Proposed Solution for Issue #20: PHP README References Missing Composer Scripts

## Investigation Summary

After reviewing the codebase, I've confirmed the current state:

1. **README References** (`php/README.md` lines 222, 227):
   - Mentions `composer cs-check` for checking code style
   - Mentions `composer cs-fix` for fixing code style issues
   - Also mentions "PHP_CodeSniffer, and PHP-CS-Fixer integration" in the features list (line 17)

2. **Composer Configuration** (`php/composer.json`):
   - No `cs-check` or `cs-fix` scripts defined
   - Only has `stan` script for PHPStan static analysis
   - No PHP-CS-Fixer or PHP_CodeSniffer dependencies installed

3. **Current State**:
   - PHPStan is configured and working (`composer stan`)
   - No code style checking/fixing tools are actually installed or configured
   - The README is misleading users about available tools

## Proposed Solution

Since PHP-CS-Fixer and PHP_CodeSniffer are not installed and the issue allows either "Add scripts or update README", I recommend:

**Option 1: Update README (Recommended - Quick Fix)**
- Remove references to `composer cs-check` and `composer cs-fix` from the README
- Update the features list to only mention PHPStan (which is actually configured)
- Keep the existing `composer stan` reference which is accurate

**Option 2: Add Scripts (Alternative - More Work)**
- Install PHP-CS-Fixer as a dev dependency
- Add `cs-check` and `cs-fix` scripts to composer.json
- Configure PHP-CS-Fixer with appropriate rules

## Recommendation

I recommend **Option 1** (update README) because:
- It's a quick fix that resolves the immediate issue
- No new dependencies needed
- PHPStan is already providing static analysis
- Code style tools can be added later if needed (separate issue)

## Implementation Details

### Files to Modify
- `php/README.md`: Remove `cs-check` and `cs-fix` references, update features list

### Changes
1. Remove lines 220-228 (the "Check code style" and "Fix code style issues" sections)
2. Update line 17 to remove "PHP_CodeSniffer, and PHP-CS-Fixer integration" from features
3. Keep the `composer stan` reference as it's accurate

