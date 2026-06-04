from dataclasses import dataclass
from typing import Optional

@dataclass
class Email:
    id: str
    sender: str
    subject: str
    date: str
    body: str
    provider: str
    category: Optional[str] = None
    urgency: Optional[str] = None
    summary: Optional[str] = None
    draft_reply: Optional[str] = None

def from_dict(data: dict) -> Email:
    return Email(
        id=data['id'],
        sender=data['sender'],
        subject=data['subject'],
        date=data['date'],
        body=data['body'],
        provider=data['provider']
    )