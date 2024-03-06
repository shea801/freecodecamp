import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

def draw_plot():
    # Read data from file
    path = "epa-sea-level.csv"
    df = pd.read_csv(path,header=0,dtype=float)
    
    # get the linear regression data from scipy for current historical data
    regres_line = linregress(df['Year'],y=df['CSIRO Adjusted Sea Level'])
    # get the y-intercept, x values, and y values from slope-intercept
    b = regres_line.intercept
    m = regres_line.slope
   
    X = df['Year'].to_list()
    X.extend(list(range(2014,2051)))
    
    Y = [float(m*x + b) for x in X]

    # get the data for the period ranging from 2013-2050
    # slope, y-intercept, x values, and y values from slope-intercept
    future_m = future_regres_line.slope
    future_b = future_regres_line.intercept
    
    future_X = df_2000_to_2013['Year'].to_list()
    future_X.extend(list(range(2014,2051)))
    
    future_Y = [float(future_m * x + future_b) for x in future_X]

    # Create scatter plot
    fig,ax = plt.subplots(figsize=(16,9),dpi=100)
    ax.scatter(data=df,x='Year',y='CSIRO Adjusted Sea Level',)
    
    # Create first line of best fit
    ax.plot(X,Y,color='r') # first line
    
    # Create second line of best fit
    ax.plot(future_X,future_Y,color='g')
    
    # Add labels and title
    ax.set_title("Rise in Sea Level",fontdict={'size':14})
    ax.set_xlim(1850,2075)
    ax.set_xlabel("Year",fontdict={'size':14})
    ax.set_ylabel("Sea Level (inches)",fontdict={'size':14})
    
    # Save plot and return data for testing (DO NOT MODIFY)
    plt.savefig('sea_level_plot.png')
    return plt.gca()