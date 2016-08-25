from flask import jsonify, Blueprint, request, Response, render_template, redirect, Flask 
import os 
from subprocess import Popen, PIPE
from git import Repo

port = os.getenv('PORT', '8080') 
app = Flask(__name__, static_url_path='') 
app.config['WTF_CSRF_ENABLED'] = False 

@app.route("/webhook/push/scrapeit", 
methods=['GET']) 
def scrapeitPush():
    delete = Popen(["rm", "-r", "/home/swayzetrain/scrapeit"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    (deleteoutput, deleteerror) = delete.communicate()
    print("Delete output: ", deleteoutput)
    print("Delete error :", deleteerror)    
    print("Delete Complete")
    Repo.clone_from("https://github.com/mtlevine0/scrapeit","/home/swayzetrain/scrapeit")
    print("Clone Done")
    copy = Popen(["cp", "/home/swayzetrain/scrapeit_properties.txt", "/home/swayzetrain/scrapeit/properties.txt"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    (copyoutput, copyerror) = copy.communicate()
    print("Copy output: ", copyoutput)
    print("Copy error :", copyerror)    
    print("Copy complete")
    service = "scrapeit"
    restart = Popen(["service", service, "restart"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    (restartoutput, restarterror) = restart.communicate()
    print("Restart output: ", restartoutput)
    print("Restart error :", restarterror)
    return("Restart Complete")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port), threaded=True)
