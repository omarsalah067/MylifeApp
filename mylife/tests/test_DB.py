import pytest
from mylife.DB import Database
import test_data
import shutil
import os


class TestDB:
    """ Tests on Database class """
    def setup_method(self):
        pass

    # test for incorrect date entry
    def test_db_functions(self):
        # load_db()
        #load from no dict file
        no_dict_db = Database(filename="mylife\\tests\\test_empty_dict.json")
        
        #load from a existing dict file
        dict_db = Database(filename="mylife\\tests\\test_working_dict.json")
        
        #save_db()
        no_dict_db.save_db()
        
        dict_db.save_db()
        
        #save_habit()
        for habit in test_data.habits:
            hdict = habit.to_dict()
            dict_db.save_habit(hdict)
            
        assert no_dict_db.db["habit"] != dict_db.db["habit"] 
        
        #validate_data()
        perfect_habit = {"id": 1, 
                        "name": "Running",
                        "desc": "Run a lap around Tierpark Park",
                        "frequency": "weekly",
                        "completion dates": [
                            "26/02/2025",
                            "01/03/2025",
                            "02/03/2025",
                            "03/03/2025",
                            "04/03/2025"
                        ]}
        assert no_dict_db.validate_habit(perfect_habit) == True
        
        alt_habit = {"id": 1, 
                    "name": "Drink water",
                    "desc": "Drink atleast 1 cup of water everyday",
                    "frequency": "daily",
                    "completion dates": []}
        
        assert no_dict_db.validate_habit(alt_habit) == True
        
        # name too long
        name_error = {"id": 1, 
                    "name": "This name is above the size limit",
                    "desc": "Drink atleast 1 cup of water everyday",
                    "frequency": "daily",
                    "completion dates": []}
        # name too short
        name_error2 = {"id": 1, 
                    "name": "n",
                    "desc": "Drink atleast 1 cup of water everyday",
                    "frequency": "daily",
                    "completion dates": []}
        
        #name containes illegal elements
        name_error3 = {"id": 1, 
                    "name": "n1ce $ne",
                    "desc": "Drink atleast 1 cup of water everyday",
                    "frequency": "daily",
                    "completion dates": []}
        
        #desc too long 
        desc_error = {"id": 1, 
                    "name": "Drink water",
                    "desc": "This description is above the size limit by 1 !_!_!",
                    "frequency": "daily",
                    "completion dates": []}
        
        #freq is not of enumeration["weekly, daily"]
        frequency_error = {"id": 1, 
                    "name": "Drink water",
                    "desc": "Drink atleast 1 cup of water everyday",
                    "frequency": "monthly",
                    "completion dates": []}
        
        #is not list of type string 
        cd_error = {"id": 1, 
                    "name": "Drink water",
                    "desc": "Drink atleast 1 cup of water everyday",
                    "frequency": "daily",
                    "completion dates": [1,2,3,4]}
        
        err_list = [name_error, name_error2, name_error3, desc_error, frequency_error, cd_error]
        
        for i in err_list:
            no_dict_db.validate_habit(i) == False
        
        #last_id()
        
        #has no habits so the last id used is -1
        assert no_dict_db.last_id() == -1
        # Has 10 habits saved so the last id in the db is 9
        assert dict_db.last_id() == 9
        
        #get_habit_by_name()
        with pytest.raises(LookupError):
            no_dict_db.get_habit_by_name("no such name")
            
        assert dict_db.get_habit_by_name("Running") == dict_db.db["habit"]["0"]
        
        
        #delete_habit()
        old_db = no_dict_db.db.copy()
        #adding habit
        entry_to_delete = {"id": 10, 
                    "name": "Drink water",
                    "desc": "Drink atleast 1 cup of water everyday",
                    "frequency": "daily",
                    "completion dates": []}
        no_dict_db.save_habit(entry_to_delete)
        
        #deleting based on key
        no_dict_db.delete_habit("10")
        assert no_dict_db.db == old_db
        
    def teardown_method(self):
        shutil.copyfile("mylife\\tests\\test_empty_dict.json", "mylife\\tests\\test_working_dict.json")
        os.remove("mylife\\tests\\test_empty_dict.json") 
        pass