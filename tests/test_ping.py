import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

print("Starting tests...")

# Test the ping-mongo endpoint
response = client.get("/api/ping-mongo")
print("Response status:", response.status_code)
print("Response json:", response.json())

# Test fetching posts to see if likes are attached properly
response = client.get("/api/posts/?requester_id=1")
print("Posts response status:", response.status_code)
if response.status_code == 200:
    posts = response.json()
    if posts:
        print("First post likes:", posts[0].get("likes"))
    else:
        print("No posts found to check likes.")
else:
    print("Error fetching posts:", response.text)

print("Tests completed successfully!")
