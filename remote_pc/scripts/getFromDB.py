#This script can print all the data from database and can be used as a getter
#!/usr/bin/python
import psycopg2
import psycopg2.extras
import sys
import rospy
 
def main():
	# Connect to an existing database
	conn = psycopg2.connect("dbname=example_db user=example_owner password=example_owner")
	# Open a cursor to perform database operations
	cur = conn.cursor()
	# Query the database and obtain data as Python objects
	cur.execute("SELECT * FROM lidar_data;")
	row = cur.fetchall()
	print row[-1]
	# Make the changes to the database persistent
	conn.commit()
	# Close communication with the database
	cur.close()
	conn.close()
	return row

if __name__ == "__main__":
	main()
