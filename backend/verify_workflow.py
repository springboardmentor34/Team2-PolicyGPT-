import sys
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import datetime

# Setup paths to import app
sys.path.append(".")
from app.main import app
from app.database.database import SessionLocal, engine
from app.models.user import User
from app.models.policy import Policy
from app.models.audit_log import AuditLog
from app.auth.security import hash_password

client = TestClient(app)

def setup_test_users():
    db = SessionLocal()
    try:
        # Create test users if they don't exist
        users_info = [
            {"email": "official_verify@policygpt.gov", "password": "password123", "full_name": "Official Verifier", "role": "government_official"},
            {"email": "admin_verify@policygpt.gov", "password": "password123", "full_name": "Admin Verifier", "role": "administrator"},
            {"email": "citizen_verify@policygpt.gov", "password": "password123", "full_name": "Citizen Verifier", "role": "citizen"}
        ]
        
        users = {}
        for ui in users_info:
            user = db.query(User).filter(User.email == ui["email"]).first()
            if not user:
                user = User(
                    email=ui["email"],
                    password=hash_password(ui["password"]),
                    full_name=ui["full_name"],
                    role=ui["role"]
                )
                db.add(user)
                db.commit()
                db.refresh(user)
            users[ui["role"]] = ui
        return users
    finally:
        db.close()

def clean_test_policies():
    db = SessionLocal()
    try:
        # Delete old verify policies
        db.query(AuditLog).delete()
        db.query(Policy).filter(Policy.title.like("%Verify Policy%")).delete()
        db.commit()
    finally:
        db.close()

def get_token(email, password):
    response = client.post("/auth/login", json={"email": email, "password": password})
    assert response.status_code == 200, f"Login failed for {email}: {response.text}"
    return response.json()["access_token"]

def run_e2e_verification():
    print("--------------------------------------------------")
    print("      POLICY WORKFLOW SYSTEM E2E VERIFICATION     ")
    print("--------------------------------------------------")

    # 1. Setup
    users = setup_test_users()
    clean_test_policies()
    
    # Authenticate
    official_token = get_token("official_verify@policygpt.gov", "password123")
    admin_token = get_token("admin_verify@policygpt.gov", "password123")
    citizen_token = get_token("citizen_verify@policygpt.gov", "password123")
    
    headers_official = {"Authorization": f"Bearer {official_token}"}
    headers_admin = {"Authorization": f"Bearer {admin_token}"}
    headers_citizen = {"Authorization": f"Bearer {citizen_token}"}
    
    # 2. Step 1: Government Official creates a draft policy
    print("\n[Step 1] Official creates Draft Policy...")
    create_resp = client.post("/policies/", json={
        "title": "Verify Policy 2026",
        "description": "E2E test policy representing modern public guidelines",
        "category": "Technology",
        "department": "IT Dept",
        "state": "National",
        "status": "DRAFT"
    }, headers=headers_official)
    assert create_resp.status_code == 200, f"Failed creation: {create_resp.text}"
    policy = create_resp.json()
    policy_id = policy["id"]
    print(f"-> Created Policy ID: {policy_id}, Status: {policy['status']}")
    
    # 3. Check Citizen isolation (should not see draft)
    print("\n[Step 2] Testing Citizen Isolation...")
    cit_resp = client.get("/policies/", headers=headers_citizen)
    assert cit_resp.status_code == 200
    cit_policies = cit_resp.json()
    verify_found = any(p["id"] == policy_id for p in cit_policies)
    print(f"-> Citizen sees verify policy in general list?: {verify_found} (Expected: False)")
    assert not verify_found, "Security violation: Citizen saw a draft policy!"
    
    cit_detail_resp = client.get(f"/policies/{policy_id}", headers=headers_citizen)
    print(f"-> Citizen directly views draft detail response code: {cit_detail_resp.status_code} (Expected: 403)")
    assert cit_detail_resp.status_code == 403
    
    # 4. Step 3: Official submits policy for approval
    print("\n[Step 3] Official submits Policy for approval...")
    submit_resp = client.post(f"/policies/{policy_id}/submit", headers=headers_official)
    assert submit_resp.status_code == 200
    policy = submit_resp.json()
    print(f"-> Submitted policy state: {policy['status']} (Expected: PENDING_APPROVAL)")
    assert policy["status"] == "PENDING_APPROVAL"
    
    # 5. Check Official cannot edit after submission
    edit_resp = client.put(f"/policies/{policy_id}", json={"title": "Violating Edit"}, headers=headers_official)
    print(f"-> Official attempts editing pending policy response code: {edit_resp.status_code} (Expected: 409)")
    assert edit_resp.status_code == 409
    
    # 6. Step 4: Administrator rejects the submission
    print("\n[Step 4] Administrator reviews and rejects policy...")
    # Approver cannot be creator rule
    app_own_resp = client.post(f"/policies/{policy_id}/approve", json={"comment": "No"}, headers=headers_official)
    print(f"-> Official attempts approving own policy response code: {app_own_resp.status_code} (Expected: 403 or 400)")
    assert app_own_resp.status_code in [400, 403]
    
    # Reject policy without reason (fails validation)
    reject_fail_resp = client.post(f"/policies/{policy_id}/reject", json={"comment": ""}, headers=headers_admin)
    print(f"-> Admin attempts rejecting without comment response code: {reject_fail_resp.status_code} (Expected: 400)")
    assert reject_fail_resp.status_code == 400
    
    # Reject policy with reason
    reject_resp = client.post(f"/policies/{policy_id}/reject", json={"comment": "Please provide clearer guidelines on data sharing."}, headers=headers_admin)
    assert reject_resp.status_code == 200
    policy = reject_resp.json()
    print(f"-> Policy rejected. Status: {policy['status']} (Expected: REJECTED)")
    assert policy["status"] == "REJECTED"
    print(f"-> Review comment recorded: '{policy['review_comment']}'")
    
    # 7. Step 5: Official edits rejected policy (reverts state back to DRAFT)
    print("\n[Step 5] Official edits rejected policy to fix guidelines...")
    edit_success_resp = client.put(f"/policies/{policy_id}", json={
        "description": "E2E test policy representing modern public guidelines with data sharing details"
    }, headers=headers_official)
    assert edit_success_resp.status_code == 200
    policy = edit_success_resp.json()
    print(f"-> Status after edit: {policy['status']} (Expected: DRAFT)")
    assert policy["status"] == "DRAFT"
    
    # Resubmit
    resubmit_resp = client.post(f"/policies/{policy_id}/submit", headers=headers_official)
    assert resubmit_resp.status_code == 200
    print(f"-> Status after resubmission: {resubmit_resp.json()['status']}")
    
    # 8. Step 6: Admin approves policy
    print("\n[Step 6] Admin approves policy...")
    approve_resp = client.post(f"/policies/{policy_id}/approve", json={"comment": "Approved and looks comprehensive."}, headers=headers_admin)
    assert approve_resp.status_code == 200
    policy = approve_resp.json()
    print(f"-> Admin approved. Status: {policy['status']} (Expected: APPROVED)")
    assert policy["status"] == "APPROVED"
    
    # 9. Step 7: Admin publishes policy
    print("\n[Step 7] Admin publishes approved policy...")
    publish_resp = client.post(f"/policies/{policy_id}/publish", headers=headers_admin)
    assert publish_resp.status_code == 200
    policy = publish_resp.json()
    print(f"-> Policy published. Status: {policy['status']} (Expected: PUBLISHED)")
    assert policy["status"] == "PUBLISHED"
    
    # 10. Verification of Search / Citizen views
    print("\n[Step 8] Citizen views published policy...")
    published_resp = client.get("/policies/published", headers=headers_citizen)
    assert published_resp.status_code == 200
    published_list = published_resp.json()
    verify_found = any(p["id"] == policy_id for p in published_list)
    print(f"-> Citizen finds verify policy in public repository?: {verify_found} (Expected: True)")
    assert verify_found
    
    # Check audit log trail database entries
    print("\n[Step 9] Validating Database Audit Logs...")
    db = SessionLocal()
    try:
        logs = db.query(AuditLog).filter(AuditLog.policy_id == policy_id).order_by(AuditLog.id).all()
        print(f"-> Number of audit trail logs tracked for policy {policy_id}: {len(logs)}")
        for log in logs:
            print(f"   * Action: {log.action} | Old: {log.old_status} -> New: {log.new_status} | Comment: {log.comment or ''}")
        assert len(logs) >= 3, "Database audit log count doesn't track full workflow."
    finally:
        db.close()
        
    print("\n==================================================")
    print("  SUCCESS! ALL WORKFLOW TRANSITIONS VERIFIED!     ")
    print("==================================================")

if __name__ == "__main__":
    run_e2e_verification()
