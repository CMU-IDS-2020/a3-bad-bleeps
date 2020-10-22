import pandas as pd
import numpy as np

from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score,f1_score,precision_score, recall_score

df = pd.read_csv('https://data.cityofchicago.org/resource/ijzp-q8t2.csv')

df_filtered = df.drop(columns = ['id', 'case_number', 'date', 'description', 'location_description', 'x_coordinate', 'y_coordinate', 'updated_on', 'latitude', 'longitude', 'location', 'fbi_code', 'block', 'district', 'ward', 'community_area', 'block', 'iucr'])
df_filtered = df_filtered.dropna(axis=0)
df_filtered = df_filtered[df_filtered['year']==2020]
df = df_filtered
X = df_filtered.drop(columns=['arrest'])
df['beat'] = df['beat'].astype('category')
# df['district'] = df['district'].astype('category')
# df['ward'] = df['ward'].astype('category')
# df['community_area'] = df['community_area'].astype('category')
# df['block'] = df['block'].astype('category')
# df['iucr'] = df['iucr'].astype('category')
df['primary_type'] = df['primary_type'].astype('category')


from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# We create the preprocessing pipelines for both numeric and categorical data.
numeric_features = ['year']
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())])

# categorical_features = ['iucr', 'primary_type', 'domestic', 'beat', 'district', 'ward', 'community_area']
categorical_features = ['primary_type', 'domestic', 'beat']
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)])

# Append classifier to preprocessing pipeline.
# Now we have a full prediction pipeline.
clf = Pipeline(steps=[('preprocessor', preprocessor),
                      ('classifier', DecisionTreeClassifier())])

X = df.drop('arrest', axis=1)
y = df['arrest']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

clf.fit(X_train, y_train)
# print("model score: %.3f" % clf.score(X_test, y_test))

