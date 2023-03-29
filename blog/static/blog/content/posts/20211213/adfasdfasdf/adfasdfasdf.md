# Corio



To run the application, simply use the command `python main.py`. You will likely need to install any missing packages. 



Once running, navigate to `http://localhost:8000/` in your web browser. 



If you do not have Flask installed, just run `pip install Flask`. 



---



09/19/21 - The current version of the application allows a user to visit the homepage, submit an individual's data and video file, and select data points on skin for subsequent for later use in skin detection. 



The currently known issues/bugs/things-to-do:



- Very little form validation during data submission (e.g. you can enter `seventy-eight` as your age).



- No video file size or dimension limits/requirements. 



- Template layout issues during skin point selection. 



- `Submit Selections` button is inactive/does nothing. 



- Filler text needs replaced on all pages.



- Form data needs to be saved to a database, spreadsheet, etc. 



- Only .MOV files allowed for video uploads. 

