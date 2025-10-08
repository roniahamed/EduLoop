# API Test Generation and Load Testing Plan

## Unit Tests for API Endpoints

### Questions App Tests (questions/tests.py)
- [x] Test GroupViewSet: GET list, POST create (admin only)
- [x] Test SubjectViewSet: GET list, POST create (admin only)
- [x] Test SubjectDetailViewSet: GET subjects by group
- [x] Test CategoryViewSet: GET list all, POST create (admin only)
- [x] Test CategoryDetailsViewSet: GET categories by subject
- [x] Test SubCategoryViewSet: GET list all, POST create (admin only)
- [x] Test SubCategoryDetailsViewSet: GET subcategories by category
- [x] Test QuestionViewSet: POST start session, GET next question, DELETE reset session
- [x] Test BulkQuestionUploadView: POST upload questions (admin only)
- [x] Test permissions: read-only for non-admin, full for admin
- [x] Test pagination on list views
- [x] Test throttling

### Users App Tests (users/tests.py)
- [x] Test ValidateAccessTokenView: POST valid token, invalid token
- [x] Test obtain_auth_token: POST login (if applicable)

## Load Testing Script
- [x] Create load_test.py: Simulate 10000 concurrent users hitting various endpoints
- [x] Use threading to spawn 10000 threads making requests
- [x] Measure response times, success rates
- [x] Include different endpoints in the load test

## Execution
- [x] Run unit tests: python manage.py test
- [ ] Run load test: python load_test.py (requires server running on localhost:8000)
- [ ] Analyze results
