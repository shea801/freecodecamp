import pandas as pd


def calculate_demographic_data(print_data=True):
    # Read data from file
    # copy the path for data set
    path = 'adult.data.csv'

    # create the pandas dataframe
    df = pd.read_csv(path)

    # rename the column titles 
    columns = {'education-num':'education_num', 'marital-status':'marital_status', 
               'capital-gain':'capital_gain','capital-loss':'capital_loss', 
               'hours-per-week':'hours_per_week', 'native-country':'native_country'}

    df.rename(columns=columns, inplace=True)

    # and drop unnecessary columns fnlwgt, capital-gain, and capital-loss
    df.drop(axis=1, columns=['fnlwgt','capital_gain', 'capital_loss'], inplace=True)

    # the dataframe uses '?' instead of a null value. So they need to be found and replaced with no value
    df.replace('?','',inplace=True)

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = df.race.value_counts()

    # What is the average age of men?
    average_age_men = round(df.age[df.sex=='Male'].mean(),1)

    # What is the percentage of people who have a Bachelor's degree?
    percentage_bachelors = round(df.education.str.contains('Bachelors').sum()/df.education.value_counts().sum() * 100, 1)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    higher_education = df[(df.education == 'Bachelors') | (df.education == 'Masters') | (df.education == 'Doctorate')]
    lower_education = df[(df.education != 'Bachelors') & (df.education != 'Masters') & (df.education != 'Doctorate')]

    # percentage with salary >50K
    higher_education_rich = round(len(higher_education[df.salary=='>50K'])/len(higher_education) * 100,1)
    lower_education_rich = round(len(lower_education[df.salary=='>50K'])/len(lower_education) * 100, 1)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df.hours_per_week.min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    num_min_workers = df.salary[df.hours_per_week==1][df.salary=='>50K']

    rich_percentage = round(num_min_workers.count()/df.hours_per_week[df.hours_per_week==1].count() * 100,1)
  
    # ### I'm going to use a for loop to create a new dataframe to get the highest percent >$50K ###
    countries = df.native_country.unique().tolist()
    highest_percent = []
    
    for x in range(len(countries)):
        gt_50 = df.salary[(df.salary=='>50K') & (df.native_country==countries[x])].count()
        total = df.salary[df.native_country==countries[x]].count()
        highest_percent.append(gt_50/total * 100)
        
    high_earners = pd.DataFrame({'countries':countries,'highest_percent':highest_percent})
    
    highest_earning_country_percentage = round(high_earners.highest_percent.max(),1)
    
    # What country has the highest percentage of people that earn >50K?
    highest_earning_country = high_earners.countries[high_earners.highest_percent==high_earners.highest_percent.max()].to_list()[0]
    
    # Identify the most popular occupation for those who earn >50K in India.
    india_occupation_gt_50k = df[['native_country','occupation','salary']][(df.native_country=='India') & (df.salary=='>50K')]
        
    top_IN_occupation = india_occupation_gt_50k.occupation.describe(include=all).iloc[2]

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation}
