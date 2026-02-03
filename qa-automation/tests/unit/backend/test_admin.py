"""Admin endpoint tests"""
import pytest
from app.models import User, Ticket, Task

class TestAdminEndpoints:
    """Test admin-only endpoints"""
    
    def test_admin_dashboard(self, client, admin_headers):
        """Test admin dashboard endpoint"""
        response = client.get('/api/admin/dashboard',
            headers=admin_headers
        )
        assert response.status_code == 200
        assert 'statistics' in response.json or 'metrics' in response.json
    
    def test_admin_dashboard_access_denied(self, client, auth_headers):
        """Test non-admin cannot access dashboard"""
        response = client.get('/api/admin/dashboard',
            headers=auth_headers
        )
        assert response.status_code == 403
    
    def test_admin_reports_tickets(self, client, admin_headers):
        """Test ticket reports endpoint"""
        response = client.get('/api/admin/reports/tickets',
            headers=admin_headers
        )
        assert response.status_code == 200
    
    def test_admin_reports_agents(self, client, admin_headers):
        """Test agent reports endpoint"""
        response = client.get('/api/admin/reports/agents',
            headers=admin_headers
        )
        assert response.status_code == 200
    
    def test_admin_reports_sla(self, client, admin_headers):
        """Test SLA reports endpoint"""
        response = client.get('/api/admin/reports/sla',
            headers=admin_headers
        )
        assert response.status_code == 200
