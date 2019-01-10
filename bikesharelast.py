import time
import pandas as pd
import numpy as np
import json
from import_util import get_user_input

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
CITIES = ['chicago', 'newyork', 'washington']

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']

DAYS = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    while True:
        city = input('Which city do you want to explore Chicago, New York or Washington? \n> ').lower()
        if city in CITIES:
            break;

    month = get_user_input('All right! now it\'s time to provide us a month name ' \
                           'or just say \'all\' to apply no month filter. \n(e.g. all, january, february, march, april, may, june) \n> ',
                           MONTHS)

    day = get_user_input('one last thing provide the day of the week , you want to analyze?' \
                         'or just say \'all\' to apply no day filter. \n(e.g. all, monday,tuesday) \n> ', DAYS)

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['dayofweek'] = df['Start Time'].dt.weekday_name;
    df['hour'] = df['Start Time'].dt.hour
    df['journey'] = df['Start Station'].str.cat(df['End Station'], sep=' to ')
    if month != 'all':
        month = MONTHS.index(month) + 1
        df = df[df['month'] == month]
    if day != 'all':
        df = df[df['dayofweek'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_com_month = df['month'].value_counts().idxmax()
    print('The most common month is :', MONTHS[most_com_month-1])

    # display the most common day of week
    most_com_day = df['dayofweek'].value_counts().idxmax()
    print('The most common Day of week is :', most_com_day)

    # display the most common start hour
    most_com_start_hour = df['hour'].value_counts().idxmax()
    print('The most common hour is :', most_com_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_sta = df['Start Station'].value_counts().idxmax()
    print('The most common Start Station is :', most_common_start_sta)

    # display most commonly used end station
    most_common_end_sta = df['End Station'].value_counts().idxmax()
    print('The most common End Station is :', most_common_end_sta)

    # display most frequent combination of start station and end station trip
    trip_series = df["Start Station"].astype(str) + " to " + df["End Station"].astype(str)
    most_popular_trip = trip_series.describe()["top"]
    print(" The Most frequent Combination of Start and End Station Trip : ", most_popular_trip)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = df['Trip Duration'].sum()
    print('total travel time is : ', total_travel_time)

    total_travel_mean_time = df['Trip Duration'].mean()
    print('total travel mean time is : ', total_travel_mean_time)

    total_travel_max_time = df['Trip Duration'].max()
    print('total travel max time is : ', total_travel_max_time)
    print("Travel time for each user type:\n")
    # display the total trip duration for each user type
    group_by_user_trip = df.groupby(['User Type']).sum()['Trip Duration']
    for index, user_trip in enumerate(group_by_user_trip):
        print(" {}: {}".format(group_by_user_trip.index[index], user_trip))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Counts of user types:\n")
    no_of_counts = df['User Type'].value_counts()
    # iteratively print out the total numbers of user types
    for index, user_count in enumerate(no_of_counts):
        print("  {}: {}".format(no_of_counts.index[index], user_count))

    print()

    if 'Gender' in df.columns:
        user_stats_gender(df)

    if 'Birth Year' in df.columns:
        user_stats_birth(df)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats_gender(df):
    """Displays statistics of analysis based on the gender of bikeshare users."""

    # Display counts of gender
    print("Counts of gender:\n")
    gender_counts = df['Gender'].value_counts()
    # iteratively print out the total numbers of genders
    for index, gender_count in enumerate(gender_counts):
        print("  {}: {}".format(gender_counts.index[index], gender_count))

    print()


def user_stats_birth(df):
    """Displays statistics of analysis based on the birth years of bikeshare users."""

    # Display earliest, most recent, and most common year of birth
    birth_year = df['Birth Year']
    # the most common birth year
    most_common_year = birth_year.value_counts().idxmax()
    print("The most common birth year:", most_common_year)
    # the most recent birth year
    most_recent = birth_year.max()
    print("The most recent birth year:", most_recent)
    # the most earliest birth year
    earliest_year = birth_year.min()
    print("The most earliest birth year:", earliest_year)


def table_statistics(df, city):
    """Displays statistics on bikeshare users."""
    print('\nCalculating Dataset Statistics...\n')
    # counts the number of missing values in the entire dataset
    no_of_miss_value = np.count_nonzero(df.isnull())
    print("The number of missing values in the {} dataset : {}".format(city, no_of_miss_value))


def displaying_data(df):
    row_length = df.shape[0]

    # iterate from 0 to the number of rows in steps of 5
    for i in range(0, row_length, 5):

        yes = input('\nWould you like to examine the particular user trip data? Type \'yes\' or \'no\'\n> ')
        if yes.lower() != 'yes':
            break

        # retrieve and convert data to json format
        # split each json row data
        row_data = df.iloc[i: i + 5].to_json(orient='records', lines=True).split('\n')
        for row in row_data:
            # pretty print each user data
            parsed_row = json.loads(row)
            json_row = json.dumps(parsed_row, indent=2)
            print(json_row)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
