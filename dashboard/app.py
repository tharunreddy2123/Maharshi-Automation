from flask import Flask, render_template
import subprocess

app = Flask(__name__)

def run(cmd):
    return subprocess.getoutput(cmd)

@app.route("/")
def home():

    pods = run("oc get pods")
    jobs = run("oc get jobs")
    cronjobs = run("oc get cronjob")

    return f"""
    <h1>OpenShift Health Dashboard</h1>

    <h2>CronJobs</h2>
    <pre>{cronjobs}</pre>

    <h2>Jobs</h2>
    <pre>{jobs}</pre>

    <h2>Pods</h2>
    <pre>{pods}</pre>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)