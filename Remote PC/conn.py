#!/usr/bin/python
import psycopg2
#note that we have to import the Psycopg2 extras library!
import psycopg2.extras
import sys
 
def main():
	conn_string = "host='localhost' dbname='testdb' user='willow' password='willow'"
	# print the connection string we will use to connect
	print "Connecting to database\n	->%s" % (conn_string)
 
	# get a connection, if a connect cannot be made an exception will be raised here
	conn = psycopg2.connect(conn_string)
 
	# conn.cursor will return a cursor object, you can use this query to perform queries
	# note that in this example we pass a cursor_factory argument that will
	# dictionary cursor so COLUMNS will be returned as a dictionary so we
	# can access columns by their name instead of index.
	cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
 
	# tell postgres to use more work memory
	work_mem = 2048
 
	# by passing a tuple as the 2nd argument to the execution function our
	# %s string variable will get replaced with the order of variables in
	# the list. In this case there is only 1 variable.
	# Note that in python you specify a tuple with one item in it by placing
	# a comma after the first variable and surrounding it in parentheses.
	cursor.execute('SET work_mem TO %s', (work_mem,))
 
	# Then we get the work memory we just set -> we know we only want the
	# first ROW so we call fetchone.
	# then we use bracket access to get the FIRST value.
	# Note that even though we've returned the columns by name we can still
	# access columns by numeric index as well - which is really nice.
	cursor.execute('SHOW work_mem')
 
	# Call fetchone - which will fetch the first row returned from the
	# database.
	memory = cursor.fetchone()
 
	# access the column by numeric index:
	# even though we enabled columns by name I'm showing you this to
	# show that you can still access columns by index and iterate over them.
	print "Value: ", memory[0]
 
	# print the entire row 
	print "Row:	", memory

	SQL = "INSERT INTO hej (asd) VALUES (%s);"
	data = ("500", )
	cursor.execute(SQL, data)
	conn.commit()

	cursor.execute("SELECT asd FROM hej")
	print cursor.fetchall()
	#print x, type(x), repr(x)

	#x = cursor.fetchone()[0]
	#print x, type(x), repr(x)
	#x = cursor.fetchone()[0]
	#print x, type(x), repr(x)
 
if __name__ == "__main__":
	main()
