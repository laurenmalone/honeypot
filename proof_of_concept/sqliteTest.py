import sqlite3
import json

conn = sqlite3.connect('sqliteDB/test.db')
print "test.db opened"

orm_object = {u"table":
                {u"table_name": ["test_table"],
                    u"column": {u"name": ["column1"],
                                u"type": ["string"]
                                }
                }
              }

print json.dumps(orm_object, indent=4)



conn.execute('''CREATE TABLE PLUGIN (ID INT PRIMARY KEY NOT NULL,
                                   NAME TEXT NOT NULL,
                                    AGE INT NOT NULL,
                                    ADDRESS CHAR(50),
                                    SALARY REAL);''')
print "Table created successfully"


conn.close()
