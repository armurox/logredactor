#!/bin/bash
# Get the commit SHA from the tag
TAG_COMMIT_SHA=$(git rev-list -n 1 $GITHUB_REF)

# Fetch the branch name using the commit SHA
BRANCH_NAME=$(git branch -r --contains $TAG_COMMIT_SHA | grep -v '\->' | grep -Eo 'origin/[^ ]+$' | grep -Eo '[^/]+$' | head -1)

echo "branch=$BRANCH_NAME" >> $GITHUB_ENV
