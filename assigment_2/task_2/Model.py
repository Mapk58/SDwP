import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline


class LogRegression:
    """
    Logistic Regression model
    """

    def __init__(self):
        self.model = Pipeline(
            [("preprocess", StandardScaler()), ("model", LogisticRegression())]
        )

    def load(self, load_path):
        """
        Load model weights

        :param load_path: path to weights object
        :return:
        """
        with open(load_path, "rb") as f:
            self.model = pickle.load(f)

    def save(self, save_path):
        """
        Save model weights

        :param save_path: path to save model weights
        :return:
        """
        with open(save_path, "wb") as f:
            pickle.dump(f, self.model)

    def predict(self, X):
        """
        Get prediction from model

        :param X: features
        :return: predictions
        """
        return self.model.predict(X)
