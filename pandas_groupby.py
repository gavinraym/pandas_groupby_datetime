
import pandas as pd
import datetime
import random

# Here I am creating a pandas dataframe using random values
df = pd.DataFrame(
    {
        # random id's for each entry. There are no duplicates when using sample()
        'id':random.sample(range(1000),250),
        # Each entry is given a random date during 2021.
        'date':[datetime.date(2021, random.randrange(1,13), random.randrange(1,29)) for date in range(250)],
        # Each entry is also given a token from 0 to 9. This is what we will groupby.
        'tokens':random.choices(range(10), k=250)
        })

print(f'Here is a sample of our original data frame:\n{df.sample(25)}\n')

# Now I am creating a new dataframe of data after grouping by token.
new_df = pd.DataFrame(
    {
        # We are looking at every token from original dataframe (df)
        'tokens':df['tokens'],
        # This line is getting the first date with each token
        'first_date':df.groupby('tokens')['date'].min(),
        # This line is getting the last date with each token
        'last_date':df.groupby('tokens')['date'].max()
        })

# Calculating the duration of entries with each token here.
new_df['duration'] = new_df['last_date'] - new_df['first_date']

# This line will remove any tokens that have a duration under 320 days.
new_df = new_df[new_df['duration']>datetime.timedelta(days=320)]

print(f'The average duration of conversations that lasted longer than 320 days is:\n{new_df["duration"].mean()}\n')

# Lastly, we will look at our data one week at a time.
for time_period in range(24):
    # time_period will represent 24 weeks.
    # start_date is the first day of the current week
    start_date = datetime.date(2021, 1,1) + (datetime.timedelta(days=7)*time_period)
    # end_date is the last day of the week
    end_date = start_date + (datetime.timedelta(days=7, hours=24))
    # gb is a groupby object where we first selected only the dates between start_date and end_date
    gb = df[df['date'].between(start_date, end_date)].groupby('tokens')
    # Adding a column for each time period with the duration of each token.
    new_df[start_date] = gb['date'].max() - gb['date'].min()

print(f'Here is  new_df. Empty cells had no conversations.\n{new_df}')