import pandas as pd
import pickle
import numpy as np

class LogRegression:
    def __init__(self, scaler=None, n_iter=100, lr=1e-3):
        self.w = None
        self.b = None
        self.n_iter = n_iter
        self.lr = lr
        self.mean = None
        self.std = None

    def load(self, load_path):
        with open(load_path, 'rb') as f:
            weight_data = pickle.load(f)
        self.w = weight_data['w']
        self.b = weight_data['b']
        self.mean = weight_data['scaler_mean']
        self.std = weight_data['scaler_std']

    def save(self, save_path):
        with open(save_path, 'wb') as f:
            pickle.dump(f, {'w':self.w, 'b':self.b, 'scaler':self.scaler})

    # update even chunks of data
    def train(self, X, y):
        X = (X - self.mean) / self.std
        self.w = np.random.rand(X.shape[1])
        self.b = 0

        for i in range(self.n_iter):
            pred = self.predict_proba(X)
            grad_w = 2 / self.w.shape[0] * (X.T @ (pred - y))
            # ??
            grad_b = 2 / self.w.shape[0] * (pred - y).mean()
            self.w = self.w - self.lr * grad_w
            self.b = self.b - self.lr * grad_b

    def predict_proba(self, X):
        X = (X - self.mean) / self.std
        sigmoid = lambda z: 1 / (1 + np.exp(-z))
        return sigmoid(self.w @ X.T + self.b).squeeze()

    def predict(self, X):
        return (self.predict_proba(X) > 0.5) * 1
    
    
def train_model(df,current_date):
    model = LogRegression()
    model.load('pretrained_data.pickle')    
    model.save('')
    
