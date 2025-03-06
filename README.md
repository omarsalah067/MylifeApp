# Mylife Habit Tracker 

**Mylife** is a command-line habit tracking application that helps you create, track, and analyze habits efficiently.  
It uses a JSON-based database for storing habits and supports streak calculations for better tracking.

## Features
-  Create, update, and delete habits
-  Mark habits as completed
-  Track streaks for daily and weekly habits
-  View habit analytics
-  Sort and filter habits
-  Simple CLI interface with `mla` shortcut

---

## Installation
### Package Installation
1. Download dist.zip folder:
    
   - Direct download from repository: 

   - Or, get the repository by termial:
        
            
            git clone https://github.com/omarsalah067/MylifeApp.git
      - Use your prefered extraction application to unzip the project.

2. Ensure you are using Python 3.9+:
    
        python --version
3. Run the App:
    navigate into the project and run `start.bat` file to automatically set up the project


### Dev Mode:
Dev mode allows for source code inspection and testing.
To enter developer mode:
1.  Download the entire source code of the app:
    
        git clone https://github.com/omarsalah067/MylifeApp.git
        cd MylifeApp
2. Open the project in your prefered IDE then run in the (virtual) terminal this command to install the package using editable mode:

        pip install -e .

3. After accessing dev mode, script setup in `pyproject.toml` should be working again allowing you to run Mylife from anywhere in the terminal using:

        mla
     - Additionally: for testing you can use pytest to run the test files and seed-db to intialise a seed database:
     
           mla seed-db
           pytest .
        
## Trouble Shooting
### 'mla' is not recognized!
If an error mesasge appears with the message: `'mla' is not a recogized command` try to use:

    python -m mylife.mla

if that fails aswell the issue is stemming from a corrupt installation, it is recommended to delete and reinstall the app again.
