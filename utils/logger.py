import csv
import os
from datetime import datetime


class AuraLogger:
    def __init__(self, file_path="logs/aura_logs.csv"):
        self.file_path = file_path

        # Create folder if not exists
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

        # Create file with header if not exists
        if not os.path.exists(self.file_path):
            with open(self.file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["timestamp", "label", "confidence", "vad"])

    def log(self, label, confidence, vad):
        timestamp = datetime.now().strftime("%H:%M:%S")

        with open(self.file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, label, round(confidence, 2), vad])