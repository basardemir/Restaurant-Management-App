import os

online = True
if online:
    DB_URL = os.getenv("DATABASE_URL")


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