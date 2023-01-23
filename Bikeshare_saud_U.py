import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\n Welcome to BikeShare Feel free to use and enjoy \n')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Which city would you like to filter by? Enter chicago, new york city, or washington: ').lower()
        if city in CITY_DATA.keys():
            break
        else:
            print("Sorry, I didn't catch that. Try again.")
            continue

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input(
            "\nWhich month would you like to filter by? Enter 'all','january', 'february', 'march', 'april', 'may', 'june'").lower()
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        if month in months:
            print('\n here we will show you the data you are chosen for {}.'.format(month.title()))
            break
        else:
            print("Sorry, I didn't catch that. Try again.")
            continue

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("\n Are you looking for a particular day? Enter 'all','sunday', 'monday', 'tuesday', 'wednesdy', 'thursday', 'friday', 'saturday'").lower()
        days = ['sunday', 'monday', 'tuesday', 'wednesdy', 'thursday', 'friday', 'saturday']
        if day in days:
            print('\n here we will show you the data you are chosen for {}s.'.format(day.title()))
            break
        else:
            print("Sorry, I didn't catch that. Try again.")
            continue

    print('#' * 50)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].apply(lambda x: x.month)
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    most_common_month = df['month'].mode()[0]
    print("Most common month is: ", most_common_month)

    # TO DO: display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print("Most common day of week is: ", most_common_day)

    # TO DO: display the most common start hour
    most_common_hour = df['hour'].mode()[0]
    print("Most common Start Time is: ", most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('#' * 50)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print("Most commonly used start station is: ", most_common_start_station)

    # TO DO: display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print("Most commonly used end station is: ", most_common_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    """ We will use gruop by to combinde start and end station but we can't use mode() then we use sort values and shows the first number of the row using head(1) """
    combine_stations = df.groupby(['Start Station', 'End Station'])
    most_combine_stations = combine_stations.size().sort_values(ascending=False).head(1)
    print('most frequent combination of start station and end station trip is: ', most_combine_stations)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('#' * 50)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('the total travel time is: ', total_travel_time)

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('the mean travel time is: ', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('#' * 50)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\n Calculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types

    user_types = df['User Type'].value_counts()

    # print(user_types)
    print('User Types:\n', user_types)

    # TO DO: Display counts of gender

    try:
        gender_types = df['Gender'].value_counts()
        print('\n Gender Types:\n', gender_types)

    except KeyError:
        print("\n Gender Types: \n No data available for this month.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('#' * 50)


def display_raw_data(df):
    """
       Displays subsequent rows of data according to user answers
       Arg:
            df - Pandas Dataframe containing city data filtered by month and day returned from load_data() function
       """

    i = 0
    answer = input('\n would like to Display the first 5 rows of data? yes or no \n').lower()
    pd.set_option('display.max_columns', None)
    while True:
        if answer == 'no':
            break
        print(df[i:i + 5])
        answer = input('\n would like to Display the next 5 rows of data? yes or no \n').lower()
        i += 5


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\n Do you need to restart? Yes or No \n').title()
        if restart.title() != 'Yes':
            print('Have a good day')
            break


if __name__ == "__main__":
    main()