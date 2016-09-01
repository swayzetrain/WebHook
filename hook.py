from flask import jsonify, Blueprint, request, Response, render_template, redirect, Flask 
from datetime import datetime, timezone
from dateutil import tz
import os 
from subprocess import Popen, PIPE
from git import Repo

port = os.getenv('PORT', '8080') 
app = Flask(__name__, static_url_path='') 
app.config['WTF_CSRF_ENABLED'] = False 

@app.route("/webhook/push/scrapeit", 
methods=['POST']) 
def scrapeitPush():
    ## Create the version file
    request_data = request.get_json()
    version_message = request_data['head_commit']['message']
    version_author = request_data['head_commit']['author']['name']
    version_timestamp = request_data['head_commit']['timestamp']
    f = open('/home/swayzetrain/WebHook/versions/scrapeit/scrapeitversion.txt','w+')
    f.write(version_message)
    f.write('\n')
    f.write(version_author)
    f.write('\n')
    f.write(version_timestamp)
    f.close()
    
    ## Delete the old Repo
    delete = Popen(["rm", "-r", "/home/swayzetrain/scrapeit"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    (deleteoutput, deleteerror) = delete.communicate()
    #print("Delete output: ", deleteoutput)
    #print("Delete error :", deleteerror)    
    #print("Delete Complete")
    
    ## Clone the updated Repo
    Repo.clone_from("https://github.com/mtlevine0/scrapeit","/home/swayzetrain/scrapeit")
    #print("Clone Done")
    
    ## Copy the Properties File
    copy = Popen(["cp", "/home/swayzetrain/scrapeit_properties.txt", "/home/swayzetrain/scrapeit/properties.txt"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    (copyoutput, copyerror) = copy.communicate()
    #print("Copy output: ", copyoutput)
    #print("Copy error :", copyerror)    
    #print("Copy complete")
    
    ## Restart the Service
    service = "scrapeit"
    restart = Popen(["service", service, "restart"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    (restartoutput, restarterror) = restart.communicate()
    #print("Restart output: ", restartoutput)
    #print("Restart error :", restarterror)
    
    
    return("Restart Complete")

@app.route("/webhook/push/scrapeit",
methods=['GET'])
def scrapeitVersion():
    f = open('/home/swayzetrain/WebHook/versions/scrapeit/scrapeitversion.txt', 'r')
    version_message = f.readline()
    version_author = f.readline()
    version_timestamp = f.readline()
    f.close()
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('America/New_York')
    #version_timestamp = version_timestamp.rstrip('Z')
    utc = datetime.strptime(version_timestamp, '%Y-%m-%dT%H:%M:%SZ')
    utc = utc.replace(tzinfo=from_zone)
    version_timeeast = utc.astimezone(to_zone)
    returnString = ('Author: %s <br> Timestamp: %s <br> Version Message: %s')%( version_author, version_timeeast, version_message)

    return (returnString)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port), threaded=True)
