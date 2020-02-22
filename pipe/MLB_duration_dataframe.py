import pandas as pd
from pprint import pprint

stadium_dict = {'Angels':1,
                'Diamondbacks':2,
                'Braves':3,
                'Red Sox':5,
                'Orioles':4,
                'Cubs':6,
                'White Sox':7,
                'Reds': 8,
                'Indians':9,
                'Rockies':10,
                'Tigers':11,
                'Marlins':12,
                'Astros':13,
                'Royals':14,
                'Dodgers':15,
                'Brewers':16,
                'Twins':17,
                'Nationals':18,
                'Mets':19,
                'Yankees':20,
                'Athletics':21,
                'Phillies':22,
                'Pirates':23,
                'Padres':24,
                'Giants':25,
                'Mariners':26,
                'Cardinals':27,
                'Rays':28,
                'Rangers':29,
                'Blue Jays':30}

data =stadium_dict.get("Braves","")

df = pd.read_csv('MLB.csv')

def get_stadium_duration(Home_Team,Away_Team):
    Home = stadium_dict.get(Home_Team,"")
    Away = stadium_dict.get(Away_Team,"")
    for index,row in df.iterrows():
        duration = 0
        if row[0] == Home:
            if row[1] == Away:
                duration = pprint(row[4])
    return duration

def get_duration(home,away):
    for index, row in df.iterrows():
        if row[0]==home:
            if row[1]==away:
                duration = row[4]
    return duration


def get_Team_Name(ID):
    for name, ide in stadium_dict.items():
        if ide == ID:
            return name

def get_duration_matrix():

    dframe = pd.DataFrame(
        [get_Team_Name(row[0]), get_Team_Name(row[1]), get_duration(row[0],row[1])] for index,row in df.iterrows()
    )
    return dframe



pprint(get_duration_matrix())
