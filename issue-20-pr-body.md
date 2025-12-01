This PR fixes issue #20 by removing references to non-existent composer scripts from the PHP README.

## Changes

- ✅ Removed `composer cs-check` and `composer cs-fix` references from Code Quality section
- ✅ Updated features list to only mention PHPStan (which is actually configured)
- ✅ Fixed misleading documentation about available code style tools

## Problem

The README mentioned `composer cs-check` and `composer cs-fix` scripts that don't exist in `composer.json`, and also claimed PHP_CodeSniffer and PHP-CS-Fixer integration which isn't actually set up.

## Solution

Since the issue allows either "Add scripts or update README", I chose to update the README to accurately reflect what's actually available:
- PHPStan static analysis (via `composer stan`) is configured and working
- Code style tools are not currently installed/configured

Fixes #20

