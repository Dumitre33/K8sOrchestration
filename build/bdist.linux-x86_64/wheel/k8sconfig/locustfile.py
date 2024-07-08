from locust import HttpUser, between, task
import time
import random
import string

class UserBehavior(HttpUser):
    wait_time = between(1,5)

    def generate_unique_name(self, base):
        unique_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        return f"{base}-{int(time.time())}-{unique_suffix}"

    @task
    def test_create_deployment(self):
        unique_name = self.generate_unique_name("test-deployment")
        data = {
            "service_name": unique_name,
            "app_label": unique_name,
            "image": "nginx",
            "port": 8080,
            "replicas": 1
        }
        response = self.client.post("/create-deployment", data=data)
        if response.status_code == 200:
            self.client.post("/delete-resource", data={"resource_type": "deployment", "resource_name": unique_name})

