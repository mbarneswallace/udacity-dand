#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 10:41:31 2017

@author: mitchellbarnes-wallace
"""
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SelectKBest
from sklearn.metrics import accuracy_score, precision_score, recall_score,f1_score,make_scorer,fbeta_score
from sklearn.grid_search import GridSearchCV
from sklearn.cross_validation import train_test_split,StratifiedShuffleSplit,StratifiedKFold
from time import time
import numpy as np

def process_classifier(key, value,trained_clf,tuned_scores,labels, features):
    if key == 'ada_dt':
        steps_clf = [("pca", PCA()),("select_k", SelectKBest()), ('classifier', value['clf'])]
        clf_parameters = value['parameters']
        clf_parameters['select_k__k'] = range(1,12,1)
    elif key == 'naive_bayes':
        steps_clf = [("select_k", SelectKBest(k=11)), ('base_estimator', value['clf'])]
        clf_parameters = value['parameters']
    else:
        steps_clf = [("pca", PCA()),("select_k", SelectKBest()), ('base_estimator', value['clf'])]
        clf_parameters = value['parameters']
        clf_parameters['select_k__k'] = range(1,12,1)
    clf_test = Pipeline(steps_clf)
    scores, tuned_parameters, time_value, best_estimator = tune_train_algorithm(clf_test, labels, features, clf_parameters)
    tuned_scores[key] = scores
    trained_clf[key] = {'best_estimator':best_estimator,'tuned_parameters':tuned_parameters}
    #print key,' Complete: ',time_value,' s'
    return tuned_scores, trained_clf
    
def test_clfs(classifier, labels, features):
    t0 = time()
    accuracy, recall, precision, f1 = [],[],[],[]
    for i in range(100):
        features_train, features_test, labels_train, labels_test = \
            train_test_split(features, labels, test_size=0.3, random_state =i)
        
        classifier = classifier.fit(features_train, labels_train)
        predicted_labels = classifier.predict(features_test)
        accuracy.append(accuracy_score(labels_test, predicted_labels))
        recall.append(recall_score(labels_test,predicted_labels))
        precision.append(precision_score(labels_test, predicted_labels))
        f1.append(f1_score(labels_test,predicted_labels))

    #store the training time
    training_time = "{:.3}".format(time() - t0)
    
    #store the scores
    scores = dict(accuracy = ("{:.3}".format(np.mean(accuracy))),\
                  precision = "{:.3}".format(np.mean(precision)),\
                  recall = "{:.3}".format(np.mean(recall)),\
                  f1 = "{:.3}".format(np.mean(f1)))
    return scores, training_time

def tune_train_algorithm(classifier, labels, features, parameters):
    #initialize the metrics for scoring
    
    t0 = time()
    
    grid_search = GridSearchCV(classifier,
    	              param_grid=parameters,
    	              scoring=make_scorer(f1_score),
    	              cv=StratifiedKFold(labels),
    	              error_score=0)
    grid_search = grid_search.fit(features, labels)
    
    #store the training time
    training_time = "{:.3}".format(time() - t0)
    
    best_parameters = grid_search.best_estimator_.get_params()
    best_estimator = grid_search.best_estimator_
    scores, time_temp = test_clfs(grid_search.best_estimator_, labels, features)
    tuned_parameters = {}
    for keys in parameters.keys():
        tuned_parameters[keys] = best_parameters[keys]
    return scores, tuned_parameters, training_time, best_estimator
