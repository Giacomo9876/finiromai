from flask import Flask, render_template
from flask import request


import sys
sys.path.append(r'C:\Users\Reidi\dev\finiromai')
import api_lol_functions
import hand_things_to_call
from api_lol_functions import LoL
import time


app = Flask(__name__)#, template_folder='template')
# app.run(debug=True)
 
# app.run(host='localhost', port=5000)


@app.route('/' , methods = ['GET', 'POST'])
def hello():
    
    a = LoL(name="ParmiJanna")
    value = a.get_balance()
    cnx = a.conn_db()
    cursor = cnx.cursor()
    query = "SELECT tknburned FROM storage WHERE id=1;"#"INSERT INTO allstorage (alltokken) VALUES(%d);"#need to make the argument of the query dinamic avoid sqlinj
    cursor.execute(query,)
    tkn_burned = cursor.fetchall()
    tkn_burned_extracted = tkn_burned[0]
    value_token_burned = tkn_burned_extracted[0]
    # start = time.time()
    # end = time.time()
    # res = end - start
    # print(res) # time in seconds
    # print(type(res))
    value_summoners = a.challenges()
    value_summ_used_last_game = value_summoners[1]
    value_summ_sum = value_summoners[0]

    if request.method == 'GET':
        return render_template('index.html', value=value, value_token_burned=value_token_burned, value_summ_sum=value_summ_sum, value_summ_used_last_game=value_summ_used_last_game)
 
    if request.method == 'POST':
        return render_template('index.html')


@app.errorhandler(404)
def not_found(error):
    return "error"#render_template('error.html'), 404