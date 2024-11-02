import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def notify_delete(event, context):
    """Triggered by a change to a Cloud Storage bucket.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    # Get details about the deleted object
    bucket_name = event['bucket']
    file_name = event['name']
    deletion_time = event['timeDeleted']

    # Email configuration
    to_email = os.environ.get('TO_EMAIL')  # Recipient's email
    from_email = os.environ.get('FROM_EMAIL')  # Sender's email
    subject = "Alert: File Deleted from GCS Bucket"
    message_body = f"""
        Hello,

        This is to notify you that an object has been deleted from your Google Cloud Storage bucket.

        Details:
        - Bucket: {bucket_name}
        - File: {file_name}
        - Deletion Time: {deletion_time}

        Regards,
        GCP Notification Service
    """

    # Create the email message
    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        plain_text_content=message_body,
    )

    # Send the email
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(f"Email sent! Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending email: {e}")
