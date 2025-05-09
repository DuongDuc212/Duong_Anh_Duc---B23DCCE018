from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import time
import pandas as pd

csv_file = 'Bài 1/result.csv'
stats_df = pd.read_csv(csv_file)
filtered_players = stats_df[stats_df['minutes'] > 900][['name', 'team']].drop_duplicates()
filtered_players_set = set(zip(filtered_players['name'].str.strip(), filtered_players['team'].str.strip()))

driver = uc.Chrome()
wait = WebDriverWait(driver, 10)

link = 'https://www.footballtransfers.com/us/leagues-cups/national/uk/premier-league'
driver.get(link)

time.sleep(3)

all_team_data = []

driver.execute_script("window.scrollBy(0, 300);")
time.sleep(1)

try:
    cookie_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Accept') or contains(text(), 'Cookie') or contains(text(), 'Close')]")
    for button in cookie_buttons:
        driver.execute_script("arguments[0].click();", button)
        time.sleep(0.5)
except:
    pass

wait.until(EC.presence_of_element_located((By.TAG_NAME, 'tbody')))
teams_table = driver.find_element(By.TAG_NAME, 'tbody')
all_teams = teams_table.find_elements(By.TAG_NAME, 'tr')

for i in range(len(all_teams)):
    teams_table = driver.find_element(By.TAG_NAME, 'tbody')
    all_teams = teams_table.find_elements(By.TAG_NAME, 'tr')
    team = all_teams[i]
    
    team_name = team.find_elements(By.TAG_NAME, 'td')[2].text
    print(f"Processing team: {team_name}")
    
    try:
        team_link = team.find_element(By.TAG_NAME, 'a')
        team_url = team_link.get_attribute('href')
        
        driver.get(team_url)
    except Exception as e:
        print(f"Could not find team link, trying JavaScript click: {str(e)}")
        driver.execute_script("arguments[0].click();", team)
    
    time.sleep(3)
    
    player_data = []
    try:
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'tbody')))
        
        players_table = driver.find_element(By.TAG_NAME, 'tbody')
        players = players_table.find_elements(By.TAG_NAME, 'tr')
        
        print(f"  Found {len(players)} players")
        
        for player in players:
            try:
                player_name_elem = player.find_element(By.XPATH, ".//th[@class='td-player']//a")
                player_name = player_name_elem.text.strip()
                
                if (player_name, team_name) not in filtered_players_set:
                    print(f"  - Skipping player: {player_name} (not in filtered list or under 900 minutes)")
                    continue
                
                try:
                    transfer_value = player.find_element(By.CLASS_NAME, 'player-tag').text
                except:
                    try:
                        transfer_value = player.find_element(By.XPATH, ".//td[contains(@class, 'value')]").text
                    except:
                        transfer_value = "Not available"
                
                player_data.append({
                    'Team': team_name,
                    'Player': player_name,
                    'Transfer Value': transfer_value
                })
                print(f"  - Added player: {player_name}, Value: {transfer_value}")
            except Exception as e:
                print(f"  - Error extracting player data: {str(e)}")
    
    except Exception as e:
        print(f"Error finding players: {str(e)}")
    
    all_team_data.extend(player_data)
    
    driver.get(link)
    time.sleep(3)
    
    driver.execute_script("window.scrollBy(0, 300);")
    time.sleep(1)

df = pd.DataFrame(all_team_data)

df.to_csv('Bài 4/premier_league_player_values.csv', index=False)
print(f"Data saved to 'premier_league_player_values.csv'. Total players: {len(all_team_data)}")

driver.quit()