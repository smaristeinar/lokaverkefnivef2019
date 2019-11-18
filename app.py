from flask import Flask, render_template,session,request,redirect,url_for,flash
import sqlite3





def create_table():
    cursor.execute("CREATE TABLE userinfo(user_name varchar(32) NOT NULL,user_password varchar(32) NOT NULL PRIMARY KEY,user_email varchar(32) NOT NULL)")

def entery(user_name,user_password,user_email):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO userinfo (user_name,user_password,user_email) VALUES (?,?,?)",(user_name,user_password,user_email))
    conn.commit()
    cursor.close()
    conn.close()

def read(name,pswrd):
    succ = 0
    listi = []
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM userinfo")
    data = cursor.fetchall()
    for row in data:
        listi.append(row)
        if row[0] == name and row[1] == pswrd:
            succ = 1
    cursor.close()
    conn.close()
    if "info" not in session:
        session["info"] = listi
    return succ

def read_user_info():
    listi = []
    conn= sqlite3.connect("user.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM userinfo")
    return cursor.fetchall()

def post(post_text, nafn):
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        print(post_text)
        print(nafn)
        cursor.execute("INSERT INTO userposts (user_post,user_name) VALUES (?,?)",(post_text, nafn))
        conn.commit()
        cursor.close()
        conn.close()

def read_posts():
        listi1 = []
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM userposts")
        data = cursor.fetchall()
        for row in data:
            listi1.append(row)
        cursor.close()
        conn.close()
        return listi1

def delete_post(post_id):
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        print("skallakalla")
        cursor.execute("DELETE FROM userposts WHERE post_id = (?)",(post_id))
        conn.commit()
        cursor.close()
        conn.close()

def delete_user(user_id):
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        print("skallakalla")
        cursor.execute("DELETE FROM userinfo WHERE user_password = (?)", (user_id,))
        conn.commit()
        cursor.close()
        conn.close()

app = Flask(__name__)
app.config["SECRET_KEY"]  ="blab"

error = False


@app.route("/")
def index():
    if "user" in session:
        return redirect(url_for("profile"))
    else:
        return render_template("index.html")

@app.route("/login",methods = ["GET","POST"])
def login():
    reg = request.form
    if request.method == "POST":
        nafn = reg.get("name")
        password = reg.get("password")
    if read(nafn,password) == 1:
        session["user"] = password
        session["name"] = nafn
        return redirect(url_for("profile"))
    else:
        return redirect(url_for("index"))

@app.route("/posting", methods = ["GET","POST"])
def posting():
    reg = request.form
    if request.method == "POST":
        text = reg.get("text")
    if "user" in session:
        post(text,session["name"])
        return redirect(url_for("userposts"))
    else:
        return redirect(url_for("index"))

@app.route("/userposts")
def userposts():
    posts = read_posts()
    return render_template("userpost.html",posts = posts)



@app.route("/register",methods=["GET","POST"])
def register():
    global error
    req = request.form
    if request.method == "POST":
        nafn = req.get("name")
        email = req.get("email")
        password = req.get("password")
    if read(nafn, password) == 0:
        entery(nafn, password, email)
        print("uplisingar eru ok set i kerfið")
        return redirect(url_for("profile"))
    else:
        print("upplisingar ekki ok set ekki i kerfið")
        flash("þessar uplýsingar standast ekki")
        return redirect(url_for("index"))

    return render_template("index.html")

@app.route("/profile")
def profile():
    if "user" in session:
        print(session["info"])
        posts = read_posts()
        return render_template("profile.html", posts = posts)
    else:
        return redirect(url_for("index"))
@app.route("/update/<id>" , methods = ["GET","POST"])
def Update(id):
        reg = request.form
        if request.method == "POST":
            text = reg.get("text")
            delete_post(id)
            post(text, session["name"])
        return redirect(url_for("profile"))

@app.route("/delete/<id>")
def delete(id):
    print(id)
    for i in read_posts():
        if i[0] == int(id) and i[2] == session["name"] or i[0] == int(id) and session["name"] == "smari" :
            print("bingo!!!!!!!!!!!!!!!!!!!")
            delete_post(id)
    return redirect(url_for("profile"))

@app.route("/deleteuser/<id>")
def deleteuser(id):
    print("bingo1")
    if session["name"] == "smari":
        delete_user(id)
    return redirect(url_for("profile"))

@app.route("/admin")
def admin():
    if session["name"] == "smari" and session["user"]=="123123":
        posts = read_posts()
        return render_template("admin.html", posts = posts)
    else:
        return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.pop("user")
    session.pop("info")
    return redirect(url_for("index"))



@app.errorhandler(404)
def page_not_found():
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run()
    app.run(debug=True, use_reloader = True)
