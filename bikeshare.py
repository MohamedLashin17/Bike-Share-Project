import time
import pandas as pd
import numpy as np

#dictionary to file names for each city
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['january', 'february', 'march', 'april', 'may', 'june']       #month list
days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']       #week days list
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # local Variables definitions
    city, filter, month, day, view_raw = '', '', 'all', 'all', 'no'
    # get user input for the city to get data for
    while city not in CITY_DATA.keys():             #while loop to handle invalid data
        city= input("Which city would you like to see data for? Chicago, New York City or Washington: \n").lower()
        if city not in CITY_DATA.keys():
            print('You\'ve entered invalid input, please try again.')
    #get user input on whether he would like to filter data by day, month or none
    while filter not in ['month', 'day', 'both', 'none']:   #while loop to handle invalid data
        filter = input('Would you like to filter the data by month, day, or both? for no filtration enter none.\n').lower()
        if filter == 'month':                       #in case of month filtraionn
            while month not in months:              #while loop to handle invalid data
                month = input('Please enter the name of the month you would like to filter data by: \n').lower()
                if month not in months:
                    print('You\'ve entered invalid input, please try again.')
        elif filter == 'day':                       #in case of day filtraionn
            while day not in days:                  #while loop to handle invalid data
                day = input('Please enter the name of the day you would like to filter data by: \n').lower()
                if day not in days:
                    print('You\'ve entered invalid input, please try again.')
        elif filter == 'both':                      #in case of both month and day filtraionn
            while month not in months:              #while loop to handle invalid data
                month = input('Please enter the name of the month you would like to filter data by: \n').lower()
                if month not in months:
                    print('You\'ve entered invalid input, please try again.')
            while day not in days:                  #while loop to handle invalid data
                day = input('Please enter the name of the day you would like to filter data by: \n').lower()
                if day not in days:
                    print('You\'ve entered invalid input, please try again.')
        elif filter == 'none':                      #in case of no filtraion
            month = 'all'
            day = 'all'
        else:
            print("you've entered invalid input, please try again.")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

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

    #display the most common month
    popular_month = df['month'].mode()[0]
    print("The most common month for travel is: {}".format(months[popular_month-1].title()))
    #display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print("The most common day of week for travel is: {}".format(popular_day))
    #display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print("The most common hour for travel is: {}:00".format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('The most common start station is {}'.format(popular_start_station))
    #display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('The most common end station is {}'.format(popular_end_station))
    #display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + ' to ' + df['End Station']
    print('The most common trip is: {}'.format(df['Trip'].mode()[0]))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #display total travel time
    trip_duration_sum = df["Trip Duration"].sum()
    print("The total travel time is {} hours and {} minutes and {} seconds".format(int(round(trip_duration_sum/ 3600)), int(round((trip_duration_sum%3600)/60)), int(round((trip_duration_sum%3600)%60)%60)))
    #display mean travel time
    trip_duration_avg = df["Trip Duration"].mean()
    print("The average travel time is {} minutes and {} seconds".format(int(round(trip_duration_avg/60)),int(round(trip_duration_avg%60))))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Display counts of user types
    print("Here is the counts of every user type:\n{}".format(df['User Type'].value_counts()))
    #Display counts of gender
    if city == 'washington':        #washington city has no gender or birth year data
        print("There is no gender data for Washington users.")
        print("There is no birth year data for Washington users.")
    else:
        print("Here is the counts of user genders:\n{}".format(df['Gender'].value_counts()))
        print('The earliest year of birth is {}'.format(int(df['Birth Year'].min())))
        print('The most recent Year of birth is {}'.format(int(df['Birth Year'].max())))
        print('The most common year of birth is {}'.format(int(df['Birth Year'].mode()[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """Takes user input on whether he would like to display raw data and perform according to the input"""
    raw, i = '', 0
    while raw not in ['yes', 'no']:
        raw = input('Would you like to display raw data? yes or no.\n').lower()
        if raw not in ['yes', 'no']:
            print('You\'ve entered invalid input, please try again.')
    while raw == 'yes':
        pd.set_option('display.max_columns',200)
        print(df.iloc[i:i+5, ])
        print('-'*40)
        i += 5
        raw = input('Would you like to display more raw data?\n').lower()
        while raw not in ['yes', 'no']:
            print('You\'ve entered invalid input, please try again.')
            raw = input('Would you like to display more raw data?\n').lower()
    print('-'*40)

def restart():
    """Takes user's input on whether he would like to restart the script"""
    res= ''
    while res not in ['yes', 'no']:
        res = input('\nWould you like to restart? Enter yes or no.\n').lower()
        if res not in ['yes', 'no']:
            print('You\'ve entered invalid input, please try again.')
    return res

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_raw_data(df)
        res = restart()
        if res != 'yes':
            break


if __name__ == "__main__":
	main()
