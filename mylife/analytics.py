from datetime import datetime
from mylife.habit import Habit

# Collectio of analysis methods

def filter_by_frequency(habits: list[Habit], frequency: str) -> list[Habit]:
    """
    Filter habits by frequency.
    
    Parameters
    ----------
    habits : list[Habit]
        A list of habit objects used as base for filering.
    
    frequency : ["daily", "weekly"]
        The key to filter by.
        
    :return: Filtered list of habits
    :rtype: list[Habit]
    """
    return list(filter(lambda h: h.frequency == frequency, habits))

def calculate_streak(completion_dates: list[str], frequency: str) -> tuple[int, int]:
    """
    Calculate the longest and current streak for a list of completion dates based on the habit's frequency. 
    
    Parameters
    ------------
    completion_dates : list[str]
        Completion dates list which will be used to calculate streak | format: %d/%m/%Y
        
    frequency : ["daily", "weekly"]
        The calculation algorthim key, used to specify which wtype of streak output.
        
    :return: tuple(Longest Streak, Current Streak)
    :rtype: tuple[int, int]
    """
    if not completion_dates:
        return 0, 0

    # Convert completion_dates (list of strings) into a list of datetime objects
    dates = [datetime.strptime(day, "%d/%m/%Y") for day in completion_dates]
    dates.sort()  # Sort dates for easier computing

    # Group completion dates day for daily, week for weekly
    unique_periods = [] 
    for day in dates:
        period = day.date() if frequency == "daily" else day.isocalendar()[:2] 
        if period not in unique_periods:  # Prevent multiple increments per week
            unique_periods.append(period)

    # Calculate the longest streak
    longest_streak = current_streak = 1
    for i in range(1, len(unique_periods)):
        if (frequency == "daily" and (unique_periods[i] - unique_periods[i - 1]).days == 1) or \
           (frequency == "weekly" and unique_periods[i][1] == unique_periods[i - 1][1] + 1):
            current_streak += 1
            longest_streak = max(longest_streak, current_streak)
        else:
            current_streak = 1
    return longest_streak, current_streak

def streaks_for_all(habits: list[Habit]) -> list:
    """Shorthand method for longest streak across all habits."""
    streaks = []
    for h in habits:
        s = calculate_streak(h.completion_dates, h.frequency)
        streaks.append(s)
    return streaks if streaks else 0

def longest_streak_habit(habit: Habit) -> int:
    """ Shorthand method for calculating the longest streak for a specific habit."""
    l,c = calculate_streak(habit.completion_dates, habit.frequency)
    return l if l else 0

def current_streak(habit: Habit) -> int:
    """ Shorthand method for calculating the current streak for a specific habit."""
    l, c = calculate_streak(habit.completion_dates, habit.frequency)
    return c if c else 0

def get_filtered_habits(filter, habits: list[Habit]) -> list[Habit]:
    """ 
    Shorthand method to return a filtered list of Habit objects based of a pre-selected filter methods.
    
    Parameters
    ----------
    filter : str
        The frequency type to be used for filtering
    habits : list[Habit]
        A list of habit objects used as base for calculation.
        
    :return: Filtered list of habits
    :rtype: list[Habit]"""
    if(not filter):
        return habits
    #Daily finder
    elif (filter == "daily"):
        result = filter_by_frequency(habits, "daily")
    #Weekly finder
    elif (filter == "weekly"):
        result = filter_by_frequency(habits, "weekly")
    return result

def get_sorted_habits(sorter, habits: list[Habit]) -> list[Habit]:
    """ Shorthand method to return a sorted list of Habit objects based of a pre-selected sorter methods
    Parameters
    ----------
    sorter : str
        The sorting option to be used, can be 'ascending', 'descending', or 'streak'
    habits : list[Habit]
        A list of habit objects used as base for calculation.
        
    :return: Sorted list of habits 
    :rtype: list[Habit]
    """
    # sort decider
    if(sorter == "ascending"):
        habits.sort(key=lambda item: item.name.lower())
    elif(sorter == "descending"):
        habits.sort(reverse=True, key=lambda item: item.name.lower())
    elif(sorter == "streak"):
        habits.sort(reverse=True, key=lambda item: current_streak(item))
    return habits

def list_habits(habits: list[Habit]):
    """lists a list of habits in  structured tabular.
    
    Parameter
    ---------
    habits : list[Habit]
        A list of habit objects used as base for display.
        
    :return: Formatted Tabular String of list
    :rtype: str
    """
    # for column width
    col_widths = {
        "ID": 3,
        "Name": max(len(h.name) for h in habits) if habits else 5,
        "Desc": max(len(h.desc) for h in habits) if habits else 5,
        "Frequency": max(len(h.frequency) for h in habits) if habits else 6
    }

    result= ""
    # Header Row
    header = f"{'ID'.ljust(col_widths['ID'])} | {'Name'.ljust(col_widths['Name'])} | {'Desc'.ljust(col_widths['Desc'])} | {'Frequency'.ljust(col_widths['Frequency'])}"
    separator = "-" * len(header)
    result += header + "\n"
    result += separator + "\n"

    # Habits lister
    for habit in habits:
        row = f"{str(habit.id).ljust(col_widths['ID'])} | {habit.name.ljust(col_widths['Name'])} | {habit.desc.ljust(col_widths['Desc'])} | {habit.frequency.ljust(col_widths['Frequency'])}"
        result += row + "\n"
    
    return result
