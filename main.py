"""
This is the main function for this the entire project.
- It should launch and close the gui and that is it
"""
from pipe import load, mlb_scrapping, preprocess
from model import Models
import os

def main():
    path = os.path.dirname(os.path.realpath(os.getcwd()))
    data_path = os.path.join(path,'Data')
    years = [str(x) for x in range(2012,2018)]
    seasons = [f"{x}-schedule-scores.shtml" for x in range(2012,2018)]
    test_season = '2019-schedule-scores.shtml'
    team_url_csv = os.path.join(data_path,'mlb_url.csv')
    MLBScraper = mlb_scrapping.MLBScraper(years[0], seasons[0], team_url_csv)
    games_df = MLBScraper()
    for i, year in enumerate(years[1:]):
        MLBScraper = mlb_scrapping.MLBScraper(year, seasons[i], team_url_csv)
        games_df.append(MLBScraper())
    print(list(games_df.columns))
    # building test_df
    MLBScraper = mlb_scrapping.MLBScraper("2019", test_season, team_url_csv)
    test_df = MLBScraper()
    test_df = test_df[test_df['team'] == 'ATL']
    test_preprocessor = preprocess.Preprocess(test_df)
    Xtest, ytest = test_preprocessor.split_xy('attendance')
    preprocessor = preprocess.Preprocess(games_df)
    X,y = preprocessor.split_xy('attendance')
    modeler = Models(X,y)
    rf = modeler.fit_random_forest()
    print(rf.score(X,y))
    print(list(rf.predict(Xtest) - ytest))
    print("Scoring for the 2019 braves season")
    rmse,r2 = modeler.test(rf,Xtest,ytest)
    print(f"RMSE : {rmse}")
    print(f'r2 : {r2}')

if __name__ == '__main__':
    main()