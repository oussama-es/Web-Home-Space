from model import Prof
from flask import(
    Flask,
    request,
    render_template,
    redirect,
    session,
    url_for,

)
from datetime import datetime
from service import DepartementService
import hashlib
app=Flask(__name__)

def generate_key(login):
    return hashlib.md5(str(login).encode('utf-8')).hexdigest()
app.secret_key='1234'
@app.route('/')
def index():
    return render_template('login.html')
@app.route('/login',methods=['POST'])
def login():
    login=request.form['login']
    pwd=request.form['password']
  
    if (login=='esisa' or login=='esima') and pwd=='1234':
        app.secret_key=generate_key(login)
        response=app.make_response(render_template('app.html'))
        session['user_id']=login
        response.set_cookie('access_time',str(datetime.now()))
        
        return response
    else:
        return render_template('login.html',error_auth='login or password incorrect')
@app.route('/logout')
def logout():
    
    session.pop('user_id',None)
    return redirect(url_for('index'))
@app.route('/addprof',methods=['POST'])
def add():
    
    if 'user_id' in session : 
        prof=Prof(request.form['prof_name'],request.form['prof_email'])
        results=service_dep.addProfToDepartement(int(request.form['dep_id']),prof)
        print(results)
        if results == True :
                return render_template('app.html')
        else :
                return render_template('add_prof.html',error_addprof=results)
    else :
        return redirect('/')
@app.route('/departements/<name>')
def listDepartementByName(name:str):
    if 'user_id' in session :
        profs=service_dep.ListDepartementByName(name)
        return render_template('departement.html',name=name,profs=profs)
    else :
        return redirect('/')
@app.route('/departements')
def listDepartements():
    if 'user_id' in session :
        return service_dep.listDepartements()
        #return render_template('departement.html',name=name,profs=profs)
    else :
        return redirect('/')
@app.route('/addview')
def addview():
    return render_template('add_prof.html')
@app.errorhandler(Exception)
def error(exception):
    return render_template('error.html',error=
     {
        "ip":request.remote_addr,
        "method":request.method,
        "error" :'sorry im here '
    })
if __name__=='__main__':
    service_dep=DepartementService()
    app.run(host="0.0.0.0",port=9090,debug=True)