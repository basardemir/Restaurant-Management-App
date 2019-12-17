import psycopg2 as dbapi2
def command(url, DB_STATEMENT):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in DB_STATEMENT:
            a = cursor.execute(statement)
        cursor.close()
    return a

if __name__ == "__main__":
    #insert uri from heroku 
    url=[
    'postgres://ivpallnyfezioy:075baf8e129b0d52dbd6d87dd3c774363b0b10b499921f821378ed7084bfc744@ec2-46-137-187-23.eu-west-1.compute.amazonaws.com:5432/dagmb1jla3rmdp']
    connection = dbapi2.connect(url[0])
    cursor = connection.cursor()
    tz = cursor.execute("select * from timezone")
    tz = cursor.fetchall()
    cursor.close() 

