import socket
import sys
import threading
import time
from flask import Flask, render_template, request, redirect, url_for, abort, session
import re
from goompy import GooMPy

WIDTH = 640
HEIGHT = 480
LATITUDE = 1.32136
LONGITUDE = 103.86038

message = 'Latitude:' + str(LATITUDE) + ' Longitude:' + str(LONGITUDE)
# @app.route("/")
# @app.route("/<state>")
# @app.route("/<location>/<state>")
# Create a dictionary called pins to store the pin number, name, and pin state:
pins = {
    22: {'name': 'TCPSERVER', 'state': False},
    23: {'name': 'RED', 'state': True},
    24: {'name': 'GREEN', 'state': True},
    25: {'name': 'YELLOW', 'state': True}
}




def GetGPSPMAP(lat, long):
    ZOOM = 15
    MAPTYPE = 'roadmap'
    goompy = GooMPy(WIDTH, HEIGHT, lat, long, ZOOM, MAPTYPE)
    file_jpg = goompy.getFileName()
    print(file_jpg)
    return file_jpg

app = Flask(__name__, static_folder='mapscache')

Value = ['r', 'g', 'y']
flgConn = False
connection = None
flgRead = False
File_JPF = GetGPSPMAP(LATITUDE, LONGITUDE)

templateData = {
    'pins': pins,
    'message': message,
    'image_file': File_JPF
}
def TCPServer():
    global connection, message,flgConn,File_JPF,pin

    TCP_IP = socket.gethostname()  # '10.146.0.2'

    TIMEOUT = 5
    print("Server TCP_IP: %s" % TCP_IP)
    TCP_PORT = 5001
    print("Server Port: %s" % TCP_PORT)
    BUFFER_SIZE = 18  # Normally 1024, but we want fast response


    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # sock.settimeout(TIMEOUT)
    try:
        sock.bind((TCP_IP, TCP_PORT))
    except socket.error as msg:
        message = 'Bind failed. Error Code : ' + str(msg[0])
        print(message)
        sys.exit()


    while flgConn:
        sock.listen(1)
        connection, client_address = sock.accept()
        print('connection from' + str(client_address))
        # Receive the data in small chunks and retransmit it
        nTime = 0
        while nTime < 10:
            data = connection.recv(BUFFER_SIZE)
            print ("Len data:" + str(len(data)))
            message = ("Len data:" + str(len(data)))
            if len(data) < 10: break
            print('receive data:' + str(data))
            Long = re.split('\s+', str(data.decode('utf_8')))
            print('Split:' + str(Long))
            File_JPF = GetGPSPMAP(float(Long[0]),float(Long[1]))
            nTime = nTime +1
            #connection.send(data)
            time.sleep(0.2)

        pins[22]['state'] = True
    connection.close()

def ConnectionLoss():
    global connection, flgConn, message, app, flgRead,templateData
    connection.close()
    flgConn = False
    flgRead = False
    message = "Connection Loss ..."
    print(message)
    # pins[changePin]['state'] = False

    with app.test_request_context('/'):
        rendered = render_template('main.html', **templateData)


# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/<changePin>/<action>")
def action(changePin, action):
    global connection, flgConn, pins, Value, message, File_JPF,templateData
    # Convert the pin from the URL into an integer:
    changePin = int(changePin)
    if changePin == 22:
        if action == "open":
            message = "Opening TCP sever ..."
            print(message)
            pins[changePin]['state'] = True
            if flgConn == False:
                flgConn = True
                t = threading.Thread(target=TCPServer)
                t.start()


        if action == "close":
            message = "Close TCP server ..."
            print(message)
            pins[changePin]['state'] = False

            flgConn = False

    templateData = {
        'pins': pins,
        'message': message,
        'image_file': File_JPF
    }

    return render_template('main.html', **templateData)


@app.route("/")
def hello():
    global pins, message,File_JPF,templateData
    templateData = {
        'pins': pins,
        'message': message,
        'image_file': File_JPF
    }
    return render_template('main.html', **templateData)

if __name__ == "__main__":
    app.run()



