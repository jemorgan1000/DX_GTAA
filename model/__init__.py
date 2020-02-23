
from sklearn import linear_model
from sklearn import svm
from sklearn import ensemble
from sklearn import metrics

class Models:

    def __init__(self,X,y):
        """

        :param X: is the dataframe before entering
        :param y: is the target variable
        """
        self.X = X
        self.y = y

    def fit_ols(self):
        """

        :return:
        """
        ols = linear_model.LinearRegression()
        ols.fit(self.X, self.y)
        return ols

    def fit_svr(self):
        """

        :return:
        """
        svr = svm.SVR()
        svr.fit(self.X, self.y)
        return svr

    def fit_elastic(self):
        elastic = linear_model.ElasticNetCV()
        elastic.fit(self.X,self.y)
        return elastic

    def fit_random_forest(self):
        rf = ensemble.RandomForestRegressor(n_estimators=200,oob_score=True,criterion='mae')
        rf.fit(self.X, self.y)
        return rf

    def test(self, mod, Xtest, ytest):
       return metrics.mean_squared_error(mod.predict(Xtest),ytest), metrics.r2_score(mod.predict(Xtest),ytest)

