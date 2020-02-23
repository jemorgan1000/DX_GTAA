import pandas as pd
from pprint import pprint


class Loader:
    """
    This file loads the
    :param files: dictionary of files and locations to pull data from
    """

    def load_file(self, file):
        """
        :param file:
        :return:
        """
        return pd.read_csv(file)

    def combine(self, files):
        """
        :param files:
        :return:
        """
        if len(files) > 1:
            dfs = [pd.read_csv(file) for file in files]
            df = pd.concat(dfs)
        else:
            df = pd.read_csv(files[0])
        if 'attendance' not in df.columns:
            raise Exception('Crucial variable not found')
        return df

    def append_durations(self, games_df, dur_df):
        """
        :param games_df:
        :param dur_df:
        :return:
        """

        duration = []
        for index, row in games_df.iterrows():
            key1 = row[1]
            key2 = row[2]
            value = 0
            for index1, row1 in dur_df.iterrows():
                if row1[0] == key1:
                    if row1[1] == key2:
                        value = row1[2]
                        break
            duration.append(value)
        games_df['duration'] = duration
        return games_df

    def append_weather(self, games_df, path):
        temp = []
        weather = []
        dates = games_df['date']
        df = pd.read_csv(path)
        for index, row in games_df.iterrows():
            key = row[0].strftime('%Y-%m-%d')
            w = 'poop'
            t = 0
            for index1, row1 in df.iterrows():
                if row1[9] == key:
                    t = row1[10]
                    w = row1[4]
                    break
            temp.append(t)
            weather.append(w)
        games_df['temp'] = temp
        games_df['weather'] = weather
        return games_df

    def append_capacity(self, games_df, path):
        max = []
        percent = []
        df = pd.read_csv(path)
        for index, row in games_df.iterrows():
            key = row[1]
            m = 0
            p = row[10]
            if p == '':
                p = 0
            for index1, row1 in df.iterrows():
                if row1[0] == key:
                    m = row1[1]
                    p = p / m
                    break
            max.append(m)
            percent.append(p)
        games_df['max_capacity'] = max
        games_df['percent_full'] = percent
        return games_df

    def append_divisions(self, games_df, path):
        conf = []
        div = []
        df = pd.read_csv(path)
        for index, row in games_df.iterrows():
            key1 = row[1]  # home
            key2 = row[2]  # away
            d = 0
            c = 0
            found = 0
            for index1, row1 in df.iterrows():
                for index2, row2 in df.iterrows():
                    if row1[0] == key1 & row2[0] == key2:
                        d = row1[1] == row2[1]
                        c = row1[0] == row2[0]
                        found = 1
                        break
                if found == 1:
                    break
            conf.append(c)
            div.append(d)
        games_df['conference'] = conf
        games_df['division'] = div
        return games_df
