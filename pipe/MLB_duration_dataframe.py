import pandas as pd
from pprint import pprint


class Duration_Matrix:
    def __init__(self, path):
        self.stadium_dict = {'LAA': 1,
                             'ARI': 2,
                             'ATL': 3,
                             'BOS': 5,
                             'BAL': 4,
                             'CHC': 6,
                             'CHW': 7,
                             'CIN': 8,
                             'CLE': 9,
                             'COL': 10,
                             'DET': 11,
                             'MIA': 12,
                             'HOU': 13,
                             'KCR': 14,
                             'LAD': 15,
                             'MIL': 16,
                             'MIN': 17,
                             'WSN': 18,
                             'NYM': 19,
                             'NYY': 20,
                             'OAK': 21,
                             'PHI': 22,
                             'PIT': 23,
                             'SDP': 24,
                             'SFG': 25,
                             'SEA': 26,
                             'STL': 27,
                             'TBR': 28,
                             'TEX': 29,
                             'TOR': 30}

        self.data = self.stadium_dict.get("Braves", "")

        self.df = pd.read_csv(path)

    def get_stadium_duration(self, Home_Team, Away_Team):
        Home = self.stadium_dict.get(Home_Team, "")
        Away = self.stadium_dict.get(Away_Team, "")
        for index, row in self.df.iterrows():
            duration = 0
            if row[0] == Home:
                if row[1] == Away:
                    duration = pprint(row[4])
        return duration

    def get_duration(self, home, away):
        for index, row in self.df.iterrows():
            if row[0] == home:
                if row[1] == away:
                    duration = row[4]
        return duration

    def get_Team_Name(self, ID):
        for name, ide in self.stadium_dict.items():
            if ide == ID:
                return name

    def get_duration_matrix(self):

        dframe = pd.DataFrame(
            [self.get_Team_Name(row[0]), self.get_Team_Name(row[1]), self.get_duration(row[0], row[1])] for index, row
            in self.df.iterrows()
        )
        return dframe
