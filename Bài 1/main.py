from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import csv

class Player:
    def __init__(self, name, nation, position, team, age):
        self.name = name
        self.nation = nation
        self.team = team
        self.position = position
        self.age = age
        self.playing_time = {
            "matches_played": "N/a",
            "starts": "N/a",
            "minutes": "N/a"
        }
        self.performance = {
            "goals": "N/a",
            "assists": "N/a",
            "yellow_cards": "N/a",
            "red_cards": "N/a"
        }
        self.expected = {
            "xG": "N/a",
            "xAG": "N/a"
        }
        self.progression = {
            "PrgC": "N/a",
            "PrgP": "N/a",
            "PrgR": "N/a"
        }
        self.per_90 = {
            "Gls": "N/a",
            "Ast": "N/a",
            "xG": "N/a",
            "xAG": "N/a",
        }
        self.goalkeeping = {
            "Performance": {
                "GA90": "N/a",
                "Save%": "N/a",
                "CS%": "N/a"
            },
            "Penalty Kicks": {
                "Save%": "N/a"
            }
        }
        self.shooting = {
            "SoT%": "N/a",
            "SoT/90": "N/a",
            "G/Sh": "N/a",
            "Dist": "N/a",
        }
        self.passing = {
            "Total": {
                "Cmp": "N/a",
                "Cmp%": "N/a",
                "TotDist": "N/a",
            },
            "Short": {
                "Cmp%": "N/a"
            },
            "Medium": {
                "Cmp%": "N/a"
            },
            "Long": {
                "Cmp%": "N/a"
            },
            "Expected": {
                "KP": "N/a",
                "1/3": "N/a",
                "PPA": "N/a",
                "CrsPA": "N/a",
                "PrgP": "N/a"
            }
        }
        self.goal_shot_creation = {
            "SCA": {
                "SCA": "N/a",
                "SCA90": "N/a"
            },
            "GCA": {
                "GCA": "N/a",
                "GCA90": "N/a"
            },
        }
        self.defensive_actions = {
            "Tackles": {
                "Tkl": "N/a",
                "TklW": "N/a",
            },
            "Challenges": {
                "Att": "N/a",
                "Lost": "N/a"
            },
            "Blocks": {
                "Blocks": "N/a",
                "Sh": "N/a",
                "Pass": "N/a",
                "Int": "N/a",
            }
        }
        self.possession = {
            "Touches": {
                "Touches": "N/a",
                "Def Pen": "N/a",
                "Def 3rd": "N/a",
                "Mid 3rd": "N/a",
                "Att 3rd": "N/a",
                "Att Pen": "N/a",
            },
            "Take-Ons": {
                "Att": "N/a",
                "Succ%": "N/a",
                "Tkld%": "N/a"
            },
            "Carries": {
                "Carries": "N/a",
                "ProDist": "N/a",
                "ProgC": "N/a",
                "1/3": "N/a",
                "CPA": "N/a",
                "Mis": "N/a",
                "Dis": "N/a"
            },
            "Receiving": {
                "Rec": "N/a",
                "PrgR": "N/a"
            }
        }
        self.misc_stats = {
            "Performance": {
                "Fls": "N/a",
                "Fld": "N/a",
                "Off": "N/a",
                "Crs": "N/a",
                "OG": "N/a",
                "Recov": "N/a"
            },
            "Aerial Duels": {
                "Won": "N/a",
                "Lost": "N/a",
                "Won%": "N/a"
            }
        }

    def setPlaying_time(self, arr):
        self.playing_time["matches_played"] = arr[0]
        self.playing_time["starts"] = arr[1]
        self.playing_time["minutes"] = arr[2]

    def setPerformance(self, arr):
        self.performance["goals"] = arr[0]
        self.performance["assists"] = arr[2]
        self.performance["yellow_cards"] = arr[3]
        self.performance["red_cards"] = arr[4]

    def setExpected(self, arr):
        self.expected["xG"] = arr[0]
        self.expected["xAG"] = arr[2]

    def setProgression(self, arr):
        self.progression["PrgC"] = arr[0]
        self.progression["PrgP"] = arr[1]
        self.progression["PrgR"] = arr[2]

    def setPer90(self, arr):
        self.per_90["Gls"] = arr[0]
        self.per_90["Ast"] = arr[1]
        self.per_90["xG"] = arr[2]
        self.per_90["xAG"] = arr[3]

    def setGoalkeeping(self, performance_arr, penalty_arr):
        self.goalkeeping["Performance"]["GA90"] = performance_arr[1]
        self.goalkeeping["Performance"]["Save%"] = performance_arr[4]
        self.goalkeeping["Performance"]["CS%"] = performance_arr[9]
        self.goalkeeping["Penalty Kicks"]["Save%"] = penalty_arr[4]

    def setShooting(self, arr):
        self.shooting["SoT%"] = arr[0]
        self.shooting["SoT/90"] = arr[1]
        self.shooting["G/Sh"] = arr[2]
        self.shooting["Dist"] = arr[3]

    def setPassing(self, total_arr, short_arr, medium_arr, long_arr, expected_arr):
        self.passing["Total"]["Cmp"] = total_arr[0]
        self.passing["Total"]["Cmp%"] = total_arr[2]
        self.passing["Total"]["TotDist"] = total_arr[3]
        self.passing["Short"]["Cmp%"] = short_arr[2]
        self.passing["Medium"]["Cmp%"] = medium_arr[2]
        self.passing["Long"]["Cmp%"] = long_arr[2]
        self.passing["Expected"]["KP"] = expected_arr[4]
        self.passing["Expected"]["1/3"] = expected_arr[5]
        self.passing["Expected"]["PPA"] = expected_arr[6]
        self.passing["Expected"]["CrsPA"] = expected_arr[7]
        self.passing["Expected"]["PrgP"] = expected_arr[8]

    def setGoalShotCreation(self, sca_arr, gca_arr):
        self.goal_shot_creation["SCA"]["SCA"] = sca_arr[0]
        self.goal_shot_creation["SCA"]["SCA90"] = sca_arr[1]
        self.goal_shot_creation["GCA"]["GCA"] = gca_arr[0]
        self.goal_shot_creation["GCA"]["GCA90"] = gca_arr[1]

    def setDefensiveActions(self, tackles_arr, challenges_arr, blocks_arr):
        self.defensive_actions["Tackles"]["Tkl"] = tackles_arr[0]
        self.defensive_actions["Tackles"]["TklW"] = tackles_arr[1]
        self.defensive_actions["Challenges"]["Att"] = challenges_arr[1]
        self.defensive_actions["Challenges"]["Lost"] = challenges_arr[3]
        self.defensive_actions["Blocks"]["Blocks"] = blocks_arr[0]
        self.defensive_actions["Blocks"]["Sh"] = blocks_arr[1]
        self.defensive_actions["Blocks"]["Pass"] = blocks_arr[2]
        self.defensive_actions["Blocks"]["Int"] = blocks_arr[3]

    def setPossession(self, touches_arr, take_ons_arr, carries_arr, receiving_arr):
        self.possession["Touches"]["Touches"] = touches_arr[0]
        self.possession["Touches"]["Def Pen"] = touches_arr[1]
        self.possession["Touches"]["Def 3rd"] = touches_arr[2]
        self.possession["Touches"]["Mid 3rd"] = touches_arr[3]
        self.possession["Touches"]["Att 3rd"] = touches_arr[4]
        self.possession["Touches"]["Att Pen"] = touches_arr[5]
        self.possession["Take-Ons"]["Att"] = take_ons_arr[0]
        self.possession["Take-Ons"]["Succ%"] = take_ons_arr[2]
        self.possession["Take-Ons"]["Tkld%"] = take_ons_arr[4]
        self.possession["Carries"]["Carries"] = carries_arr[0]
        self.possession["Carries"]["ProDist"] = carries_arr[2]
        self.possession["Carries"]["ProgC"] = carries_arr[3]
        self.possession["Carries"]["1/3"] = carries_arr[4]
        self.possession["Carries"]["CPA"] = carries_arr[5]
        self.possession["Carries"]["Mis"] = carries_arr[6]
        self.possession["Carries"]["Dis"] = carries_arr[7]
        self.possession["Receiving"]["Rec"] = receiving_arr[0]
        self.possession["Receiving"]["PrgR"] = receiving_arr[1]

    def setMiscStats(self, performance_arr, aerial_duels_arr):
        self.misc_stats["Performance"]["Fls"] = performance_arr[0]
        self.misc_stats["Performance"]["Fld"] = performance_arr[1]
        self.misc_stats["Performance"]["Off"] = performance_arr[2]
        self.misc_stats["Performance"]["Crs"] = performance_arr[3]
        self.misc_stats["Performance"]["OG"] = performance_arr[4]
        self.misc_stats["Performance"]["Recov"] = performance_arr[5]
        self.misc_stats["Aerial Duels"]["Won"] = aerial_duels_arr[0]
        self.misc_stats["Aerial Duels"]["Lost"] = aerial_duels_arr[1]
        self.misc_stats["Aerial Duels"]["Won%"] = aerial_duels_arr[2]

    def __str__(self) -> str:
        return self.name + " " + str(self.age) + " " + self.team + "\n" + str(self.performance) + \
            "\n" + str(self.per_90) + \
            "\n" + str(self.goalkeeping) + \
            "\n" + str(self.shooting)

class Player_Manager:
    def __init__(self) -> None:
        self.list_player = []

    def add(self, player):
        self.list_player.append(player)

    def find(self, name, team):
        for i in self.list_player:
            if i.name == name and i.team == team:
                return i
        return None

    def filtering(self):
        self.list_player = list(filter(lambda p: p.playing_time["minutes"] > 90, self.list_player))

    def show(self):
        for i in self.list_player:
            print(i)

    def sort(self):
        self.list_player = sorted(self.list_player, key=lambda x: (x.name.split()[-1], -x.age))

header_player = [
    "name", "nation", "team", "position", "age",
    "matches_played", "starts", "minutes",
    "goals", "assists", "yellow_cards", "red_cards",
    "xG", "xAG",
    "PrgC", "PrgP", "PrgR",
    "per90_Gls", "per90_Ast", "per90_xG", "per90_xAG",
    "SoT%", "SoT/90", "G/Sh", "Dist",
    "Pass_Cmp", "Pass_Cmp%", "TotDist",
    "Short_Cmp%", "Medium_Cmp%", "Long_Cmp%", 
    "KP", "1/3", "PPA", "CrsPA", "PrgP",
    "SCA", "SCA90", "GCA", "GCA90",  
    "Tkl", "TklW", "Challenges_Att", "Challenges_Lost",
    "Blocks", "Blocks_SH", "Blocks_Pass", "Blocks_Int",
    "Touches", "Def_Pen", "Def_3rd", "Mid_3rd", "Att_3rd", "Att_Pen",
    "Take_Att", "Take_Succ%", "Take_Tkld%",
    "Carries", "Carries_ProDist", "Carries_ProgC", "Carries_1/3", "Carries_CPA", "Carries_Mis", "Carries_Dis",
    "REC", "REC_PrgR",
    "Fls", "Fld", "Off", "Crs", "OG", "Recov", "Aerial_Won", "Aerial_Lost", "Aerial_Won%"
]

def row_player(player):
    return [
        player.name, player.nation, player.team, player.position, player.age,
        player.playing_time["matches_played"], player.playing_time["starts"], player.playing_time["minutes"],
        player.performance["goals"], player.performance["assists"], player.performance["yellow_cards"], player.performance["red_cards"],
        player.expected["xG"], player.expected["xAG"],
        player.progression["PrgC"], player.progression["PrgP"], player.progression["PrgR"],
        player.per_90["Gls"], player.per_90["Ast"], player.per_90["xG"], player.per_90["xAG"],
        player.shooting["SoT%"], player.shooting["SoT/90"], player.shooting["G/Sh"], player.shooting["Dist"],
        player.passing["Total"]["Cmp"], player.passing["Total"]["Cmp%"], player.passing["Total"]["TotDist"],
        player.passing["Short"]["Cmp%"], player.passing["Medium"]["Cmp%"], player.passing["Long"]["Cmp%"],
        player.passing["Expected"]["KP"], player.passing["Expected"]["1/3"], player.passing["Expected"]["PPA"], 
        player.passing["Expected"]["CrsPA"], player.passing["Expected"]["PrgP"],
        player.goal_shot_creation["SCA"]["SCA"], player.goal_shot_creation["SCA"]["SCA90"],  # Added SCA fields
        player.goal_shot_creation["GCA"]["GCA"], player.goal_shot_creation["GCA"]["GCA90"],  # Added GCA fields
        player.defensive_actions["Tackles"]["Tkl"], player.defensive_actions["Tackles"]["TklW"], 
        player.defensive_actions["Challenges"]["Att"], player.defensive_actions["Challenges"]["Lost"],
        player.defensive_actions["Blocks"]["Blocks"], player.defensive_actions["Blocks"]["Sh"], 
        player.defensive_actions["Blocks"]["Pass"], player.defensive_actions["Blocks"]["Int"],
        player.possession["Touches"]["Touches"], player.possession["Touches"]["Def Pen"], 
        player.possession["Touches"]["Def 3rd"], player.possession["Touches"]["Mid 3rd"], 
        player.possession["Touches"]["Att 3rd"], player.possession["Touches"]["Att Pen"],
        player.possession["Take-Ons"]["Att"], player.possession["Take-Ons"]["Succ%"], 
        player.possession["Take-Ons"]["Tkld%"],
        player.possession["Carries"]["Carries"], player.possession["Carries"]["ProDist"], 
        player.possession["Carries"]["ProgC"], player.possession["Carries"]["1/3"], 
        player.possession["Carries"]["CPA"], player.possession["Carries"]["Mis"], 
        player.possession["Carries"]["Dis"],
        player.possession["Receiving"]["Rec"], player.possession["Receiving"]["PrgR"],
        player.misc_stats["Performance"]["Fls"], player.misc_stats["Performance"]["Fld"], 
        player.misc_stats["Performance"]["Off"], player.misc_stats["Performance"]["Crs"], 
        player.misc_stats["Performance"]["OG"], player.misc_stats["Performance"]["Recov"],
        player.misc_stats["Aerial Duels"]["Won"], player.misc_stats["Aerial Duels"]["Lost"], 
        player.misc_stats["Aerial Duels"]["Won%"]
    ]
class DataCrawler:
    def __init__(self):
        self.player_manager = Player_Manager()
    
    def convert_to_float(self, value):
        return float(value) if value != '' else "N/a"
    
    def extract_web_data(self, url, xpath, data_category):
        driver = webdriver.Chrome()
        extracted_data = []
        
        try:
            driver.get(url)
            table = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            all_rows = table.find_elements(By.TAG_NAME, 'tr')
            
            for row in all_rows:
                columns = row.find_elements(By.TAG_NAME, 'td')
                row_data = []
                
                for col_index, column in enumerate(columns[:-1]):
                    text_content = column.text.strip()
                    
                    if col_index == 1:
                        words = text_content.split()
                        row_data.append(words[1] if len(words) == 2 else text_content)
                    else:
                        if col_index >= 4:
                            text_content = text_content.split("-")[0]
                            text_content = text_content.replace(",", "")
                            text_content = self.convert_to_float(text_content)
                        row_data.append(text_content)
                
                if row_data:
                    extracted_data.append(row_data)
        finally:
            driver.quit()
            print(f"Completed crawling {data_category} data")
            
        return extracted_data
    
    def process_standard_stats(self):
        url = "https://fbref.com/en/comps/9/2024-2025/stats/2024-2025-Premier-League-Stats"
        data = self.extract_web_data(url, '//*[@id="stats_standard"]', "Standard")
        print("Standard data sample:", data[0])
        
        for player_data in data:
            player = self.player_manager.find(player_data[0], player_data[3])
            
            if not player:
                player = Player(
                    player_data[0],
                    player_data[1],
                    player_data[2],
                    player_data[3],
                    player_data[4]
                )
                
                player.setPlaying_time(player_data[6:9])
                player.setPerformance([
                    player_data[13],
                    player_data[14],
                    player_data[11],
                    player_data[16],
                    player_data[17]
                ])
                player.setExpected(player_data[18:21])
                player.setProgression(player_data[22:25])
                player.setPer90(player_data[25:])
                
                self.player_manager.add(player)
        
        self.player_manager.filtering()
    
    def process_goalkeeper_stats(self):
        url = 'https://fbref.com/en/comps/9/2024-2025/keepers/2024-2025-Premier-League-Stats'
        data = self.extract_web_data(url, '//*[@id="stats_keeper"]', "Goalkeeping")
        
        for player_data in data:
            player = self.player_manager.find(player_data[0], player_data[3])
            if player:
                player.setGoalkeeping(player_data[10:20], player_data[20:])
    
    def process_shooting_stats(self):
        url = 'https://fbref.com/en/comps/9/2024-2025/shooting/2024-2025-Premier-League-Stats'
        data = self.extract_web_data(url, '//*[@id="stats_shooting"]', "Shooting")
        
        for player_data in data:
            player = self.player_manager.find(player_data[0], player_data[3])
            if player:
                player.setShooting(player_data[7:19])
    
    def process_passing_stats(self):
        url = 'https://fbref.com/en/comps/9/2024-2025/passing/2024-2025-Premier-League-Stats'
        data = self.extract_web_data(url, '//*[@id="stats_passing"]', "Passing")
        
        for player_data in data:
            player = self.player_manager.find(player_data[0], player_data[3])
            if player:
                player.setPassing(
                    player_data[7:12],
                    player_data[12:15],
                    player_data[15:18],
                    player_data[18:21],
                    player_data[21:]
                )
    
    def process_goal_creation_stats(self):
        url = 'https://fbref.com/en/comps/9/2024-2025/gca/2024-2025-Premier-League-Stats'
        data = self.extract_web_data(url, '//*[@id="stats_gca"]', "Goal and Shot Creation")
        
        for player_data in data:
            player = self.player_manager.find(player_data[0], player_data[3])
            if player:
                player.setGoalShotCreation(player_data[7:9], player_data[15:17])
    
    def process_defensive_stats(self):
        url = 'https://fbref.com/en/comps/9/2024-2025/defense/2024-2025-Premier-League-Stats'
        data = self.extract_web_data(url, '//*[@id="stats_defense"]', "Defensive Actions")
        
        for player_data in data:
            player = self.player_manager.find(player_data[0], player_data[3])
            if player:
                player.setDefensiveActions(
                    player_data[7:12],
                    player_data[12:16],
                    player_data[16:23]
                )
    
    def process_possession_stats(self):
        url = 'https://fbref.com/en/comps/9/2024-2025/possession/2024-2025-Premier-League-Stats'
        data = self.extract_web_data(url, '//*[@id="stats_possession"]', "Possession")
        
        for player_data in data:
            player = self.player_manager.find(player_data[0], player_data[3])
            if player:
                player.setPossession(
                    player_data[7:14],
                    player_data[14:19],
                    player_data[19:27],
                    player_data[27:29]
                )
    
    def process_miscellaneous_stats(self):
        url = 'https://fbref.com/en/comps/9/2024-2025/misc/2024-2025-Premier-League-Stats'
        data = self.extract_web_data(url, '//*[@id="stats_misc"]', "Miscellaneous")
        
        for player_data in data:
            player = self.player_manager.find(player_data[0], player_data[3])
            if player:
                misc_data = player_data[10:14] + player_data[18:20]
                player.setMiscStats(misc_data, player_data[20:23])
    
    def export_to_csv(self, filename='Bài 1/result.csv'):
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            writer.writerow(header_player)
            
            for player in self.player_manager.list_player:
                writer.writerow(row_player(player))
        
        print(f"Data exported to {filename}")
    
    def collect_all_data(self):
        self.process_standard_stats()
        self.process_goalkeeper_stats()
        self.process_shooting_stats()
        self.process_passing_stats()
        self.process_goal_creation_stats()
        self.process_defensive_stats()
        self.process_possession_stats()
        self.process_miscellaneous_stats()
        self.player_manager.sort()
        self.export_to_csv()

if __name__ == "__main__":
    crawler = DataCrawler()
    crawler.collect_all_data()
