# Name: Mike Apreza
# NetID: maprez3
# Class: CS 341
# Overview: This project uses Python3 and SQLite. When first
#   run, the program will show basic statistics about the
#   CTA2 database. Then, the user will be able to input a
#   command (1-9 or x to exit). The following commands are
#   executed by the following functions:
#   1 - stationSearch()
#   2 - allRiders()
#   3 - top10Busy()
#   4 - least10Busy()
#   5 - stationsInLine()
#   6 - riderByMonth()
#   7 - riderByYear()
#   8 - twoStationInYear()
#   9 - stationsInColor()

import sqlite3
import matplotlib.pyplot as figure


###########################################################  
#
# print_stats
# Given a connection to the CTA database, executes various
# SQL queries to retrieve and output basic stats.
#
def print_stats(dbConn):
    dbCursor = dbConn.cursor()
    
    print("General stats:")
    # stations
    dbCursor.execute("Select count(*) From Stations;")
    row = dbCursor.fetchone();
    print("  # of stations:", f"{row[0]:,}")
    # of stops
    dbCursor.execute("Select count(Stop_Name) From Stops;")
    row = dbCursor.fetchone();
    print("  # of stops:", f"{row[0]:,}")
    # of ride entries
    dbCursor.execute("Select count(*) From Ridership;")
    row = dbCursor.fetchone();
    print("  # of ride entries:", f"{row[0]:,}")
    # date range
    dbCursor.execute("Select date(Ride_Date) From Ridership order by Ride_Date asc limit 1;")
    row = dbCursor.fetchone();
    dbCursor.execute("Select date(Ride_Date) From Ridership order by Ride_Date desc limit 1;")
    row2 = dbCursor.fetchone();
    print("  date range:", row[0], "-", row2[0])
    # total ridership
    dbCursor.execute("Select sum(Num_Riders) From Ridership;")
    row = dbCursor.fetchone();
    totalRidership = row[0]
    print("  Total ridership:", f"{row[0]:,}")

    # weekday ridership
    dbCursor.execute("Select sum(Num_Riders) From Ridership where Type_of_Day = 'W';")
    row = dbCursor.fetchone();
    percent = (row[0]/totalRidership)*100
    s = "%5.2f"% (percent)
    s = "(" + s + "%)"
    print("  Weekday ridership:", f"{row[0]:,}", s)
    # saturday ridership
    dbCursor.execute("Select sum(Num_Riders) From Ridership where Type_of_Day = 'A';")
    row = dbCursor.fetchone();
    percent = (row[0]/totalRidership)*100
    s = "%4.2f"% (percent)
    s = "(" + s + "%)"
    print("  Saturday ridership:", f"{row[0]:,}", s)
    # sunday/holiday ridership
    dbCursor.execute("Select sum(Num_Riders) From Ridership where Type_of_Day = 'U';")
    row = dbCursor.fetchone();
    percent = (row[0]/totalRidership)*100
    s = "%4.2f"% (percent)
    s = "(" + s + "%)"
    print("  Sunday/holiday ridership:", f"{row[0]:,}", s)
    

###########################################################  
#
# stationSearch
# The user input a partial station name, and the program
# outputs the results, or a message if none are found.
#

def stationSearch(dbConn):
  dbCursor = dbConn.cursor()
  searchStr = input("\nEnter partial station name (wildcards _ and %): ")
  
  sql = "SELECT Station_ID, Station_Name FROM Stations WHERE Station_Name like ? ORDER BY Station_Name asc;"

  dbCursor.execute(sql, [searchStr])
  rows = dbCursor.fetchall()
  
  if len(rows) == 0:
    print("**No stations found...")
  else:
    for row in rows:
      print(row[0], ":", row[1])
    print("\n")


###########################################################  
#
# allRiders
# The user will see the ridership of each station in ascending
# order by station name along with the percentage the value
# represents across all ridership.
#

def allRiders(dbConn):
  dbCursor = dbConn.cursor()
  print("** ridership all stations **")
  # Get total ridership
  dbCursor.execute("Select sum(Num_Riders) From Ridership;")
  rows = dbCursor.fetchone();
  totalRidership = rows[0]
  # Get the station names with ridership
  dbCursor.execute("SELECT Station_Name, SUM(Num_Riders) FROM Stations JOIN Ridership on (Stations.Station_ID = Ridership.Station_ID) GROUP BY Station_Name ORDER BY Station_Name asc;")
  rows = dbCursor.fetchall()
  # Print out formated info 
  for row in rows:
    percent = (row[1]/totalRidership)*100
    print(row[0], ":", f"{row[1]:,}", f"({percent:.2f}%)")
  print("\n")


###########################################################  
#
# top10Busy
# The user will see the top 10 busiest stations in terms
# of ridership in descending order by ridership.
#

def top10Busy(dbConn):
  dbCursor = dbConn.cursor()
  print("** top-10 stations **")
  # Get total ridership
  dbCursor.execute("Select sum(Num_Riders) From Ridership;")
  rows = dbCursor.fetchone();
  totalRidership = rows[0]
  # Get the station names with ridership
  dbCursor.execute("SELECT Station_Name, SUM(Num_Riders) FROM Stations JOIN Ridership on (Stations.Station_ID = Ridership.Station_ID) GROUP BY Station_Name ORDER BY SUM(Num_Riders) desc;")
  rows = dbCursor.fetchmany(10)
  # Print out formated info 
  for row in rows:
    percent = (row[1]/totalRidership)*100
    print(row[0], ":", f"{row[1]:,}", f"({percent:.2f}%)")
  print("\n")
  

###########################################################  
#
# least10Busy
# The user will see the least 10 busiest stations in
# terms of ridership in descending order by ridership.
#

def least10Busy(dbConn):
  dbCursor = dbConn.cursor()
  print("** least-10 stations **")
  # Get total ridership
  dbCursor.execute("Select sum(Num_Riders) From Ridership;")
  rows = dbCursor.fetchone();
  totalRidership = rows[0]
  # Get the station names with ridership
  dbCursor.execute("SELECT Station_Name, SUM(Num_Riders) FROM Stations JOIN Ridership on (Stations.Station_ID = Ridership.Station_ID) GROUP BY Station_Name ORDER BY SUM(Num_Riders) asc;")
  rows = dbCursor.fetchmany(10)
  # Print out formated info 
  for row in rows:
    percent = (row[1]/totalRidership)*100
    print(row[0], ":", f"{row[1]:,}", f"({percent:.2f}%)")
  print("\n")


###########################################################  
#
# stationsInLine
# The user inputs a line color, and they will see all the
# stop names that are part of that line in ascending order.
#

def stationsInLine(dbConn):
  dbCursor = dbConn.cursor()
  # Set code
  sql = "SELECT Stop_Name, Direction, ADA FROM Stops JOIN StopDetails ON (Stops.Stop_ID = StopDetails.Stop_ID) INNER JOIN Lines ON(StopDetails.Line_ID = Lines.Line_ID) WHERE Color LIKE ? ORDER BY Stop_Name asc;"
  # Get user input
  search = input("\nEnter a line color (e.g. Red or Yellow): ")
  
  # Find data
  dbCursor.execute(sql, [search])
  rows = dbCursor.fetchall()
  # Print data
  if len(rows) == 0:
    print("**No such line...")
  else:
    for row in rows:
      if row[2] == 1:
        ada = "yes"
      else:
        ada = "no"
      print(row[0], ": direction = ", row[1], "(accessible? ", f"{ada})")
  print("\n")


###########################################################  
#
# riderByMonth
# The total ridership by ascending month with be shown.
# Then the user will be given the option to plot the
# data. If the user types in anything but "y", the data
# will not be plotted. Else, it will be plotted.
#

def riderByMonth(dbConn):
  dbCursor = dbConn.cursor()
  print("** ridership by month **")
  # Find data
  dbCursor.execute("SELECT strftime('%m', DATE(Ride_Date)), SUM(Num_Riders) FROM Ridership GROUP BY strftime('%m', DATE(Ride_Date)) ORDER BY strftime('%m', DATE(Ride_Date)) asc;")
  rows = dbCursor.fetchall()
  # Print data
  for row in rows:
    print(row[0], ":", f"{row[1]:,}")
  # Ask if user wants to plot
  plot = input("Plot? (y/n)")
  
  # Do appropriate action
  if plot == "y":
    # 2 empty vectors/lists
    x = []
    y = []
    # Add each (x, y) coordinate
    for row in rows:
      x.append(row[0])
      y.append(row[1])
    
    figure.xlabel("Month")
    figure.ylabel("# of Riders (x * 10^8)")
    figure.title("Monthly Ridership")
    figure.plot(x, y)
    figure.show()
  

###########################################################  
#
# riderByYear
# The total ridership by ascending year with be shown.
# Then the user will be given the option to plot the
# data. If the user types in anything but "y", the data
# will not be plotted.
#

def riderByYear(dbConn):
  dbCursor = dbConn.cursor()
  print("** ridership by year **")
  # Find data
  dbCursor.execute("SELECT strftime('%Y', DATE(Ride_Date)), SUM(Num_Riders) FROM Ridership GROUP BY strftime('%Y', DATE(Ride_Date)) ORDER BY strftime('%Y', DATE(Ride_Date)) asc;")
  rows = dbCursor.fetchall()
  # Print data
  for row in rows:
    print(row[0], ":", f"{row[1]:,}")
  # Ask if user wants to plot
  plot = input("\nPlot? (y/n)")
  
  # Do appropriate action
  if plot == "y":
    # 2 empty vectors/lists
    x = []
    y = []
    # Add each (x, y) coordinate
    for row in rows:
      year = row[0]
      x.append(year[2] + year[3])
      y.append(row[1])
    
    figure.xlabel("Year")
    figure.ylabel("# of Riders (x * 10^8)")
    figure.title("Yearly Ridership")
    figure.plot(x, y)
    figure.show()

###########################################################  
#
# twoStationInYear
# The user inputs a year and the names of two stations. The user
# will see the daily ridership at each station for the first and
# last 5 days of that year. If the first station name does not 
# exist or multiple stations are yielded, then an error message
# will be shown and the command will be aborted.
# The user will be asked if they want to see the data plotted.
# If yes, the plot will appear. If not, or if another thing is
# typed, then nothing will show.
#

def twoStationInYear(dbConn):
  dbCursor = dbConn.cursor()
  # Get user data
  year = input("\nYear to compare against? ")
  
  year = str(year)
  station1 = input("\nEnter station 1 (wildcards _ and %): ")
  # Find the station 1 ID
  sqlID = "SELECT Station_ID FROM Stations WHERE Station_Name LIKE ?;"
  dbCursor.execute(sqlID, [station1])
  row1 = dbCursor.fetchall()
  if len(row1) < 1: # If no station found
    print("**No station found...")
    return
  elif len(row1) > 1:
    print("**Multiple stations found...")
    return
  else:
    dbCursor.execute(sqlID, [station1])
    row1 = dbCursor.fetchone()
    sID1 = row1[0]
  station2 = input("\nEnter station 2 (wildcards _ and %): ")
  # Find the station 2 IDs
  dbCursor.execute(sqlID, [station2])
  rows2 = dbCursor.fetchall()
  if len(rows2) < 1:  # If no station found
    print("**No station found...")
    return
  elif len(rows2) > 1:
    print("**Multiple stations found...")
    return
  else:
    dbCursor.execute(sqlID, [station2])
    rows2 = dbCursor.fetchone()
    sID2 = rows2[0]
  # Make SQL code
  sql = "SELECT DATE(Ride_Date), SUM(Num_Riders) FROM Ridership WHERE Station_ID = ? and strftime('%Y', Ride_Date) = ? GROUP BY DATE(Ride_Date) ORDER BY DATE(Ride_Date) asc LIMIT 5;"
  sql2 = "SELECT DATE(Ride_Date), SUM(Num_Riders) FROM Ridership WHERE Station_ID = ? and strftime('%Y', Ride_Date) = ? GROUP BY DATE(Ride_Date) ORDER BY DATE(Ride_Date) desc LIMIT 5;"
  # Get the first and last 5 of station 1
  dbCursor.execute(sql, [sID1, year])
  first5Station1 = dbCursor.fetchall()
  dbCursor.execute(sql2, [sID1, year])
  last5Station1 = dbCursor.fetchall()
  # Get the first and last 5 of station 1
  dbCursor.execute(sql, [sID2, year])
  first5Station2 = dbCursor.fetchall()
  dbCursor.execute(sql2, [sID2, year])
  last5Station2 = dbCursor.fetchall()

  # Print data
  sql = "SELECT Station_Name FROM Stations WHERE Station_ID = ?;"
  dbCursor.execute(sql, [sID1])
  sName1 = dbCursor.fetchone()
  print("Station 1:", sID1, sName1[0])
  for row in first5Station1:
    print(row[0], row[1])
  last5Station1.reverse()
  for row in last5Station1:
    print(row[0], row[1])

  dbCursor.execute(sql, [sID2])
  sName2 = dbCursor.fetchone()
  print("Station 2:", sID2, sName2[0])
  for row in first5Station2:
    print(row[0], row[1])
  last5Station2.reverse()
  for row in last5Station2:
    print(row[0], row[1])

  # Ask if user wants to plot
  plot = input("\nPlot? (y/n)")
  
  # Do appropriate action
  if plot == "y":
    # Get all the data
    sql = "SELECT DATE(Ride_Date), SUM(Num_Riders) FROM Ridership WHERE Station_ID = ? and strftime('%Y', Ride_Date) = ? GROUP BY DATE(Ride_Date) ORDER BY DATE(Ride_Date) asc;"
    # Get the first and last 5 of station 1
    dbCursor.execute(sql, [sID1, year])
    station1Data = dbCursor.fetchall()
    dbCursor.execute(sql, [sID2, year])
    station2Data = dbCursor.fetchall()
    # 4 empty vectors/lists
    x = []
    count = 1
    while count <= 366:
      x.append(count)
      count = count + 1
    y = []
    y2 = []
    # Add each (x, y) coordinate
    for row in station1Data:
      y.append(row[1])
    for row in station2Data:
      y2.append(row[1])
    
    figure.xlabel("Day")
    figure.ylabel("# of Riders")
    figure.title("Riders Each Day of " + year)
    figure.plot(x, y)
    figure.plot(x, y2)
    figure.legend([sName1[0], sName2[0]])
    figure.show()


###########################################################  
#
# stationsInColor
# The user will input a line color. The station names that
# are part of that line will be displayed in ascending order.
# 
#

def stationsInColor(dbConn):
  dbCursor = dbConn.cursor()
  color = input("\nEnter a line color (e.g. Red or Yellow): ")
  
  # Find data
  sql = "SELECT DISTINCT(Station_Name), Latitude, Longitude FROM Stops INNER JOIN Stations ON(Stations.Station_ID = Stops.Station_ID) JOIN StopDetails ON(Stops.Stop_ID = StopDetails.Stop_ID) INNER JOIN Lines ON(StopDetails.Line_ID = Lines.Line_ID) WHERE Color LIKE ? ORDER BY Station_Name asc;"
  dbCursor.execute(sql, [color])
  stations = dbCursor.fetchall()
  # Does data exist?
  if len(stations) == 0:
    print("**No such line...")
    return
  # It does, so print it out
  for row in stations:
    print(row[0], ":",  f"{(row[1],row[2])}")
  # Ask if user wants to plot
  plot = input("Plot? (y/n) ")
  
  # If yes, plot
  if plot == "y":
    x = []
    y = []
    for row in stations:
      x.append(row[2])
      y.append(row[1])
    image = figure.imread("chicago.png")
    xydims = [-87.9277, -87.5569, 41.7012, 42.0868]
    figure.imshow(image, extent=xydims)
    # Color is the value input by user, except Purple-Express
    if(color.lower() == "purple-express"):
      color = "Purple"
    # Add coordinates
    figure.plot(x, y, "o", c=color)
    # Annotate each coordinate with its station name
    for row in stations:
      figure.annotate(row[0], (row[2], row[1]))
    figure.xlim([-87.9277, -87.5569])
    figure.ylim([41.7012, 42.0868])
    # Show the plot
    figure.title(color + " Line")
    figure.show()


###########################################################  
#
# main
#
print('** Welcome to CTA L analysis app **')
print()

dbConn = sqlite3.connect('CTA2_L_daily_ridership.db')

# print basics
print_stats(dbConn)

# Go into the loop
cmd = input("\nPlease enter a command (1-9, x to exit): ")
while (cmd != "x"):
  if (cmd == "1"):
    stationSearch(dbConn)
  elif (cmd == "2"):
    allRiders(dbConn)
  elif (cmd == "3"):
    top10Busy(dbConn)
  elif (cmd == "4"):
    least10Busy(dbConn)
  elif (cmd == "5"):
    stationsInLine(dbConn)
  elif (cmd == "6"):
    riderByMonth(dbConn)
  elif (cmd == "7"):
    riderByYear(dbConn)
  elif (cmd == "8"):
    twoStationInYear(dbConn)
  elif (cmd == "9"):
    stationsInColor(dbConn)
  else:
    print("**Error, unknown command, try again...\n")
  # Ask for input again
  cmd = input("\nPlease enter a command (1-9, x to exit): ")


#
# done
#
