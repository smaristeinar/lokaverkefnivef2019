import sqlite3

#create table 0601992809_verkefn7.users(
# user_name varchar(32) NOT NULL,
# user_password varchar(32) NOT NULL PRIMARY KEY,
# user_email varchar(32) NOT NULL
# );


conn = sqlite3.connect("users.db")
cursor = conn.cursor()
def drop_table():
    cursor.execute("DROP TABLE userposts")
def create_table():
    cursor.execute("CREATE TABLE userposts(post_id INTEGER NOT NULL PRIMARY KEY,user_post text NOT NULL,user_name varchar(32) NOT NULL)")
def update_table():
    cursor.execute("UPDATE userposts SET user_post = sss WHERE post_id = 1")
def delete_post():
    cursor.execute("DELETE FROM userposts WHERE post_id = 1")
def seletall():
    cursor.execute("SELECT * FROM userposts")
    data = cursor.fetchall()
    for row in data:
        print(row)
#def create_table():
#    cursor.execute("CREATE TABLE userinfo(user_name varchar(32) NOT NULL,user_password varchar(32) NOT NULL PRIMARY KEY,user_email varchar(32) NOT NULL)")

#def entery(user_name,user_password,user_email):
#    cursor.execute("INSERT INTO userinfo (user_name,user_password,user_email) VALUES (?,?,?)",(user_name,user_password,user_email))
#    conn.commit()
sucsess = 0
#def read():
#    succ = 0
#    conn = sqlite3.connect("users.db")
#    cursor = conn.cursor()
#    cursor.execute("SELECT * FROM userinfo")
#    data = cursor.fetchall()
#    for row in date:
#        if row[0] == "smari":
#            succ = 1
#    cursor.close()
#    conn.close()
#    return succ


#entery("smari", "123123", "smarikul@hotmail.com")
seletall()
delete_post()
seletall()
cursor.close()
conn.close()
