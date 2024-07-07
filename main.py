import matplotlib.pyplot as plt
import numpy as np
import datetime
import os
import re



class Logger:
    def __init__(self, log_folder, create_thread=False):
        self.log_folder = log_folder
        self.create_thread = create_thread
        self.fh = None
        self.open_file()

    def time_in_microseconds(self):
        return int(datetime.datetime.now().timestamp() * 1000000)

    def open_file(self):
        if not os.path.exists(self.log_folder):
            os.makedirs(self.log_folder)
        now = datetime.datetime.now()
        filename = f"{self.log_folder}/{now.strftime('%m.%d.%Y')}.log"
        self.fh = open(filename, 'a')

    def write_header(self):
        now = datetime.datetime.now()
        self.fh.write(f"------------- {now.strftime('%H:%M:%S')} -------------\n")

    def write_line(self, prefix, filename, line, function, message):
        now = datetime.datetime.now()
        ms = self.time_in_microseconds() % 1000000 // 1000
        timestamp = now.strftime(f"%H:%M:%S.{ms:03d}")
        filename = os.path.basename(filename)
        log_message = f"[{prefix}] {timestamp}: {filename}({line}): {function} {message}\n"
        self.fh.write(log_message)

    def log_write(self, prefix, filename, line, function, message):
        self.write_line(prefix, filename, line, function, message)

    # Function to parse a single line of the log file and extract real and imaginary parts
    def parse_log_line(self, line):
        match = re.search(r"'Real': ([\d\.-]+), 'Imaginary': ([\d\.-]+)", line)
        if match:
            return float(match.group(1)), float(match.group(2))
        else:
            return None

    def calculate_phases(self, log_data):
        # Parse the log file and extract data
        real_parts = []
        imaginary_parts = []

        for line in log_data:
            result = self.parse_log_line(line)
            if result:
                real, imaginary = result
                real_parts.append(real)
                imaginary_parts.append(imaginary)

        # Convert lists to numpy arrays for easier manipulation
        real_parts = np.array(real_parts)
        imaginary_parts = np.array(imaginary_parts)

        # Calculate the phase
        return np.arctan2(imaginary_parts, real_parts)


def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    LOG_FOLDER = os.path.join(root_dir, 'LOGS')
    file_path = '~/LOGS/01.15.2024.log'

    # Create an instance of the Logger class
    logger = Logger(LOG_FOLDER)

    with open(file_path, 'r') as file:
        log_data = file.readlines()

    phases = logger.calculate_phases(log_data)

    # Create the plot
    fig, ax = plt.subplots()
    ax.plot(phases, label='Phase Data')
    ax.set_title('Phase Plot')
    ax.set_xlabel('Sample Number')
    ax.set_ylabel('Phase (radians)')
    ax.legend()

    # Show the plot
    plt.show()


if __name__ == "__main__":
    main()
