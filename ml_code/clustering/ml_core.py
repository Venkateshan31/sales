import numpy as np
import pandas as pd
import pickle
from matplotlib import pyplot as plt
from sklearn import metrics
from sklearn import model_selection
from sklearn import preprocessing
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib

plt.rcParams['figure.figsize'] = (16, 9)
plt.style.use('ggplot')
data = pd.read_csv('ml_code/clustering/dataset.csv')

f1 = data['back_camera'].values
f2 = data['front_camera'].values
f3 = data['resolution_1'].values
f4 = data['resolution_2'].values
f5 = data['screen_size'].values
f6 = data['battery'].values
f7 = data['price'].values
f8 = data['sales'].values

X = np.array(list(zip(f1, f2, f3, f4, f5, f6, f7, f8)))
X2 = np.array(list(zip(f1, f2, f3, f4, f5, f6, f7)))

k = 4
clf = KMeans(init='k-means++', n_clusters=k, n_init=10)
clf = clf.fit(X)
labels = clf.predict(X)
C = clf.cluster_centers_

colors = ['r', 'g', 'b', 'y']
fig, ax = plt.subplots()
for i in range(k):
    points = np.array([X[j] for j in range(len(X)) if labels[j] == i])
    ax.scatter(points[:, 1], points[:, 2], s=7, c=colors[i])
ax.scatter(C[:, 1], C[:, 2], marker='*', s=300, c='#050505')
print("Silhouette Score: %.7f" % (metrics.silhouette_score(X, labels, metric='euclidean')))
y = clf.labels_
# print(y)
data2 = data.drop('sales', axis=1)
data2['y'] = y
X_train, X_test, y_train, y_test = train_test_split(X2, y, test_size=0.3, random_state=0)
logreg = LogisticRegression()
logreg.fit(X_train, y_train)
print('Accuracy of logistic regression on training set: {:.2f}'.format(logreg.score(X_train, y_train)))
print('Accuracy of logistic regression on test set: {:.2f}'.format(logreg.score(X_test, y_test)))
kfold = model_selection.KFold(n_splits=10, random_state=7)
results = model_selection.cross_val_score(logreg, X_train, y_train, cv=kfold, scoring="accuracy")
print("10-fold cross validation average accuracy: %.3f" % (results.mean()))
X_new = [[10, 5, 5400, 5400, 5, 2000, 100]]
y_pred = logreg.predict(X_new)

data3 = data2.loc[data2['y'] == y_pred[0]]
data3 = data3.drop('y', axis=1)
data3['sales'] = data['sales']


X3 = data3.iloc[:, :-1].values
y2 = data3.iloc[:, 7].values
X2_train, X2_test, y2_train, y2_test = train_test_split(X3, y2, test_size=0.3, random_state=0)
scaler = preprocessing.StandardScaler().fit(X2_train)
scaler.transform(X2_train)
scaler.transform(X2_test)
lreg = LinearRegression()
lreg.fit(X2_train, y2_train)
print('Accuracy of linear regression on training set: {:.2f}'.format(lreg.score(X2_train, y2_train)))
print('Accuracy of linear regression on test set: {:.2f}'.format(lreg.score(X2_test, y2_test)))
y_pred2 = lreg.predict(X_new)
print("Predicted Sales: %.3f" % (y_pred2[0]))

'''
fig,ax = plt.subplots()  
ax.scatter(data2['quarter'], data2['sales'], marker='*', s=300, c='#050505')       
'''

# Saving the Logistic Regression Model
classifier_model = pickle.dumps(clf)
regression_model = pickle.dumps(logreg)

# Saving the model to a file
joblib.dump(clf, 'classifier_model.pkl')
joblib.dump(logreg, 'regression_model.pkl')