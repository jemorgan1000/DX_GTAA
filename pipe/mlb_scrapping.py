import requests
import lxml.html as lh
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np


syear='2017' #set year of season
season='2017-schedule-scores.shtml' #set season ending link
team_url_csv="mlb_url.csv"



class MLBScraper:

    def __init__(self, years, season, team_url_csv):
        self.years = years
        self.season = season
        self.team_url_csv = team_url_csv


    def get_current_season_links(self, url, team, url_ref):
        """

        :param url:
        :param team:
        :param url_ref:
        :return:
        """
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


    def get_abbrev(self):
        """
        Gets the team abbreviations
        :return:
        """
        ds=pd.read_csv(self.team_url_csv)
        team_url_list = ds.iloc[:,0].tolist()
        self.team_url_list = list(set(team_url_list))
        team_abrv=[]
        for i in team_url_list:
            team_abrv.append(i[-4:-1])
        return team_abrv

    def get_raw_data(self):
        """
        This  builds the data
        :return:
        """
        games_df = pd.DataFrame()
        team_abrv = self.get_abbrev()
        for u,w in zip(self.team_url_list, team_abrv):
            dfatl= self.get_current_season_links(u,w,season) #
            games_df = games_df.append(dfatl) #add new dataframe to empty one
        games_df= games_df[games_df[0] != None]
        games_df.columns = ['date','bx','team','home_away','opponent','win_loss','runs','runs_allowed','innings','record','rank','games_behind_raw','win_pitcher','loss_pitcher','save_pitcher','game_time','day_night_raw','attendance','streak_raw','schedule_comment','team_abbv']
        games_df['bx'].replace('', np.nan, inplace=True)
        games_df.dropna(subset=['bx'], inplace=True)
        games_df.date = games_df.date + ' ' + syear
        return games_df

    def get_home_dummies(self, games_df):
        """

        :param games_df:
        :return:
        """
        home_dummy = pd.get_dummies(games_df['home_away'])
        home_dummy.columns = ['home','away']
        home_dummy['home']
        games_df['home'] = home_dummy['home']
        return games_df

    def get_night_dummy(self, games_df):
        """

        :return:
        """
        night_dummy = pd.get_dummies(games_df['day_night_raw'])
        games_df['night_game'] = night_dummy['N']
        return games_df

    def split_wins(self, games_df):
        """

        :param games_df:
        :return:
        """
        split_wins = games_df['win_loss'].str.split('-',n=1,expand = True)
        split_wins[0]
        games_df['win_loss_new'] = split_wins[0]
        #games_df.drop(columns = ["win_loss"],inplace = True)
        games_df['innings'].replace('',9,inplace=True)
        return games_df

    def split_record(self, games_df):
        """

        :param games_df:
        :return:
        """
        split_record = games_df['record'].str.split('-',n=1,expand = True)
        split_record.columns = ['win_total','loss_total']
        games_df['win_total'] = split_record['win_total']
        games_df['loss_total'] = split_record['loss_total']
        return games_df

    def get_streaks(self, games_df):
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
        return games_df


    def get_durration(self, games_df):
        duration = []
        split_time = games_df['game_time'].str.split(':',n=1,expand = True)
        split_time
        i = 0
        for i in range(0,len(games_df.game_time)):
            duration.append(int(split_time[0].iloc[i])*60 + int(split_time[1].iloc[i]))
        games_df['game_duration'] = duration
        return games_df



    def get_games_behind(self, games_df):
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
        return games_df


    def convert_types(self, games_df):
        """

        :param games_df:
        :return:
        """
        i = 0
        games_df['runs'] = games_df['runs'].astype(int)
        games_df['runs_allowed'] = games_df['runs_allowed'].astype(int)
        games_df['innings'] = games_df['innings'].astype(int)
        return games_df

    def parse_dates(self, games_df):
        """

        :param games_df:
        :return:
        """
        reg_str = r'\([0-9]\)'
        games_df.date = pd.to_datetime(games_df.date.str.replace(reg_str, ''))
        return games_df

    def clean_attendance(self, games_df):
        """

        :param games_df:
        :return:
        """
        games_df.update(pd.to_numeric(games_df.attendance.str.replace(',', '')))
        return games_df

    def get_win_losses(self, games_df):
        games_df.insert(len(games_df.columns), 'wins', games_df.record.str.split('-').apply(lambda x: x[0]))
        games_df.insert(len(games_df.columns), 'loss', games_df.record.str.split('-').apply(lambda x: x[0]))
        games_df.drop(columns=['record'], axis=1, inplace=True)
        return games_df


    def level_df(self, games_df):
        """

        :param games_df:
        :return:
        """
        games_df_home = games_df[games_df.home_away != "@"]
        games_df_away = games_df[~(games_df.home_away != "@")]
        away_cols = ['date', 'team', 'opponent', 'wins', 'loss', 'streak', 'games_behind']
        games_df_away = games_df_away[away_cols]
        games_df_away.rename(mapper={'team': "away_team", 'opponent': 'home_team'}, axis=1, inplace=True)
        cols = ['date', 'team', 'opponent', 'wins', 'loss', 'streak', 'games_behind', 'night_game', 'streak',
                'games_behind', 'attendance']
        # probably duplicating for double headers
        games_df_home = games_df_home[cols]

        temp = games_df_home.merge(games_df_away,left_on=['date','team','opponent'],
                                       right_on=['date','home_team','away_team'],suffixes=['_home','_away'])
        temp.drop(columns=['home_team','away_team'],inplace=True)
        return temp

    def __call__(self):
        games_df = self.get_raw_data()
        games_df = self.get_home_dummies(games_df)
        games_df = self.get_night_dummy(games_df)
        games_df = self.split_wins(games_df)
        games_df = self.split_record(games_df)
        games_df = self.get_streaks(games_df)
        games_df = self.get_streaks(games_df)
        games_df = self.get_durration(games_df)
        games_df = self.get_games_behind(games_df)
        games_df = self.convert_types(games_df)
        games_df = self.parse_dates(games_df)
        games_df = self.clean_attendance(games_df)
        games_df = self.get_win_losses(games_df)
        games_df = self.level_df(games_df)
        return games_df

        