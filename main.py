"""
This is the main function for this the entire project.
- It should launch and close the gui and that is it
"""
from pipe import load
import os


def main():
    path = os.path.dirname(os.path.realpath(os.getcwd()))
    data_path = os.path.join(path,'Data')
    mlb_path = os.path.join(data_path,'mlb_2017.csv')
    loader = load.Loader()
    files = [mlb_path]
    df = loader.combine(files)
    print(df.head())




if __name__ == '__main__':
    main()