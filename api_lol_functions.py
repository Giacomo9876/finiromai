import requests
import json
import mysql.connector
from mysql.connector import errorcode
from web3 import HTTPProvider
from web3 import Web3
from web3.middleware import geth_poa_middleware
from dotenv import load_dotenv
import os
load_dotenv()

# TO DO
# ECONOMY
# DEPLOY
# AGGIUSTARE FRONTEND
# EXCHANGE


class LoL:
    
    name = ""
    api_key = os.getenv("API_KEY")
    amount = 0
    value_match_list = []
    
    def __init__(self, name):
        self.name = name
        

    def conn_for_burn(self):
        #10
        # Connessione alla blockchain
        w3 = Web3(Web3.HTTPProvider('https://goerli.infura.io/v3/eba9e534005045928e460351c954cbf8'))
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        amount_to_burn = self.amount
        caller = "0xFdB5e4A6273Ddf2A1D09a377C9E4eb407b3De2C4"
        private_key = os.getenv("API_SECRET")  # To sign the transaction
        # Initialize address nonce
        nonce = w3.eth.get_transaction_count(caller)
        print(w3.is_connected())
        contract_address = '0x6117A5F053e65Aa9bcbE064cD186Ed9580353bCa'
        data = open('abi.json')
        abi = json.load(data)
        # contract = w3.eth.contract(address=contract_address, abi=abi)
        data = open('bytecode')
        bytecodedelcazzo = data.readline()
        bytecode = bytecodedelcazzo
        
        # 3. Create variables
        account_from = {
            'private_key': private_key,
            'address': caller,
        }
        
        contract_instance = w3.eth.contract(address=contract_address, abi=abi)

        #value = contract_instance.functions.burn(contract_address, amount_to_burn).call()
        transaction = contract_instance.functions.burn(caller, amount_to_burn).build_transaction({'from': account_from['address'], 'nonce': w3.eth.get_transaction_count(account_from['address']),})#build_transaction({"chainId": Chain_id, "from": caller, "nonce": nonce})
        signed_tx = w3.eth.account.sign_transaction(transaction, private_key)
        print(signed_tx)
        # Send transaction
        send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

        # Wait for transaction receipt
        tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)
        print(tx_receipt) # Optional
        
    
    def get_balance(self):
        
        w3 = Web3(Web3.HTTPProvider('https://goerli.infura.io/v3/eba9e534005045928e460351c954cbf8'))
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        contract_address = '0x6117A5F053e65Aa9bcbE064cD186Ed9580353bCa'
        data = open(r'D:\Dev\finiromai\abi.json')
        abi = json.load(data)
        
        token = w3.eth.contract(address=contract_address, abi=abi) # declaring the token contract
        token_balance = token.functions.totalSupply().call() # returns int with balance, without decimals
        print(token_balance)
        
        return token_balance
        
        
    def url_summoners(self, name):
        #1
        url = "https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"
        
        final_url = url + name + "?api_key=" + self.api_key
        return final_url
    
    
    def get_summoners(self):
        #2
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
        #3
        summoners = self.get_summoners()
        puuid = summoners['puuid']
        return puuid
    
    
    def get_matchid_list(self):
        #5
        lenght_game = len(self.value_match_list)
        
        if not self.value_match_list:
            print("List is empty, calling riot api to get match id list game")
            puuid = self.get_puuid()
            final_url = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=20&api_key={self.api_key}"
            r = requests.get(final_url)
            data = r.json()
            self.value_match_list = data
            return self.value_match_list
        elif lenght_game >= 20:
            print("returning list beacuse list already filled")
        
            
    def list_game_by_puuid(self):
        #4
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
        #8
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
            
        return self.amount
    
    
    def read_data_db(self):
        #7 
        final_result = []
        
        try:
            cnx = mysql.connector.connect(user=os.getenv("USER"), password=os.getenv("PWD"),
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
        #9
        game_played = match_list_updated
        print("AOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
        print(game_played)
        print("--------------------")
        
        try:
            cnx = mysql.connector.connect(user=os.getenv("USER"), password=os.getenv("PWD"),
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
        # 6
        game_played = self.value_match_list
        game_stored = self.read_data_db()
        games_equalities = []
        cioccato = False
        amount_to_burn = self.match_id_azir_search()
        
        
        for games in range(len(game_played)):
            
            match = game_played[games]
            print("AAAAAAAAAAAAAAAAAAAAAA")
            print(match)
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
            games_equalities = []
        else:
            print(f"non ci sono 12 nuovi game da inserire, ma soltanto: {nmb}")
        
        
        bruciare = self.conn_for_burn()
        
        print("CIAOOOOOOOOOOOOO: "+ str(amount_to_burn))
    
        print("##################################")

# a = LoL(name="ParmiJanna")

# print(a.get_balance())