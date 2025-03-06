import click
from mylife.habit import Habit
from mylife.DB import Database
from mylife.analytics import *

database = Database()

@click.group()
def main():
    """
    Mylife CLI Application


    This CLI-based habit tracker allows users to create, track, update, and delete 
    habits through a command-line interface. It interacts with the 'Database', 'Habit', 
    and 'Analytics' modules to manage and analyze user habits.
    
    \b
          Run the script in a terminal and interact using command-line options. 
    USGE: mla [--help] <command> [<args>, -[P], --[options], (value)]
    Note: If 'mla' is not recogmnized, call file directly using 'python -m mla'
    """
    pass
    

@main.command()
@click.option('-n', '--name', prompt='Habit name', help='The name of the habit to be marked')
@click.option('-cd', default=None, help="Used for specifying a completion date rather than automatic current date selection | format 'DD/MM/YYY'.")
def check(name: str, cd: str):
    """
    Marks a habit as completed, either for today or a specified date.
    """
    try:
        habit = Habit.from_dict(database.get_habit_by_name(name))
    except LookupError as e:
        if e:
            click.echo(f'Error: {e}')
            return
    if cd:
        habit.check(cd)
    else:
        habit.check()
    if database.save_habit(habit.to_dict()):
        click.echo(f'Habit "{name}" checked off!')
        return True
    click.echo(f'Habit "{name}" not found!')

@main.command()
@click.option('-s', '--sort', type=click.Choice(['ascending', 'descending', 'streak'], case_sensitive=False), default=None, help="sort the result by name ('ascending', 'descending') or streak ('streak').")
@click.option('-f', '--filter', type=click.Choice(['daily', 'weekly'], case_sensitive=False), default=None, help="filters by frequency value: 'daily' or 'weekly'")
def lsh(filter=None, sort=None):
    """  
    Lists all habits, with optional filtering (daily/weekly) and sorting 
        (ascending, descending, or by streak). 
    """
    data_dict = database.load_db()["habit"]
    if not data_dict:
        click.echo("No habits found in the database.")
        return
    habits = []
    for x in data_dict:
        habits.append(Habit.from_dict(data_dict[x]))
    
    
    #Quick list
    if (not filter and not sort):
        click.echo(list_habits(habits))
        return True
    
    # Filter Logic
    filtered_list = get_filtered_habits(filter, habits)
    
    # Sorter Logic
    sorted_list = get_sorted_habits(sort, filtered_list)
    click.echo(list_habits(sorted_list))
         
@main.command()
@click.option('--name', prompt='Habit name', type=str, help='Name of the habit. Only text!')
@click.option('--desc', prompt='Habit description',type=str, help='Short description of the habit you want to create (no longer than 50 chr!).')
@click.option('--frequency', prompt='frequency', type=click.Choice(['daily', 'weekly']), help="Habit's frequency: write either 'daily' or 'weekly'.")
def create(name, desc, frequency):
    """ Creates a new habit with the specified name, description, and frequency.""" 
    try:
        database.get_habit_by_name(name)
    except LookupError as e:
        if e:
            id = database.last_id() + 1
            habit = Habit(id=id, name=name, desc=desc, frequency=frequency)
            if database.save_habit(habit.to_dict()):
                click.echo(f'Habit: "{name}" successfully created!')
            return
        else: 
            click.echo(f'Habit with the name "{name}" already exists')
    
@main.command()
@click.option("-n","--name", default=None, help="name of a habit for a single targetted analysis")
def anal(name=None):
    """Displays analytics for a single habit or all habits in the database."""
    data = database.load_db()["habit"]
    
    if name:
        try:
            habit = Habit.from_dict(database.get_habit_by_name(name))
        except LookupError as e:
            click.echo(f'Error: {e}')
            return
        
        if habit.frequency == "daily":
            freq = "day(s)"
        else:
            freq = "week(s)"
        click.echo(f'Analytics for Habit: "{name}"')
        click.echo(f'- Frequency: {habit.frequency}')
        click.echo(f'- Total Completions: {len(habit.completion_dates)}')
        click.echo(f'- Current Streak: {current_streak(habit)} {freq}')
        click.echo(f'- Longest Streak: {longest_streak_habit(habit)} {freq}')
        return
            
    habits = [Habit.from_dict(x) for x in data.values()]      
    streaks = streaks_for_all(habits)  
    if streaks:
        click.echo(f'Longest streak overall: {max(streaks, key=lambda x: x[0])[0]}')
        
        daily = filter_by_frequency(habits, 'daily')
        click.echo(f'Daily habits (current streaks):')
        for h, s in zip(daily, streaks):  
            click.echo(f' - {h.name}: {s[1]}')

        weekly = filter_by_frequency(habits, 'weekly')
        click.echo(f'Weekly habits (current streaks):')
        for h, s in zip(weekly, streaks): 
            click.echo(f' - {h.name}: {s[1]}')
    return

@main.command()
@click.argument("habit_name", type=str)
@click.option('--name', help='Name of the habit. Only text!')
@click.option('--desc', help='Short description of the habit you want to create (no longer than 50 chr!).')
@click.option('--frequency', type=click.Choice(['daily', 'weekly']), help="Habit's frequency: write either 'daily' or 'weekly'.")
@click.option('--completion_dates',default=None, help="Habit's completion dates | format 'DD/MM/YYY'.")
def update( habit_name, name=None, desc=None, frequency=None, completion_dates=None):
    """ Updates an existing habit's details. """
    old_habit = database.get_habit_by_name(habit_name)
    habit_id = int(old_habit["id"])
    name = str(name) or old_habit["name"]
    desc = str(desc) or old_habit["desc"]
    frequency = frequency or old_habit["frequency"]
    completion_dates = completion_dates or old_habit.get("completion dates", [])
    
    new_habit= {
        "id": habit_id,
        "name": name,
        "desc": desc,
        "frequency": frequency,
        "completion dates": completion_dates
    }
        
    #old_habit = Habit.update(Habit.from_dict(old_habit), new_habit)
    if database.save_habit(new_habit):
        click.echo(f'Habit: "{new_habit["name"]}" successfully changed!')
        click.echo(str(new_habit))
        return
    click.echo(f'Error: Failed to updated!')
    return
    
    
@main.command()
@click.argument("habit_name", type= str)
@click.confirmation_option( prompt="Are you sure you want to delete?")
def delete(habit_name):
    """ Deletes a habit based on its name after confirmation."""
    try:
        habit = database.get_habit_by_name(habit_name)
    except LookupError as e:
        click.echo(f"Error: {e}")
        return
    database.delete_habit(habit["id"])
    click.echo(f"habit '{habit["name"]}' deleted")
    return
    
@main.command(hidden=True)
@click.confirmation_option(prompt="Are you sure you want to inject the seed database?")
@click.option("--file", default="mylife\\seed_dict.json", help="Path to seed data file")
def seed_db(file):
    """Injects the seed database (hidden command)."""
    if database.inject_seed_data(file):
        click.echo("Seed database has been successfully injected!")
    else:
        click.echo("Failed to inject the seed database.")
        
#Used to call the function once the file is called in main
if __name__ == '__main__':
    main()     

