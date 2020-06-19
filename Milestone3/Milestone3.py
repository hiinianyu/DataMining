from pyhive import hive
import pandas as pd

host_name = "localhost"
port = 10000
database = "default"

def hiveconnection(host_name,port,database):
    conn=hive.Connection(host=host_name, port=port, database=database)
    cur=conn.cursor()
    cur.execute('Select * from data_table')
    result=cur.fetchall()

    return result

output = hiveconnection(host_name, port, database)
df = pd.DataFrame(output)