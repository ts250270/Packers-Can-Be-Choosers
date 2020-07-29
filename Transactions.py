import pyodbc 

def LoadTransactionsFromDB():
    #connection = pyodbc.connect('server = localhost; user=sa; password=Qwe1234;  Database = Retail14')
    connection = pyodbc.connect('Driver={SQL Server};'
                      'Server=localhost;'
                      'Database=Retail14;'
                      'Uid=sa;'
                      'Pwd=Qwe12345;')
    cursor = connection.cursor()
    cursor.execute("SELECT retailtransactionId from Selling_retailTransaction;")
    trans = list(cursor.fetchall())
    return trans

