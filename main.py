import os
import requests
from fastapi import FastAPI, Request
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

JIRA_BASE_URL = "https://magicworkshop-ai.atlassian.net/rest/api/3/issue"
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")


@app.post("/jira-webhook")
async def jira_webhook(request: Request):
    """
    Receives Jira webhook payload, extracts issue key,
    and updates the issue via Jira API.
    """
    payload = await request.json()

    # Extract issue key from incoming payload
    issue_key = payload.get("issue", {}).get("key")

    if not issue_key:
        return {"error": "No issue key found in payload"}

    # Payload to update Jira issue
    update_payload = {
        "fields": {
            "customfield_10042": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {"type": "text", "text": "10 story pts"}
                        ]
                    }
                ]
            },
            "customfield_10041": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {"type": "text", "text": "* Python Developer - 0.5\n* UI Developer - 1\n* DevOps Engineer - 0.5"}
                        ]
                    }
                ]
            }
        }
    }

    # Call Jira API to update the issue
    jira_url = f"{JIRA_BASE_URL}/{issue_key}"

    response = requests.put(
        jira_url,
        json=update_payload,
        auth=(CLIENT_ID, CLIENT_SECRET),
        headers={"Content-Type": "application/json"}
    )

    return {
        "issue_key": issue_key,
        "jira_url": jira_url,
        "status_code": response.status_code,
        "response": response.text if response.text else "OK"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
