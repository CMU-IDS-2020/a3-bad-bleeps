import pandas as pd
import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score,f1_score,precision_score, recall_score

df = pd.read_csv('2020_crimes.csv')

df_filtered = df.drop(columns = ['ID', 'Case Number', 'Date', 'Description', 'Location Description', 'X Coordinate', 'Y Coordinate', 'Updated On', 'Latitude', 'Longitude', 'Location', 'FBI Code', 'Block', 'Beat', 'Ward', 'Community Area', 'Block', 'IUCR'])
df_filtered = df_filtered.dropna(axis=0)
df = df_filtered
X = df_filtered.drop(columns=['Arrest'])
# df['beat'] = df['beat'].astype('category')
df['District'] = df['District'].astype('category')
# df['ward'] = df['ward'].astype('category')
# df['community_area'] = df['community_area'].astype('category')
# df['block'] = df['block'].astype('category')
# df['iucr'] = df['iucr'].astype('category')
df['Primary Type'] = df['Primary Type'].astype('category')

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# We create the preprocessing pipelines for both numeric and categorical data.
numeric_features = ['Year']
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())])

# categorical_features = ['iucr', 'primary_type', 'domestic', 'beat', 'district', 'ward', 'community_area']
categorical_features = ['Primary Type', 'Domestic', 'District']
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
                      ('classifier', LogisticRegression(max_iter=300))])

X = df.drop('Arrest', axis=1)
y = df['Arrest']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = clf.fit(X_train, y_train)
#print("model score: %.3f" % clf.score(X_test, y_test))
