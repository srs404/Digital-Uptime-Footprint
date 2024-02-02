import datetime, os
import pytz

'''
# Title: Uptime Tracker (Class)
# ~ Description: This class is used to track the uptime of a system and write the uptime and downtime to a log file.

@Methods:
    - get_last_uptime
    - extract_datetime
    - calculate_downtime
    - write_to_log

@Example: tracker = UptimeTracker()
            tracker.write_to_log()

@Note: The log file should be in the format of a markdown file.
        The log file should contain the "ACTIVE" keyword to identify the uptime.
        The log file should contain the "DIFFERENCE" keyword to identify the downtime.
        The timezone is set to "US/Pacific" in this example.
        
        The log file last lines should be in the following format:
        | ACTIVE :: 01-01-2021 12:00:00 AM | DIFFERENCE :: 0 Days, 0 Hours, 0 Minutes, 0 Seconds | <br>
        | ACTIVE :: 01-01-2021 12:00:00 AM |
'''
class UptimeTracker:
    def __init__(self):
        self.log_file = "README.md" # Specify the log file here
        self.__uptime = self.get_last_uptime() # Get the last uptime from the log file
        self.__current_time = datetime.datetime.now(pytz.timezone('US/Pacific'))  # Specify the timezone here
    
    '''
    # Title: get_last_uptime
    # ~ Description: This function reads the log file and returns the last uptime.

    @Parameters: self (implicit)
    @Returns: The last uptime as a datetime object, or None if the uptime is not found.

    @Example: get_last_uptime() -> datetime.datetime(2021, 1, 1, 0, 0, tzinfo=<DstTzInfo 'US/Pacific' PST-1 day, 16:00:00 STD>)
    '''
    def get_last_uptime(self):
        try:
            with open(self.log_file, "r") as file:
                lines = file.readlines()
                for line in reversed(lines):
                    if "ACTIVE" in line:
                        uptime_str = line.strip()
                        return self.extract_datetime(uptime_str)
        except FileNotFoundError:
            return None
    
    '''
    # Title: extract_datetime
    # ~ Description: This function extracts the datetime from the input string.

    @Parameters: self (implicit), input_string (str)
    @Returns: The datetime as a datetime object, or None if the datetime is not found.

    @Example: extract_datetime("| ACTIVE :: 01-01-2021 12:00:00 AM |") -> datetime.datetime(2021, 1, 1, 0, 0, tzinfo=<DstTzInfo 'US/Pacific' PST-1 day, 16:00:00 STD>)

    @Note: The input string should be in the format "| ACTIVE :: 01-01-2021 12:00:00 AM |".
            The timezone is set to "US/Pacific" in this example.
            The input string should contain the "ACTIVE" keyword.
    '''
    def extract_datetime(self, input_string):
        try:
            # Remove the "PST" part from the input string
            input_string = input_string.replace("PST", "").strip()
            
            start_index = input_string.find("| ACTIVE :: ") + len("| ACTIVE :: ")
            end_index = input_string.find(" |", start_index)
            
            if start_index != -1 and end_index != -1:
                datetime_str = input_string[start_index:end_index].strip()
                # Convert the datetime string to a datetime object with timezone information
                return pytz.timezone('US/Pacific').localize(datetime.datetime.strptime(datetime_str, "%d-%m-%Y %I:%M:%S %p"))
            else:
                raise ValueError("Datetime format not found in the input string.")
        except ValueError as e:
            print(e)
            return None

    '''
    # Title: calculate_downtime
    # ~ Description: This function calculates the downtime by subtracting the current time from the uptime.

    @Parameters: self (implicit)
    @Returns: The downtime as a datetime object, or None if the uptime is not set.
    '''
    def calculate_downtime(self):
        if self.__uptime is not None:
            downtime = self.__current_time - self.__uptime
            return downtime

        return None

    '''
    # Title: write_to_log
    # ~ Description: This function writes the current uptime and downtime to the log file.

    @Parameters: self (implicit)
    @Returns: None
    '''
    def write_to_log(self):
        downtime = self.calculate_downtime()
        
        # Read existing lines to calculate the maximum line length
        existing_lines = []
        try:
            with open(self.log_file, "r") as file:
                existing_lines = file.readlines()
                if existing_lines:
                    existing_lines = [line.strip() for line in existing_lines]
        except FileNotFoundError:
            pass

        # Calculate the maximum line length
        max_line_length = max(len(line) for line in existing_lines) if existing_lines else 0

        # Write the uptime and downtime to the log file
        with open(self.log_file, "a") as file:
            if self.__uptime is not None:

                # Convert downtime to Format
                downtime = self.__current_time - self.__uptime
        
                days = downtime.days
                seconds = downtime.seconds
                hours, remainder = divmod(seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
        
                downtime_str = ""
                if days > 0:
                    downtime_str += f"{days} Days, "
                if hours > 0:
                    downtime_str += f"{hours} Hours, "
                if minutes > 0:
                    downtime_str += f"{minutes} Minutes, "
                if seconds > 0 or downtime_str == "":
                    downtime_str += f"{seconds} Seconds"
        
                downtime_str.strip()  # Remove trailing space

                line = f" DIFFERENCE :: {downtime_str} | <br>"
                file.write(line + "\n")
                
                # Append the current uptime line
                line = f"| ACTIVE :: {self.__current_time.strftime('%d-%m-%Y %I:%M:%S %p %Z')} |"
                file.write(line)
            else:
                # If there's no previous uptime, just write the current uptime line
                # Note: If you have previous markdown lines, you need to add dummy lines to the log file to maintain the 
                # markdown table format. For example, if the last line is "| ACTIVE :: 01-01-2021 12:00:00 AM |"
                line = f"| ACTIVE :: {self.__current_time.strftime('%d-%m-%Y %I:%M:%S %p %Z')} |"
                file.write(line)


'''-----------------------------------------------------------------------------------------------------------------
# Title: Main Driver Code
# ~ Description: This is the main driver code for the uptime tracker.
'''
if __name__ == "__main__":
    tracker = UptimeTracker()
    tracker.write_to_log()

    # Git Commit and Push
    os.system("git add *")
    os.system("git commit -m 'Updated_Uptime'")
    os.system("git push origin main")
