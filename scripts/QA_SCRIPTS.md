# QA Scripts Reference

QA automation scripts remain in their original locations for organizational purposes but are documented here for easy reference.

## Location

QA scripts are located in: `qa-automation/scripts/`

## Available Scripts

### Master QA Runner
```bash
./qa-automation/scripts/master-qa-runner.sh
```
Runs all QA checks including tests, linting, security scans, and performance tests.

### Run All QA Tests
```bash
./qa-automation/scripts/run-all-qa.sh
```
Runs comprehensive QA test suite.

### Performance Tests
```bash
./qa-automation/scripts/run-performance-tests.sh
```
Runs performance and load tests.

### Security Scan
```bash
./qa-automation/scripts/run-security-scan.sh
```
Runs security vulnerability scans.

### Security Scan (Alternative)
```bash
./qa-automation/security/security-scan.sh
```
Alternative security scanning script.

## Setup Scripts

### Python Dependencies
```bash
./qa/setup-python-deps.sh
```
Setup Python dependencies for QA automation.

## Notes

- These scripts are kept in their original locations to maintain integration with the QA automation system
- They are referenced here for easy discovery
- See `qa-automation/README.md` for more details
