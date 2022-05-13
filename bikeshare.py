# project by Daniel Krieg
# project submission to Udacity in April 2022 - reviewed positively.

import time
from datetime import timedelta
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_DATA = ['january', 'february', 'march', 'april', 'may', 'june']

DAY_DATA = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    global city
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\nYou can choose between the following cities:\n- Chicago\n- New York City\n- Washington')
   
   # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input("Please choose:   ").lower()
            test_criteria = CITY_DATA[city]
            print("\nAlright.\nLet\'s explore {}".format(city.title()))    
            break
        except KeyError:
            print('\nOh dear - I do not have any data about {}.\nPlease retry with one of the three cities mentioned above.\n'.format(city.title()))

    # get user input for month (all, january, february, ... , june)
    month = input('Please enter a month ["January", ..., "June"] to filter or \"all\":     ')
    while True:
        if month == 'all':
           break
        if month in MONTH_DATA:
           month = MONTH_DATA.index(month) + 1
           break
        else:
           month = input('Oooops...\nThis didn\'t work. Please try again:     ')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Please enter a weekday ["Monday", ..., "Sunday"] to filter or \"all\":     ')
    while True:
        if day == 'all':
           break
        if day in DAY_DATA:
           day = DAY_DATA.index(day) + 1
           break
        else:
           day = input('Oh gosh - {} is not a weekday and not \"all\".\nPlease try again:     '.format(day.title()))

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
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
   
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek # Monday = 0 / Sunday = 6
    df['start_hour'] = df['Start Time'].dt.hour


    # filter by month if applicable
    if month != 'all':
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]
    return df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    popular_month = MONTH_DATA[popular_month -1].title()
    print('The most common month for bike rentals in {} is {}.\n'.format(city.title(), popular_month))
    
    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    popular_day = DAY_DATA[popular_day].title()
    print('The most common day is {}.\n'.format(popular_day))

    # display count per start hour
    popular_hour_group = df.groupby(['start_hour'])['Start Time'].count()
    print('Heres a count of rides per start hour:\n',popular_hour_group)

    # display the most common start hour
    popular_hour = df['start_hour'].mode()[0]
    xm = 'am'
    if popular_hour > 12:
        popular_hour = popular_hour - 12
        xm = 'pm'
    print('\nThe most common start hour is at {} {}.\n'.format(popular_hour, xm))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]

    # display most commonly used end station    
    popular_end_station = df['End Station'].mode()[0]
    print('The most common start station is {}...\n ...and most people finish their rental at {}.\n'.format(popular_start_station, popular_end_station))


    # display most frequent combination of start station and end station trip
    df['Start End'] = df['Start Station'] + " to " + df['End Station']
    popular_trip = df['Start End'].mode()[0]
    print('The most frequently used trip is from {}.'.format(popular_trip))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = int(df['Trip Duration'].sum())
    total_travel_time = timedelta(seconds=total_travel_time)
    print('The total duration of all filtered rides is {} [hh:mm:ss].'.format(total_travel_time))

    # display mean travel time
    mean_travel_time = int(df['Trip Duration'].mean())
    mean_travel_time = timedelta(seconds=mean_travel_time)
    print('The mean travel time of all filtered rides is {} [hh:mm:ss].'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_user_type = df.groupby(['User Type'])['User Type'].count()
    print('Amount of rentals per user type:\n{}'.format(count_user_type))    

    # Display counts of gender
    if city != 'washington':
        count_gender = df.groupby(['Gender'])['Gender'].count()
        print('\nAmount of rentals per gender:\n{}'.format(count_gender))     
    else:
        print('\nSorry dude, no gender information available for {}'.format(city.title()))

    # Display earliest, most recent, and most common year of birth
    if city != 'washington':
        oldest = int(df['Birth Year'].min())
        age = 2017 - oldest
        print('\nThe oldest person who rented a bike within the filtered data was born in {}\nThis means, he or she was {} years old when renting the bike in 2017'.format(oldest, age))     
    
        youngest = int(df['Birth Year'].max())
        age = 2017 - youngest
        print('\nThe youngest person who rented a bike within the filtered data was born in {}\nThis means, he or she was {} years old when renting the bike in 2017'.format(youngest, age))     
    
        most_common = int(df['Birth Year'].mode()[0])
        #age = 2017 - youngest
        print('\nThe most common year of birth from customers renting a bike in the selected timeframe is {}'.format(most_common))     
    
    else:
        print('\nSorry dude, no birthday information available for {}'.format(city.title()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_raw_data(df):
    """Ask if the user wants to see raw data."""

    #while True:
    raw = input('Would you like to see some raw data? Enter yes or no.\n')
    if raw.lower() == 'yes':
        i = 0
       # df = df[df['Index'] <= i]            
        print(df.head(5))

        while True:
            raw = input('How about some more raw data? Enter yes or no.\n')
            if raw.lower() == 'yes':
                i = i + 5
                j=  i + 5
                print('Here are rows {} to {}:'.format(i,j-1))
                print(df.iloc[i:j])
            else:
                break
        

def main():
    """Main function that calls all subfunctions after another"""
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        input("Press Enter to continue...")
        station_stats(df)
        input("Press Enter to continue...")
        trip_duration_stats(df)
        input("Press Enter to continue...")
        user_stats(df)
        input("Press Enter to continue...")
        show_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
