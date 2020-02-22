import requests
import lxml.html as lh
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np



class

syear='2017' #set year of season
season='2017-schedule-scores.shtml' #set season ending link
team_url_csv="mlb_url.csv"
csv_out= 'mlb_games.csv'


def get_current_season_links(url, team, url_ref):
    # url='https://www.baseball-reference.com/teams/ATL/'
    # url_ref='2018-schedule-scores.shtml'
    page = requests.get(url + url_ref)  # downloads html contents of the website and stores them
    # page.status_code tells if download was successful. starting with 2 is good, with 4 or 5 means wrong
    # can print content with page.content for html
    soup = BeautifulSoup(page.text, 'html.parser')  # parse HTML content for information in <p> tag

    soup_filter = soup.find("div",
                            {"id": "all_team_schedule"})  # find all instances of a certain tag, in this case "div"

    l = []
    # Loop over table rows, collect all table data entries, store row text, add to list
    for tr in soup_filter.find_all('tr')[1:]:
        tds = tr.find_all('td')
        row = [tr.text for tr in tds]
        l.append(row)

    dfout = pd.DataFrame(l)

    dfout['Team'] = team

    return dfout


ds=pd.read_csv(team_url_csv)
team_url_list = ds.iloc[:,0].tolist()
team_url_list = list(set(team_url_list))
team_abrv=[]
for i in team_url_list:
    team_abrv.append(i[-4:-1])

games_df = pd.DataFrame()
for u,w in zip(team_url_list,team_abrv):
    #print(u)
    #print(w)
    dfatl=get_current_season_links(u,w,season) #
    games_df=games_df.append(dfatl) #add new dataframe to empty one

games_df= games_df[games_df[0] != None]
games_df.columns = ['date','bx','team','home_away','opponent','win_loss','runs','runs_allowed','innings','record','rank','games_behind_raw','win_pitcher','loss_pitcher','save_pitcher','game_time','day_night_raw','attendance','streak_raw','schedule_comment','team_abbv']
games_df['bx'].replace('', np.nan, inplace=True)
games_df.dropna(subset=['bx'], inplace=True)
games_df.date = games_df.date + ' ' + syear
print(games_df.head(10))

home_dummy = pd.get_dummies(games_df['home_away'])
home_dummy.columns = ['home','away']
home_dummy['home']
games_df['home'] = home_dummy['home']
games_df.head()


night_dummy = pd.get_dummies(games_df['day_night_raw'])
night_dummy
games_df['night_game'] = night_dummy['N']
games_df.head()


split_wins = games_df['win_loss'].str.split('-',n=1,expand = True)
split_wins[0]
games_df['win_loss_new'] = split_wins[0]
#games_df.drop(columns = ["win_loss"],inplace = True)
games_df.head()

games_df['innings'].replace('',9,inplace=True)
games_df.head()


split_record = games_df['record'].str.split('-',n=1,expand = True)
split_record.columns = ['win_total','loss_total']
split_record
games_df['win_total'] = split_record['win_total']
games_df['loss_total'] = split_record['loss_total']
games_df.head()


streaks = []
i = 0
#len(games_df.streak_raw)
for i in range(0,len(games_df.streak_raw)):
    streaks.append(len(games_df.streak_raw.iloc[i]))
    if games_df.streak_raw.iloc[i].find("-") == 0:
        streaks[i] = streaks[i] * -1
    else:
        streaks[i] = streaks[i]
games_df['streak'] = streaks
games_df.head()



games_df.game_time.head()
duration = []
split_time = games_df['game_time'].str.split(':',n=1,expand = True)
split_time
i = 0
for i in range(0,len(games_df.game_time)):
    duration.append(int(split_time[0].iloc[i])*60 + int(split_time[1].iloc[i]))
games_df['game_duration'] = duration
games_df.head()




i = 0
gb = []
for i in range(0,len(games_df.games_behind_raw)):
    if games_df.games_behind_raw.iloc[i] == " Tied":
        gb.append(0.0)
    elif games_df.games_behind_raw.iloc[i].find(" ") == 0:
        if games_df.games_behind_raw.iloc[i].find("up") == 0:
            split_space = games_df['games_behind_raw'].iloc[i].split(' ')
            x = float(split_space[1])
            gb.append(x)
        else:
            gb.append(float(games_df.games_behind_raw.iloc[i]) * -1)
    else:
        gb.append(float(games_df.games_behind_raw.iloc[i][len("up"):]))
games_df['games_behind'] = gb
games_df.head()


i = 0
games_df['runs'] = games_df['runs'].astype(int)
games_df['runs_allowed'] = games_df['runs_allowed'].astype(int)
games_df['innings'] = games_df['innings'].astype(int)


games_df.to_csv(csv_out+syear+'.csv')