
from flask import Flask, render_template, request , session 
from flask_mysqldb import MySQL



app = Flask(__name__)



app.secret_key = 'Votify_key@123'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'your_db_password'
app.config['MYSQL_DB'] = 'vote_data'


mysql = MySQL(app)


@app.route('/')
def home():                       # --------- THIS WILL WORK PROPERLY ✅✅✅✅✅✅✅
    return render_template('index.html')



@app.route('/login' , methods = ['GET' , 'POST'])   # --------- THIS WILL WORK PROPERLY ✅✅✅✅✅✅✅
def login():
    
    if request.method == 'POST':   # When the user input the data in the login form 
         
        name = request.form["name"]
        age = request.form['age']
        aadhaar = request.form['aadhaar']
        mobile_no  = request.form['mobile']

        session['aadhaar'] = aadhaar

        #--------------Make a connection between the page and database --------------------------------------------------
        cur = mysql.connection.cursor()

        cur.execute('SELECT aadhaar FROM vote_details WHERE aadhaar = %s' , (aadhaar,))
        check_aadhar = cur.fetchone()

        if not check_aadhar : 

            cur.execute('INSERT INTO vote_details (Name , Age , Aadhaar , Mobile_no) VALUES (%s , %s , %s , %s)' , (name , age , aadhaar , mobile_no )) # ye line tb execute krni krni chaaiye jb yser register na ho 

            # Save the changes which is performed
            mysql.connection.commit()

            # Close the database after the work --------------------------------------------------------
            cur.close()
            return render_template('vote.html')
        
        else : 
            return render_template('thanks.html')

    
    else:    # WHen the try to access the Admin Panel


        return render_template('login.html')
    


@app.route('/vote')    # --------- THIS WILL WORK PROPERLY ✅✅✅✅✅✅✅
def vote():
    # Vote Page
    return render_template('vote.html')



@app.route('/submit_vote', methods=['POST']) #-------------Working on it💀💀💀💀💀💀💀💀💀 on (GET) -----------------------------------------------------------------
def submit_vote():
    cur = mysql.connection.cursor()

    candidate = request.form['vote'] # 'vote' matches the input name
    aadhaar = session.get('aadhaar')   # assuming your form has this field
    cur.execute('INSERT INTO vote_details (Aadhaar, selected_leader) VALUES (%s, %s) ON DUPLICATE KEY UPDATE selected_leader = %s', (aadhaar, candidate, candidate))
    # print(f"Vote received for: {candidate}")  # Optional: log it

    mysql.connection.commit()
    cur.close()
    session.pop('aadhaar', None)


    return render_template('thanks.html')




@app.route('/admin_login')
def admin_login():
        
    return render_template('admin_login.html')
    




@app.route('/admin', methods=['POST'])
def admin():

    # ------------------ Yha p credentials match waala kaam hora h -------------------------------------
    user_id = "Admin@123"
    password = "Votify@123"
    user_key = 123456

    input_id = request.form['username']
    input_pass = request.form['password']
    
    # try:
    input_key = int(request.form['security-key'])
    # except ValueError:
    #     return render_template('index.html')



    if input_id == user_id and input_pass == password and input_key == user_key:

        #---------------------------------- Count krne ka code yah pr likha jaayega ----------------------------------------------

        cur = mysql.connection.cursor()

        # cur.execute('SELECT selected_leader AS leader_name COUNT(*) AS total_votes FROM vote_details GROUP BY selected_leader ORDER BY total_votes DESC')
        # cur.execute('SELECT selected_leader AS leader_name , COUNT(*) AS total_votes FROM vote_details WHERE selected_leader = "modi"')
        # leader_modi = cur.fetchone() 

        # cur.execute('SELECT selected_leader AS leader_name  , COUNT(*) AS total_votes FROM vote_details WHERE selected_leader = "rahul"')
        # leader_rahul = cur.fetchone() 

        # cur.execute('SELECT selected_leader AS leader_name ,  COUNT(*) AS total_votes FROM vote_details WHERE selected_leader = "mamta"')
        # leader_mamta = cur.fetchone() 

        # cur.execute('SELECT selected_leader AS leader_name , COUNT(*) AS total_votes FROM vote_details WHERE selected_leader = "nota"')
        # leader_nota = cur.fetchone() 
        cur.execute("""
            SELECT selected_leader, COUNT(*) AS votes
            FROM vote_details
            WHERE selected_leader IS NOT NULL
            GROUP BY selected_leader
        """)
        results = cur.fetchall()  # [('modi', 10), ('rahul', 5), ...]

        total_votes = sum(row[1] for row in results) if results else 1  # avoid division by zero

        vote_percentages = [
            {'leader': row[0], 'percentage': round((row[1] / total_votes) * 100, 1)}
            for row in results
        ]

        cur.close()
        return render_template('admin.html', vote_percentages=vote_percentages)

             

        # cur.close()
        # # conn.close()

        # return render_template('admin.html', vote_summary=vote_summary)


    else:
        return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True, port=8000)




#E:\CODES\New_project\templates\vote.html E:\CODES\New_project\venv\app.py

# ------------------Check the user input as is not the previous voter -------------------------------------------------------
#  cur = mysql.connection.cursor()
        
#         # 1. CHECK IF USER EXISTS
#         cur.execute("SELECT * FROM users WHERE email = %s", [user_email])
#         existing_user = cur.fetchone() # Fetch one row

#         if existing_user:
#             # 2a. USER EXISTS: REDIRECT TO THANKS PAGE
#             flash('You have already submitted your details. Thank you!', 'info')
#             cur.close()
#             return redirect(url_for('thanks'))
#         else:
#             # 2b. NEW USER: SAVE AND REDIRECT TO VOTE PAGE
#             try:
#                 # Insert the new user into the database
#                 cur.execute("INSERT INTO users (email, name) VALUES (%s, %s)", 
#                             (user_email, user_name))
#                 mysql.connection.commit()
#                 flash('Welcome! Please cast your vote now.', 'success')
#                 cur.close()
#                 return redirect(url_for('vote'))



