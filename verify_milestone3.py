import requests

def test_user(email, password, expected_authme_status, expected_analytics_status):
    print(f"\n--- Testing user: {email} ---")
    session = requests.Session()
    
    # 1. Login
    try:
        login_resp = session.post("http://127.0.0.1:8000/auth/login", json={"email": email, "password": password})
        if login_resp.status_code != 200:
            print(f"FAILED LOGIN: {login_resp.status_code} {login_resp.text}")
            return
            
        token = login_resp.json().get("access_token")
        print(f"Login success. Token received.")
    except Exception as e:
        print(f"Login request failed: {e}")
        return

    # 2. Auth /me
    headers = {"Authorization": f"Bearer {token}"}
    try:
        me_resp = session.get("http://127.0.0.1:8000/auth/me", headers=headers)
        print(f"/auth/me Status: {me_resp.status_code}")
        if me_resp.status_code != expected_authme_status:
            print(f"  EXPECTED {expected_authme_status}, GOT {me_resp.status_code}")
    except Exception as e:
        print(f"/auth/me request failed: {e}")

    # 3. Analytics
    try:
        analytics_resp = session.get("http://127.0.0.1:8000/analytics/overview", headers=headers)
        print(f"/analytics/overview Status: {analytics_resp.status_code}")
        if analytics_resp.status_code != expected_analytics_status:
            print(f"  EXPECTED {expected_analytics_status}, GOT {analytics_resp.status_code}")
            print(f"  Response: {analytics_resp.text}")
        elif analytics_resp.status_code == 200:
            data = analytics_resp.json()
            print(f"  Successfully fetched analytics:")
            print(f"  Total Policies: {data['metrics']['total_policies']}")
            print(f"  Total Users: {data['metrics']['total_users']}")
            print(f"  AI Trend: {data['insights']['trend']}")
            print(f"  AI Rec:   {data['insights']['recommendation']}")
    except Exception as e:
        print(f"/analytics/overview request failed: {e}")

if __name__ == "__main__":
    test_user("admin@policygpt.gov.in", "Password123", 200, 200)
    test_user("official@policygpt.gov.in", "Password123", 200, 200)
    test_user("citizen@policygpt.gov.in", "Password123", 200, 403)
