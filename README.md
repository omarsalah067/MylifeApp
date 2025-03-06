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
1. Download dist folder:
    
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
1.  Download the entire source code of the app and install the package using editable mode:
    
        git clone https://github.com/omarsalah067/MylifeApp.git
2. Open the project in your prefered IDE then run in the (virtual) terminal:

        pip install -e .

    After accessing dev mode, script setup in `pyproject.toml` should be working again allowing you to run Mylife from anywhere in the terminal using:

        mla
     - Additionally: After setup, you can run this command to test the project.
     
            pytest .
        
## Trouble Shooting
### 'mla' is not recognized!
If an error mesasge appears with the message: "'mla' is not a recogized command" try to use:

    python -m mylife.mla

if that fails aswell the issue is stemming from a curropt installation, it is recommended to delete and reinstall the app again.
