from fastapi import FastAPI, Request

app = FastAPI()


@app.post("/jira-webhook")
async def jira_webhook(request: Request):
    """
    Receives Jira webhook payload and returns a static response
    for updating Jira custom fields.
    """
    # You can access the incoming payload if needed:
    # payload = await request.json()

    # Return static response
    return {
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
