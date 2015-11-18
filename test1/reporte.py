import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import Encoders
import urllib2
import datetime

now = datetime.date.today()

mp3file = urllib2.urlopen("http://104.236.113.108:8000/compra/reporte/")
output = open('reporte(%s).pdf' % (str(now), ),'wb')
output.write(mp3file.read())
output.close()

SUBJECT = 'Reporte (%s)' % (str(now), )

FROM = 'luismiguel.mopa@gmail.com'
TO = 'luismiguel.mopa@gmail.com'

msg = MIMEMultipart()
msg['Subject'] = SUBJECT 
msg['From'] = FROM
msg['To'] = TO

part = MIMEBase('application', "octet-stream")
part.set_payload(open('reporte(%s).pdf' % (str(now), ), "rb").read())
Encoders.encode_base64(part)

part.add_header('Content-Disposition', 'attachment; filename="reporte(%s).pdf"' % (str(now), ))

msg.attach(part)

server = smtplib.SMTP("smtp.gmail.com", 587)
server.ehlo()
server.starttls()
server.login(FROM, 'nogbbaxooebbqvvv')
server.sendmail(FROM, TO, msg.as_string())
server.close()