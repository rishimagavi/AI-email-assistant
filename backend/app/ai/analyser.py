import os
import anthropic
from dotenv import load_dotenv
from app.models.email import Email

load_dotenv()

# Toggle this to False when you want to use real Claude API
USE_MOCK = True

MOCK_RESPONSE = {
    "category": "Legal",
    "urgency": "High",
    "summary": "Client requesting urgent update on property settlement case.",
    "draft_reply": "Dear [Sender], thank you for reaching out. I am currently reviewing the details of your case and will provide a comprehensive update shortly. Please do not hesitate to contact me if you have any immediate concerns."
}

def parse_analysis(text: str) -> dict:
    result = {}
    for line in text.strip().split('\n'):
        if line.startswith('Category:'):
            result['category'] = line.replace('Category:', '').strip()
        elif line.startswith('Urgency:'):
            result['urgency'] = line.replace('Urgency:', '').strip()
        elif line.startswith('Summary:'):
            result['summary'] = line.replace('Summary:', '').strip()
        elif line.startswith('Draft Reply:'):
            result['draft_reply'] = line.replace('Draft Reply:', '').strip()
    return result

def analyse_email(email: Email) -> Email:
    if USE_MOCK:
        if not email.category:
            email.category = MOCK_RESPONSE['category']
        if not email.urgency:
            email.urgency = MOCK_RESPONSE['urgency']
        if not email.summary:
            email.summary = MOCK_RESPONSE['summary']
        if not email.draft_reply:
            email.draft_reply = MOCK_RESPONSE['draft_reply']
        return email

    client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""Analyse this email and return:
1. Category (Legal, Client, Community, Admin, Personal)
2. Urgency (High / Medium / Low)
3. A brief one-line summary
4. A draft reply that is professional and tailored (not generic)

Email:
From: {email.sender}
Subject: {email.subject}
Body: {email.body}

Format your response exactly like this:
Category: ...
Urgency: ...
Summary: ...
Draft Reply: ...
"""
            }
        ]
    )
    result = parse_analysis(message.content[0].text)
    email.category = result.get('category')
    email.urgency = result.get('urgency')
    email.summary = result.get('summary')
    email.draft_reply = result.get('draft_reply')
    return email