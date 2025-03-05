from mylife.habit import Habit
import pytest

class TestHabit:
    def setup_method(self):
        pass
    
    # Passes all functions with flying colors
    def test_habit_function(self):
        # Create Functionality
        habit = Habit(0, "Running", "Run a lap Tierpark", "weekly", (["05/02/2024", "07/02/2024", "12/02/2024", "15/02/2024", "19/02/2024", "04/03/2024"]))
        
        # habit's data callability
        assert type(habit.completion_dates) == list
        
        # Check() functionality
        old_length = len(habit.completion_dates)
        habit.check()
        assert old_length < len(habit.completion_dates)
        
        #to_dict() Functionality
        assert type(habit.to_dict()) == dict
        
        #str conversion of Habit object
        assert type(str(habit)) == str
        
        # Update() functionality
        old_desc = habit.desc
        update_dict = {"name": "", "desc": "Run atleast a lap in Tierpark", "frequency": "", "completion dates": [""]}
        habit = habit.update(update_dict)
        
        assert old_desc != habit.desc
        
    # Accepts unintended frequencies if supplied directly without running through schema map first (in reality is impossible)
    def test_habit_creation(self):
        #Correct Habit creation example:
        perfect_habit = Habit(0, "Running", "Run a lap Tierpark", "weekly", (["05/02/2024", "07/02/2024", "12/02/2024", "15/02/2024", "19/02/2024", "04/03/2024"]))
        assert type(perfect_habit.id) == int
        assert type(perfect_habit.name) == str
        assert type(perfect_habit.desc) == str
        assert perfect_habit.frequency == "daily" or perfect_habit.frequency == "weekly"
        assert type(perfect_habit.completion_dates) == list
        
        # Wrong example (handled by schema.py in app)  
        err_habit = Habit(0, "Running", "Run a lap Tierpark", "monthly", (["05/02/2024", "07/02/2024", "12/02/2024", "15/02/2024", "19/02/2024", "04/03/2024"]))
        # Incorrect err habit will be not one of the eumerated habit frequencies:
        assert not err_habit.frequency == "daily" or not err_habit.frequency == "weekly"

        #alternative: no completion_dates param (intended)
        alt_habit = Habit(0, "Running", "Run a lap Tierpark", "weekly")
        assert alt_habit.completion_dates == []
        
    def teardown_method(self):
        pass