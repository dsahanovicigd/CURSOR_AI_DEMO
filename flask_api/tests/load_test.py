"""
Load testing script for Locust
Run with: locust -f tests/load_test.py --headless -u 50 -r 10 -t 30s
"""

from locust import HttpUser, task, between
import random


class APIUser(HttpUser):
    """Simulates API user behavior"""
    wait_time = between(1, 3)
    
    def on_start(self):
        """Login before starting tests"""
        # Register/login user
        username = f"loadtest_{random.randint(1000, 9999)}"
        self.client.post("/api/auth/register", json={
            "username": username,
            "email": f"{username}@example.com",
            "password": "password123"
        })
        
        # Login and store token
        response = self.client.post("/api/auth/login", json={
            "username": username,
            "password": "password123"
        })
        if response.status_code == 200:
            self.token = response.json().get("access_token")
            self.headers = {"Authorization": f"Bearer {self.token}"}
    
    @task(3)
    def get_products(self):
        """Get products list"""
        self.client.get("/api/products")
    
    @task(2)
    def get_product_by_id(self):
        """Get specific product"""
        product_id = random.randint(1, 10)
        self.client.get(f"/api/products/{product_id}")
    
    @task(1)
    def get_user_profile(self):
        """Get user profile"""
        self.client.get("/api/auth/me", headers=self.headers)
    
    @task(1)
    def get_orders(self):
        """Get user orders"""
        self.client.get("/api/orders", headers=self.headers)
    
    @task(1)
    def search_products(self):
        """Search products"""
        search_terms = ["product", "test", "item", "sample"]
        term = random.choice(search_terms)
        self.client.get(f"/api/products?search={term}")
