from mylife.analytics import *
import test_data
import pytest

class TestAnalytics:
    """ Tests on analytics class """
    def setup_method(self):
        pass
    
    # Accepts unintended frequencies if supplied directly without running through schema map first
    def test_on_filter(self):
        habits = test_data.habits
        filter_by_frequency(habits, "daily")
        filter_by_frequency(habits, "weekly")
        # frequency is an required param but will return empty lits if frequency value is not of ["daily", "weekly"] but doesn't raise error (Intended)
        filter_by_frequency(habits, "monthly")
        filter_by_frequency(habits, frequency=None)
        
        #single habit param call is impossible and returns TypeError as intended
        with pytest.raises(TypeError):
            filter_by_frequency(habits[0], habits[0].frequency)

    # Passes all functions with flying colors
    def test_on_calculator(self):
        habits = test_data.habits
        
        #single habit param call:
        assert type(calculate_streak(habits[0].completion_dates, habits[0].frequency)) == tuple
        
        #Loop on list call:
        for habit in habits:
            assert type(calculate_streak(habit.completion_dates, habit.frequency)) == tuple
            
        #Empty completion dates: (should return empty tuple of time int so it doesnt break the code)
        assert calculate_streak(completion_dates=None, frequency="daily") == (0,0)
        
        streaks_for_all(habits)
            
    def teardown_method(self):
        pass