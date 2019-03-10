import os
import smtplib
import requests
import time
from ArubaCloud.PyArubaAPI import CloudInterface
EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')
ARUBA_NAME = os.environ.get('ARUBA_NAME')
ARUBA_PASS = os.environ.get('ARUBA_PASS')


def notify():
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.ehlo()
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        subject = 'Site is down!'
        body = 'Make sure your server is up.\nServer request status is not 200'
        msg = f'Subject: {subject}\n\n{body}'
        smtp.sendmail(EMAIL_ADDRESS, 'mail@abogomolov.com', msg)


def reboot_server():
    ci = CloudInterface(dc=1)
    ci.login(ARUBA_NAME, ARUBA_PASS, True)
    server = ci.get_vm()[0]
    if server.status != 3:
        print('server is not working')
        ci.poweron_server(server)
    else:
        print('restarting server')
        ci.poweroff_server(server)
        time.sleep(15)
        ci.poweron_server(server)


try:
    r = requests.get('http://proxy.abogomolov.com', timeout=5)
    if r.status_code != 200:
        print(r.status_code)
        notify()
        reboot_server()
#    else:
#        print('everything is fine')
except Exception as e:
    print('Error occured')
    notify()
    reboot_server()

