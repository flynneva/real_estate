#/usr/bin/env python3
import sys
import csv
import pandas as pd
import matplotlib.pyplot as plt

from pick import pick

def totalRows(filename):
    with open(filename) as f:
      return sum(1 for line in f)

def export_county(datafile, county_fid):
  # TODO: add logic to add csv only if its missing
  log_file = datafile + '.csv'
  last_row = totalRows(log_file) - 1

  with open(log_file, newline='') as csvfile:
    print("Opened " + log_file)
    reader = csv.reader(csvfile, delimiter=',')
    county_fname = str(county_fid) + '.csv'
    with open(county_fname, 'w', newline='') as csvCounty:
      writer = csv.writer(csvCounty, delimiter=',')
      index = 0
      row_counter = last_row
      first_row = ''
      county = ''
      for row in reader:
        if (index == 0):
          first_row = row
          first_row[0] = 'date'
          writer.writerow(first_row)
          break
      index = 0 
      for row in reversed(list(reader)):
        if (row_counter == 0):
          break
        if (row[1] == str(county_fid)):
          county = row[2]
          year = row[0][:4]
          month = row[0][-2:]
          row[0] = year + '-' + month
          writer.writerow(row)
          index += 1
        row_counter -= 1

      if (index == 0):
        print("No data found for given County FID")
        print("Double check that " + county_fid + " is a valid County FID")
      else:
        print("Wrote " + str(index) + " rows of data for " + county_fid + " " + county)

def generate_graphs(datafile):

  x = []
  y = []

  # TODO: add logic to add csv only if its missing
  log_file = datafile + '.csv'
  data = pd.read_csv(log_file)
  print("Opened " + log_file)
  # create plot
  fig, ax = plt.subplots(2, 2, figsize=(16, 10))

  # set values
  ax[0,0].plot(data['date'], data['active_listing_count']) 
  ax[0,0].set_title('Active Listing Count Over Time')
  ax[0,0].set_ylabel('Active Listing Count')
  ax[0,0].set_xlabel('Month')
  ax[0,0].tick_params(axis='x', labelrotation=70)
  ax[0,1].plot(data['date'], data['median_listing_price']) 
  ax[0,1].set_title('Median Listing Price Over Time')
  ax[0,1].set_ylabel('Median Listing Price [USD]')
  ax[0,1].set_xlabel('Month')
  ax[0,1].tick_params(axis='x', labelrotation=70)
  ax[1,0].plot(data['date'], data['price_reduced_count']) 
  ax[1,0].set_title('Count of Listings that Reduced their Price')
  ax[1,0].set_ylabel('Reduced Price Count')
  ax[1,0].set_xlabel('Month')
  ax[1,0].tick_params(axis='x', labelrotation=70)
  ax[1,1].plot(data['date'], data['median_days_on_market']) 
  ax[1,1].set_title('Median Days on Market')
  ax[1,1].set_ylabel('Number of Days')
  ax[1,1].set_xlabel('Month')
  ax[1,1].tick_params(axis='x', labelrotation=70)
  # draw plot
  fig.tight_layout(pad=2.0)
  plt.show() 

def generate_and_graph(datafile, county_fid):
  export_county(datafile, county_fid)
  generate_graphs(county_fid)

def main():
  if len(sys.argv) < 1:
    exit(1)
  #file_name = sys.argv[1]
  #county_fid_input = sys.argv[2]

  splash_title = 'Please choose what you would like to do: '
  options = [ 'Export and Graph County Data',
              'Only Export County data to CSV',
              'Only Generate Graphs for County',
              'Exit' ]
  option, index = pick(options, splash_title)

  if (index == 3):
    print("Thanks for using this script!")
    print("Exiting script...")
    exit(1)
  elif (index == 0):
    file_name = input("Enter name of Realtor.com CSV file:  ")
    if (file_name == ''):
      print("No filename given....exiting script")
      exit(1)
    county_fid_input = input("Enter County FID to filter:  ")
    if (county_fid_input == ''):
      print("No County FID given....exiting script")
      exit(1)
    generate_and_graph(file_name, county_fid_input)
  elif (index == 2):
    print("Generating graphs...")
    file_name = input("Enter name of filtered CSV file:  ")
    if (file_name == ''):
      print("No filename given....exiting script")
      exit(1)
    generate_graphs(file_name)
  elif (index == 1):
    file_name = input("Enter name of Realtor.com CSV file:  ")
    if (file_name == ''):
      print("No filename given....exiting script")
      exit(1)
    county_fid_input = input("Enter County FID to filter:  ")
    if (county_fid_input == ''):
      print("No County FID given....exiting script")
      exit(1)
    export_county(file_name, county_fid_input)

if __name__ == "__main__":
  main()
