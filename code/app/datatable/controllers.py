from flask import Blueprint,Flask,render_template,request,redirect,url_for,flash,session,jsonify,make_response,abort
from app.datatable.models import Datatable
from app.login.models import User
from bs4 import BeautifulSoup
from selenium import webdriver
from pyvirtualdisplay import Display
import requests
from app import db
from io import StringIO
import csv
import time

mod_datatable = Blueprint('mod_datatable',__name__,template_folder='templates')

    
@mod_datatable.route('/data', methods=['POST'])
def insert():
    if 'user_id' not in session:
        return redirect('/login')
    username = request.form['username1']
    username = username.strip()
    if len(username) != 11:
        flash('Not a valid NCT_number','danger')
        r =  make_response(render_template('indexAdmin.html',requests=User.query.filter_by(userid = int(session['user_id'])).first()))
        return r
    else:
        url ="https://clinicaltrials.gov/ct2/results?cond=&term="+username+"%09&cntry1=&state1=&Search=Search&recrs=a&recrs=b"
        display = Display(visible=0, size=(800, 600))
        display.start()
        browser = webdriver.Firefox()
        browser.get(url)
        html=browser.page_source    
        soup = BeautifulSoup(html,"lxml")
        tag = soup.find_all('table')[0]
        tbody = tag.find('tbody')
        rows = tbody.find_all('tr')
        for tr in rows:
            cols = tr.find_all('td')
            status = cols[2].text
            study_title = cols[3].text
            condition = cols[4].text
            intervention = cols[5].text
            location = cols[6].text
            # print(status)
            data1 = Datatable(username,status,study_title,condition,intervention,location);
            browser.quit()
            display.stop()
            db.session.add(data1)
            try:
                db.session.commit() 
                flash('Data inserted','success')
                r =  make_response(render_template('indexAdmin.html',requests=User.query.filter_by(userid = int(session['user_id'])).first()))
                return r
            except Exception as e:
                db.session.rollback()
                flash('NCT_number already exists','danger')
                r =  make_response(render_template('indexAdmin.html',requests=User.query.filter_by(userid = int(session['user_id'])).first()))
                return r                        
                 
@mod_datatable.route('/display')
def display():
    if 'user_id' not in session:
        return redirect('/login')
    query=Datatable.query.all()
    r = make_response(render_template('display.html',requests=query,details=User.query.filter_by(userid = int(session['user_id'])).first()))
    return r

@mod_datatable.route('/datatable/search',methods=["POST"])
def search1():
    if 'user_id' not in session:
        return redirect('/login')
    searchval=request.form['data']
    value = request.form['searchvalue']
    if searchval=='NCTNumber':
        query=Datatable.query.filter(Datatable.NCT_number.like("%"+value+"%")).all()
        r = make_response(render_template('display.html',requests = query,details=User.query.filter_by(userid = int(session['user_id'])).first()))
        return r
    elif searchval=='Location':
        query=Datatable.query.filter(Datatable.Location.like("%"+value+"%")).all()
        r = make_response(render_template('display.html',requests = query,details=User.query.filter_by(userid = int(session['user_id'])).first()))
        return r
    elif searchval=='Condition':
        query=Datatable.query.filter(Datatable.Condition.like("%"+value+"%")).all()
        r = make_response(render_template('display.html',requests = query,details=User.query.filter_by(userid = int(session['user_id'])).first()))
        return r
    elif searchval=='Status':
        if value.find("Not")!=-1:
            query=Datatable.query.filter(Datatable.Status.like("Not%")).all()
        else:
            query=Datatable.query.filter(Datatable.Status.like(value+"%")).all()
        r = make_response(render_template('display.html',requests = query,details=User.query.filter_by(userid = int(session['user_id'])).first()))
        return r
    else:
        r = make_response(render_template('indexAdmin.html',requests=User.query.filter_by(userid = int(session['user_id'])).first()))
        return r    

@mod_datatable.route('/datatable/download',methods=["POST"])
def download():
    if 'user_id' not in session:
        return redirect('/login')
    searchval=request.form['data']
    value = request.form['searchvalue']
    if searchval=='NCTNumber':
        query=Datatable.query.filter(Datatable.NCT_number.like("%"+value+"%")).all()
    elif searchval=='Location':
        query=Datatable.query.filter(Datatable.Location.like("%"+value+"%")).all()
    elif searchval=='Condition':
        query=Datatable.query.filter(Datatable.Condition.like("%"+value+"%")).all()
    elif searchval=='Status':
        if value.find("Not")!=-1:
            query=Datatable.query.filter(Datatable.Status.like("Not%")).all()
        else:
            query=Datatable.query.filter(Datatable.Status.like(value+"%")).all()
    else:
        query = ''

    check = 1
    if len(query)==0:
        check=0
    if check == 0:
        flash('No results exist for Search Query','danger')
        r = make_response(render_template('download.html',requests=User.query.filter_by(userid = int(session['user_id'])).first()))
        return r
    
    flash('downloaded successfully','success')
    ans=[]
    temp=['NCT Number','Status','Study title','Condition','Intervention','Location']
    ans.append(temp)
    for row in query:
        val=[]
        val.append(str(row.NCT_number))
        val.append(str(row.Status))
        val.append(str(row.Study_title))
        val.append(str(row.Condition))
        val.append(str(row.Intervention))
        val.append(str(row.Location))
        ans.append(val)

    si = StringIO()
    cw = csv.writer(si)
    cw.writerows(ans)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@mod_datatable.route('/download',methods=["GET"])
def searchdl():
    if 'user_id' not in session:
        return redirect('/login')
    r = make_response(render_template('download.html',requests=User.query.filter_by(userid = int(session['user_id'])).first()))
    return r


@mod_datatable.route('/view',methods=["GET"])
def searchview():
    if 'user_id' not in session:
        return redirect('/login')
    r = make_response(render_template('view.html',requests=User.query.filter_by(userid = int(session['user_id'])).first()))
    return r

