import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv",index_col=0,parse_dates=[0])

# Clean data
df = df[(df.value > df.value.quantile(.025)) & (df.value < df.value.quantile(.975))]


def draw_line_plot():
    # Draw line plot
    df_line = df.copy()
    fig,ax = plt.subplots(figsize=(15,10),dpi=100)
    ax.plot(df_line.index,
            df_line.value,
            c='#b30000',
            linewidth=1.5)
    ax.set(title="Daily freeCodeCamp Forum Page Views 5/2016-12/2019",
           xlabel="Date",
           ylabel="Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    
    # use the index to create the data for two new columns
    df_bar['year']=df_bar.index.year
    df_bar['month']=df_bar.index.month
    
    # group the data
    df_bar=df_bar.groupby(['year','month'],as_index=False).mean()
    df_bar.sort_values('month',inplace=True)
    
    months = ['January','February','March','April','May','June',
              'July','August','September','October','November','December']
    month_mapper={x:y for x,y in zip(range(1,13),months)}
    
    # replace the int's representing months with the month's proper name
    df_bar['month'] = df_bar.month.apply(lambda x: month_mapper[x],)
    
    # Draw bar plot
    fig,ax = plt.subplots(figsize=(15,10),dpi=100)
    ax = sns.barplot(data=df_bar,x='year',y='value',hue='month',palette='Set1')
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.legend(loc='upper left',title='Months')

    #Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    m = df_box.month.unique().tolist()
    mon = m[-4:]+m[:8]
    fig,axs = plt.subplots(ncols=2,figsize=(20,10),dpi=100)
    
    sns.boxplot(data=df_box,x='year',y='value',ax=axs[0])
    sns.boxplot(data=df_box,x='month',y='value',ax=axs[1],order=mon)

    axs[0].set(title="Year-wise Box Plot (Trend)",
               xlabel='Year',
               ylabel='Page Views',
               ylim=(0,200000),
               yticks=np.linspace(0,200000,11))
              
    axs[1].set(title="Month-wise Box Plot (Seasonality)",
               xlabel='Month',
               ylabel='Page Views',
               ylim=(0,200000),
               yticks=np.linspace(0,200000,11))

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
