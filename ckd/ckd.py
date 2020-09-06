# -*- coding: utf-8 -*-
"""CKD.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rBjpZbdYb6RV8psKyp1jgvLVMq6K1FtH
"""

# description: this program classifies patients as having chronic kidney disease (ckd) or not
#               using Artificial Neural Networks (ANN)

#import libraries
import glob
from keras.models import Sequential, load_model
import numpy as np
import pandas as pd
from keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
import matplotlib.pyplot as plt
import keras as k
import keras.initializers

#Load the data
from google.colab import files
uploaded = files.upload()

df = pd.read_csv('kd.csv')
#print the first 5 rows
df.head()

#get the shape of the data(the number of rows &cols)
df.shape

#create a list of column names to keep
columns_to_retain = ['sg','al','sc','hemo','pcv','dm','htn','classification']

#Drop the columns that are not in columns_to_retain
df = df.drop(  [col for col in df.columns if not col in columns_to_retain] , axis=1  )

#Drop the rows with na or missing values
df = df.dropna(axis=0)

#Transform the non-numeric data in the columns
for column in df.columns:
  if df[column].dtype == np.number:
    continue
  df[column] = LabelEncoder().fit_transform( df[column] )

#Print the First 5 rows of the new cleaned data set
df.head()

#split the data into independent (x) data set and dependent (y) data set (the target)
X = df.drop(['classification'], axis=1)
y = df['classification']

#Feature Scaling
#min-max scaler method scales the data set so that all the input features lie between 0 and 1
x_scaler = MinMaxScaler()
x_scaler.fit(X)
column_names = X.columns
X[column_names] = x_scaler.transform(X)

#split the data into 80% training and 20% testing &shuffle
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, shuffle=True)

#Build the model
model = Sequential()
model.add( Dense(256, input_dim = len(X.columns) , kernel_initializer = k.initializers.random_normal(seed=13), activation='relu'))
model.add( Dense(1, activation= 'hard_sigmoid'))

#compile the model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

#Train the model
history = model.fit(X_train, y_train, epochs = 2000, batch_size= X_train.shape[0])

#save the model
model.save('ckd.model')

#visualize the model loss and accuracy
plt.plot(history.history['accuracy'])
plt.plot(history.history['loss'])
plt.title('model accuracy and loss')
plt.title('accuracy and loss')
plt.xlabel('epoch')

print('shape of the training data:', X_train.shape)
print('shape of test data:', X_test.shape)

#shown the actual and predicted values
pred = model.predict(X_test)  
pred =  [1 if y>=0.5 else 0 for y in pred]
pred

print('Original  : {0}' .format(", ".join(str(x) for x in y_test)))
print('Predicted : {0}' .format(", ".join(str(x) for x in pred)))