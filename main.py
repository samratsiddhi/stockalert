from flask import Flask,redirect,url_for,request,render_template,flash
import psycopg2 as ps
import yfinance as yf
import re

app = Flask(__name__)
app.secret_key = "12345"

@app.route("/", methods = ['GET', 'POST'])
def home():
    if request.method == "POST":
        info = {
            'symbol' : request.form['symbol'].upper(),
            'contact_type' : request.form['contact_type'],
            'contact_info' : request.form['contact_info'],
            'upper' : request.form['upper'],
            'lower' : request.form['lower'],
            'frequency' : request.form['frequency']
        }
        valid  = validate_data(info)
        if valid == True: #if form data is valid
            conn, cur = connect_to_db()
            if conn != 0: #if connection successful
                insert = insert_info(info,cur)
                conn.close()
                if insert == 'success': #if insert successful
                    flash('You were successfully subscribed to ' + info['symbol'])
                    return redirect(url_for('home'))
                else: #if insert unsuccessful
                    flash('Error occure' +insert)
                    return redirect(url_for('home'))
            else:#if connection unsuccessful
                flash("Cannot connect to db try later")
                return redirect(url_for('home'))               
        else:#if form data is invalid
            return redirect(url_for('home'))
    else:
        return render_template('stockalert.html')


# connection to database
def connect_to_db():
    try:
        conn = ps.connect('host=127.0.0.1  \
                      dbname= stockalert \
                      user = postgres  \
                      password = 1234'
                      )
        conn.set_session(autocommit=True)
        cur = conn.cursor()
        return conn,cur
    except ps.Error as e:
        return 0,0

# validating form data and inserting data into database
def insert_info(info,cur):
    # insert data into database
    try:
        cur.execute("INSERT INTO stock_subscriber (symbol,contact_type,contact_info,upper,lower,frequency) values(%s,%s,%s,%s,%s,%s)",(info['symbol'],info['contact_type'],info['contact_info'],info['upper'],info['lower'],info['frequency']))
        result = "success"
    except ps.Error as e:
        result = e
    return result
    
# validate form data  
def validate_data(info):
    ticker = yf.Ticker(info['symbol'])
    # validating the given stock symbol
    try:
        stock = ticker.info
    except:
        valid = False
        flash("Cannot get info of," + info['symbol'] +" it probably does not exist")
        
    if info['upper'] < info['lower']:
        valid = False
        flash("The upper limit has to be greater than lower limit")
    
    
    if info['contact_type'] == 'e':
        email = info['contact_info']
        pat = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
        if re.match(pat,email):
            valid = True
        else:
            valid = False
            flash("Email has to be entered as contact info if you have chosen email as contact type["+email +"]Is not valis")
    else:
        phone = info['contact_info']
        num = phone[1:]
        if phone[0]=='+' and num.isdigit() and len(num)>10:
            valid = True
        else:
            valid = False
            flash("A proper phone number with the country code has to be entered as contact info if you have chosen sms as contact type [" + phone + " ]Is not valis")
    return valid

       
if __name__ == "__main__":
    app.run()