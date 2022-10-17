import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

class LogRegression:
    def __init__(self):
        self.model =  Pipeline([
            ('preprocess', StandardScaler()),
            ('model', LogisticRegression())
        ])

    def load(self, load_path):
        with open(load_path, 'rb') as f:
            self.model = pickle.load(f)

    def save(self, save_path):
        with open(save_path, 'wb') as f:
            pickle.dump(f, self.model)

    def predict(self, X):
        return self.model.predict(X)

