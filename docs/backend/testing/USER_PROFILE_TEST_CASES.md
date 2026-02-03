# Comprehensive User Profile Management Test Cases

## Overview

This document describes comprehensive test cases for the User Profile Management feature, covering user registration, profile updates, password changes, and account deletion.

**Test File**: `tests/test_user_profile_comprehensive.py`

**Total Test Cases**: 100+ test scenarios

---

## Test Categories

### 1. Positive Test Cases ✅
Tests that verify the system works correctly with valid inputs and expected successful outcomes.

### 2. Negative Test Cases ❌
Tests that verify proper error handling for invalid inputs and unauthorized actions.

### 3. Edge Cases 🔍
Tests that verify boundary conditions, unusual scenarios, and special character handling.

### 4. Security Test Cases 🔒
Tests that verify authorization, authentication, and protection against security vulnerabilities.

---

## Test Coverage Breakdown

### User Registration (35+ test cases)

#### Positive Test Cases
- ✅ Register with minimal required fields
- ✅ Register with all optional fields
- ✅ Register as agent with availability status
- ✅ Register with maximum length username
- ✅ Register with special characters in name
- ✅ Register with Unicode characters

#### Negative Test Cases
- ❌ Missing required fields (username, email, password)
- ❌ Duplicate username
- ❌ Duplicate email
- ❌ Invalid email format
- ❌ Password too short (< 8 characters)
- ❌ Username too short (< 3 characters)
- ❌ Username too long (> 80 characters)
- ❌ Invalid role value
- ❌ Invalid availability status

#### Edge Cases
- 🔍 Empty string fields
- 🔍 Whitespace-only fields
- 🔍 Unicode characters in names
- 🔍 Maximum length password
- 🔍 Large expertise areas array

#### Security Test Cases
- 🔒 Password never returned in response
- 🔒 Password stored as hash, not plaintext
- 🔒 SQL injection attempts in username
- 🔒 XSS attempts in name fields
- 🔒 Rate limiting for rapid registrations

---

### Profile Updates (30+ test cases)

#### Positive Test Cases
- ✅ Update own profile (first_name, last_name, email)
- ✅ Update multiple fields simultaneously
- ✅ Agent updates availability status
- ✅ Agent updates expertise areas
- ✅ Admin updates other user profiles
- ✅ Admin updates user role
- ✅ Admin updates user active status

#### Negative Test Cases
- ❌ Non-admin updates other user's profile
- ❌ Invalid email format
- ❌ Duplicate email
- ❌ Name fields too long
- ❌ Non-admin attempts role update
- ❌ Non-admin attempts active status update
- ❌ Update non-existent user
- ❌ Update without authentication

#### Edge Cases
- 🔍 Empty string updates
- 🔍 Partial updates (only one field)
- 🔍 Special characters in names
- 🔍 Unicode characters

#### Security Test Cases
- 🔒 Authorization check prevents unauthorized updates
- 🔒 Admin cannot remove own admin role
- 🔒 Admin cannot deactivate own account
- 🔒 SQL injection attempts in update fields

---

### Password Changes (15+ test cases)

#### Positive Test Cases
- ✅ User changes own password successfully
- ✅ Password change with special characters
- ✅ Password change with Unicode
- ✅ Admin changes user password
- ✅ Password updated, old password invalidated
- ✅ New password works for login

#### Negative Test Cases
- ❌ Password too short (< 8 characters)
- ❌ Change password without authentication
- ❌ Non-admin changes other user's password

#### Edge Cases
- 🔍 Change password to same value
- 🔍 Maximum length password
- 🔍 Multiple rapid password changes

#### Security Test Cases
- 🔒 Password never returned in response
- 🔒 Password stored as hash
- 🔒 Token invalidation after password change (if implemented)

---

### Account Deletion (15+ test cases)

#### Positive Test Cases
- ✅ User deletes own account
- ✅ Admin deletes user account
- ✅ Account deletion cascades to related data

#### Negative Test Cases
- ❌ Non-admin deletes other user's account
- ❌ Delete non-existent account
- ❌ Delete without authentication
- ❌ Delete with invalid token

#### Edge Cases
- 🔍 Delete account twice
- 🔍 Delete account with active sessions

#### Security Test Cases
- 🔒 Authorization check prevents unauthorized deletion
- 🔒 Admin self-deletion prevention
- 🔒 SQL injection in user ID
- 🔒 IDOR (Insecure Direct Object Reference) vulnerability test

---

### Integration Tests (5+ test cases)

- 🔄 Complete user lifecycle (register → update → change password → delete)
- 🔄 Concurrent updates handling
- 🔄 Multiple operations in sequence

---

## Test Data Examples

### Valid Test Data

```json
{
  "username": "testuser123",
  "email": "test@example.com",
  "password": "SecurePass123",
  "first_name": "John",
  "last_name": "Doe",
  "role": "customer",
  "availability_status": "available",
  "expertise_areas": ["Python", "Flask", "API Development"]
}
```

### Invalid Test Data Examples

```json
// Too short password
{
  "username": "user",
  "email": "user@example.com",
  "password": "short"
}

// Duplicate username
{
  "username": "existinguser",
  "email": "new@example.com",
  "password": "SecurePass123"
}

// Invalid email
{
  "username": "user",
  "email": "notanemail",
  "password": "SecurePass123"
}
```

### Edge Case Test Data

```json
// Maximum length username
{
  "username": "a" * 80,
  "email": "long@example.com",
  "password": "SecurePass123"
}

// Unicode characters
{
  "username": "unicodeuser",
  "email": "unicode@example.com",
  "password": "SecurePass123",
  "first_name": "José",
  "last_name": "Müller"
}

// Special characters
{
  "username": "specialuser",
  "email": "special@example.com",
  "password": "SecurePass123",
  "first_name": "O'Brien",
  "last_name": "van der Berg"
}
```

---

## Running the Tests

### Run All User Profile Tests

```bash
cd flask_api
source venv/bin/activate
pytest tests/test_user_profile_comprehensive.py -v
```

### Run Specific Test Class

```bash
# Run only registration tests
pytest tests/test_user_profile_comprehensive.py::TestUserRegistration -v

# Run only profile update tests
pytest tests/test_user_profile_comprehensive.py::TestProfileUpdates -v

# Run only password change tests
pytest tests/test_user_profile_comprehensive.py::TestPasswordChanges -v

# Run only account deletion tests
pytest tests/test_user_profile_comprehensive.py::TestAccountDeletion -v
```

### Run Specific Test Case

```bash
# Run a specific test
pytest tests/test_user_profile_comprehensive.py::TestUserRegistration::test_register_user_with_minimal_fields -v
```

### Run with Coverage

```bash
pytest tests/test_user_profile_comprehensive.py --cov=app --cov-report=html
```

### Run with Detailed Output

```bash
pytest tests/test_user_profile_comprehensive.py -v -s
```

---

## Expected Test Results

### Success Criteria

- ✅ All positive test cases return expected status codes (200, 201, 204)
- ✅ All negative test cases return appropriate error codes (400, 401, 403, 404)
- ✅ All security test cases prevent unauthorized access
- ✅ All edge cases handle boundary conditions correctly
- ✅ No sensitive data (passwords) exposed in responses
- ✅ All passwords properly hashed

### Common Assertions

```python
# Successful registration
assert response.status_code == 201
assert 'password' not in response.json

# Successful update
assert response.status_code == 200
assert response.json['field'] == 'expected_value'

# Unauthorized access
assert response.status_code == 403

# Validation error
assert response.status_code == 400

# Not found
assert response.status_code == 404
```

---

## Security Considerations Tested

### 1. Authentication
- ✅ All protected endpoints require valid JWT token
- ✅ Invalid tokens are rejected
- ✅ Expired tokens are rejected

### 2. Authorization
- ✅ Users can only update their own profiles
- ✅ Admins can update any user
- ✅ Non-admins cannot change roles
- ✅ Non-admins cannot change active status

### 3. Input Validation
- ✅ SQL injection attempts are handled safely
- ✅ XSS attempts are sanitized
- ✅ Field length limits are enforced
- ✅ Required fields are validated

### 4. Data Protection
- ✅ Passwords are never returned in responses
- ✅ Passwords are hashed using secure algorithms
- ✅ Sensitive operations require authentication

### 5. Rate Limiting
- ✅ Rapid requests are rate-limited (if configured)
- ✅ Prevents abuse and DoS attacks

---

## Test Maintenance

### Adding New Test Cases

When adding new features to user profile management:

1. **Add positive test case** - Verify feature works with valid input
2. **Add negative test case** - Verify proper error handling
3. **Add edge case** - Test boundary conditions
4. **Add security test** - Verify authorization and security

### Test Naming Convention

- `test_<action>_<condition>` - Descriptive test names
- Example: `test_update_profile_with_invalid_email`
- Example: `test_change_password_without_authentication`

### Test Organization

- Group related tests in classes
- Use descriptive docstrings
- Include expected results in docstrings
- Use fixtures for common setup

---

## Coverage Goals

- **Line Coverage**: > 90%
- **Branch Coverage**: > 85%
- **Function Coverage**: 100%

### Current Coverage Areas

- ✅ User registration endpoint
- ✅ Profile update endpoint
- ✅ Password change functionality
- ✅ Account deletion endpoint
- ✅ Authorization checks
- ✅ Input validation
- ✅ Error handling

---

## Known Limitations

1. **Token Invalidation**: Password changes may not invalidate existing tokens (JWT limitation)
2. **Rate Limiting**: Exact rate limit behavior depends on configuration
3. **Cascade Deletion**: Behavior depends on database cascade settings
4. **Concurrent Updates**: Last write wins (no optimistic locking)

---

## Future Enhancements

- [ ] Add tests for email verification
- [ ] Add tests for password reset functionality
- [ ] Add tests for two-factor authentication
- [ ] Add tests for account recovery
- [ ] Add performance/load tests
- [ ] Add tests for audit logging

---

## References

- **API Documentation**: `/api/docs` (Swagger UI)
- **User Model**: `app/models/user.py`
- **User Routes**: `app/users/routes.py`
- **User Schemas**: `app/schemas/user.py`
- **Auth Routes**: `app/auth/routes.py`

---

## Support

For questions or issues with these test cases:
1. Check the test file comments
2. Review the API documentation
3. Check existing test fixtures in `tests/conftest.py`
4. Review model definitions for field constraints
