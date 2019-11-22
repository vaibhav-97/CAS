#the sse sample
from flask import Flask, render_template, request,Response
from threading import Lock

#lock for synchronization
mutex=Lock()
mutex.acquire(1)
value=""
app=Flask(__name__)
from time import sleep

@app.route('/empty.html')
def empty():
    return render_template("empty.html")


@app.route('/a.html')
def gethtml():
    return render_template("a.html")



def runget():
    while True:
        mutex.acquire(1)
        yield 'data: '+value+'\n\n'



#the sse-trigger
@app.route("/send/<val>")
def send(val):
    global value
    value=val
    mutex.release()
    return "[]"



#the sse-target event
@app.route("/get")
def get():
    print("get called")
    return Response(runget(),mimetype="text/event-stream")


app.run(debug=True)