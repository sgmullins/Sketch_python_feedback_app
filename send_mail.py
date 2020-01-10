import smtplib
from email.mime.text import MIMEText

def send_mail(customer, product, rating, comments):
	port = 2525
	smtp_server = 'smtp.mailtrap.io'
	login = '5a67d7289d5d92'
	password = '969ceaf7689d61'
	message = f"<h3>New Feedback Submission</h3><ul><li>Customer: {customer}</li><li>Product: {product}</li><li>Rating: {rating}</li><li>Comments: {comments}</li></ul>"
	sender_email ='email1@example.com'
	receiver_email = 'email2@example.com'
	msg = MIMEText(message, 'html')
	msg['Subject'] = 'SketchUp Feedback'
	msg['From'] = sender_email
	msg['To'] = receiver_email

	#send email
	with smtplib.SMTP(smtp_server, port) as server:
		server.login(login, password)
		server.sendmail(sender_email, receiver_email, msg.as_string())
