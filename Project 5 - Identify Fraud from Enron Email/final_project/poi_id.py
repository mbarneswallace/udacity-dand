#!/usr/bin/python

import sys
import pickle

sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data
#import matplotlib.pyplot
import random
import pandas as pd
import numpy as np
from time import time
from sklearn.metrics import accuracy_score, precision_score, recall_score,f1_score,make_scorer,fbeta_score


### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
features_list = ['poi','salary', 'deferral_payments', 'total_payments', 'loan_advances', 'bonus','expenses','other', 'long_term_incentive', \
                 'director_fees','deferred_income', 'total_stock_value', 'restricted_stock_deferred', 'exercised_stock_options',  \
                 'restricted_stock',  'to_messages',  'from_poi_to_this_person','from_messages', \
                 'from_this_person_to_poi', 'shared_receipt_with_poi']

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

### Task 2: Remove outliers

##Find all of the names with error in the data
##most of the data can be cross referenced to ensure it was extracted appropiately. 
##(e.g. total_payments should reconcile to all payment subcategories, salary, loan_advances etc.)

#intialize names lists to pull names with potentionally erronous data
df = pd.DataFrame.from_dict(data_dict,orient = 'index')
df = df[features_list]

df = df.replace('NaN', np.nan)

stock_data = ['exercised_stock_options','restricted_stock','restricted_stock_deferred'] #all of the columns for stock values
payment_data = ['deferral_payments', 'salary','loan_advances', 'bonus',\
                 'deferred_income',  'expenses', 'other', 'long_term_incentive', \
                 'director_fees'] #array for all the columns for payment data

#1323 initial Null values in this array 
null_values = df.isnull().sum().sum()
df.iloc[:,:15] = df.iloc[:,:15].fillna(0)

# Find name with all NaN/No Information
all_values_zero = df.loc[(df[features_list[1:]]).sum(axis=1,skipna=True) == 0]
#two people with zero values CHAN RONNIE  & LOCKHART EUGENE E, the latter is complete empty, & removed from the dataset
df = df.drop('LOCKHART EUGENE E')
# Find the outliers - i.e. Total - (LARGE VALUE) 
top_5_payments = df.nlargest(5,'total_payments',keep='first')['total_payments']
top_5_stocks = df.nlargest(5,'total_stock_value',keep='first')['total_stock_value']
# the top earner is an employee named TOTAL, which looks to be the total of all values, values removed
df = df.drop('TOTAL')

#Double check names
index_length = pd.DataFrame(index=df.index,data = df.index.str.len(),columns = ['length'])
top_5_lengths = index_length .nlargest(5,'length',keep='first')
#THE TRAVEL AGENCY IN THE PARK  is the largest name in the dataframe, and is an agency not a person, this data is removed
df = df.drop('THE TRAVEL AGENCY IN THE PARK')

# Find the mistake values 

#compare the sum of the stock values to the total of stock values, return any row that contain errornous data
stock_irreconcilable = df.loc[(df[stock_data]).sum(axis=1) != df['total_stock_value']]
#compare the sum of the payment values to the total of payments, return any row that contain errornous data
payment_irreconcilable = df.loc[(df[payment_data]).sum(axis=1) != df['total_payments']]

#'BELFER ROBERT', 'BHATNAGAR SANJAY' are the two mistake people, with their data shifted, fixed here
corrected_data = {'BELFER ROBERT': {'expenses':3285,'director_fees': 102500, 'deferred_income': -102500,\
                                  'total_payments':3285,'restricted_stock':44093, 'restricted_stock_deferred':-44093,\
                                  'deferral_payments':0,'loan_advances':0,'long_term_incentive':0,'salary':0,'defered_income':0\
                                  ,'other':0,'exercised_stock_options':0, 'total_stock_value':0 },\
    'BHATNAGAR SANJAY':{'expenses':137864,'total_payments':137864,'exercised_stock_options':15456290,'restricted_stock':2604490,\
                        'restricted_stock_deferred':-2604490,'total_stock_value':15456290,'deferral_payments':0,\
                        'loan_advances':0,'long_term_incentive':0,'salary':0,'defered_income':0\
                                  ,'other':0,'bonus':0,'director_fees':0 }}
df = df.replace(corrected_data)

## Hard to find any more mistake values - the max values in the remaining data set are POI's. 
## No best way to handle the remaining Null values in the messages data. I will use a mean approach for these remaining values, 
## and for the null values in the message data I will replace them with the median of the other values in that column.

df = df.fillna(df.median())
 
### Task 3: Create new feature(s)
## Create two new features: Difference between total payments and total stocks - stocks_payments_delta,
## The ratio of all emails from and to a POI and their total messages: ratio_poi_total_messages

df['stocks_payments_delta'] = df['total_stock_value'] - df['total_payments']
df['ratio_poi_total_messages'] = (df['from_poi_to_this_person'] + df['from_this_person_to_poi'])/(df['to_messages']+df['from_messages'])

features_list  += ['stocks_payments_delta']
features_list += ['ratio_poi_total_messages']

# scale the dataframe
#df = (df- df.min())/(df.max()-df.min())
#convert dataframe back to dictionary
data_dict = df.to_dict(orient = 'index')

#salary vs bonus plot - temp for testing
#plot_data = featureFormat(data_dict, ['salary','bonus'])
#for point in plot_data:
#    x = point[0]
#    y = point[1]
#    matplotlib.pyplot.scatter(x,y)

### Store to my_dataset for easy export below.
my_dataset = data_dict

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

from sklearn.feature_selection import SelectKBest
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range = (0,1))
features_scaled = scaler.fit(features)
best = SelectKBest(k ="all").fit(features,labels)
k_best_features = {}
for i in range(len(features_list)-1):
    k_best_features[features_list[i+1]] = best.scores_[i]
k_best_df = pd.DataFrame.from_dict(k_best_features,orient = 'index' )

#print k_best_df.sort_values(0,ascending = 0)

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

#import all algorithms used
from sklearn.naive_bayes import GaussianNB
from sklearn.decomposition import PCA
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.pipeline import Pipeline
from test_and_train import process_classifier,test_clfs
from sklearn.feature_selection import SelectKBest
from sklearn.pipeline import Pipeline

#set parameters to be tested in the GridSearch
parameters_nb = {}
parameters_dt = {'base_estimator__criterion':['gini','entropy'],'base_estimator__min_samples_leaf':range(1, 50, 5),'base_estimator__max_depth':range(1, 10),\
                 'base_estimator__class_weight': ['balanced', None],'base_estimator__random_state':[42]}
parameters_rf = {'base_estimator__n_estimators':[1,15,30,100],'base_estimator__max_features':[1,3,5,7,10],'base_estimator__criterion':['gini','entropy']}
parameters_lr = {'base_estimator__C':[0.001,0.01,0.1,1,10,100,1000],'base_estimator__class_weight':['balanced']}
parameters_ada_dt = {'classifier__n_estimators': range(1,10)}

classifiers_test = {'naive_bayes':{'clf':GaussianNB()}\
                              ,'decision_tree':{'clf':DecisionTreeClassifier()}\
                              ,'random_forrest':{'clf':RandomForestClassifier()}\
                              ,'logistic_regression':{'clf':LogisticRegression()}}

initial_scores = {}


for key, value in classifiers_test.iteritems():
    
    steps_clf = [('pca',PCA()),('base_estimator', value['clf'])]
    clf_test = Pipeline(steps_clf)
    scores, time_completed = test_clfs(clf_test, labels, features)
    initial_scores[key] = scores
    #print key,' Complete: ',time_completed,' s'

initial_scores = pd.DataFrame.from_dict(initial_scores, orient = 'index')
#print initial_scores

classifiers_tune = {'naive_bayes':{'clf':GaussianNB(), 'parameters':parameters_nb}\
                             ,'decision_tree':{'clf':DecisionTreeClassifier(), 'parameters':parameters_dt}\
                              ,'ada_dt':{'clf':AdaBoostClassifier(base_estimator = DecisionTreeClassifier()), 'parameters':(parameters_ada_dt)}}

trained_clf = {}
tuned_scores = {}
#test all of the Machine Learning Algorithms for their best parameters, see if they pass muster
for key, value in classifiers_tune.iteritems():
    tuned_scores, trained_clf = process_classifier(key, value,trained_clf,tuned_scores,labels, features)

tuned_scores = pd.DataFrame.from_dict(tuned_scores, orient = 'index')
#print tuned_scores

### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html
# Example starting point. Try investigating other evaluation techniques!

clf = Pipeline([('select_k' ,SelectKBest(k = 11)),('clf', GaussianNB())])

print test_clfs(clf, labels,features)

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)