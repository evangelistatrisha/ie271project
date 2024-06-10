import dbconnect as db

def addfewgenres(): 
 
    # We use the function modifydatabase() -- it has 2 arguments 
    # The first argument is the sql code, where we use a placeholder %s 
    # The second argument is ALWAYS a list of values to replace the %s in the sql code 
 
       # The %s are known as placeholders for the values to place in the db. 
    # Using placeholders is a good way to avoid “SQL INJECTION” into the db 
    # Better than directly adding variables into the sql string 
 
    # importing datetime object from the datetime package (i know confusing) 
    # so we can get current the current date and time 
    from datetime import datetime 
 
    # The order of values on this list must correspond to the query above 
    # If the SQL has no placeholders, use an empty list (i.e. []) 
   
    # Just some feedback that the code succeeded 
    print('done!') 

sql_query = """ SELECT * FROM employee""" 
values = [] 
# number of column names must match the attributes for table genres 
columns = ['employee_id', 'name', 'position'] 
 
df = db.querydatafromdatabase(sql_query, values, columns) 
print(df)


