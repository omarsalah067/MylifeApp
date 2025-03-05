from datetime import datetime
from mylife.DB import Database

class Habit:
    """
    Habit Class
    ===========

    This class represents a habit and provides methods to manage its attributes, 
    track completions, update data, and convert it to/from dictionary format for 
    database storage.

    Attributes
    ----------
    id : int
        The unique identifier for the habit.
    name : str
        The name of the habit.
    desc : str
        A short description of the habit.
    frequency : str
        The frequency of the habit ("daily" or "weekly").
    completion_dates : list[str]
        A list of dates (formatted as "DD/MM/YYYY") when the habit was marked as completed.

    Methods
    -------
    check(completion_date: str = datetime.now().strftime("%d/%m/%Y"))

    update(new_data: dict) -> Habit

    to_dict() -> dict

    from_dict(dict1: dict) -> Habit
        
    __str__() -> str
        
    """

    def __init__(self, id: int, name: str, desc: str, frequency: str, completion_dates= None):
        self.id = id
        self.name = name
        self.desc = desc
        self.frequency = frequency
        self.completion_dates= completion_dates or []

    def check(self, completion_date: str = datetime.now().strftime("%d/%m/%Y")):
        """Mark the habit as completed at a specific time."""
        self.completion_dates.append(completion_date)
        self.completion_dates.sort()


    def update(self, new_data: dict[str, any]):
        """ 
        Updates the habit's attributes based on a dictionary of new values. 
        Saves changes to the database.
        """
        if (new_data["name"]): self.name = new_data["name"]
        if (new_data["desc"]): self.desc = new_data["desc"]
        if (new_data["frequency"]): self.frequency = new_data["frequency"]
        if (new_data["completion dates"]): self.completion_dates = new_data.get("completion dates", [])
        database = Database()
        database.save_habit(self.to_dict())
        database.save_db()
        return self

    def to_dict(self) -> dict[str, any]:
        """ Converts the Habit object into a dictionary for JSON storage. """
        habit_dict = {
            "id": self.id,
            "name": self.name,
            "desc": self.desc,
            "frequency": self.frequency,
            "completion dates": self.completion_dates
        }
        return habit_dict
    
    @staticmethod
    def from_dict(dict1: dict[str: any]):
        """Convert dictionary back to Habit object."""
        return Habit(
            id=int(dict1["id"]),
            name=dict1["name"],
            desc=dict1["desc"],
            frequency=dict1["frequency"],
            completion_dates=dict1.get("completion dates", [])
        )
    
    def __str__(self):
        return f"{self.name} | {self.desc} | frequency: {self.frequency}"

        
