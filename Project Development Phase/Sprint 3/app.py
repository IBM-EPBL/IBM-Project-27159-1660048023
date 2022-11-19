import ibm_db
from flask import Flask, render_template, request,session,url_for


app = Flask(__name__)
config ={

}

conn=ibm_db.pconnect("DATABASE=bludb;HOSTNAME=125f9f61-9715-46f9-9399-c8177b21803b.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;\
            PORT=30426;PROTOCOL=TCPIP;UID=rzy37188;PWD=ZrxvZT8bygGK2hcV;SECURITY=SSL;SSLServiceCertificate=DigiCertGlobalRootCA.crt", "", "")

print(conn)
print("connected tot the database")




@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

@app.route('/forgot')
def forgot():
    return render_template('forgotten-password.html')


@app.route('/')
def dash():
    return render_template('dashboard.html')

@app.route('/job_board')
def job_board():
    return render_template('job_board.html')

@app.route('/job_post')
def job_post():
    return render_template('job_post.html')

@app.route('/view_form')
def view_form():
    return render_template('view_form.html')

@app.route('/fill_form')
def fill_form():
    return render_template('fill_form.html')




@app.route('/profiles', methods=["POST", "GET"])
def profile():
    
        return render_template('update_profile.html',)
        #post =post



@app.route('/s_signup', methods=['POST','GET'])
def s_signup():
    
      return render_template('seeker_signup.html')
         
        
@app.route('/r_signup', methods=['POST','GET'])
def r_signup():
    #if request.method == 'POST':
        # conn = connection()

    
            return render_template('recruiter_signup.html')
        

@app.route('/s_login', methods=['POST','GET'])
def s_login():
     #if request.method == 'POST':
       
            return render_template('seeker_login.html')

@app.route('/r_login', methods=['POST','GET'])
def r_login():
    # if request.method == 'POST':
       # conn =connection()
      
            return render_template('recruiter_login.html')

@app.route('/logout')
def logout():
    #session.pop('loggedin', None)
    #session.pop('username', None)
    return redirect(url_for('login'))

      

if __name__=='__main__':
    app.config['SESSION_TYPE']= 'filesystem'
    app.run(debug=True)

       