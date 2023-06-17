from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler
import mysql.connector
import time
import os
from api_lol_functions import LoL

from apscheduler.schedulers.background import BackgroundScheduler

class JobToDo:
    
    def shitcalling(self):
        a = LoL(name="ParmiJanna")
        b = a.list_game_by_puuid()
        d = a.get_matchid_list()
        a.check_match_id()
        print(a.amount)
        cnx = mysql.connector.connect(user=os.getenv("USER"), password=os.getenv("PWD"),
                              host='127.0.0.1',
                              database='azircoin')
        cursor = cnx.cursor()
        query = "SELECT tknburned FROM storage WHERE id=1;"#"INSERT INTO allstorage (alltokken) VALUES(%d);"
        cursor.execute(query,)
        # cnx.commit()
        tkn_burned = cursor.fetchall()
        tkn_burned_extracted = tkn_burned[0]
        value = tkn_burned_extracted[0]
        print(type(tkn_burned_extracted))
        print(value)
        value = value + a.amount
        print(value)
        query = 'UPDATE storage SET tknburned = %s WHERE id = 1; '
        args = (value),
        cursor.execute(query, args)
        cnx.commit()
        cnx.close()
        
    def conn_web(self):

        scheduler = BackgroundScheduler()
        scheduler.add_job(self.shitcalling, 'interval', seconds=30)#23h = 82800
        scheduler.start()
        print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

        try:
            # This is here to simulate application activity (which keeps the main thread alive).
            while True:
                time.sleep(3)
        except (KeyboardInterrupt, SystemExit):
            # Not strictly necessary if daemonic mode is enabled but should be done if possible
            scheduler.shutdown()
        
 

a = JobToDo()
print(a.conn_web())