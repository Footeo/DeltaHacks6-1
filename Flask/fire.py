# -*- coding: utf-8 -*-
"""Fire.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15cmpGu8b4wN8Il9uGoWfkxx3kgJwe2jj
"""

#import libraries
import numpy as np
import pandas as pd
pd.set_option('display.max_rows', 999)

# import matplotlib.pyplot as mp
# import seaborn as sns

#opening a data file
# from google.colab import files
# uploaded = files.upload()
data_frame = pd.read_csv(r'Flask\datasets\forestfires.csv')

#rows and columns
data_frame.head(10)
#data_frame = data_frame.drop(labels ='X',axis=1)
#data_frame = data_frame.drop(labels ='Y',axis=1)
#data_frame = data_frame.drop(labels ='month',axis=1)
#data_frame = data_frame.drop(labels ='day',axis=1)
data_frame['fire'] = 0
#data_frame = data_frame.drop(labels ='FFMC',axis=1)
#data_frame = data_frame.drop(labels ='DC',axis=1)
#data_frame = data_frame.drop(labels ='ISI',axis=1)

#get information from all rows, in column 1 (which is diagnosis) and putting it into an array of 0 and 1
data_frame.head(20)

for index, row in data_frame.iterrows():
  if float((row['area'])) > 0.0:
    data_frame.at[index,'fire'] = 1


#data_frame = data_frame.drop(labels= 0.0, axis =1)
data_frame.head(200)

from sklearn.preprocessing import OrdinalEncoder
encoder = OrdinalEncoder()
X = []#[['jan'],['feb'],['mar'],['apr'],['may'],['jun'],['jul'],['aug'],['sep'],['oct'],['nov'],['dec']]
#X.reshape(-1,1)
#encoder.fit(X)

for index, row in data_frame.iterrows():
  #print(row['month'])
  temp = [row['month']]
  X.append(temp)

#lab_Y.fit(Y)

#data_frame.iloc[:,2] = encoder.fit_transform(data_frame.iloc[:,2].values)
data_frame.iloc[:,2] = encoder.fit_transform(X)

data_frame.head(10)

#sns.heatmap(data_frame.iloc[:,0:10].corr(), annot=True, fmt = ".0%")
#sns.pairplot(data_frame.iloc[:,:1], hue='area')

# mp.subplots(figsize=(10,10))
# sns.heatmap(data_frame.iloc[:,0:14].corr(), annot=True, fmt = ".0%")
# mp.savefig('svm_conf.png', dpi=400)

# data_frame.plot(kind='density', subplots=True, layout=(4,4), sharex=False, sharey=False, figsize=(10,10))
# mp.savefig('foo.png')

encoder = OrdinalEncoder()
X = []

for index, row in data_frame.iterrows():
  temp = [row['day']]
  X.append(temp)

#lab_Y.fit(Y)

data_frame.iloc[:,3] = encoder.fit_transform(X)

data_frame.head(10)

# put data into independent (x) and dependent datasets (y)
#Y should tell us whether someone is malignant or not
#X should tell us the features

x = data_frame.iloc[:, 0:12].values
y = data_frame.iloc[:,13].values
from sklearn.model_selection import train_test_split, cross_val_score
xtrain, xtest, ytrain, ytest = train_test_split(x,y, test_size = 0.25, random_state = 0)


#Feature scaling the data; step of Data Pre Processing which is applied to independent variables or features of data
#basically helps to normalise the data within a particular range
#fit transform basically puts it into an array
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
xtrain = sc.fit_transform(xtrain)
xtest = sc.fit_transform(xtest)

#Creating different models to test our dataset

def models(xtrain, ytrain):

  #LogesticRegression; used when Y value only has 2 values
  from sklearn.linear_model import LogisticRegression
  lin = LogisticRegression (random_state = 0)
  print (sum(cross_val_score (lin, xtrain, ytrain, cv=5))/5)
  lin.fit(xtrain,ytrain)

  #Decision Tree; 
  from sklearn.tree import DecisionTreeClassifier 
  tree = DecisionTreeClassifier(criterion = "entropy", random_state = 0)
  print (sum(cross_val_score (tree, xtrain, ytrain, cv=5))/5)
  tree.fit(xtrain, ytrain)

  #random forest classifer
  from sklearn.ensemble import RandomForestClassifier
  forest = RandomForestClassifier(n_estimators = 10, criterion = 'entropy', random_state = 0)
  print (sum (cross_val_score (forest, xtrain, ytrain, cv=5))/5)
  forest.fit(xtrain, ytrain)

  from sklearn.ensemble import BaggingRegressor
  bag = BaggingRegressor()
  print (sum (cross_val_score (forest, xtrain, ytrain, cv=5))/5)
  bag.fit(xtrain,ytrain)

  #Accuracy 
  print('Logestic Regression accuracy:',lin.score(xtrain, ytrain))
  print('Decision Tree Classifer accuracy:',tree.score(xtrain, ytrain))
  print('Random Forest Classifier  accuracy:',forest.score(xtrain, ytrain))
  print('Bagging Regressor accuracy:',bag.score(xtrain, ytrain))
  return lin, tree, forest, bag

#print(ytrain)

model = models(xtrain, ytrain)

from sklearn.metrics import accuracy_score



#Random Forest Classifier  accuracy
newxtest = data_frame.iloc[:, 0:12].values
newytest = data_frame.iloc[:, 13].values
pred = model[2].predict(newxtest)

print("Prediction")
print(pred)
print()
print("Actual")
print(newytest)
print("Accuracy Score",accuracy_score(newytest, model[2].predict(newxtest)))

word = [1] * len(pred)
for i in range (len(pred)):
  if (pred[i]== 1):
    word[i] = "Fire"
  else:
    word[i] = "No Fire"
print(word)
print()