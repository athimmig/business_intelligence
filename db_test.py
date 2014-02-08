# Important imports
import sys
import MySQLdb
from MySQLdb import *

# Database parameters
MYSQL_DB        = 'movies'
MYSQL_TABLE     = 'movies'
MYSQL_HOST      = 'localhost'
MYSQL_USER      = 'root'
MYSQL_PASSWORD  = 'cangetin'

# Attempt to insert a record into the database
def insert_database(movie):
    # Get the cursor
    cursor = connection.cursor()

    # Extract the data from the dict
    # keys
    print movie.keys()

    #values
    print movie.values()

    #key-values
    print str(movie)

    # Extract the data
    rank = movie['rank']
    rating = movie['rating']
    title = movie['title']
    review_count = movie['review_count']
    year = movie['year']

    # Debug: checking types, all are coming out as tuples
    print "TYPES:"
    print "rank: ", type(rank)
    print "rating:", type(rating)
    print "title:", type(title)
    print "review_count:", type(review_count)
    print "year:", type(year)

    # I think this is failing because the datatypes don't match
    sql = """INSERT INTO movies
             VALUES 
             (null, {:d}, {:d}, \"{:s}\", {:d}, {:d})""".format(
             rank, rating, title, review_count, year)

    print sql
    print "Trying to commit..."
    try:
        cursor.execute(sql)
        connection.commit()
        print "Commited"
    except MySQLdb.Error, e:
        connection.rollback()
        print "Error %d: %s" % ( e.args[0], e.args[1] )

    connection.close()

movie = {}

# Open spider-database connection
try:
    connection = MySQLdb.connect(host = MYSQL_HOST,
                           user = MYSQL_USER,
                           passwd = MYSQL_PASSWORD,
                           db = MYSQL_DB)
    print "Connection established."

except MySQLdb.Error, e:
    print "Unable to connect to database."
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)

if (connection):
    movie = {'rank': 1,
            'rating': 100,
            'title': "Pacific Rim",
            'review_count': 84,
            'year': 2013 }

    insert_database(movie) #pass is movie once it's working