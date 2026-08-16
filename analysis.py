import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
df = sns.load_dataset('penguins')
#to take a quik look at the file
print(f"Data Frame:\n {df}")
#to chech how many rows and columns
print(f"\nThere are {df.shape[0]} rows and {df.shape[1]} columns.")
#to check columns
print("\nThere are columns as below:")
print(df.columns)
#to check data types
print("\n Data types:")
print(df.dtypes)
#to get some info
print("\nSome more information:")
print(df.info())

#additional to check the one last row
print("\nPresented the last row:")
print(df.iloc[[(df.shape[0] - 1)],:])

#check if there are any duplicates
print("\nCheck if there are any duplicates:")
print(df.duplicated().any())

#check if there are any NaN
print("\nHow many missing values/data are in the DataFrame:")
print(df.isna().sum())
#check NaN
print("\nThe percentage of missing values/data:")
print(df.isna().mean()*100)
print("\n Rows with missing values:")
print(df[df.isna().any(axis=1)])
#the average measeures according to species
print("\nThe average measeures according to species:")
print(df.groupby('species')[[
    'bill_length_mm',
    'bill_depth_mm',
    'flipper_length_mm',
    'body_mass_g'
    ]].mean()
)
#fill in NaN with average amounts accoring to species
df['bill_length_mm'] = df['bill_length_mm'].fillna(
    df.groupby('species')['bill_length_mm'].transform('mean').round(1)
)
df['bill_depth_mm'] = df['bill_depth_mm'].fillna(
    df.groupby('species')['bill_depth_mm'].transform('mean').round(1)
)
df['flipper_length_mm'] = df['flipper_length_mm'].fillna(
    df.groupby('species')['flipper_length_mm'].transform('mean').round(1)
)
df['body_mass_g'] = df['body_mass_g'].fillna(
    df.groupby('species')['body_mass_g'].transform('mean').round(1)
)
#fill in sex NaN with 'unknown'
df['sex'] = df['sex'].fillna('Unknown')
#check transformed NaN
print("\nCheck rows with filled NaN data:")
print(df.iloc[[3,8,9,10,11,47,246,286,324,336,339]])
#chech if tere are any NaN
print("\nDouble check if there are any missing values any more:")
print(df.isna().sum())
#chart with the number of penguins by island and sex
count_data = df.groupby(['island', 'sex']).size().unstack(fill_value=0)
ax = count_data.plot(
    kind='bar',
    stacked=True
)
plt.xlabel('Island')
plt.ylabel('Count')
plt.title('Number of penguins by island and sex')
plt.legend(title='Sex')

for container in ax.containers:
    ax.bar_label(container, label_type='center')
plt.show()

#transform data to check for any outliers regarding weight
df_weight = df.drop(columns=['sex','bill_length_mm','bill_depth_mm', 'flipper_length_mm'])
print(f"\nData Frame with weight:\n{df_weight}")
plt.figure(figsize=(8, 5))
sns.boxplot(
    data=df_weight,
    x='species',
    y='body_mass_g'
)
plt.xlabel('Species')
plt.ylabel('Body mass (g)')
plt.title('Body mass by Species')
plt.show()
#check outliers
Q1 = df_weight.groupby('species')['body_mass_g'].transform('quantile', 0.25)
Q3 = df_weight.groupby('species')['body_mass_g'].transform('quantile', 0.75)
IQR = Q3 - Q1
outliers = df_weight[
    (df_weight['body_mass_g'] < Q1 - 1.5 * IQR) |
    (df_weight['body_mass_g'] > Q3 + 1.5 * IQR)
]
print(f"\nRows with outliers data: \n{outliers}")
