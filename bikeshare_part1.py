import time
import numpy as np
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

days = ['monday', 'tuesday', 'wednesday', 'thursday',
        'friday', 'saturday', 'sunday', 'all']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" for no filter
        (str) day - name of the weekday to filter by, or "all" for no filter
    """
    print('---\nHello!\nLet\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington).
    while True:
        city = input('---\nFor which city would you like to see data?\
                     \nChoose one city (Chicago, New York City, or Washington)\
                     \n').lower()
        if city not in CITY_DATA.keys():
            print('Sorry, I do not have "{}" data!'.format(city))
            continue
        else:
            break

    # get user input for filter type (by month, by day, both, none)
    while True:
        filter = input('---\nHow would you like to filter the data?\
                       \n(Month, Day, Both, None)\n').lower()
        if filter not in ['month', 'day', 'both', 'none']:
            print('Sorry, this was not a valid filter!')
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)
    if filter == 'month' or filter == 'both':
        while True:
            month = input('---\nWhich month?\
                          \n(January, February, March, April, May, June, All)\
                          \n').lower()
            if month not in months:
                print('Sorry, this is not a valid option!')
                continue
            else:
                break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    if filter == 'day' or filter == 'both':
        while True:
            day = input('---\nWhich day?\n(Monday, Tuesday, Wednesday, ' +
                        'Thursday, Friday, Saturday, Sunday, All)\n').lower()
            if day not in days:
                print('Sorry, this is not a valid option!')
                continue
            else:
                break

    if filter == 'none' or filter == 'day':
        month = 'all'

    if filter == 'none' or filter == 'month':
        day = 'all'

    print('-'*40)
    print('Applying Filters: ({}, {}, {})...'.format(city, month, day).title())
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city & filters by month and day if applicable

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" for no filter
        (str) day - name of the weekday to filter by, or "all" for no filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # extract data
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Weekday'] = df['Start Time'].dt.day_name()
    df['Hour'] = df['Start Time'].dt.hour

    # filter by month
    if month != 'all':
        month = months.index(month) + 1
        df = df[df['Month'] == month]

    # filter by day
    if day != 'all':
        df = df[df['Weekday'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('Calculating The Most Frequent Times of Travel...\n---')
    start_time = time.time()

    # display the most common month
    common_month = int(df['Month'].mode())
    print('Most Common Month: {}'.format(months[(common_month)-1].title()))

    # display the most common day of week
    common_weekday = df['Weekday'].mode()[0]
    print('Most Common Day of Week:', common_weekday)

    # display the most common start hour
    common_start_hour = (df['Hour'].mode())[0]
    print('Most Common Start Hour: {}:00'.format(common_start_hour))

    print("---\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('Calculating The Most Popular Stations and Trip...\n---')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('Most Commonly Used Start Station: ', common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('Most Commonly Used End Station: ', common_end_station)

    # display most frequent combination of start station and end station trip
    freq_trip = (df['Start Station'] + ' (to) ' + df['End Station']).mode()[0]
    print('Most Common Trip: (from)', freq_trip)

    print("---\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('Calculating Trip Duration...\n---')
    start_time = time.time()

    # display total travel time
    total_travel_time = int(df['Trip Duration'].sum())
    ttt = 'Total Travel Time: {} seconds = {} hours'
    print(ttt.format(total_travel_time, pd.Timedelta(total_travel_time, "s")))

    # display mean travel time
    mean_travel_time = int(df['Trip Duration'].mean())
    att = 'Average Travel Time: {} seconds = {} hours'
    print(att.format(mean_travel_time, pd.Timedelta(mean_travel_time, "s")))

    print("---\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('Calculating User Stats...\n---')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Counts of User Types:')
    print(user_types)

    # Display counts of gender
    print('\nCounts of Gender:')
    if 'Gender' in df.columns:
        genders = df['Gender'].value_counts()
        print(genders)
        gender_note = '**Note: We only have gender data for {}% of users'
        print(gender_note.format(int(100*df['Gender'].count()/df.shape[0])))
    else:
        print('No gender data available')

    # Display earliest, most recent, and most common year of birth
    print('\nYear of Birth Summary:')
    if 'Birth Year' in df.columns:
        print('Earliest: ', int(df['Birth Year'].min()))
        print('Most Recent: ', int(df['Birth Year'].max()))
        print('Most Common: ', int(df['Birth Year'].mode()))
        byear_note = '**Note: We only have birthyear data for {}% of users'
        print(byear_note.format(int(100*df['Birth Year'].count()/df.shape[0])))
    else:
        print('No birthyear data available')

    print("---\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        for i in range(0, df.shape[0], 5):
            while True:
                rawdata = input('Would you like to see raw trip data?\
                                \nChoose (Yes or No)\n').lower()
                if rawdata == 'yes':
                    pd.set_option('display.max_columns', None)
                    i += 5
                    print('---\n5 rows of data...\n')
                    print(df.iloc[i-5:i, :], '\n---')
                    continue
                else:
                    break
            break

        restart = input('---\nWould you like to restart?\
                        \nChoose (Yes or No)\n').lower()
        if restart != 'yes':
            print('---\nGood Bye!')
            break


if __name__ == "__main__":
    main()
