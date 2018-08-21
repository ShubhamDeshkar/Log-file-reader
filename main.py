import csv
import pickle
import datetime
import re


# Create a log_file object (CSV file object)
log_file_object = open('LogFileOut_2018.csv')

# Create a CSV reader
log_file_reader = csv.reader(log_file_object)

# Convert the data into a list
data_list = list(log_file_reader)
#print(data_list)

# Close the CSV file
log_file_object.close()

# Keeping the regular expression ready
regex = re.compile('\d{8}-\d{6}')

logFile = open('LogFileOut_2018.csv', 'w', newline='\n')
logWriter = csv.writer(logFile)

data_list[0].append('DataPaths')
logWriter.writerow(data_list[0])

# Use 2 for loops for obtaining the date and timestamps
for index in range(1, len(data_list) + 1):
      flight_stamp = data_list[index][-1]
      flight_timeObject = datetime.datetime.strptime(flight_stamp, '%Y-%m-%d %H:%M:%S')

      if index == len(data_list) - 1:
            break
      standby_stamp = data_list[index + 1][0]
      standby_timeObject = datetime.datetime.strptime(standby_stamp, '%Y-%m-%d %H:%M:%S')

      # Open the pickle file
      with open('DataFilePaths.pkl', 'rb') as dataPathFile:

            # Read the file
            data = pickle.load(dataPathFile)

            # Initialize an empty list
            list_to_append = []
            
            # For every line of datapath
            for i in range(0, len(data)):

                  # Load the dataPath in an object
                  dataPath = data[0][i]

                  # Check for specific keywords not in dataPath name
                  # Doubt about this line of code, Ask Austin
                  if 'pds' not in dataPath and 'zcal' not in dataPath and 'old' not in dataPath:
                        
                        # check for pattern match and extract the datetime
                        # object
                        result = regex.search(dataPath)
                        dateTime = result.group()

                        # Convert into datetime object
                        dateTimeObject = datetime.datetime.strptime(dateTime,'%Y%m%d-%H%M%S')

                        # Check if it is in the range of flight_stamp and
                        # standby_stamp. If yes, put it in the list
                        if(flight_timeObject <= dateTimeObject <= standby_timeObject):

                              # Append to the list
                              list_to_append.append(str(dataPath[30:]))

      # Append the new list to it
      data_list[index].append(list_to_append)
      print('appended: {}/{}'.format(str(index), len(data_list)-2))

      # Write to the file row by row      
      logWriter.writerow(data_list[index])


# Finally close the file
logFile.close()
