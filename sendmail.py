import os, random, sys, json, smtplib, getpass
from time import strftime
from pprint import pprint
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

class Attachements:
	def __init__(self, attachments_folder="attachments"):	
		self.__attachments_folder = attachments_folder
		self.__attachments = self.__load_attachements()
		random.seed()

	def __load_attachements(self):
		return [os.path.join(self.__attachments_folder, f) for f in os.listdir(self.__attachments_folder) if os.path.isfile(os.path.join(self.__attachments_folder, f))]

	def get_attchment_by_id(self, index=0):
		return self.__attachments[index]

	def get_random_attachement(self):
		return random.choice(self.__attachments)

class SMTP_Config:
	def __init__(self, smtp_server, smtp_port, smtp_use_ssl, smtp_username, smtp_password):
		self.smtp_server	= smtp_server
		self.port			= smtp_port
		self.use_ssl		= smtp_use_ssl
		self.smtp_username	= smtp_username
		self.smtp_password	= smtp_password
		
class EmailsSender:

	def __init__(self, config_file_path):

		with open(config_file_path) as config_file:
			self.__config = json.load(config_file)

		self.__attachments = Attachements()

	def __prep_msg(self):
		msg = MIMEMultipart('mixed')

		if self.__config["batch_config"]["randomize_senders"]:
			msg['From'] = random.choice(self.__config["batch_config"]["senders_override"])
		else:
			msg['From'] = self.__config["message"]["from"]

		msg['To'] = self.__config["message"]["to"]			
		msg['Subject'] = self.__config["message"]["subject"] if self.__config["message"]["subject"] else self.__default_subject(self.__config["smtp_config"]["smtp_server"])
				
		# Attach file?
		attachment_file_path = ""
		if self.__config["batch_config"]["randomize_attachements"]:
			attachment_file_path = self.__attachments.get_random_attachement()
		elif self.__config["message"]["attachment"]:
			attachment_file_path = self.__attachments.get_attchment_by_id(self.__config["message"]["attachment_id"])

		if attachment_file_path:
			with open(attachment_file_path, "rb") as f:
				part1 = MIMEApplication(f.read(),Name = os.path.basename(attachment_file_path))
				part1['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(attachment_file_path)
				msg.attach(part1)
		
		# Create the body of the message (a plain-text and an HTML version).
		html = """\
		<html>
		  <head></head>
		  <body>
			<p>Hi!<br>
			   How are you?<br>
			   Here is the <a href="http://www.google.com">link</a> we discussed.
			   All the best.
			</p>
		  </body>
		</html>
		"""

		part2 = MIMEText(html, 'html')
		msg.attach(part2)

		return msg, attachment_file_path

	def __send_email(self):

		msg, attachment_file_path = self.__prep_msg()

		print "-------------------------"
		print "From:\t\t" 		+ msg['From']
		print "To:\t\t" 		+ msg['To']
		print "Subject:\t" 		+ msg['Subject']
		print "Attachement:\t" 	+ attachment_file_path

		smtp_server 	= self.__config["smtp_config"]["smtp_server"]
		smtp_port 		= self.__config["smtp_config"]["smtp_port"]
		smtp_use_ssl 	= self.__config["smtp_config"]["smtp_use_ssl"]
		smtp_username 	= self.__config["smtp_config"]["smtp_username"]
		smtp_password	= self.__config["smtp_config"]["smtp_password"]

		print ""

		try:
			print "Connecting to SMTP server at %s:%s... " % (smtp_server, smtp_port) ,
			s = smtplib.SMTP_SSL(smtp_server, smtp_port) if smtp_use_ssl else smtplib.SMTP(smtp_server, smtp_port)
			print "Done"
			
			if smtp_username:
				if smtp_password == '':
					smtp_password = getpass.getpass('password:')
				
				print "Authenticating..." ,
				s.login(smtp_username, smtp_password)
				print "Done"
			
			print "Sending message..." ,
			res = s.sendmail(msg['From'], msg['To'], msg.as_string())
			print res
			print "Done"
			
			s.quit()

		except Exception as e:
			print e

		print "-------------------------\n"
			
	def send_emails(self):

		number_of_emails = int(self.__config["batch_config"]["number_of_emails"])

		for i in range(number_of_emails):
			print "%2d of %2d" % (i+1, number_of_emails)
			
			self.__send_email()
			
			if number_of_emails > 1:
				self.__wait_counter(random.randint(self.__config["batch_config"]["min_wait"], self.__config["batch_config"]["max_wait"]))

	def __wait_counter(self, period_in_sec):
		for i in range(period_in_sec):
			sys.stdout.write("Waiting %s seconds: %3d\r" % (period_in_sec, i+1))
 			sys.stdout.flush()
 			time.sleep(1)

 		print ""

	def __default_subject(self, text):
		return " - ".join(["ReSec Test", text, strftime("%Y-%m-%d %I:%M:%S")])


if __name__ == '__main__':
	
	if len(sys.argv) != 2:
		print sys.argv[0] + " <config file name>"
		exit()

	mail_sender = EmailsSender(sys.argv[1])
	mail_sender.send_emails()
		
	