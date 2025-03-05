import json
from jsonschema import validate, ValidationError
from mylife.schema import schema 
import os
# dir_path = os.path.dirname(os.path.realpath(__file__))

class Database:
    """ 
    Database Class
    ==============
    database class used to save and load data into JSON file

    Attributes
    ----------
    last_id : int
        the last id used in the database, used for correct incrementation.
    filename : str
        a string that is used to cotrol the location of the JSON file creation or selection of database
    db_schema : dict
        The default schema structure for the database.
    db : dict
        The in-memory representation of the loaded database.
        
    Methods
    -------
    
    save_db()
    
    load_db()
    
    validate_habit(habit_data: dict[str, any]) : Boolean or ValidationError

    save_habit(habit_data: dict[str, any])
    
    last_id() : int last_id OR -1
    
    get_habit_by_name(name: str) : dict[str, any] OR LookUpError
    
    delete_habit(id: str)
    """

    #def __init__(self, filename= (dir_path + "\\MylifeData.json")):
    def __init__(self, filename= "mylife\\MylifeData.json"):
        self.filename = filename
        self.db_schema = {"database": self.filename, "habit": {}}  # Dictionary-based storage
        self.db = self.load_db()

    def save_db(self):
        """Save database to JSON file."""
        with open(self.filename, "w") as f:
            json.dump(self.db, f, indent=4)

    def load_db(self):
        """Load database, initialize if missing."""
        try:
            with open(self.filename, "r") as f:
                content = f.read().strip()
                if not content:
                    self.db = self.db_schema
                    self.save_db()
                    return self.db
                return json.loads(content)
        except (FileNotFoundError, json.JSONDecodeError): # json Decoder Error sometimes rises because File not found error was caught so both must be expected.
            self.db = self.db_schema
            self.save_db()
            return self.db
        
    def inject_seed_data(self, seed_filename="mylife\\seed_dict.json"):
        """Injects a predefined seed database into the current database."""
        if not os.path.exists(seed_filename):
            print(f"Error: Seed file '{seed_filename}' not found!")
            return False

        try:
            with open(seed_filename, "r") as f:
                seed_data = json.load(f)

            # Merge seed data with the existing database
            self.db["habit"].update(seed_data["habit"])
            self.save_db()
            print("Seed database injected successfully!")
            return True

        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error loading seed data: {e}")
            return False
        
    def validate_habit(self, habit_data: dict[str, any]):
        """
        Validate habit data against JSON Schema.
        
        Parameters
        ----------
        habit_data : dict[str, any]
            The habit dictionary.

        Raises
        ------
        ValidationError
            If the data has any ellegal element detected by JSON schema     
        """
        try:
            validate(instance=habit_data, schema=schema)  # Validate using JSON Schema
            return True
        except ValidationError as e:
            print(f"Validation Error: {e.message}")  # Print validation error message
            return False
    
    def save_habit(self, habit_data: dict[str, any]):
        """Save or update a habit in the database with validation."""
        if not self.validate_habit(habit_data):  # Validate habit before saving
            print("Error: Habit data is not valid!")
            return False

        self.db["habit"][str(habit_data["id"])] = habit_data  # Store Habit Using ID as Key
        self.save_db()
        return True
    
    def delete_habit(self, habit_id):
        """ Delete an entry based on id primary key """
        del self.db["habit"][str(habit_id)]  
        self.save_db()
    
    def last_id(self) -> int:
        """ takes the last id as an int, or returns -1 if there is no data.
        :return: Last ID | -1
        :rtype: int"""
        if not self.db["habit"]:
            return -1
        return max(int(id) for id in self.db["habit"])

    def get_habit_by_name(self, name) -> dict[str, any]:
        """ 
        looks up the database and tries to find the habit then returns it, else throws a Lookup Error
        
        :return: habit 
        :rtype: dict[str, any]
        
        Raises
        ------
        LookUpError
            If there is no habit under the name parameter
        """
        for habit in self.db["habit"].values():
            if habit["name"] == name:
                return habit
        raise LookupError(f"name {name} was not found in database!")