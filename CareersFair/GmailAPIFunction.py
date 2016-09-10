#create MIMEMultipart
from email.MIMEMultipart import MIMEMultipart
#def create_message(sender, to, subject, message_text):
def create_message(sender, to, subject):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEMultipart()
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return message

#create MIMEText
from email.MIMEText import MIMEText
def create_text(message, message_text, textType):
    message.attach(MIMEText(message_text, textType))
    return message

#with attachments
from email.MIMEBase import MIMEBase
from email import encoders
def create_attachment(file_address, filename, message):
  attachment = open(file_address, 'rb')
  part = MIMEBase('application', 'octet-stream')
  part.set_payload((attachment).read())
  encoders.encode_base64(part)
  part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
  message.attach(part)
  return message

def create_draft(service, user_id, message_body):
  """Create and insert a draft email. Print the returned draft's message and id.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message_body: The body of the email message, including headers.

  Returns:
    Draft object, including draft id and message meta data.
  """
  try:
    message = {'message': message_body}
    draft = service.users().drafts().create(userId=user_id, body=message).execute()
    print 'Draft id: %s\nDraft message: %s' % (draft['id'], draft['message'])
    return draft
  except errors.HttpError, error:
    print 'An error occurred: %s' % error
    return None

import base64
from apiclient import errors
from quickstart import get_credentials
from apiclient.discovery import build
from httplib2 import Http
def send_message(message):
  """Send an email message.

  Args:
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """
  try:
    credentials = get_credentials()
    service = build('gmail', 'v1', http = credentials.authorize(Http()))

    message = {'raw': base64.urlsafe_b64encode(message.as_string())}
    message = (service.users().messages().send(userId='me', body=message)
               .execute())
    print 'Message Id: %s' % message['id']
    return message
  except errors.HttpError, error:
    print 'An error occurred: %s' % error

