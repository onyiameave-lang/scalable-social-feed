import requests

BASE_URL = "http://127.0.0.1:5000"

def test_login():
    print("Testing login...")
    data = {"username": "test", "password": "1234"}
    r = requests.post(f"{BASE_URL}/login", json=data)
    assert r.status_code == 200, f"Failed login: {r.text}"
    token = r.json().get("token")
    assert token, "No token returned"
    print("Login successful, token:", token)
    return token

def test_create_post(token, title, content):
    print(f"Creating post: {title}")
    headers = {"Authorization": f"Bearer {token}"}
    data = {"title": title, "content": content}
    r = requests.post(f"{BASE_URL}/posts", headers=headers, json=data)
    assert r.status_code == 201, f"Failed to create post: {r.text}"
    print("Post created:", r.json())

def test_get_feed(token):
    print("Retrieving feed...")
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{BASE_URL}/feed", headers=headers)
    assert r.status_code == 200, f"Failed to get feed: {r.text}"
    posts = r.json()
    print("Feed contains posts:", posts)

if __name__ == "__main__":
    token = test_login()
    test_create_post(token, "Hello World", "This is my first automated post")
    test_create_post(token, "Second Post", "Testing feed retrieval")
    test_get_feed(token)
