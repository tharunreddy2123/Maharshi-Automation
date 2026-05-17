import subprocess
import smtplib
import os
from email.mime.text import MIMEText

print("Starting OpenShift Health Check")

# Collect Data
pods = subprocess.getoutput("oc get pods")
deployments = subprocess.getoutput("oc get deployment")
services = subprocess.getoutput("oc get svc")
routes = subprocess.getoutput("oc get route")

# Create Report
report = f"""
===================================
OpenShift Health Check Report
===================================

PODS
-----------------------------------

{pods}

DEPLOYMENTS
-----------------------------------

{deployments}

SERVICES
-----------------------------------

{services}

ROUTES
-----------------------------------

{routes}

===================================
Health Check Completed
===================================
"""

print(report)

# Mail Configuration
sender = os.environ['MAIL_USERNAME']
password = os.environ['MAIL_PASSWORD']

receiver = os.environ['MAIL_RECEIVER']

msg = MIMEText(report)

msg['Subject'] = 'OpenShift Health Check Report'
msg['From'] = sender
msg['To'] = receiver

# Send Mail
server = smtplib.SMTP('smtp.gmail.com', 587)

server.starttls()

server.login(sender, password)

server.send_message(msg)

server.quit()

print("Email Sent Successfully")