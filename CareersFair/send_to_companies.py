from GmailAPIFunction import create_message
from GmailAPIFunction import create_draft
from GmailAPIFunction import create_text
from GmailAPIFunction import send_message
from GmailAPIFunction import create_attachment

email_model = open('../company_email.html', 'r')
email_model = email_model.read()

contactUrl = raw_input("address of contactList: ")
contactList = open(contactUrl, 'r').read()
contactList = contactList.split('\n')
#contactList = contactList.readlines()
for contactInfo in contactList:
    contactInfo = contactInfo.split(",")
    email_dear_to = contactInfo[2]
    email_to = contactInfo[0]
    print email_dear_to + "-->" + email_to
    email_body = email_model.replace("<company>", email_dear_to)
    new_message = create_message('me', email_to, 'Cambridge Engineering Careers Fair on 2nd November 2016')
    new_message = create_text(new_message, email_body, 'html')
    new_message = create_attachment('../BookingForm2016.docx', 'BookingForm2016.docx', new_message)
    new_message = create_attachment('../2016-CUES-Careers-Fair-Information-Packages.pdf', '2016-CUES-Careers-Fair-Information-Packages.pdf', new_message)
    send_message(new_message)
#    break

