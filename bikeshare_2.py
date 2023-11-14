import time
import pandas as pd


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Gets user input for city (chicago, new york, washington).
    CITY_DATA = { 'chicago': 'chicago.csv',
          'new york': 'new_york_city.csv',
          'washington': 'washington.csv' }
    while True:
        city = input("Which city do you want to explore data for? Chicago, New York or Washington? ")
        city = city.lower()
        if city in CITY_DATA:
            break
        else:
            print("\n\nThat\'s not a valid input!", "\n", "Ensure you enter the correct city in the options")
            continue
    # Gets user input for month (January, February, ... June).
    time_filt = input("\n\nAre you filtering data by a specific month, day, or not at all? Enter \"none\" for no time filter. ")
    time_filt = time_filt.lower()
    if time_filt == "month":
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        day = "all"
        while True:
            month = input("\n\nWhich Month? January, February, March, April, May, or June? ")
            month = month.title()
            if month in months:
                break
            else:
                print("Invalid Selection! Please enter a month in the list.")
                continue

# Gets user input for day of week (all, monday, tuesday, ... sunday).
    elif time_filt == "day":
        month = "all"
        day_int = [1,2,3,4,5,6,7]
        while True:
            try:
                day = int(input("Which day? Enter value as an integer, e.g, 1=Sunday: "))
                if day in day_int:
                    break
                else:
                    print("\nOops! Out of range. Please enter values between 1 and 7")
                    continue
            except ValueError:
                print("\nThat\'s not an int! Enter value as an integer.")
    else:
        print("Applying no filter.........")
        month = "all"
        day = "all"

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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df["Start Time"])
    df['month'] = df["Start Time"].dt.month
    df['day_of_week'] = df["Start Time"].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    if month != "all":
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    elif month == "all":
        df
    if day != 'all':
        days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        day = days[day - 1]
        df = df[df['day_of_week'] == day.title()]
    elif day == "all":
        df
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    # Computes the most common month.

    popular_month = df["month"].mode()[0]
    popular_month = months[popular_month - 1]
    print("\nMost Popular Month:", popular_month)
    # Computes the most common day of week.
    popular_weekday = df["day_of_week"].mode()[0]
    print("\nMost Popular Weekday:", popular_weekday)
    # Computes the most common start hour.
    popular_hour = df["hour"].mode()[0]
    print("\nMost Popular Start Hour:", popular_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Computes most commonly used start station.
    popular_strt_stn = df["Start Station"].mode()[0]
    print("\nMost Popular Start Station:", popular_strt_stn + ",", "Count:", df["Start Station"].value_counts()[popular_strt_stn])

    # Computes most commonly used end station.
    popular_end_stn = df["End Station"].mode()[0]
    print("\nMost Popular End Station:", popular_end_stn + ",", "Count:", df["End Station"].value_counts()[popular_end_stn])

    # Computes most frequent combination of start station and end station trip.
    popular_strt_end_stn_combo = df.groupby(['Start Station', 'End Station']).size().idxmax()
    popular_strt_end_stn_combo_count = df[['Start Station', 'End Station']].value_counts().reset_index(name='count')
    print("\nMost Frequent Combination of Start Station and End Station:", popular_strt_end_stn_combo , "Count:", popular_strt_end_stn_combo_count["count"].max())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Computes total travel time.
    tot_trv_time = df["Trip Duration"].sum()
    print("\nTotal Trip Duration:", tot_trv_time)
    # Computes mean travel time.
    avg_trv_time = df["Trip Duration"].mean()
    print("\nAverage Trip Duration:", avg_trv_time)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Computes counts of user types.
    user_typ_count = df["User Type"].value_counts()
    print("\n", user_typ_count)
    # Computes counts of gender.
    if "Gender" in df:
        gender_count = df["Gender"].value_counts()
        print("\n", gender_count)
    else:
        print("\nNo Available Gender Data")
    # Computes earliest, most recent, and most common year of birth.
    if "Birth Year" in df:
        earliest_yob = df["Birth Year"].min()
        print("\nEarliest Birth Year:", int(earliest_yob))
        most_recent_yob = df["Birth Year"].max()
        print("\nMost Recent Birth Year:", int(most_recent_yob))
        popular_yob = df["Birth Year"].mode()[0]
        print("\nMost Common Birth Year:", str(int(popular_yob)) + ",", "Count:", df["Birth Year"].value_counts()[popular_yob])
    else:
        print("\nNo Available Birth Year Data")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    """
    Asks user if they want to see 5 lines of raw data.
    Then returns 5 lines of raw data if user inputs `yes`. Iterates until user response with a `no`
    """
    position = 5
    data = df
    while True:
        answer = input('Would you like to see 5 lines of raw data? Enter yes/y or no/n: ')
        if (answer.lower() == 'yes') | (answer.lower() == 'y'):
            print(data.iloc[position-5:position])
            position += 5
        else:
            break



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
