#!/usr/bin/env python
# coding=ISO-8859-1

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import os

def sendGmail(gmailuser, gmailpwd, to, subject, text, attach):
	msg = MIMEMultipart()

	msg['From'] = gmailuser
	msg['To'] = to
	msg['Subject'] = subject

	msg.attach(MIMEText(text))

	part = MIMEBase('application', 'octet-stream')
	if attach != None:
		part.set_payload(open(attach, 'rb').read())
		Encoders.encode_base64(part)
		part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(attach))
		msg.attach(part)

	mailServer = smtplib.SMTP("smtp.gmail.com", 587)
	mailServer.ehlo()
	mailServer.starttls()
	mailServer.ehlo()
	mailServer.login(gmailuser, gmailpwd)
	mailServer.sendmail(gmailuser, to, msg.as_string())
	# Should be mailServer.quit(), but that crashes...
	mailServer.close()
