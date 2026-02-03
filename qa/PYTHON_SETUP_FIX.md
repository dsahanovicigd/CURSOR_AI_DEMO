# Python Dependencies Setup Fix

## Issue
On macOS (and some Linux distributions), Python environments are externally managed, preventing direct `pip3 install` without flags.

## Solution
Use a Python virtual environment for QA scripts. The QA runner script now automatically creates and uses a virtual environment.

## Quick Fix

### Option 1: Automatic Setup (Recommended)
```bash
# Run the setup script
./qa/setup-python-deps.sh
```

### Option 2: Manual Setup
```bash
# Create virtual environment
python3 -m venv qa/.venv

# Activate it
source qa/.venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install jinja2 markdown pylint pylint-json2html pylint-flask
```

### Option 3: User Installation (Alternative)
If you prefer not to use a virtual environment:
```bash
pip3 install --user jinja2 markdown pylint pylint-json2html pylint-flask
```

## What Changed

1. **Updated `qa/scripts/run-qa-local.sh`:**
   - Automatically creates `qa/.venv` if needed
   - Activates virtual environment before running Python scripts
   - Handles missing dependencies gracefully

2. **Created `qa/setup-python-deps.sh`:**
   - Standalone script to set up Python dependencies
   - Creates virtual environment and installs packages

3. **Updated Documentation:**
   - `qa/README.md` - Updated installation instructions
   - `qa/SETUP.md` - Added virtual environment instructions

4. **Updated `.gitignore`:**
   - Added `qa/.venv/` to ignore virtual environment directory

## Verification

After setup, verify installation:
```bash
source qa/.venv/bin/activate
python3 -c "import jinja2; print('✅ jinja2 installed')"
python3 -c "import pylint; print('✅ pylint installed')"
deactivate
```

## Notes

- The virtual environment is created in `qa/.venv/` (gitignored)
- The QA runner script automatically activates it when needed
- You can manually activate it with: `source qa/.venv/bin/activate`
- Deactivate with: `deactivate`
