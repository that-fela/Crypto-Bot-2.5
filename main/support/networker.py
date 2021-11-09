# reconnects to the internet incase it disconnects

# REDUNDENT

import os
import urllib.request
import time as t
import smtplib

def test(name_of_router, show=True, run_time=1):
    def isconnected():
        try:
            urllib.request.urlopen('http://www.google.com') #Python 3.x
            return True
        except:
            return False

    disconnects = 0
    tStop = t.time() + run_time
    while tStop > t.time():
        if not isconnected():
            print("!!!DISCONNECTED!!!")
            os.system("cmd /c \"netsh wlan connect name=" + name_of_router)
            disconnects += 1
        else:
            if show:
                print("TESTING")
        t.sleep(1)

def send_email(body):
    gmail_user = 'nz.john.byworth@gmail.com'
    gmail_password = '123NZgames'

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_password)

        sent_from = 'nz.john.byworth@gmail.com'
        to = ['nz.john.byworth@gmail.com']
        subject = 'Own'

        server.sendmail(sent_from, to, body)
        server.close()

        print('Email sent!')

    except:
        print('Something went wrong...')