import os
import csv
from datetime import datetime
import tkinter as tk

# Task A: Input Validation

def validate_date_input(prompt,valid_range):
    while True:
        try:
            User_input = int(input(prompt))
          
            if User_input in valid_range:  
                return User_input
            else:
                print(f"out of range-values must be in the range {valid_range.start} to {valid_range.stop -1}")#To find the correct range for days, month and years
        except ValueError:
            print("integer required")
            
date_range = range(1,32)
month_range = range(1,13)
year_range = range(2000,2025)

def get_survey_date():
    while True:
        try:
            day = validate_date_input("please enter the day of the survey in the format DD:",date_range)
            month = validate_date_input("please enter the month of the survey in the format MM:",month_range)
            year = validate_date_input("please enter the year of the survey in the format YYYY:",year_range)
            survey_date = datetime(year, month, day)
            break
        except ValueError:
            print(f"invalid date:day is out of range of month")#Identify the leap years and correct days for the each month
    return day, month, year





#Task B : Processed Outcomes



def validate_csv_data(day, month, year):
    try:
        survey_date = datetime(year, month, day)
        date_str = survey_date.strftime('%d%m%Y')  #Convert survey date into a string in the DDMMYYYY format
        filename = f'traffic_data{date_str}.csv'
        with open (filename, newline='') as csvfile:
            data = list(csv.reader(csvfile))
            print(f'Data file:{filename} There ia a available file for these data.')
            return data, filename
    except FileNotFoundError:
        print(f'There is not a file related to this date {day:02d}-{month:02d}-{year}. Please try again.')
        return None, filename
    
# function to calculate vehicle data and traffic details
def vehicle_data(data):
    
    total_vehicles = 0
    total_trucks = 0
    total_electric_vehicles = 0
    total_bicycles = 0
    total_two_wheeled_vehicles = 0
    total_buses_leaving_north = 0
    total_vehicles_without_turning = 0
    total_vehicles_over_speed_limit = 0
    total_vehicles_elmavenue_rabbitroad = 0
    total_vehicles_hanley_highway_westway = 0
    total_scooters_at_elmavenue_rabbitroad = 0
    vehicles_per_hour_hanley = {} # Dictionary to store vehicle counts per hour for Hanley Highway/westway
    rain_hours = set() #Set to store unique rain hours
    #initialze a dictionary to store traffic data for each junction
    traffic_data = {"Elm Avenue/Rabbit Road": {}, "Hanley Highway/Westway": {}}
    

    
# Assign values from each row of data
    for row in data[1:]:
        (JunctionName, Date, timeofDay,Travel_Direction_in, Travel_Direction_out, Weather_Conditions,
         junction_speed_limit, vehicle_speed, vehicle_Type, Electric_hybrid, *rest) = row
        
        #Count the all vehicles
        total_vehicles += 1
        
        #Update vehicle counts based on each conditions
        if vehicle_Type == "Truck":
            total_trucks += 1
            
        if Electric_hybrid == "True":
             total_electric_vehicles += 1
             
        if vehicle_Type in ['Bicycle', 'Motorcycle', 'Scooter']:
             total_two_wheeled_vehicles += 1
             
        if JunctionName == "Elm Avenue/Rabbit Road" and Travel_Direction_out == "N" and vehicle_Type == "Buss":
             total_buses_leaving_north += 1
             
        if Travel_Direction_in == Travel_Direction_out:
            total_vehicles_without_turning += 1
            
        if int(vehicle_speed) > int(junction_speed_limit):
             total_vehicles_over_speed_limit += 1
             
        if vehicle_Type == "Bicycle":
            total_bicycles += 1
            
        if JunctionName == "Elm Avenue/Rabbit Road":
            total_vehicles_elmavenue_rabbitroad += 1
            if  vehicle_Type == "Scooter":
                 total_scooters_at_elmavenue_rabbitroad += 1
                
        if JunctionName == "Hanley Highway/Westway":
            total_vehicles_hanley_highway_westway += 1

            time_hour = datetime.strptime(timeofDay, '%H:%M:%S').hour #If timeofDay 14:30:15, then time_hour will be 14 
            if time_hour not in vehicles_per_hour_hanley:
                vehicles_per_hour_hanley[time_hour] = 0
            vehicles_per_hour_hanley[time_hour] += 1 #count the highest number of vehicle in an hour on Hanley Highway/Westway
            

        if "Rain" in Weather_Conditions:
            rain_time = datetime.strptime(timeofDay, '%H:%M:%S') #Convert the time string to a datetime object
            rain_hours.add(rain_time.hour)
            
    total_rain_hours = len(rain_hours)

# Checking the peak hour for Hanley Highway/Westway

    if vehicles_per_hour_hanley:
        peak_hour_on_hanley_highway_westway = max(vehicles_per_hour_hanley, key = vehicles_per_hour_hanley.get)
        highest_vehicle_count = vehicles_per_hour_hanley[peak_hour_on_hanley_highway_westway]

    else:
        peak_hour_msg = 'No vehicle data available for Hanley Highway/Westway.'
        highest_vehicle_count_msg = ''

            
    # Add the summary of vehicle counts for the result list
    
    result =[]
    
    result.append(f'Total number of vehicles recorded for this date is: {total_vehicles}')
    
    result.append(f'Total number of trucks recorded for this date is: {total_trucks}')
    
    result.append(f'Total number of electric vehicles for this date is: {total_electric_vehicles}')
    
    result.append(f'Total number of two-wheeled vehicles for this date is: {total_two_wheeled_vehicles}')
    
    result.append(f'Total number of buses leaving Elm Avenue/Rabbit Road heading North is: {total_buses_leaving_north}')
    
    result.append(f'Total number of through both junctions not turning left or right is: {total_vehicles_without_turning}')
    
    result.append(f'Percentage of total vehicles recorded that are trucks for this date is: {round((total_trucks / total_vehicles) * 100)}%')
    
    result.append(f'Total number of vehicles recorded as over the speed limit for this date is: {total_vehicles_over_speed_limit}')
    
    result.append(f'Total number of vehicles recorded through Elm Avenue/Rabbit Road junction is: {total_vehicles_elmavenue_rabbitroad}')
    
    result.append(f'Total number of vehicles recorded through Hanley Highway/Westway junction is: {total_vehicles_hanley_highway_westway}')
    
    result.append(f'Percentage of scooters at Elm Avenue/Rabbit Road: {int(total_scooters_at_elmavenue_rabbitroad / total_vehicles_elmavenue_rabbitroad * 100)}%')
    
    result.append(f'Average number of bikes per hour for this date is: {round(total_bicycles / 24)}')
    
    result.append(f'Number of hours of rain for this date is: {total_rain_hours}')
    
    result.append(f'The highest number of vehicle in an hour on Hanley Highway/Westway is:{ highest_vehicle_count}')
    
    result.append(f'The most vehicles through Hanley Highway/Westway were recorded between {peak_hour_on_hanley_highway_westway}:00 and'f' {(peak_hour_on_hanley_highway_westway + 1)}:00.')


    return result

#Function to display

def display_outcomes(results, filename):
    print(f'\nResults for file: {filename}')

    for outcome in results:
        print(outcome)

    
    
   
   
#Task C: Save Results to Text File

#Function to save the results into a text file
def save_results_to_file(results, filename):
    with open("results.txt","a") as file:
        # write the all results in result.txt file
        file.write(f"\nResults for file: {filename}\n")
        
        for line in results:
            file.write(line + "\n")
        file.write("*********************************\n")
        print(f"Results have been saved to results.txtfor the file: {filename}")
        
#Task D: Histogram Display

class HistogramApp:
    def __init__(self,traffic_data,date):
        
        self.traffic_data = traffic_data
        self.date = date
        self.root = tk.Tk()
        
        

    def setup_window(self):
        self.root.title(f'Histogram of Vehicle Frequency Per Hour - {self.date} ')
        self.canvas = tk.Canvas(self.root,width =1200, height=600,bg='white')# create a canva with fixed size
        self.canvas.pack()
        
    def draw_histogram(self):

        
        margin = 70
        canvas_width = 1200
        canvas_height = 600
        max_bar_height = 450
        hour_gap = 10
        total_hours = 24
        junctions = ["Elm Avenue/Rabbit Road","Hanley Highway/Westway"]
        
        max_count = max(max(self.traffic_data.get(junction_name,{}).values(),default = 0) for junction_name in junctions)
        group_width = (1000 - total_hours * hour_gap)/ total_hours
        bar_width = group_width/ len(junctions)

        for hour in range(total_hours):
            hour_start_x = margin + hour * (group_width + hour_gap)
            for junction_index, junction in enumerate(junctions):
                if hour in self.traffic_data[junction]:
                    count = self.traffic_data[junction].get(hour,0)
                    x0 = hour_start_x + junction_index * bar_width
                    y0 = canvas_height - margin
                    x1 = x0 + bar_width
                    y1 = y0 - (count/max_count) * max_bar_height
                    color = 'orange' if junction == "Elm Avenue/Rabbit Road" else "aqua"
                    self.canvas.create_rectangle(x0,y0,x1,y1, fill = color)

                    self.canvas.create_text((x0 +x1)/2 , y1 - 10 ,text = str(count), fill = 'black' ,font = ('Arial',10))

            if any(hour in self.traffic_data[junction] for junction in junctions):
                self.canvas.create_text((hour_start_x + (group_width/2)),canvas_height - margin + 20, text = str(hour), fill = 'black' , font = ('Arial',10))
                    

    def add_legend(self):
        self.canvas.create_text(600, 20, text = f'Histogram of Vehicle Frequency Per Hour - {self.date}',font = ('Arial',12,'bold'))
        self.canvas.create_text(600,580, text = "Hours 00:00 to 24:00", font = ('Arial',12,'bold'))
        self.canvas.create_text(30, 300, text="vehicle count",font=('Arial', 12,'bold'),angle = 90)

        self.canvas.create_rectangle(50, 40, 70, 60, fill = 'orange')
        self.canvas.create_text(90,50, text="Elm Avenue/Rabbit Road", anchor = tk.W, font=('Arial',10,'bold'))
        self.canvas.create_rectangle(50, 70, 70, 90, fill = 'aqua')
        self.canvas.create_text(90,80, text="Hanley Highway/Westway", anchor = tk.W, font=('Arial',10,'bold'))

    def run(self):
        self.setup_window()
        self.draw_histogram()
        self.add_legend()
        self.root.mainloop()


#Task E: Code loops to handle multiple csv files
        
class MultiCSVProcessor:
    def __init__(self):
        
        self.current_data = None

    def load_csv_file(self, filename):
        #load the csv file and handle errors if file is not available
        try:
            with open(filename, newline='') as csvfile:
                self.current_data = list(csv.reader(csvfile))
                print(f"Data from {filename} has been loaded successfully.")
        except FileNotFoundError:
            print(f"File {filename} not found. Please try again.")
            self.current_data = None

    def clear_previous_data(self):
        # clear the previous data from result.txt
        self.current_data = None
        if 'results.txt' in os.listdir():
            with open('results.txt', 'w') as f:
                f.write("") # Clear the results file
        

    def handle_user_interaction(self):
        # asked user choice to contnue program or end the program
        while True:
            user_choice = input("Do you want to load a new dataset? (Y is yes /N is no): ").strip().upper()
            if user_choice == "Y":
                
                return True
            elif user_choice == "N":
                print("End of the program")
                
                return False
            else:
                print("Invalid input. Please enter 'Y' or 'N'.")
   

        
        
           

    def process_files(self):
        counter = 0 # to stop print this statement when program run first time "previous data has been cleared" 
        while True:
            self.clear_previous_data ()
            if counter >= 1:
                print("previous data has been cleared")
            self.clear_previous_data()
            day, month, year = get_survey_date()
            date_str = f"{day:02d}{month:02d}{year}"
            filename = f"traffic_data{date_str}.csv"

            self.load_csv_file(filename)
            if self.current_data:
                results = vehicle_data(self.current_data)
                display_outcomes(results, filename)
                save_results_to_file(results, filename)

                traffic_data = {"Elm Avenue/Rabbit Road": {},"Hanley Highway/Westway": {}}
                for row in self.current_data[1:]:
                    JunctionName, _, timeofDay, *_ = row
                    hour = datetime.strptime(timeofDay, '%H:%M:%S').hour
                    if JunctionName in traffic_data:
                        if hour not in traffic_data[JunctionName]:
                            traffic_data[JunctionName][hour] = 0
                        traffic_data[JunctionName][hour] += 1

                app = HistogramApp(traffic_data, f"{day:02d}-{month:02d}-{year}")
                app.run()
                
                counter += 1

            if not self.handle_user_interaction():
                break
            


# Instantiate and run the MultiCSVProcessor
processor = MultiCSVProcessor()
processor.process_files()


        


            
            
    
   

                    
  


            
            




      
        
      
      
        
    
