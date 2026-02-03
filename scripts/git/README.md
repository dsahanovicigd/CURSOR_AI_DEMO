# Git Scripts

Scripts for Git operations and version control.

## Scripts

- **COMMIT_COMMAND.sh** - Standard commit command template
- **commit_and_push.sh** - Commit changes and push to remote
- **commit_latest.sh** - Commit latest changes
- **commit_push_backend_fix.sh** - Commit and push backend fixes
- **commit_push_final_fixes.sh** - Commit and push final fixes
- **commit_push_fixes.sh** - Commit and push general fixes
- **commit_push_latest.sh** - Commit and push latest changes
- **commit_push_zap_fix.sh** - Commit and push ZAP scan fixes

## Usage

```bash
# Standard commit
./scripts/git/COMMIT_COMMAND.sh "Your message"

# Commit and push
./scripts/git/commit_and_push.sh "Your message"

# Commit latest changes
./scripts/git/commit_latest.sh
```

## Notes

- Most scripts accept commit message as argument
- Some scripts have specific purposes (backend fixes, ZAP fixes, etc.)
- Review script contents before using to understand their specific behavior
