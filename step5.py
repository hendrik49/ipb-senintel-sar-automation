import os, datetime
from datetime import timedelta, date
from scipy.io import loadmat, savemat
import numpy as np
import pandas as pd
import time
from pathlib import Path
from PIL import Image
from spectral import *
import tifffile as tiff
from tqdm import tqdm
import pandas as pd
import config
home = os.getcwd()

# Params 
dateStr = config.dateStr
ext1 = 'img'
ext2 = 'hdr'
splitStr       = '_'
daysInterval   = 12
time_formatStr = "%d-%b-%Y"
bandName = ['Sigma0_VH','Sigma0_VV']
ext = ['vh', 'vv']
train_path = config.train_path
folder = config.folder
numfiles = len(filter(lambda x: "Sigma0_" in x, os.listdir(folder)))/4

# Built in Function

def nearest_date(items, pivot):
    return min(items, key=lambda x: abs(x - pivot))

def get_list_date(files):
    temp = files.split('.')[0].split('_')
    return datetime.datetime.strptime(temp[len(temp)-1], '%d%b%Y')

def find_files(list_date, files, ext, j, dateStr, daysInterval):
    date_curr = nearest_date(list_date[ext[j]], datetime.datetime.strptime(str(dateStr), '%d%b%Y'))
    date_prev = date_curr - datetime.timedelta(daysInterval)
    idx_curr = list_date[ext[j]].index(date_curr)
    idx_prev = list_date[ext[j]].index(date_prev)
    return files[ext[j]][idx_curr], files[ext[j]][idx_prev]

def get_img_file(img_file, hdr_file, val):
    hdr_vh = folder +'/'+hdr_file[0][val]
    img_vh = folder +'/'+img_file[0][val]
    hdr_vv = folder +'/'+hdr_file[1][val]
    img_vv = folder +'/'+img_file[1][val]
    l = [[hdr_vh, img_vh], [hdr_vv, img_vv]]
    if Path(hdr_vh).is_file() and Path(img_vh).is_file():
        if Path(hdr_vv).is_file() and Path(img_vv).is_file():
            get_info = envi.read_envi_header(hdr_vh)
            d1 = int(get_info['lines'])
            d2 = int(get_info['samples'])
            dim = (d1,d2,2)
            im_subset = np.zeros((dim))
    for ix in tqdm(range(len(l))):
        get_img = envi.open(l[ix][0])
        img_open = get_img.open_memmap(writeable = True)
        im = img_open[:d1,:d2,0]
        im_subset[:,:,ix] = im
    return im_subset

def normalize_rows(x):
    """
    function that normalizes each row of the matrix x to have unit length.

    Args:
     ``x``: A numpy matrix of shape (n, m)

    Returns:
     ``x``: The normalized (by row) numpy matrix.
    """
    return x/np.linalg.norm(x, ord=2, axis=1, keepdims=True)

# Make Dictionary of processing image
print("creating dictionoary files....")

img = {
    'vh': [f for f in os.listdir(folder) if f.endswith('.' + 'img') and "_VH" in f], 
    'vv': [f for f in os.listdir(folder) if f.endswith('.' + 'img') and "_VV" in f]}
hdr = {
    'vh': [f for f in os.listdir(folder) if f.endswith('.' + 'hdr') and "_VH" in f],
    'vv': [f for f in os.listdir(folder) if f.endswith('.' + 'hdr') and "_VV" in f]}

date_img = {
    'vh': [get_list_date(i) for i in img[ext[0]]], 
    'vv': [get_list_date(i) for i in img[ext[1]]] }

date_hdr = {
    'vh': [get_list_date(i) for i in hdr[ext[0]]], 
    'vv': [get_list_date(i) for i in hdr[ext[1]]] }


img_file = [find_files(date_img, img, ext, j, 
                       dateStr, daysInterval) for j in range(len(date_img))]
hdr_file = [find_files(date_hdr, hdr, ext, j, 
                       dateStr, daysInterval) for j in range(len(date_hdr))]

img_current = get_img_file(img_file, hdr_file, 0) ## 0 for current, 1, previous
img_previous = get_img_file(img_file, hdr_file, 1) ## 0 for current, 1, previous

print("the files are....")
print(img_file)

#Create features dimension
img_features = np.zeros((img_current.shape[0], img_current.shape[1], 6))

#Extract features
print("Extracting features....")

img_features[:,:,0] = img_current[:,:,0]
img_features[:,:,1] = img_current[:,:,1]
img_features[:,:,2] = img_current[:,:,0]/img_current[:,:,1]
img_features[:,:,3] = img_current[:,:,0]-img_previous[:,:,0]
img_features[:,:,4] = img_current[:,:,1]-img_previous[:,:,1]
img_features[:,:,5] = img_current[:,:,0]/img_current[:,:,1]-\
                      img_previous[:,:,0]/img_previous[:,:,1]

[d1,d2,d3] = img_features.shape
print("Extracting features complete....")


#reshape and normalize features values
print("Reshape features and normalize....")
test_features = np.reshape(img_features,[d1*d2,d3])
test_features = normalize_rows(test_features)
print("Reshape features and normalize complete....")

#read data traning from matlab
print("Reading traning features from "+train_path )
mat = loadmat(train_path)  # load mat-file
mdata = mat['train_mat']  # variable in mat file
mtype = mdata.dtype
ndata = {n: mdata[n][0,0] for n in mtype.names}
data_headline = ndata['feature_name']
headline = data_headline[0]


#load data training into dataframe
print("Loading traning features into dataframe... ")
data_raw = ndata['train_data']
data_df = np.reshape(data_raw,[250,6]);
data_df = normalize_rows(data_df);
data_df = pd.DataFrame(data_raw)
data_test = pd.DataFrame(ndata['train_label'])


#initiate train features and label features
print("Initiate train features and label features... ")
train_features = data_df
train_labels = data_test
print("Creating traning features is complete....")

#create RF Regressor
print("create RF Regressor with 10000 esitimators... ")
from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor(n_estimators = 1000, random_state = 42)

# Train the model on training data
print("Train the model using training data... ")
rf.fit(train_features, train_labels.values.ravel());
rf.score(train_features, train_labels.values.ravel())

# Use the forest's regressor to predict method on the test data
print("Predict the data using the model... ")
y_pred = rf.predict(test_features)

# Show prediction result
pd.DataFrame(y_pred).head()

from sklearn import metrics
#print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))  
#print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))  
#print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred))) 


#create RF Classifier
#from sklearn.ensemble import RandomForestClassifier
#rfc =  RandomForestClassifier(n_estimators = 1000, random_state = 42, max_depth=15)

#rfc.fit(train_features, train_labels.values.ravel());
#rfc.score(train_features, train_labels.values.ravel())


# Use the forest's classifier predict method on the test data
#yc_pred = rfc.predict(test_features)

# Show prediction result
#pd.DataFrame(y_pred).head()
