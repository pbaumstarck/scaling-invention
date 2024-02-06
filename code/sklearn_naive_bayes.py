#!/usr/bin/env python3

import numpy as np

# load the iris dataset
from sklearn.datasets import load_iris
iris = load_iris()
   
# store the feature matrix (X) and response vector (y)
X = iris.data
y = iris.target


import matplotlib.pyplot as plt


   
# splitting X and y into training and testing sets
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=1)
# breakpoint()
   
# training the model on training set
from sklearn.naive_bayes import GaussianNB
gnb = GaussianNB()
gnb.fit(X_train, y_train)
   
# making predictions on the testing set
y_pred = gnb.predict(X_test)
   
# comparing actual response values (y_test) with predicted response values (y_pred)
from sklearn import metrics
print("Gaussian Naive Bayes model accuracy(in %):", metrics.accuracy_score(y_test, y_pred)*100)
breakpoint()

ixes = np.nonzero(y_test != y_pred)
print('nonzeroes:', ixes)

feature1 = 0
feature2 = 3

_, ax = plt.subplots()
scatter = ax.scatter(iris.data[:, feature1], iris.data[:, feature2], c=iris.target)
scatter = ax.scatter(iris.data[ixes, feature1], iris.data[ixes, feature2], c='r')
ax.set(xlabel=iris.feature_names[feature1], ylabel=iris.feature_names[feature2])
_ = ax.legend(
    scatter.legend_elements()[0], iris.target_names, loc="lower right", title="Classes"
)
plt.show()
