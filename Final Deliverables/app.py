from flask import Flask,request,render_template,redirect,flash,url_for,session
from flask_bootstrap import Bootstrap
import ibm_db





app = Flask(__name__)
Bootstrap(app)

app.secret_key='aSGSGFSGsd'


conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=125f9f61-9715-46f9-9399-c8177b21803b.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30426;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=rzy37188;PWD=ZrxvZT8bygGK2hcV;", "", "")


@app.route('/')
def home():
   
    return render_template("index.html")



@app.route('/features')
def features():
   
    return render_template("features.html")
@app.route('/integrations')
def integrations():
   
    return render_template("integrations.html")


@app.route('/login',methods=["POST","GET"])
def login():
   if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        sql = "SELECT COUNT(*) FROM users WHERE EMAIL=? AND PASSWORD=?"
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt, 1, email)
        ibm_db.bind_param(stmt, 2, password)
        ibm_db.execute(stmt)
        res = ibm_db.fetch_assoc(stmt)
        if res['1'] == 1:
            session['loggedin'] = True
            session['email'] = email
            return render_template('joblist.html')
        else:  #flash("email/ Password isincorrect! ")
             return render_template('login.html')
           
   else:
         return render_template('login.html') 
       

@app.route('/corporate_login',methods=["POST","GET"])
def corporate_login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        sql = "SELECT COUNT(*) FROM users WHERE EMAIL=? AND PASSWORD=?"
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt, 1, email)
        ibm_db.bind_param(stmt, 2, password)
        ibm_db.execute(stmt)
        res = ibm_db.fetch_assoc(stmt)
        if res['1'] == 1:
            session['loggedin'] = True
            session['email'] = email
            return render_template('postjob.html')
        else:  #flash("email/ Password isincorrect! ")
            return render_template('corporate_login.html')  
    else:
         return render_template('corporate_login.html')  
                    
    


@app.route('/register',methods=["POST","GET"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        
        sql1 = "INSERT INTO USERS VALUES (?,?,?)"
        stmt1 = ibm_db.prepare(conn,sql1)
        ibm_db.bind_param(stmt1,1,name)
        ibm_db.bind_param(stmt1, 2, email)
        ibm_db.bind_param(stmt1, 3, password)
        ibm_db.execute(stmt1)
        print("inserted")
        return redirect(url_for('joblist'))
    return render_template("Register.html")

           
               

@app.route('/postjob',methods=["POST","GET"])
def postjob():
    if request.method == "POST":
        jobtitle = request.form.get('jt')
        jobdescription = request.form.get('jd')
        skill1 = request.form.get('skill-1')
        skill2 = request.form.get('skill-2')
        skill3 = request.form.get('skill-3')
        Date = request.form.get('date')
        Companyname = request.form.get('Company-name')
        CompanyEmail = request.form.get('company-email')
        valve = 10
        insert_sql = "INSERT INTO JOBLIST VALUES (?,?,?,?,?,?,?,?)"
        prep_stmt = ibm_db.prepare(conn, insert_sql)
        ibm_db.bind_param(prep_stmt, 1, jobtitle)
        ibm_db.bind_param(prep_stmt, 2, jobdescription)
        ibm_db.bind_param(prep_stmt, 3, skill1)
        ibm_db.bind_param(prep_stmt, 4, skill2)
        ibm_db.bind_param(prep_stmt, 5, skill3)
        ibm_db.bind_param(prep_stmt, 6, Date)
        ibm_db.bind_param(prep_stmt, 7, Companyname)
        ibm_db.bind_param(prep_stmt, 8, CompanyEmail)
        ibm_db.execute(prep_stmt)
        return redirect(url_for('joblist'))
    else:
        return 'wrong credentials'

@app.route('/joblist',methods=["POST","GET"])
def joblist():
    if request.method == "POST":
        search_key =  request.form.get('search-bar')
        sql = "SELECT * FROM JOBLIST"
        stmt = ibm_db.exec_immediate(conn, sql)
        dictionary = ibm_db.fetch_both(stmt)
        jt_list = []
        jd_list = []
        companies = []
        lastdate = []
        while dictionary != False:
            if search_key == dictionary['SKILL1'] or search_key == dictionary['SKILL2'] or search_key == dictionary['SKILL3'] :
                jt_list.append(dictionary['JOBTITLE'])
                jd_list.append(dictionary['JOBDES'])
                companies.append(dictionary['COMPANYNAME'])
                dictionary = ibm_db.fetch_both(stmt)
            else:
                dictionary = ibm_db.fetch_both(stmt)
        lent = len(jd_list)
        no = 0
        return render_template("joblist.html", jtr=jt_list, jdr=jd_list, len=lent,cn=companies)
    else:
        sql = "SELECT * FROM JOBLIST"
        stmt = ibm_db.exec_immediate(conn, sql)
        dictionary = ibm_db.fetch_both(stmt)
        jt_list = []
        jd_list = []
        companies = []
        while dictionary != False:
            jt_list.append(dictionary['JOBTITLE'])
            jd_list.append(dictionary['JOBDES'])
            companies.append(dictionary['COMPANYNAME'])
            dictionary = ibm_db.fetch_both(stmt)
        lent = len(jd_list)
        no = 0
        return render_template("joblist.html",jtr=jt_list,jdr=jd_list,len = lent,cn=companies)


@app.route('/applyjob', methods = ['GET', 'POST'])
def applyjob():
  
       return render_template('applyjob.html')

        


           
        
      
        
     
if __name__ == '__main__':
    app.secret_key = "secret123"
    #when the debug mode is on, we do not need to restart the server again and again
    app.run(debug=True)
