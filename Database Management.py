import sqlite3
from OpenAI_Lookup import ask_gpt

# Connect to the SQLite database
conn = sqlite3.connect('Databases/DJ Equipment/marketplace_cdj.db')

# Create a cursor object
cursor = conn.cursor()

# Execute the SELECT query
cursor.execute("SELECT * FROM listings")

# Fetch all the rows from the query result
rows = cursor.fetchall()

# Iterate through each row
for row in rows:
    # Access the individual columns using index or column names
    title = row[2]  # Assuming column1 is the first column in the table
    price= row[1]  # Assuming column2 is the second column in the table
    description = row[4].replace("\n", "").replace("\r", "")

    post_content = str(f"Title of Post: {title}\nDescription of Post: {description} \n")
    print(ask_gpt(post_content))

# Close the cursor and the database connection
cursor.close()
conn.close()