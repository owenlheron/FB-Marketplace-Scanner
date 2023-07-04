How to configure this project to run properly on a new account. 

Step 1: Get API keys for Brevo, Open Cage and OpenAI and enter API keys in Distance_Finder.py, Mail.py, and Database Management API.

    Need Brevo API for Mail sending: 
    Need Open Cage API for Distance calculations: https://opencagedata.com/
    Need OpenAI API for analyzing post data:

Step 2: Go to Main_Program and enter user inputs
    
    Enter keywords you want to find in search list (limit 6 per)
    Enter your town
    Enter your email
    Create a SearchStruct for each search list with a unique identifier - include your town, and email
    Add each Search_struct to search_list
    Enter your search refresh rates
    