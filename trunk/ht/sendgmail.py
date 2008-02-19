#!/usr/bin/env python
# coding=ISO-8859-1

# import os
# import sys
# import logging

# try:
    # import libgmail
# except ImportError:
    # print 'Error importing libgmail'
	# Urghhh...
    # sys.path.insert(1,
                    # os.path.realpath(os.path.join(os.path.dirname(__file__),
                                                  # os.path.pardir)))

    # import libgmail

# def sendGmail(usermail, password, to, subject, msg):
	# ga = libgmail.GmailAccount(usermail, password)
	# print "\nPlease wait, logging in..."
	# try:
		# ga.login()
	# except libgmail.GmailLoginFailure:
		# print "\nLogin failed. (Wrong username/password?)"
	# else:
		# print "Log in successful.\n"
		# gmsg = libgmail.GmailComposedMessage(to, subject, msg)
		# if ga.sendMessage(gmsg):
			# print "Message sent `%s` successfully." % subject
		# else:
			# print "Could not send message."

		# print "Done."
		
#!/usr/bin/python

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
	   part.add_header('Content-Disposition',
	           'attachment; filename="%s"' % os.path.basename(attach))
	   msg.attach(part)

   mailServer = smtplib.SMTP("smtp.gmail.com", 587)
   mailServer.ehlo()
   mailServer.starttls()
   mailServer.ehlo()
   mailServer.login(gmailuser, gmailpwd)
   mailServer.sendmail(gmailuser, to, msg.as_string())
   # Should be mailServer.quit(), but that crashes...
   mailServer.close()

def prueba():
	gmailuser = 'betisman@gmail.com'
	gmailpwd = 'logaritmo'
	#to = 'betisman@gmail.com'
	to = 'betisman@gmail.com'
	subject = 'Esto es una prueba automatica'
	msg = 'Si te ha llegado este mensaje, enhorabuena, has sido agraciado con el honor de ser conejillo de indias en la prueba del programita que envía emails a través de gmail creado por Betisman.\n\nUn saludo enorme.'
	msg = open('xmls\\carr.txt', 'r').read()
	try:
		sendGmail(gmailuser, gmailpwd, to, subject, msg, None)
		print 'Mail enviado correctamente a la direccion ' + to
	except Exception:
		print 'El mail (creo) no ha sido enviado.'

prueba()