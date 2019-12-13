import os

online = False
if online:
    DB_URL = os.getenv("DATABASE_URL")
else:
    DB_URL ="postgres://ivpallnyfezioy:075baf8e129b0d52dbd6d87dd3c774363b0b10b499921f821378ed7084bfc744@ec2-46-137-187-23.eu-west-1.compute.amazonaws.com:5432/dagmb1jla3rmdp"

def get_results(cursor):
    desc = cursor.description
    column_names = [col[0] for col in desc]
    data = [dict(zip(column_names,row)) for row in cursor.fetchall()] #array of dict
    #data[0].values() values of the first row
    res = []
    for i in data:
        res.append(i.values())
    cursor.close()
    return (res) #2d array 