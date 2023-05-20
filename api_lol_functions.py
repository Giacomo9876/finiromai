import requests
import json
import mysql.connector
from mysql.connector import errorcode
from fuoco_valore import BurnValue

class LoL:
    
    name = ""
    api_key = "RGAPI-1da04f57-a576-4d40-bbf7-67e00774ad7f"
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
                
        # return "amount burned: "+ str(self.amount)+" In total game played: "+str(game_counter)  
        return self.amount  
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
                print(x)
                x = str(x)
                x = x.replace("(", "")
                x = x.replace("'", "")
                x = x.replace(",", "")
                x = x.replace(")", "")
                final_result.append(x)
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
    
    
    def send_data_db(self, match_list_updated):
        
        game_played = match_list_updated
        
        
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
        print(len(game_stored))
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        games_equalities = []
        final_list = []
        cioccato = False
        prova = BurnValue("0x5B38Da6a701c568545dCfcB03FcB875f56beddC4", 2100)
        amount_to_burn = self.match_id_azir_search()
        
        # inserire logica che in base a determinate condizioni fa:
        # 1 se value_match_list vuota nulla inviare valore di default di eliminazione valori
        # 2 se piena fare una query e controllare tra gli elementi della query se ci sono riscontri con la nuova lista di game presa
        # 3 inserire i match che sono effettivamente nuovi
        # debugging questa funzione necessita di essere controllata per prima in modo da decidere prima che dati inviare al db, quindi
        # leggere i dati, controllarli poi inserirli
        
        for games in range(len(game_played)):
            
            match = game_played[games]
            print("AAAAAAAAAAAAAAAAAAAAAA")
            print(games)
            print(match)
            print("AAAAAAAAAAAAAAAAAAAAAA")
            print(type(game_stored[games]))
            print("AAAAAAAAAAAAAAAAAAAAAA")
            # controllo se il match è presente nella lista del db se non lo è aggiungo a lista e poi invio nei controlli
            for i in game_stored:
            
                if i == match:
                    print("Riscontro positivo, match già presente nel db")
                    cioccato = True
                    break
            
            
            if cioccato is True:
                print("Riscontro positivo: game non aggiunto alla lista finale.")
                cioccato = False
            else:
                print("Riscontro negativo, match da inserire")
                games_equalities.append(game_played[games])
                cioccato = False
                
        print(games_equalities)
        nmb = len(games_equalities)
        
        if nmb >= 12:
            print("12 nuovi game rilevati, si può proseguire con l'inserimento")
            self.send_data_db(games_equalities)
            prova.get_token_to_burn_from_lol(amount_to_burn)
        else:
            print(f"non ci sono 12 nuovi game da inserire, ma soltanto: {nmb}")
        
        
        
    
a = LoL(name="ParmiJanna")
b = a.list_game_by_puuid()
d = a.get_matchid_list()
c = len(b)
# print("CSTO DIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
# print(a.value_match_list)
# print("CSTO DIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
print(a.get_summoners())
print(a.match_id_azir_search())
print(d)
print("YOU ARRIVED HERE BITCHHHHHHHHHHHHHHHHH")
a.check_match_id()
# a.read_data_db()
# a.send_data_db()