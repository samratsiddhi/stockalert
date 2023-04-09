import psycopg2 as ps
import yfinance as yf
import pandas as pd
import smtplib
from twilio.rest import Client

sender_email = "example@gmail.com"
sender_password = "password"
user_sid = 'twilio  sid'
user_token = 'twilio token'
uesr_twilio_num = 'twilio number'

# connection to database
def connect_to_db():
    try:

        # set db user name and password
        conn = ps.connect('host=127.0.0.1  \
                      dbname= stockalert \
                      user = postgres  \
                      password = 1234'
                      )
        conn.set_session(autocommit=True)
        cur = conn.cursor()
        return conn,cur
    except ps.Error as e:
        print (e)

# retriving data from db
def retrive_data(conn,cur):
    cur.execute('''SELECT * from stock_subscriber''')
    result = cur.fetchall()
    return result

# sending notification
def sendNotification(contact_info,contact_type,symbol):
    # if contact type is email send email else send sms
    message = "The stock price of "+ symbol + "has exceeded your threshhold"
    if contact_type == 'e':
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        # server.login('samratsiddhi0@gmail.com','misndnnbzvqaembo')
        server.login(globals()['sender_email'],globals()['sender_password'])
        # server.sendmail('samratsiddhi0@gmail.com',contact_info,message)
        server.sendmail(globals()['sender_email'],contact_info,message)
    else:
        sid = globals()['user_sid']
        token = globals()['user_token']
        twilio_num = globals()['uesr_twilio_num']
        target_num = contact_info

        client = Client(sid,token)

        message = client.messages.create(
            body = message,
            from_ = twilio_num,
            to = target_num
        )



conn,cur = connect_to_db()
records = retrive_data(conn,cur)
df = pd.DataFrame(records,columns =['id','symbol','contact_type','contact_info','upper','lower','frequency','current_hour'])
for index, row in df.iterrows():
    # checking to see if it is time to check the stock price
    current_hour = row['current_hour']+1
    if(current_hour == row['frequency']):
        # checking the price of the stock
        symbol = row['symbol']
        stock =yf.Ticker(symbol)
        price = stock.info['regularMarketPrice']
        print(price)
        if price>row['upper'] or price<row['lower']:
            sendNotification(row['contact_info'],row['contact_type'],row['symbol'])
        cur.execute(" UPDATE stock_subscriber SET current_hour = 0 where id = %s ",(row['id'],))
    else:  
        cur.execute(" UPDATE stock_subscriber SET current_hour = %s where id = %s ",(row['current_hour']+1,row['id']))
conn.close()