from flask import Flask,request,render_template,redirect,flash,url_for,session
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_mail import Message
import ibm_db
import ibm_boto3
from ibm_botocore.client import Config,ClientError
import json







COS_ENDPOINT ='https://s3.jp-tok.cloud-object-storage.appdomain.cloud'
COS_API_KEY_ID="N4Il1nx1AhrgMhoAtXgkvC6i4DZzWYE428HMpQSNByAh"
COS_INSTANCE_CRN="crn:v1:bluemix:public:iam-identity::a/31fa813cf7134a2b87f66465bde60656::serviceid:ServiceId-8d6fd9a6-0638-4c58-9270-cc40705c2385"

app = Flask(__name__)
Bootstrap(app)
mail = Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'jobhunter52501@gmail.com'
app.config['MAIL_PASSWORD'] = 'Mdu@12345'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


cos = ibm_boto3.resource("s3",ibm_api_key_id=COS_API_KEY_ID,ibm_service_instance_id=COS_INSTANCE_CRN,config=Config(signature_version="oauth"),endpoint_url=COS_ENDPOINT)

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=125f9f61-9715-46f9-9399-c8177b21803b.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30426;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=rzy37188;PWD=ZrxvZT8bygGK2hcV;", "", "")

def get_bucket_contents(bucket_name):
    print("Retrieving bucket contents from: {0}".format(bucket_name))
    try:
        files = cos.Bucket(bucket_name).objects.all()
        files_names = []
        for file in files:
            files_names.append(file.key)
            print("Item: {0} ({1} bytes).".format(file.key, file.size))
        return files_names
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to retrieve bucket contents: {0}".format(e))

@app.route('/')
def home():
   
    return render_template("index.html")

@app.route('/contacts')
def contacts():
   
    return render_template("contacts.html")
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
#--------------------------------Bucket storage------------------------------------------------------------#
def multi_part_upload(bucket_name, item_name,file_path):
    try:
        print("Starting file transfer for {0} to bucket: {1}\n".format(item_name, bucket_name))
        part_size = 1024 * 1024 * 5
        file_threshold = 1024 * 1024 * 15
        transfer_config = ibm_boto3.s3.transfer.TransferConfig(
            multipart_threshold=file_threshold,
            multipart_chunksize=part_size
        )
        print("out")
        with open(file_path, "rb") as file_data:
            cos.Object(bucket_name, item_name).upload_fileobj(
                Fileobj=file_data,
                Config=transfer_config
            )

        print("Transfer for {0} Complete!\n".format(item_name))
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to complete multi-part upload: {0}".format(e))

@app.route('/applyjob', methods = ['GET', 'POST'])
def applyjob():
  
       return render_template('applyjob.html')

        

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
                    
           
        
      
        
     



if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='0.0.0.0',port=8080,debug=True)
