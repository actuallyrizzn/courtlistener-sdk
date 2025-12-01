This PR fixes issue #19 by updating the Documentation URL in setup.py to point to the correct location.

## Changes

- ✅ Updated Documentation URL from `/docs` to `/tree/main/docs`
- ✅ Fixes 404 error when accessing documentation link from PyPI
- ✅ Now correctly points to the docs directory in the repository

## Problem

The `project_urls` Documentation link pointed to `https://github.com/actuallyrizzn/courtlistener-sdk/docs` which returns a 404 because GitHub doesn't serve directories directly.

## Solution

Updated the URL to `https://github.com/actuallyrizzn/courtlistener-sdk/tree/main/docs` which is the correct GitHub URL pattern for browsing directory contents.

Fixes #19

