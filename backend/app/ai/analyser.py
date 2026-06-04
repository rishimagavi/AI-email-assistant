import os
import anthropic
from dotenv import load_dotenv
from app.models.email import Email

load_dotenv()

USE_MOCK = False

MOCK_RESPONSE = {
    "category": "court_tribunal",
    "urgency": "High",
    "summary": "Client requesting urgent update on property settlement case.",
    "draft_reply": "Dear [Sender], thank you for reaching out. I am currently reviewing the details of your case and will provide a comprehensive update shortly. Please do not hesitate to contact me if you have any immediate concerns."
}

VALID_CATEGORIES = [
    "court_tribunal",
    "client_matters",
    "opposing_counsel",
    "community_probono",
    "law_society",
    "admin_finance"
]

def parse_analysis(text: str) -> dict:
    result = {}
    lines = text.strip().split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('Category:'):
            result['category'] = line.replace('Category:', '').strip()
        elif line.startswith('Urgency:'):
            result['urgency'] = line.replace('Urgency:', '').strip()
        elif line.startswith('Summary:'):
            result['summary'] = line.replace('Summary:', '').strip()
        elif line.startswith('Draft Reply:'):
            draft_lines = [line.replace('Draft Reply:', '').strip()]
            i += 1
            while i < len(lines):
                draft_lines.append(lines[i].strip())
                i += 1
            result['draft_reply'] = '\n'.join(draft_lines).strip()
            break
        i += 1
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
                "content": f"""You are an AI assistant for a Victorian lawyer in solo practice in Australia.

Analyse this email and respond in EXACTLY this format with no extra text:
Category: <one of: court_tribunal, client_matters, opposing_counsel, community_probono, law_society, admin_finance>
Urgency: <one of: High, Medium, Low>
Summary: <one line summary>
Draft Reply: <full professional draft reply tailored to this specific email>

Email:
From: {email.sender}
Subject: {email.subject}
Body: {email.body}
"""
            }
        ]
    )
    result = parse_analysis(message.content[0].text)
    email.category = result.get('category', 'admin_finance')
    email.urgency = result.get('urgency', 'Low')
    email.summary = result.get('summary', '')
    email.draft_reply = result.get('draft_reply', '')
    return email