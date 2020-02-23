
from sklearn import preprocessing
import pandas as pd

class Preprocess:
    def __init__(self, df):
        """

        :param df: Dataframe of interest
        """
        df = df.loc[:,~df.columns.duplicated()]
        for col in df.columns:
            if col not in ['date','team','opponent']:
               df.loc[:,col] = pd.to_numeric(df[col])
        df = df.dropna(how='any')
        df = df.drop(columns=['team','date','opponent'])
        self.df = df




    def normalize(self, X):
        """
        This Function normalizes the data to the correct
        :return:
        """
        return preprocessing.scale(X)


    def split_xy(self, dep):
        """
        This splits the function into a dependent variable
        :param dep:
        :return:
        """
        y = self.df[dep]
        X = self.df[[col for col in self.df.columns if col != dep]]
        return X, y