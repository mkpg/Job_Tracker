
from jinja2 import environment
from flask import Flask,render_template,request,redirect,session
import os
from dotenv import load_dotenv
import pg8000
from urllib.parse import urlparse
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()
app = Flask(__name__)
db_url = os.getenv('Neon_DB_Connect')
url = urlparse(db_url)

con = pg8000.dbapi.connect(
    user = url.username,
    password = url.password,
    host=url.hostname,
    port = 5432,
    database=url.path.replace("/","")
    )

curs = con.cursor()
app.secret_key= os.getenv("sessionkey")

# print(con)
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect("/home")
    return redirect("/Login")
        

@app.route('/Register',methods = ["POST","GET"])
def Register():
    if request.method == 'POST':
        name = request.form.get("User_name")
        email = request.form.get("Email")
        p = request.form.get("Password")
        ph_no = request.form.get("Phone_No")
        curs.execute('select email from users where email=%s',(email,))
        row = curs.fetchone()
        
        curs.execute('select phone_no from users where phone_no=%s',(ph_no,))
        phr = curs.fetchone()
        
        if row:
            return render_template("Register.html",message = "Email is already exists")
        elif phr:
            return render_template("Register.html",message= "Phone Number is already exists")
        else:
            if not p :
                return "Password is required"
            else:
                password = generate_password_hash(p)
            

            if not name :
                return "Name is required"
            if not email:
                return "Email is required"

            if not ph_no:
                return "Phone number is required"
            # HERE INSERT
            curs.execute("Insert into users (user_name,email,Password_hash,Phone_No) values(%s,%s,%s,%s)",(name,email,password,ph_no))
            con.commit()

            # FROM THIS IS THE SESSION I MADE
            curs.execute("select user_id from users where user_name = %s",(name,))
            user_id = curs.fetchone()
            user_id = user_id[0]
            session['user_name'] = name
            session['user_id'] = user_id
            return redirect("/") # I RETURNED TO REDIRECT TO THE INDEXPAGE INSTEAD OF HOME

    else:
        return render_template("Register.html")
    


    # the below is working without session details so above is with session from flask

    # if request.method == 'POST':
    #     name = request.form.get("User_name")
    #     email = request.form.get("Email")
    #     password = generate_password_hash(request.form.get("Password"))
    #     ph_no = request.form.get("Phone_No")
    #     curs.execute("Insert into users (user_name,email,Password_hash,Phone_No) values(%s,%s,%s,%s)",(name,email,password,ph_no))
    #     con.commit()
    #     return redirect("/")
    # else:
    #     return render_template("Register.html")
    
@app.route('/Login',methods = ['POST','GET'])
def Login():
    if request.method == 'POST':
        user_name = request.form.get('User_name')
        passwords = request.form.get("Password")
        if not user_name:
            return "Please Enter the User Name"
        elif not passwords:
            return "Please Enter Your Secret"

        curs.execute("select password_hash from users where user_name = %s",(user_name,))
        row = curs.fetchone()
        if row:
            pass_true = check_password_hash(row[0],passwords)
            if pass_true:
                curs.execute("select user_id from users where user_name = %s",(user_name,))
                user_id = curs.fetchone()
                user_id = user_id[0]
                session["user_id"] = user_id
                session['user_name'] = user_name
                return redirect("/")
            else:
                return "Login failed"
        else:
            return "User not found"
    else:
        return render_template("Login.html")



    # the below is working without session details so above is with session from flask


    # if request.method == 'POST':
    #     user_name = request.form.get('User_name')
    #     passwords = request.form.get("Password")
    #     curs.execute("select password_hash from users where user_name = %s",(user_name,))
    #     row = curs.fetchone()
    #     if row:
    #         pass_true = check_password_hash(row[0],passwords)
    #         if pass_true:
    #             return redirect("/")
    #         else:
    #             return "Login failed"
    #     else:
    #         return "User not found"
    # else:
    #     return render_template("Login.html")
        

@app.route('/home')
def home():
    if 'user_id' in session:
        curs.execute("select count(*) from job_applications where user_id = %s;",(session['user_id'],))
        applications = curs.fetchone()[0]
        curs.execute("select count(*) from job_applications where status = 'applied' and user_id = %s;",(session['user_id'],))
        applied = curs.fetchone()[0]
        curs.execute("select count(*) from job_applications where status = 'rejected' and user_id = %s;",(session['user_id'],))
        rejected = curs.fetchone()[0]
        curs.execute("select count(*) from job_applications where status = 'in-progress' and user_id = %s;",(session['user_id'],))
        progress = curs.fetchone()[0]
        curs.execute("select company from job_applications where user_id = %s;",(session['user_id'],))
        company = curs.fetchall()
        curs.execute("select job_id,job_name,company,status,apply_date,expected_date from job_applications where user_id = %s;",(session['user_id'],))
        abc = curs.fetchall()
        return render_template(
            "Home.html",
            applications = applications,
            user_name = session['user_name'],
            applied = applied,
            rejected = rejected,
            progress = progress,
            company = company,
            all_data = abc
        )
    return redirect('/Login')

@app.route('/addjob',methods = ['POST','GET'])
def addjob():
    if 'user_id' in session:    
        if request.method == 'POST' :

            job_n = request.form.get('job_name')
            Comp=request.form.get("Company_name")
            status=request.form.get("status")
            app_date =request.form.get('app_date')
            exp_data = request.form.get('exp_date')
            if job_n == "":
                return "please enter the name of the job"
            elif Comp == "":
                return "please enter the name of the company"
            elif app_date == "":
                return "please enter the date of application"
            elif exp_data == "":
                return "please enter the expected date"
            curs.execute('''insert into job_applications(user_id,job_name,company,status,apply_date,expected_date) 
            values (%s,%s,%s,%s,%s,%s)''',(session['user_id'],job_n,Comp,status,app_date,exp_data))
            con.commit()
            return redirect('/home')
        else:
            return render_template("addjob.html")
    return redirect('/Login')


@app.route('/edit',methods = ["POST",'GET'])
def edit():
    if 'user_id' in session:
        if request.method == "POST":
            job_id = request.form.get('job_id')
            curs.execute("select job_id,job_name,company,status,apply_date,expected_date from job_applications where job_id = %s and user_id = %s;",(job_id,session['user_id']))
            abc = curs.fetchone()
            return render_template("editjob.html",all_data=abc)
        else:
            return redirect('/home')
    else:
        return redirect('/Login')
@app.route("/update",methods = ["POST","GET"])
def update():
    if 'user_id' in session:
        if request.method == 'POST':
            job_n=request.form.get('job_name')
            Comp = request.form.get('Company_name')
            status = request.form.get('status')
            app_date = request.form.get('app_date')
            exp_date = request.form.get('exp_date')
            job_id = request.form.get('job_id')

            if not job_n:
                return "please enter the name of the job"
            elif not Comp :
                return "please enter the name of the company"
            elif not app_date:
                return "please enter the date of application"
            elif not exp_date:
                return "please enter the expected date"
            curs.execute('''update job_applications set job_name = %s, company = %s, status = %s, apply_date = %s, expected_date = %s where job_id = %s and user_id = %s''',(job_n,Comp,status,app_date,exp_date,job_id,session['user_id']))
            con.commit()
            return redirect('/home')
    else:
        return redirect('/Login')

@app.route('/delete',methods = ["POST",'GET'])
def delete():
    if 'user_id' in session:
        if request.method == 'POST':
            job_id = request.form.get("job_id")
            curs.execute("delete from job_applications where job_id=%s and user_id = %s;",(job_id,session['user_id']))
            con.commit()
            return redirect('/home')
        else:
            return render_template("Home.html")
    return redirect('/Login')

@app.route('/profile')
def profile():
    if 'user_id' in session:
        curs.execute("select user_name,email,phone_no from users where user_id = %s;",(session['user_id'],))
        abc = curs.fetchone()
        return render_template("profile.html",user_name = abc[0],email=abc[1],phone=abc[2])
    else:
        return redirect('/Login')


@app.route('/psw',methods = ["POST","GET"])
def psw():
    if 'user_id' in session:
        if request.method == "POST":
            return render_template("psw.html")
        else:
            return render_template("psw.html")
    else:
        return redirect("/Login")

@app.route('/psw_verify',methods=["POST"])
def psw_verify():
    if 'user_id' in session:
        if request.method == "POST":
            curs.execute("select password_hash from users where user_id = %s",(session['user_id'],))
            ps_hash = curs.fetchone()
            ps_hash = ps_hash[0]
            current = request.form.get("Current")
            if check_password_hash(ps_hash,current):
                session["Verified"] = True
                return render_template("psw.html",Verified = session["Verified"])
            else:
                return render_template("psw.html",Verified = False)

            # if Verified:   
            #     np = request.form.get("new_pass")
            #     npv = request.form.get("new_pass_verify")
            #     if np == npv:
            #         newpass = generate_password_hash(np)
            #         curs.execute('update users set password_hash =%s where user_id = %s',(newpass,session['user_id']))
            #         con.commit()
            #         return redirect('/home')
            #     else:
            #         return "new password and password verify are not same"
            # else:
            #     return "wrong password"

        else:
            return redirect("/psw")
    else:
        return redirect("/Login")

@app.route('/logout')
def logout():
    if 'user_id' in session:
        session.clear()
    return redirect('/Login')

@app.route("/psw_update",methods = ["POST"])
def psw_update():
    if 'user_id' in session:
        if request.method == 'POST':
            if "Verified" in session:
                np = request.form.get("new_pass")
                npv = request.form.get("new_pass_verify")
                if not np:
                    return "please enter the new password"
                elif not npv:
                    return "please enter the new password verify"
                elif np == npv:
                    newpass = generate_password_hash(np)
                    curs.execute('update users set password_hash =%s where user_id = %s',(newpass,session['user_id']))
                    con.commit()
                    return redirect('/home')
                else:
                    return "new password and password verify are not same"
            else:
                return redirect("/psw")
        else:
            return redirect("/psw")
    else:
        return redirect("/Login")


if __name__=='__main__':
    app.run(debug=True)

