from flask import Flask, render_template
from flask import request
import mysql.connector
import os

import sys
sys.path.append(r'D:\Dev\finiromai')
import api_lol_functions
from api_lol_functions import LoL

app = Flask(__name__)#, template_folder='template')
app.run(debug=True)
 
# app.run(host='localhost', port=5000)


@app.route('/' , methods = ['GET', 'POST'])
def hello():
    
    a = LoL(name="ParmiJanna")
    value = a.get_balance()
    cnx = mysql.connector.connect(user=os.getenv("USER"), password=os.getenv("PWD"),
                              host='127.0.0.1',
                              database='azircoin')
    cursor = cnx.cursor()
    query = "SELECT tknburned FROM storage WHERE id=1;"#"INSERT INTO allstorage (alltokken) VALUES(%d);"
    cursor.execute(query,)
    # cnx.commit()
    tkn_burned = cursor.fetchall()
    tkn_burned_extracted = tkn_burned[0]
    value_token_burned = tkn_burned_extracted[0]
    if request.method == 'GET':
        return render_template('index.html', value=value, value_token_burned=value_token_burned)
 
    if request.method == 'POST':
        return render_template('index.html')


@app.errorhandler(404)
def not_found(error):
    return "error"#render_template('error.html'), 404