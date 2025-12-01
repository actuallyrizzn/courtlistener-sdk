# Proposed Solution for Issue #19: Python Packaging Documentation URL Fix

## Investigation Summary

After reviewing the codebase, I've confirmed the current state:

1. **Current Documentation URL** (`python/setup.py` line 66):
   - `"Documentation": "https://github.com/actuallyrizzn/courtlistener-sdk/docs"`
   - This URL returns a 404 because GitHub doesn't serve directories directly

2. **Available Documentation**:
   - Documentation exists in the `docs/` directory at the repo root
   - Files include: `user_guide.md`, `api_reference.md`, `advanced_usage.md`, etc.

## Proposed Solution

Update the Documentation URL in `project_urls` to point to the correct location:

**Option 1: Point to docs directory in GitHub (Recommended)**
- Change to: `"https://github.com/actuallyrizzn/courtlistener-sdk/tree/main/docs"`
- This allows users to browse the documentation files directly on GitHub

**Option 2: Point to a specific documentation file**
- Change to: `"https://github.com/actuallyrizzn/courtlistener-sdk/blob/main/docs/README.md"`
- Points to a specific entry point

## Recommendation

I recommend **Option 1** (`/tree/main/docs`) because:
- It's more flexible - users can browse all documentation files
- It's the standard GitHub pattern for directory links
- It matches the issue description suggestion

## Implementation Details

### Files to Modify
- `python/setup.py`: Update the Documentation URL in `project_urls`

### Changes
- Line 66: Change `"https://github.com/actuallyrizzn/courtlistener-sdk/docs"` to `"https://github.com/actuallyrizzn/courtlistener-sdk/tree/main/docs"`

