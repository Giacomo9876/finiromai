from apscheduler.schedulers.background import BackgroundScheduler
import time
import os
from api_lol_functions import LoL

from apscheduler.schedulers.background import BackgroundScheduler

class JobToDo:

    _valuedb = "tknburned"
    _dbvalue = "storage"
    
    def shitcalling(self):
        a = LoL(name="ParmiJanna")
        b = a.list_game_by_puuid()
        d = a.get_matchid_list()
        a.check_match_id()
        print(a.amount)
        cnx = a.conn_db()
        cursor = cnx.cursor()
        query = f"SELECT {self._valuedb} FROM {self._dbvalue} WHERE id=1;"#"INSERT INTO allstorage (alltokken) VALUES(%d);"
        cursor.execute(query,)
        # cnx.commit()
        tkn_burned = cursor.fetchall()
        tkn_burned_extracted = tkn_burned[0]
        value = tkn_burned_extracted[0]
        value = value + a.amount
        query = f'UPDATE {self._dbvalue} SET {self._valuedb} = %s WHERE id = 1;'
        args = (value),
        cursor.execute(query, args)
        cnx.commit()
        cnx.close()
        
 

a = JobToDo()
print(a.shitcalling())