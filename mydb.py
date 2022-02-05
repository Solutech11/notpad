import mysql.connector


mydb= mysql.connector.connect(
    user='root',
    host = "localhost",
    password ="",
    database= "notepad"
)

mycursor= mydb.cursor(dictionary=True)


mycursor.execute(
    """CREATE TABLE IF NOT EXISTS user(
        id INT AUTO_INCREMENT,
        name VARCHAR(250) NOT NULL,
        email VARCHAR(250) NOT NULL,
        passworrd VARCHAR(250) NOT NULL,
        Unique(email),
        Primary Key(id)
    );
    """
)

mycursor.execute(
    """CREATE TABLE IF NOT EXISTS notes(
        id INT AUTO_INCREMENT NOT NULL,
        email VARCHAR(250) NOT NULL,
        Date VARCHAR(250) NOT NULL,
        Title VARCHAR(250) NOT NULL,
        notes NVARCHAR(4294967295),
        Primary Key(id)
    );
    """
)