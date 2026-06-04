from fastapi import APIRouter
from app.models.email import Email
from app.ai.analyser import analyse_email
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

router = APIRouter()

USE_MOCK_EMAILS = True

def get_emails():
    if USE_MOCK_EMAILS:
        from tests.mock_emails import get_mock_emails
        return get_mock_emails()
    else:
        from app.connectors.gmail_connector import fetch_emails
        from app.models.email import from_dict
        raw = fetch_emails(max_results=20)
        return [from_dict(e) for e in raw]

@router.get("/emails")
def list_emails():
    emails = get_emails()
    analysed = [analyse_email(e) for e in emails]
    return [vars(e) for e in analysed]