from twilio.rest import Client

def send_sms_reminder(customer_phone, message):
    account_sid = 'your_account_sid'
    auth_token = 'your_auth_token'
    client = Client(account_sid, auth_token)
    client.messages.create(
        to=customer_phone,
        from_="your_twilio_number",
        body=message
    )
