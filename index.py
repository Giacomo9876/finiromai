from flask import Flask
from flask import request
from flask import render_template
from flask import abort, redirect, url_for

app = Flask(__name__)
 
app.run(host='localhost', port=5000)


@app.route('/lolapi' , methods = ['GET'])
def create():
    
    if request.method == 'GET':
        return render_template('api.html')
 
    if request.method == 'POST':
        pass


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404