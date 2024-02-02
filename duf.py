import datetime, os
import pytz  # Import the pytz library

class UptimeTracker:
    def __init__(self):
        self.log_file = "uptime.txt"
        self.__uptime = self.get_last_uptime()
        self.__current_time = datetime.datetime.now(pytz.timezone('US/Pacific'))  # Specify the timezone here
    
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

    def get_uptime(self):
        return self.__uptime

    def get_current_time(self):
        return self.__current_time

    def calculate_downtime(self):
        if self.__uptime is not None:
            downtime = self.__current_time - self.__uptime
            return downtime

        return None

    def write_to_log(self):
        downtime = self.calculate_downtime()
        
        # Read existing lines to calculate the maximum line length
        existing_lines = []
        try:
            with open(self.log_file, "r") as file:
                existing_lines = file.readlines()
        except FileNotFoundError:
            pass

        max_line_length = max(len(line) for line in existing_lines) if existing_lines else 0

        # Create new lines with aligned "|"
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

                line = f" DIFFERENCE :: {downtime_str} |"
                file.write(line + "\n")
                
                # Append the current uptime line
                line = f"| ACTIVE :: {self.__current_time.strftime('%d-%m-%Y %I:%M:%S %p %Z')} |"
                file.write(line)
            else:
                # If there's no previous uptime, just write the current uptime line
                line = f"| ACTIVE :: {self.__current_time.strftime('%d-%m-%Y %I:%M:%S %p %Z')} |"
                file.write(line)

if __name__ == "__main__":
    tracker = UptimeTracker()
    tracker.write_to_log()

    # Git Commit and Push
    os.system("git add .")
    os.system("git commit -m 'Updated_Uptime'")
    os.system("git push origin main")
