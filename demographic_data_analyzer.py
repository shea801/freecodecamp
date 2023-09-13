import pandas as pd
import numpy as np


path = "C:\\Users\\sheah\\Downloads\\Programming\\Practice_Data\\adult\\adult.txt"

df = pd.read_csv(path,header=None, delimiter=",")

df.columns = ['age', 'workclass', 'fnlwgt', 'education', 'education_num', 
              'marital_status', 'occupation','relationship','race', 'sex', 
              'capital_gain', 'capital_loss', 'hours_per_week', 'native_country', 'salary']

# The data set uses a question mark ('?') to identify null or missing values. The dataset 
# needs the '?' replaced with np.nan, and the whitespace removed from the string type columns

# strip whitespace from the columns with strings:
for x in range(len(df.columns)):
    if type(df.iloc[0,x]) == str:
        for y in range(len(df.index)):
            df.iloc[y,x] = df.iloc[y,x].strip() 

# Now we can replace the '?' with np.nan 
df.replace('?', np.nan, inplace=True)

# now drop columns that aren't needed or have data with unknown relevance or descriptions
df.drop(axis=1, columns=['fnlwgt','capital_gain','capital_loss'],inplace=True)


# Create Pandas Series with race as the index which shows the total number of people
# representing each race

race = pd.Series(df.race.value_counts(), name='race')

# detrmine the average age of males within the dataset
male_mean_age = df.age[df.sex=='Male'].mean()
male_mean_age = round(male_mean_age,2)

# percentage of people who have a bachelors degree
bachelors_degree = df.education.str.contains('Bachelors').sum()

# percent of people making over 50K who have advanced education (Bachelors, Masters, Doctorate)
adv_ed = df[(df.education == 'Bachelors') | (df.education == 'Masters') | (df.education == 'Doctorate')]

# Use the above dataframe to determine the percentage of adv. ed. ppl who earn over $50K
adv_ed_percent = len(adv_ed[df.salary=='>50K'])/len(adv_ed) * 100
adv_ed_percent = f"{round(adv_ed_percent,2)}%"

# percent of people making over $50K a year **WITHOUT** advanced educaiton
def no_adv_ed_gt_50k():
    
    #create a list of strings that don't qualify as advanced education
    s = ['HS-grad','11th','10th','7th-8th','Prof-school','9th','12th','5th-6th','1st-4th']
    
    #create counters to get an overall number of people without advanced education
    gt_50 = 0
    le_50 = 0
    
    # loop through df.education column and compare to the salary column
    for x in range(len(df.education)):
        for y in s:
            if df.education.iloc[x]==y and df.salary.iloc[x]=='>50K':
                gt_50 += 1
            elif df.education.iloc[x]==y and df.salary.iloc[x]=='<=50K':
                le_50 += 1

    percent = (gt_50/(gt_50 + le_50))*100
    return f"Percent of ppl w/out adv. ed. making > $50K: {round(percent,2)}%"

# minimum nuber of hours a person works per week?
min_work_hours = df.hours_per_week.min()

# pecentage of people who work the minimum number of hours and make gt $50K

# create another function to do the work
def min_hrs_gt_50K():    
    min_hours_and_gt_50 = df.hours_per_week==1

    gt_50 = df.salary[min_hours_and_gt_50]=='>50K'

    total = df.hours_per_week[min_hours_and_gt_50]
    
    percent = (total[gt_50].count()/total.count())*100

    return f"{percent}%"

# Which country has the highest number of people making greater than $50K
# And what is that percentage of the overall number of people making over $50K

# Lets get the country with the most >$50K earners
highest_earning_country = df.native_country[df.salary=='>50K'].value_counts().head(1)


# create a function to get the percentage
def highest_earning_country_percentage():
    total = df.native_country[df.salary=='>50K'].count()
    US_total = df.native_country[df.salary=='>50K'].value_counts()[0]
    percent = (US_total/total) * 100
    
    return f"{round(percent,2)}%"


# Most common occupation in India that makes more than $50K
india_occupation_gt_50k = df[['native_country','occupation','salary']][df.native_country=='India'][df.salary=='>50K']

occupation_gt_50 = india_occupation_gt_50k.occupation.value_counts().head(1)

print(
    f"How many people of each race are represented in this dataset?\n{race}\n",
    f"What is the average age of men? Ans: {male_mean_age}\n",
    f"What is the percent of people who have a Bachelor's degree? Ans: {bachelors_degree}\n",
    f"What percent of people with advanced education making more than 50K? Ans: {adv_ed_percent}\n",
    f"What percent of people w/out advanced education make more than 50K?\n{no_adv_ed_gt_50k()}\n",
    f"What is the minimum number of hours a person works per week? Ans: {min_work_hours}\n",
    f"What percentage of the people who work the minimum number of hours per week have a salary of more than 50K?\nAns: {min_hrs_gt_50K()}\n",
    f"What country has the highest percentage of people that earn >50K? Ans: {highest_earning_country}\n",
    f"What percentage does that country make up of all countries earning over $50K?\nAns: {highest_earning_country_percentage()}\n",
    f"Identify the most popular occupation for those who earn >50K in India? Ans: {occupation_gt_50}?")