#!/usr/bin/python
import psycopg2
#note that we have to import the Psycopg2 extras library!
import psycopg2.extras
import sys
 
def main():
	# Connect to an existing database
	conn = psycopg2.connect("dbname=testdb user=willow password=willow")

	# Open a cursor to perform database operations
	cur = conn.cursor()

	# Execute a command: this creates a new table
	cur.execute("CREATE TABLE test2 (id serial PRIMARY KEY, num integer, data varchar);")

	# Pass data to fill a query placeholders and let Psycopg perform
	# the correct conversion (no more SQL injections!)
	#cur.execute("INSERT INTO test2 (num, data) VALUES (%s, %s)",(100, "abc'def"))

	# Query the database and obtain data as Python objects
	cur.execute("SELECT * FROM test2;")
	cur.fetchone()
	(1, 100, "abc'def")

	# Make the changes to the database persistent
	conn.commit()

	# Close communication with the database
	cur.close()
	conn.close()


if __name__ == "__main__":
	main()
