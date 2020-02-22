import pandas as pd


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

