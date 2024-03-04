import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv("medical_examinations.csv")

# Add 'overweight' column

df['overweight'] = np.where((df.weight/((df.height/100)**2)) > 25, 1, 0)

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.

df.cholesterol = df.cholesterol.apply(lambda x: 1 if x > 1 else 0)
df.gluc = df.gluc.apply(lambda x: 1 if x > 1 else 0)

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat =df.melt(id_vars='cardio',
                  value_vars=['active','alco','cholesterol', 'gluc', 'overweight', 'smoke'])

    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    df_cat = df_cat.groupby(['cardio','variable','value']).size().reset_index()
    df_cat.rename(columns={0:'total'},inplace=True)    

    # Draw the catplot with 'sns.catplot()'
    fig = sns.catplot(data=df_cat,
                      kind='bar',
                      x='variable',
                      col='cardio',
                      hue='value')
    
    # Get the figure for the output
    fig = fig.figure

    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = pd.read_csv("medical_examinations.csv")
    df_heat['overweight'] = np.where((df_heat['weight']/((df_heat['height']/100)**2)) > 25, 1, 0)
    df_heat.cholesterol = df_heat.cholesterol.apply(lambda x: 1 if x > 1 else 0)
    df_heat.gluc = df_heat.gluc.apply(lambda x: 1 if x > 1 else 0)
    
    # remove low over hi blood pressures
    # remove the upper and lower 2.5% from height and weight
    df_heat = df_heat[(df_heat['ap_lo'] <= df_heat['ap_hi']) &
                      (df_heat['height'] >= df_heat['height'].quantile(.025)) &
                      (df_heat['height'] <= df_heat['height'].quantile(.975)) &
                      (df_heat['weight'] >= df_heat['weight'].quantile(.025)) & 
                      (df_heat['weight'] <= df_heat['weight'].quantile(.975))].copy().reset_index(drop=True)
    
    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(corr)

    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(20,20))
    
    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(data=correlated, 
                mask=masked,
                linewidths=.7,
                annot=True,
                fmt='.1f',
                square=True)

    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
