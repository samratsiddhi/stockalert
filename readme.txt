this is the documentation of how to set up the web application after downloading this folder to your pc

1. install postgresql

2. intall the required libraries
    psycopg2 
    yfinance
    pandas
    smtplib
    flask
    twilio

3. Set up db name and password in main.py and notify.py

4. Set up the  credential of email and twilio you want to recieve notifications from

5. run main.py to subscribe to stocks   

6. use task schedular to run notify.py every hour