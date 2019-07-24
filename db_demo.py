from flask import Flask, redirect, url_for, render_template, session, request
import requests
import requests
from multiprocessing.pool import ThreadPool
import os

import json
import urllib
app = Flask(__name__)
app.secret_key= os.urandom(123)
@app.route('/',methods=["GET","POST"])
def login():
    error=""
    if request.method=="POST":
        session['user'] = request.form["nm"]
        pswrd = request.form["password"]
        verify= requests.get('https://api.github.com/user', auth=(session['user'],pswrd))
        if(verify.status_code==200):
            return redirect(url_for("main"))
        else:
            error="Invalid Credentials"
            return render_template("login.html",error=error)
    return render_template("login.html",error=error)
@app.route('/main')
def main():
    count=1
    namelist=[]
    forklist=[]
    watcherlist=[]
    starlist=[]
    sizelist=[]
    if "user" in session:
        user= session['user']
        x1= requests.get('https://api.github.com/users/'+session['user'])
        y1= x1.json()
        # return str(y1)
        n = y1["name"]
        img = y1["avatar_url"]
        bio= y1["bio"]
        x2= requests.get('https://api.github.com/users/'+session['user']+'/followers')
        y2= x2.json()
        z2= len(y2)
        x3 = requests.get('https://api.github.com/users/' + session['user'] + '/following')
        y3 = x3.json()
        z3 = len(y3)
        info= requests.get('https://api.github.com/users/'+session['user']+'/repos')
        info1= info.json()
        for i in info1:
            count=count+1
            namelist.append(i["name"])
            forklist.append(i["forks"])
            watcherlist.append(i["watchers"])
            starlist.append(i["stargazers_count"])
            sizelist.append(i["size"])
        return render_template("main.html",n=n,z2=z2,z3=z3,namelist=namelist,forklist=forklist,watcherlist=watcherlist,
                               starlist=starlist,sizelist=sizelist,count=count,img=img,bio=bio)
    else:
        return redirect(url_for("login"))
@app.route("/graph")
def graph():
    if "user" in session:
        namelist=[]
        watcherlist=[]
        info = requests.get('https://api.github.com/users/' + session['user'] + '/repos')
        info1 = info.json()
        for i in info1:
            namelist.append(i["name"])
            watcherlist.append(i["watchers"])
        return render_template("graph.html",namelist=namelist,watcherlist=watcherlist)
    else:
        return redirect(url_for("login"))
@app.route("/logout")
def logout():
    if "user" in session:
        session.pop("user",None)
        return redirect(url_for("login"))
    else:
        return "<p>You are already logged out</p>"

if __name__ == '__main__':
    app.run(debug=True)
