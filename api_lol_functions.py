import requests
import json
import mysql.connector
from mysql.connector import errorcode

class LoL:
    
    name = ""
    api_key = "RGAPI-8a8ee802-5a92-40fc-a586-8846943115c0"
    amount = 0
    value_match_list = []
    
    def __init__(self, name):
        self.name = name
        

    def url_summoners(self, name):
        url = "https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"
        
        final_url = url + name + "?api_key=" + self.api_key
        return final_url
    
    def get_summoners(self):
        url = self.url_summoners(self.name)
        try:
        
            r = requests.get(url)
            data = r.json()
            print(type(data))
            print(r.status_code)
            return data
        
        except Exception as e:
            dir(e)
            print("Chiamata fallita non 200, controllare api_key")
        
        
    
    def get_puuid(self):
        summoners = self.get_summoners()
        puuid = summoners['puuid']
        return puuid
    
    
    def get_matchid_list(self):
        
        lenght_game = len(self.value_match_list)
        
        if not self.value_match_list:
            print("List is empty, calling riot api to get match id list game")
            puuid = self.get_puuid()
            final_url = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=20&api_key={self.api_key}"
            r = requests.get(final_url)
            data = r.json()
            print(type(data)) 
            print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
            print(data)
            print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
            self.value_match_list = data
            return self.value_match_list
        elif lenght_game >= 20:
            print("returning list beacuse list already filled")
        
            
    
    def list_game_by_puuid(self):
        
        puuid = self.get_puuid()
        final_url = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=20&api_key={self.api_key}"
        try:
            r = requests.get(final_url)
            data = r.json()
            return data
        
        except Exception as e:
            dir(e)
            print("Chiamata fallita non 200, controllare api_key")
        
    def match_id_azir_search(self):
        
        summoner_found = False
        amount_listed = []
        games = self.list_game_by_puuid()
        game_counter = len(games)
        for i in games:
            url = f"https://europe.api.riotgames.com/lol/match/v5/matches/{i}?api_key={self.api_key}"
            r = requests.get(url)
            data = r.json()
            role = data["info"]
            player = role["participants"]
            
            for k in player:
                
                champion = k["championName"]
                summoner_name = k["summonerName"]
                game_result = k["win"]
                
                if summoner_name == "ParmiJanna":
                    summoner_found = True
                else:
                    continue
                
                if champion == "Azir" and summoner_name == "ParmiJanna" and game_result == True and summoner_found == True:
                    self.amount += 250
                elif champion == "Azir" and summoner_name == "ParmiJanna" and summoner_found == True:
                    self.amount += 150
                elif champion != "Azir" and summoner_name == "ParmiJanna" and game_result == True and summoner_found == True:
                    self.amount += 200
                elif champion != "Azir" and summoner_name == "ParmiJanna" and summoner_found == True:
                    self.amount += 100
                else:
                    print("Error non founding the summoners right")
                    
                amount_listed.append(self.amount)
                print("Adding amount: "+ str(self.amount))
                print(amount_listed)
                print(len(amount_listed))
                
        return "amount burned: "+ str(self.amount)+" In total game played: "+str(game_counter)        
            #champion = data[][]  jq needed .info.participants. instead using jq navigating into key with python(integrations with library jq on windows seems not working)
    
    def read_data_db(self):
        
        final_result = []
        
        try:
            cnx = mysql.connector.connect(user='root', password='root',
                              host='127.0.0.1',
                              database='azircoin')
            
            query = "SELECT matchid FROM marchtable;"
            cursor = cnx.cursor(buffered=True) 
            cursor.execute(query)
            cnx.commit()
            myresult = cursor.fetchall()
            for x in myresult:
                final_result.append(list(x))
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            cnx.close()
        
        return final_result
    
    
    def send_data_db(self):
        
        game_played = self.value_match_list
        
        
        try:
            cnx = mysql.connector.connect(user='root', password='root',
                              host='127.0.0.1',
                              database='azircoin')
            cursor = cnx.cursor()
            for prova in game_played:
                query = "INSERT INTO marchtable (matchid) VALUES(%s);"
                args = (prova),
                cursor.execute(query, args)
                cnx.commit()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            cnx.close()
        
        
        
    def check_match_id(self):
        
        game_played = self.value_match_list
        game_stored = self.read_data_db()
        
        # inserire logica che in base a determinate condizioni fa:
        # 1 se value_match_list vuota nulla inviare valore di default di eliminazione valori
        # 2 se piena fare una query e controllare tra gli elementi della query se ci sono riscontri con la nuova lista di game presa
        # 3 inserire i match che sono effettivamente nuovi
        # debugging questa funzione necessita di essere controllata per prima in modo da decidere prima che dati inviare al db, quindi
        # leggere i dati, controllarli poi inserirli
        
        for games in range(len(game_played)):
            
            match = game_stored[games]
            print("AAAAAAAAAAAAAAAAAAAAAA")
            print(type(match))
            print(match)
            print("AAAAAAAAAAAAAAAAAAAAAA")
            print(type(game_played[games]))
            print("AAAAAAAAAAAAAAAAAAAAAA")
            print(type(game_stored[games]))
            print("AAAAAAAAAAAAAAAAAAAAAA")
            if game_played[games] == match[0]:
                print("Riscontro positivo: game eliminato da entrambe le liste.")
            else:
                print("Riscontro non trovato, matchid valido.")
                
        
        pass
        
        
    
a = LoL(name="ParmiJanna")
b = a.list_game_by_puuid()
d = a.get_matchid_list()
c = len(b)
print("CSTO DIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
print(a.value_match_list)
print("CSTO DIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
print(a.get_summoners())
print(a.match_id_azir_search())
print(d)
print("YOU ARRIVED HERE BITCHHHHHHHHHHHHHHHHH")
print("YOU ARRIVED HERE BITCHHHHHHHHHHHHHHHHH")
a.read_data_db()
a.send_data_db()
a.check_match_id()
# controllare bene l'ordine e perchè la if fa come gli pare