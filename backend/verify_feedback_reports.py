import sys
import os
from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.main import app

client = TestClient(app)

def test_feedback_and_reports():
    print("==================================================")
    print("     TESTING FEEDBACK & REPORT GENERATION APIs    ")
    print("==================================================")

    # 1. Test POST /feedback
    print("\n[Step 1] Submitting Feedback (POST /feedback)...")
    post_payload = {
        "user_name": "Ravi",
        "rating": 5,
        "message": "Very useful"
    }
    response = client.post("/feedback", json=post_payload)
    print(f"-> Response Status: {response.status_code}")
    assert response.status_code == 201, f"Expected 201 Created, got {response.status_code}: {response.text}"
    fb = response.json()
    print(f"-> Created Feedback: ID={fb['id']}, User={fb['user_name']}, Rating={fb['rating']}, Message='{fb['message']}'")
    assert fb["user_name"] == "Ravi"
    assert fb["rating"] == 5
    assert fb["message"] == "Very useful"
    created_id = fb["id"]

    # 2. Test GET /feedback
    print("\n[Step 2] Viewing All Feedback (GET /feedback)...")
    response = client.get("/feedback")
    print(f"-> Response Status: {response.status_code}")
    assert response.status_code == 200
    feedbacks = response.json()
    print(f"-> Total Feedbacks Returned: {len(feedbacks)}")
    assert len(feedbacks) > 0
    found = any(item["id"] == created_id for item in feedbacks)
    assert found, "Newly created feedback was not returned in GET /feedback list!"
    print("-> Successfully verified newly created feedback in list!")

    # 3. Test DELETE /feedback/{id}
    print(f"\n[Step 3] Deleting Feedback ID {created_id} (DELETE /feedback/{created_id})...")
    del_resp = client.delete(f"/feedback/{created_id}")
    print(f"-> Response Status: {del_resp.status_code}")
    print(f"-> Message: {del_resp.json()}")
    assert del_resp.status_code == 200

    # Verify deletion
    verify_del = client.get("/feedback")
    remaining = verify_del.json()
    deleted_found = any(item["id"] == created_id for item in remaining)
    assert not deleted_found, f"Feedback ID {created_id} still present after DELETE call!"
    print("-> Successfully verified feedback deletion!")

    # 4. Test GET /reports/summary
    print("\n[Step 4] Fetching Report Summary (GET /reports/summary)...")
    rep_resp = client.get("/reports/summary")
    print(f"-> Response Status: {rep_resp.status_code}")
    assert rep_resp.status_code == 200
    summary = rep_resp.json()
    print("-> Summary Metrics:")
    print(f"   * Total Policies: {summary['total_policies']}")
    print(f"   * Published Policies: {summary['published_policies']}")
    print(f"   * Total Schemes: {summary['total_schemes']}")
    print(f"   * Total Feedback: {summary['total_feedback']}")
    print(f"   * Average Rating: {summary['average_rating']}")
    assert summary["total_policies"] >= 0
    assert summary["total_schemes"] >= 0

    # 5. Test GET /reports/export/pdf
    print("\n[Step 5] Exporting PDF Report (GET /reports/export/pdf)...")
    pdf_resp = client.get("/reports/export/pdf")
    print(f"-> Response Status: {pdf_resp.status_code}")
    print(f"-> Content-Type: {pdf_resp.headers.get('content-type')}")
    print(f"-> File Size: {len(pdf_resp.content)} bytes")
    assert pdf_resp.status_code == 200
    assert "pdf" in pdf_resp.headers.get("content-type", "").lower()
    assert len(pdf_resp.content) > 0
    print("-> PDF Report export verified!")

    # 6. Test GET /reports/export/excel
    print("\n[Step 6] Exporting Excel/Spreadsheet Report (GET /reports/export/excel)...")
    excel_resp = client.get("/reports/export/excel")
    print(f"-> Response Status: {excel_resp.status_code}")
    print(f"-> Content-Type: {excel_resp.headers.get('content-type')}")
    print(f"-> File Size: {len(excel_resp.content)} bytes")
    assert excel_resp.status_code == 200
    assert len(excel_resp.content) > 0
    print("-> Excel Report export verified!")

    print("\n==================================================")
    print("  ALL FEEDBACK AND REPORT API TESTS PASSED 100%!  ")
    print("==================================================")

if __name__ == "__main__":
    test_feedback_and_reports()
