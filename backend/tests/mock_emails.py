from app.models.email import Email

MOCK_EMAILS = [
    Email(
        id="mock_001",
        sender="John Smith",
        subject="Hearing Scheduled - Matter No. 2024/CV/4521",
        date="Thu, 04 Jun 2026 09:00:00 +1000",
        body="Dear Counsellor, please be advised that the above matter has been scheduled for hearing on 15 June 2026 at 10:00am at the County Court of Victoria. Please confirm your availability at your earliest convenience.",
        provider="mock",
        category="court_tribunal",
        urgency="High",
        summary="Hearing scheduled for Matter 4521 on 15 June, confirmation required.",
        draft_reply="Dear Mr Smith, thank you for the notification. I confirm my availability for the hearing scheduled on 15 June 2026 at 10:00am at the County Court of Victoria. Please let me know if any further documentation is required prior to the hearing date."
    ),
    Email(
        id="mock_002",
        sender="Sarah Johnson",
        subject="Referral - Family Law Matter",
        date="Thu, 04 Jun 2026 08:30:00 +1000",
        body="Hi, I was referred to you by Michael Chen. I am going through a difficult separation and need advice regarding custody arrangements for my two children. Could we schedule a consultation at your earliest convenience?",
        provider="mock",
        category="client_matters",
        urgency="High",
        summary="New client referral seeking consultation for custody arrangements.",
        draft_reply="Dear Ms Johnson, thank you for reaching out. I am sorry to hear about the difficulties you are experiencing. I would be happy to arrange a consultation to discuss your situation in detail. Please reply with your availability over the next week and I will confirm a time that suits."
    ),
    Email(
        id="mock_003",
        sender="Michael Davies",
        subject="RE: Settlement Offer - Jones v Peters",
        date="Wed, 03 Jun 2026 16:45:00 +1000",
        body="Dear Colleague, further to our previous correspondence, my client has instructed me to put forward a revised settlement offer of $85,000 inclusive of costs. This offer remains open for acceptance until close of business Friday 6 June 2026.",
        provider="mock",
        category="opposing_counsel",
        urgency="High",
        summary="Revised settlement offer of $85,000 open until Friday COB.",
        draft_reply="Dear Mr Davies, thank you for the revised offer. I have received your correspondence and will present the offer to my client promptly. I will revert to you with instructions prior to the deadline of Friday 6 June 2026."
    ),
    Email(
        id="mock_004",
        sender="Community Legal Centre",
        subject="Volunteer Legal Aid - June Session",
        date="Wed, 03 Jun 2026 14:00:00 +1000",
        body="Dear Legal Professional, we are reaching out to invite you to participate in our June community legal aid session on 20 June 2026. Your expertise would be invaluable to members of our community who cannot afford legal representation.",
        provider="mock",
        category="community_probono",
        urgency="Medium",
        summary="Invitation to volunteer at community legal aid session on 20 June.",
        draft_reply="Dear Coordinator, thank you for the invitation to participate in the June legal aid session. I am pleased to confirm my availability on 20 June 2026 and look forward to contributing to this important community initiative. Please send through any preparation materials at your convenience."
    ),
    Email(
        id="mock_005",
        sender="Law Institute of Victoria",
        subject="CPD Reminder - 2 Points Remaining",
        date="Tue, 02 Jun 2026 10:00:00 +1000",
        body="This is a reminder that your Continuing Professional Development requirements for this year are due by 31 March. You currently have 8 of the required 10 points completed. Please log in to the portal to record any outstanding activities.",
        provider="mock",
        category="law_society",
        urgency="Medium",
        summary="2 CPD points remaining before annual deadline.",
        draft_reply="Thank you for the reminder. I will log in to the portal and update my CPD records accordingly."
    ),
    Email(
        id="mock_006",
        sender="Office National",
        subject="Invoice #4521 - Monthly Office Supplies",
        date="Tue, 02 Jun 2026 07:00:00 +1000",
        body="Please find attached your monthly invoice for office supplies. Total amount due: $124.50. Payment is due within 30 days.",
        provider="mock",
        category="admin_finance",
        urgency="Low",
        summary="Monthly office supplies invoice of $124.50 due within 30 days.",
        draft_reply="Thank you for the invoice. Payment will be processed within the due date."
    ),
]

def get_mock_emails():
    return MOCK_EMAILS