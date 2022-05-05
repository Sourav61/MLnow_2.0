# -*- coding: utf-8 -*-
"""3.1_Univariate.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/Sourav61/MLnow_2.0/blob/main/3.1_Univariate.ipynb
"""

#@title This notebook was created for code illustration of the `ML.now()` course

print('''
`Univariate Linear Regression`

[Link to Download the dataset](https://www.kaggle.com/arashnic/hr-ana?select=train.csv)

**Date Created**: 
June 11, 2021

**Author**:
 Sourav Pahwa

**Reach out**:
[GitHub](https://github.com/Sourav61) | [LinkedIn](https://www.linkedin.com/in/sourav-pahwa-93b4041b6/) | [Gmail](mailto:sourav61pahwa@gmail.com)

[[Course Repository](https://github.com/Sourav61/MLnow_2.0)]

Feel free to check out my [website](https://sourav61.github.io/progate/) for more information''')

# from google.colab import drive
# drive.mount('/content/drive')

import numpy as np
import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt
import missingno as msno

import sklearn
from scipy import stats
import imblearn

import warnings
warnings.filterwarnings('ignore')

plt.rcParams['figure.figsize'] = (16,5)
plt.style.use('fivethirtyeight')

plt.style.available

df = pd.read_csv('train.csv')
dft = pd.read_csv('test.csv')

print("The shape of training Data is: ", df.shape)

print("The shape of training Data is: ", dft.shape)

df.columns

dft.columns

df.describe().style.background_gradient(cmap='PuBu', low=0, high=0, axis=0, subset=None, text_color_threshold=0.408, vmin=None, vmax=None)

df.describe(include="object")

df.info()

dft.info()

df.head(10)

df.tail(10)

dft.head(10)

dft.tail(10)

def inspect_data(data):
    return pd.DataFrame({"Data Type":data.dtypes,"No of Levels":data.apply(lambda x: x.nunique(),axis=0), "Levels":data.apply(lambda x: str(x.unique()),axis=0)})
inspect_data(df)

df.dtypes

df.duplicated().sum()

df.isnull().sum(axis=0)

df_total = df.isnull().sum()

df_percent = ((df.isnull().sum()/df.shape[0])*100).round(2)

dft_total = dft.isnull().sum()

dft_percent = ((dft.isnull().sum()/dft.shape[0])*100).round(2)

df_missing_data = pd.concat([df_total, df_percent, dft_total, dft_percent],
                                axis=1, 
                                keys=['df_Total', 'df_Percent %','dft_Total', 'dft_Percent %'],
                                sort = True)

df_missing_data.style.bar(color = ['green'])

msno.matrix(df.drop('employee_id', axis='columns').sample(500))
plt.show()

msno.bar(df.drop('employee_id', axis='columns'))
plt.show()

msno.matrix(dft.drop('employee_id', axis='columns').sample(500))
plt.show()

msno.bar(dft.drop('employee_id', axis='columns'))
plt.show()

df['education'] = df['education'].fillna(df['education'].mode()[0])
df['previous_year_rating'] = df['previous_year_rating'].fillna(df['previous_year_rating'].mode()[0])

print("Number of Missing Values Left in the Training Data :", df.isnull().sum().sum())

dft['education'] = dft['education'].fillna(dft['education'].mode()[0])
dft['previous_year_rating'] = dft['previous_year_rating'].fillna(dft['previous_year_rating'].mode()[0])

print("Number of Missing Values Left in the Training Data :", dft.isnull().sum().sum())

msno.matrix(df.drop('employee_id', axis='columns').sample(500))
plt.show()

msno.bar(df.drop('employee_id', axis='columns'))
plt.show()

msno.matrix(dft.drop('employee_id', axis='columns').sample(500))
plt.show()

msno.bar(dft.drop('employee_id', axis='columns'))
plt.show()

plt.rcParams['figure.figsize'] = (15, 5)
plt.style.use('fivethirtyeight')

plt.subplot(1, 2, 1)
sns.countplot(df['is_promoted'],)

plt.xlabel('Promoted or Not?', fontsize = 15)

plt.subplot(1, 2, 2)
df['is_promoted'].value_counts().plot(kind = 'pie', explode = [0, 0.1], autopct = '%.2f%%', startangle = 90,
                                       labels = ['1','0'], shadow = True, pctdistance = 0.5)
plt.axis('off')

plt.suptitle('Target Class Balance', fontsize = 20)
plt.legend()
plt.show()

plt.figure(figsize = (14, 6)) 
plt.subplot(1,1,1)
sns.distplot(df["is_promoted"], bins = 20)
plt.show()

df1 = df[['no_of_trainings', 'age', 'previous_year_rating', 'length_of_service', 'KPIs_met >80%', 'awards_won?', 'avg_training_score', 'is_promoted']]

df1.head(10)

df1.tail(10)

sns.pairplot(df1,
             x_vars = [ 'is_promoted', 'no_of_trainings', 'length_of_service', 'KPIs_met >80%', 'awards_won?', 'avg_training_score' ],
             y_vars = [ 'is_promoted', 'no_of_trainings', 'KPIs_met >80%', 'awards_won?' ],
       diag_kind='kde', hue='is_promoted'
             )
plt.show()

sns.pairplot(df1,
             x_vars = [ 'is_promoted', 'no_of_trainings', 'age', 'previous_year_rating', 'length_of_service', 'KPIs_met >80%', 'awards_won?', 'avg_training_score'],
             y_vars = [ 'is_promoted', 'no_of_trainings', 'age', 'previous_year_rating', 'length_of_service', 'KPIs_met >80%', 'awards_won?', 'avg_training_score' ],
       diag_kind='kde', hue='is_promoted'
             )
plt.show()

sns.stripplot(y='length_of_service', x='awards_won?', data=df1)

fig, axarr = plt.subplots(3,2, figsize=(20,20))

sns.stripplot(y='length_of_service', x='awards_won?', data=df1, hue=None, ax=axarr[0][0])
sns.stripplot(y='length_of_service', x='is_promoted', data=df1, hue=None, ax=axarr[1][1])
sns.stripplot(y='previous_year_rating', x='is_promoted', data=df1, hue=None, ax=axarr[1][0])
sns.stripplot(y='KPIs_met >80%', x='is_promoted', data=df1, hue=None,  ax=axarr[0][1])
sns.stripplot(y='avg_training_score', x='is_promoted', data=df1, hue=None, ax=axarr[2][0])
sns.stripplot(y='no_of_trainings', x='is_promoted', data=df1, hue=None, ax=axarr[2][1])
plt.show()

df.select_dtypes('number').head(50)

plt.rcParams['figure.figsize'] = (15, 5)
plt.style.use('fivethirtyeight')

plt.subplot(1, 5, 1)
sns.boxplot(df['employee_id'], color = 'red')
plt.xlabel('employee id', fontsize = 12)
plt.ylabel('Range', fontsize = 12)

plt.subplot(1, 5, 2)
sns.boxplot(df['no_of_trainings'], color = 'red')
plt.xlabel('no_of_trainings', fontsize = 12)
plt.ylabel('Range', fontsize = 12)

plt.subplot(1, 5, 3)
sns.boxplot(df['age'], color = 'red')
plt.xlabel('age', fontsize = 12)
plt.ylabel('Range', fontsize = 12)

plt.subplot(1, 5, 4)
sns.boxplot(df['previous_year_rating'], color = 'red')
plt.xlabel('previous_year_rating', fontsize = 12)
plt.ylabel('Range', fontsize = 12)

plt.subplot(1, 5, 5)
sns.boxplot(df['length_of_service'], color = 'red')
plt.xlabel('Length of Service', fontsize = 12)
plt.ylabel('Range', fontsize = 12)

plt.rcParams['figure.figsize'] = (15, 5)
plt.style.use('fivethirtyeight')

plt.subplot(1, 4, 1)
sns.boxplot(df['KPIs_met >80%'], color = 'red')
plt.xlabel('KPIs_met >80%', fontsize = 12)
plt.ylabel('Range', fontsize = 12)

plt.subplot(1, 4, 2)
sns.boxplot(df['awards_won?'], color = 'red')
plt.xlabel('awards_won?', fontsize = 12)
plt.ylabel('Range', fontsize = 12)

plt.subplot(1, 4, 3)
sns.boxplot(df['avg_training_score'], color = 'red')
plt.xlabel('Average Training Score', fontsize = 12)
plt.ylabel('Range', fontsize = 12)

plt.subplot(1, 4, 4)
sns.boxplot(df['is_promoted'], color = 'red')
plt.xlabel('is_promoted', fontsize = 12)
plt.ylabel('Range', fontsize = 12)

df[df['length_of_service'] > 13]

plt.rcParams['figure.figsize'] = (16,5)
plt.style.use('fivethirtyeight')

plt.subplot(1, 3, 1)
labels = ['0','1']
sizes = df['KPIs_met >80%'].value_counts()
colors = plt.cm.Wistia(np.linspace(0, 1, 4))
explode = [0, 0]

plt.pie(sizes, labels = labels, colors = colors, explode = explode, shadow = True, startangle = 90)
plt.title('KPIs Met > 80%', fontsize = 20)
 
plt.subplot(1, 3, 2)
labels = ['1', '2', '3', '4', '5']
sizes = df['previous_year_rating'].value_counts()
colors = plt.cm.Wistia(np.linspace(0, 1, 4))
explode = [0, 0, 0, 0, 0.1]

plt.pie(sizes, labels = labels, colors = colors, explode = explode, shadow = True, startangle = 90)
plt.title('Previous year Ratings', fontsize = 20)

plt.subplot(1, 3, 3)
labels = ['0', '1']
sizes = df['awards_won?'].value_counts()
colors = plt.cm.Wistia(np.linspace(0, 1, 4))
explode = [0,0.2]

plt.pie(sizes, labels = labels, colors = colors, explode = explode, shadow = True, startangle = 90)
plt.title('Awards Won?', fontsize = 20)

plt.legend()
plt.show()

plt.rcParams['figure.figsize'] = (17, 4)
sns.countplot(df['no_of_trainings'], palette = 'husl')
plt.xlabel(' ', fontsize = 15)
plt.title('Distribution of Trainings undertaken by the Employees')
plt.show()

plt.rcParams['figure.figsize'] = (17, 4)
sns.distplot(df['no_of_trainings'])
plt.show()

plt.rcParams['figure.figsize'] = (8, 4)
plt.hist(df['age'], color='cyan')
plt.title('Distribution of Age among the Employees', fontsize = 15, c='m')
plt.xlabel('Age of the Employees', color='blue')
plt.grid()
plt.show()

plt.rcParams['figure.figsize'] = (12, 6)
sns.countplot(y = df['department'], palette = 'gist_stern_r', orient = 'v')
plt.xlabel('')
plt.ylabel('Department Name', fontsize=15, fontweight=2, color='red')
plt.title('Distribution of Employees in Different Departments', fontsize = 20, fontweight = 2, color='green')
plt.grid()

plt.show()

plt.rcParams['figure.figsize'] = (12,15)
plt.style.use('fivethirtyeight')
sns.countplot(y = df['region'], palette = 'inferno', orient = 'v')
plt.xlabel('')
plt.ylabel('Region',color='red', fontweight=2)
plt.title('Different Regions', fontsize = 20, color="brown", fontweight=2)
plt.xticks(rotation = 45)
plt.yticks(rotation = 30)
plt.grid()
plt.show()

plt.rcParams['figure.figsize'] = (16,5)

plt.subplot(1, 3, 1)
labels = df['education'].value_counts().index
# print(labels)
sizes = df['education'].value_counts()
colors = plt.cm.copper(np.linspace(0, 1, 5))
explode = [0, 0, 0.1]

plt.pie(sizes, labels = labels, colors = colors, explode = explode, shadow = True, startangle = 90)
plt.title('Education', fontsize = 20)

plt.subplot(1, 3, 2)
labels = df['gender'].value_counts().index
sizes = df['gender'].value_counts()
colors = plt.cm.copper(np.linspace(0, 1, 5))
explode = [0, 0.1]

plt.pie(sizes, labels = labels, colors = colors, explode = explode, shadow = True, startangle = 90)
plt.title('Gender', fontsize = 20)

plt.subplot(1, 3, 3)
labels = df['recruitment_channel'].value_counts().index
print(labels)
sizes = df['recruitment_channel'].value_counts()
colors = plt.cm.copper(np.linspace(0, 1, 5))
explode = [0, 0, 0.1]

plt.pie(sizes, labels = labels, colors = colors, explode = explode, shadow = True, startangle = 90)
plt.title('Recruitment Channel', fontsize = 20)

plt.show()

df2 = df1[['avg_training_score', 'is_promoted']]
df2.head(10)

df2.tail(10)

sns.pairplot(df2,
             x_vars = ['avg_training_score', 'is_promoted'],
             y_vars =  ['avg_training_score', 'is_promoted'],
       diag_kind='kde'
             )

dftrain = df2.sample(frac=0.8, random_state=0) 
dftest = df2.drop(dftrain.index)

print(dftrain.head(10))
print(dftest.head(10))

print(dftrain.shape)
print(dftest.shape)

dftrain = dftrain.copy()
dftest = dftest.copy()

print(dftrain.head(10))
print(dftest.head(10))

dftr = dftrain.pop('is_promoted')
dfte = dftest.pop('is_promoted')

print(dftr.head(10))
print(dfte.head(10))

print(dftrain.head())
print(dftest.head())

import math

numFeatures = len(dftrain.columns)
inputNeurons = (2*numFeatures)/3
print(math.ceil(inputNeurons))

import tensorflow as tf 
from tensorflow import keras
model = tf.keras.Sequential([
                             tf.keras.layers.Dense(units = inputNeurons, activation = 'relu'),
                             tf.keras.layers.Dense(units = 2*inputNeurons, activation='relu'),
                             tf.keras.layers.Dense(1)
])

model.compile(
    optimizer = tf.keras.optimizers.Adam(learning_rate = 0.001),
    loss = 'mean_absolute_error',
    metrics = ['mae', 'mse']
)

numEpochs = 300
history = model.fit(x = dftrain, y = dftr, validation_data = (dftest, dfte), epochs = numEpochs)

features = print(len(dftrain.columns))
print(features)
print(len(dftr))

df2.to_csv("newData.csv")

print(history)

model.summary()

def curvePlots(tempString):
  plt.plot(history.history[tempString])
  plt.plot(history.history[f'val_{tempString}'])
  plt.xlabel('NumEpochs')
  plt.ylabel(tempString)
  plt.legend([tempString, f'val_{tempString}'])
  plt.show()


curvePlots('mse')
curvePlots('mae')
curvePlots('loss')

model.predict([3])

print(f'Prediction for employee rating 3: {model.predict([3])}')

tempListforPreds = [1,2,3,4,5]
print(f'''

input List = {tempListforPreds}


List of Predictions:
{model.predict(tempListforPreds)}

List of Predictions (flattened out):
{model.predict(tempListforPreds).flatten()}
''')

print(dftest)

pred = model.predict(dftest).flatten()

print(len(pred))
print(pred)

def predPlot(labels, predictions):
  plt.scatter(labels, predictions)
  plt.ylabel('Predictions')
  plt.xlabel('True Value or Labels')
  plt.axis('equal')
  plt.axis('square')
  plt.xlim([0, plt.xlim()[1]])
  plt.ylim([0, plt.ylim()[1]])
  plt.show()

predPlot(dfte, pred)

def errorPlot(preds, labels, counts):
  errors = preds - labels
  plt.hist(errors, counts)
  plt.xlabel('Error')
  plt.ylabel('Counts')
  plt.show()

errorPlot(pred, dfte, numEpochs)