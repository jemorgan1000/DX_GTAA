"""
This is the main function for this the entire project.
- It should launch and close the gui and that is it
"""
from pipe import load, mlb_scrapping
import os


def main():
    path = os.path.dirname(os.path.realpath(os.getcwd()))
    data_path = os.path.join(path,'Data')
    mlb_path = os.path.join(data_path,'mlb2017_v1.csv')
    #loader = load.Loader()
    #files = [mlb_path]
    #df = loader.combine(files)
    #df.drop(columns=['Unnamed: 0'],inplace=True)
    syear = '2017'  # set year of season
    season = '2017-schedule-scores.shtml'  # set season ending link
    team_url_csv = os.path.join(data_path,'mlb_url.csv')
    MLBScraper = mlb_scrapping.MLBScraper(syear, season, team_url_csv)
    games_df = MLBScraper()
    print(games_df.head())

if __name__ == '__main__':
    main()