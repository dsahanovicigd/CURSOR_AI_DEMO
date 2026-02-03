# User Profile Management Tests - Quick Reference

## Quick Start

```bash
# Run all user profile tests
pytest tests/test_user_profile_comprehensive.py -v

# Run with coverage
pytest tests/test_user_profile_comprehensive.py --cov=app --cov-report=term

# Run specific category
pytest tests/test_user_profile_comprehensive.py::TestUserRegistration -v
```

## Test Statistics

- **Total Test Cases**: 100+
- **Test Classes**: 5
- **Categories**: Positive, Negative, Edge Cases, Security

## Test Class Overview

| Class | Purpose | Test Count |
|-------|---------|------------|
| `TestUserRegistration` | User registration scenarios | 35+ |
| `TestProfileUpdates` | Profile update scenarios | 30+ |
| `TestPasswordChanges` | Password change scenarios | 15+ |
| `TestAccountDeletion` | Account deletion scenarios | 15+ |
| `TestUserProfileIntegration` | Integration scenarios | 5+ |

## Key Test Scenarios

### Registration
- ✅ Valid registration with all fields
- ❌ Duplicate username/email
- 🔍 Unicode and special characters
- 🔒 Password security

### Profile Updates
- ✅ Update own profile
- ❌ Unauthorized updates
- 🔍 Partial updates
- 🔒 Authorization checks

### Password Changes
- ✅ Change password successfully
- ❌ Weak passwords rejected
- 🔍 Special characters
- 🔒 Password hashing

### Account Deletion
- ✅ Delete own account
- ❌ Unauthorized deletion
- 🔍 Cascade behavior
- 🔒 Security checks

## Common Commands

```bash
# Run all tests
pytest tests/test_user_profile_comprehensive.py

# Run with verbose output
pytest tests/test_user_profile_comprehensive.py -v

# Run specific test
pytest tests/test_user_profile_comprehensive.py::TestUserRegistration::test_register_user_with_minimal_fields

# Run with coverage report
pytest tests/test_user_profile_comprehensive.py --cov=app --cov-report=html

# Run and stop on first failure
pytest tests/test_user_profile_comprehensive.py -x

# Run tests matching pattern
pytest tests/test_user_profile_comprehensive.py -k "password"
```

## Expected Results Summary

| Test Type | Expected Status | Description |
|-----------|----------------|-------------|
| Positive | 200/201/204 | Successful operations |
| Negative | 400 | Validation errors |
| Unauthorized | 401 | Missing/invalid auth |
| Forbidden | 403 | Insufficient permissions |
| Not Found | 404 | Resource doesn't exist |

## Security Test Checklist

- [x] Password never in response
- [x] Password properly hashed
- [x] SQL injection prevented
- [x] XSS attempts handled
- [x] Authorization enforced
- [x] Authentication required
- [x] Rate limiting (if configured)

## Troubleshooting

**Tests failing?**
1. Check database is initialized
2. Verify fixtures are set up correctly
3. Check test user exists
4. Verify JWT tokens are valid

**Import errors?**
1. Ensure virtual environment is activated
2. Install dependencies: `pip install -r requirements.txt`
3. Check Python path includes project root

**Authorization failures?**
1. Verify JWT secret key matches
2. Check token expiration
3. Ensure user roles are correct
