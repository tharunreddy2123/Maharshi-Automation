import subprocess
import smtplib
import os
from email.mime.text import MIMEText

print("Starting OpenShift Health Check")

# Get All Accessible Projects
projects_cmd = "oc projects -q"
projects = subprocess.getoutput(projects_cmd).splitlines()

report = """
========================================
OpenShift Cluster Health Check Report
========================================
"""

for project in projects:

    report += f"\n\n####################################"
    report += f"\nPROJECT: {project}"
    report += f"\n####################################\n"

    # Pods
    pods = subprocess.getoutput(f"oc get pods -n {project}")

    # Deployments
    deployments = subprocess.getoutput(f"oc get deployment -n {project}")

    # Services
    services = subprocess.getoutput(f"oc get svc -n {project}")

    # Routes
    routes = subprocess.getoutput(f"oc get route -n {project}")

    report += f"\nPODS\n------------------\n{pods}\n"
    report += f"\nDEPLOYMENTS\n------------------\n{deployments}\n"
    report += f"\nSERVICES\n------------------\n{services}\n"
    report += f"\nROUTES\n------------------\n{routes}\n"

print(report)

# Mail Configuration
sender = os.environ['MAIL_USERNAME']
password = os.environ['MAIL_PASSWORD']
receiver = os.environ['MAIL_RECEIVER']

msg = MIMEText(report)

msg['Subject'] = 'OpenShift Multi-Project Health Check Report'
msg['From'] = sender
msg['To'] = receiver

# Send Email
server = smtplib.SMTP('smtp.gmail.com', 587)

server.starttls()

server.login(sender, password)

server.send_message(msg)

server.quit()

print("Email Sent Successfully")
