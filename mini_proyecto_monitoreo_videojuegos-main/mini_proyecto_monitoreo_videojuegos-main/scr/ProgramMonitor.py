import os
import psutil
import time
import datetime
from pymongo import MongoClient
from geopy.distance import geodesic
import smtplib
from email.mime.text import MIMEText
from geopy.geocoders import Nominatim
import requests


class LocationMonitor:
    def __init__(self, target_location):
        self.target_location = target_location

    def get_current_location(self):
        try:
            ip_info = requests.get("https://ipinfo.io").json()
            ip_address = ip_info.get("ip", "")

            geolocator = Nominatim(user_agent="location_monitor")
            location = geolocator.geocode(ip_address)

            if location:
                current_location = (location.latitude, location.longitude)
                return current_location
            else:
                print("No se pudo obtener la ubicación actual.")
                return None
        except Exception as e:
            print(f"Error obteniendo la ubicación actual: {e}")
            return None

    def is_outside_target_area(self):
        current_location = self.get_current_location()
        distance = geodesic(current_location, self.target_location).meters
        return distance > 100


class EmailNotifier:
    def __init__(self, sender_email, sender_password, receiver_email):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.receiver_email = receiver_email

    def send_email(self, subject, message):
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(self.sender_email, self.sender_password)

            msg = MIMEText(message)
            msg["Subject"] = subject
            msg["From"] = self.sender_email
            msg["To"] = self.receiver_email

            server.sendmail(self.sender_email, self.receiver_email, msg.as_string())
            server.quit()
        except Exception as e:
            print(f"Error sending email: {e}")


class ProgramMonitor:
    def __init__(self, target_location):
        self.PROGRAMS_TO_LOG = []
        self.PREVIOUS_STATE = set()
        self.LOG_FILE_PATH = os.path.abspath("program_log.txt")
        self.location_monitor = LocationMonitor(target_location)
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["program_monitor"]
        self.collection = self.db["program_logs"]
        self.email_notifier = EmailNotifier(sender_email="BryanDaviid333@gmail.com",
                                            sender_password="ffco lbue izbz ryeh",
                                            receiver_email="davidchalan54@gmail.com")

    def filter_inappropriate_programs(self, program_name):
        return program_name.lower() in [p.lower() for p in self.PROGRAMS_TO_LOG]

    def log_program_execution(self, program_name, username, action, cpu_percent, memory_percent):
        log_entry = {
            "timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "program_name": program_name,
            "username": username,
            "action": action,
            "cpu_percent": cpu_percent,
            "memory_percent": memory_percent
        }

        try:
            self.collection.insert_one(log_entry)
        except Exception as e:
            print(f"Error writing to MongoDB: {e}")
            

    def monitor_programs(self, batch_size=10):
        processes = psutil.process_iter(["name", "username", "cpu_percent", "memory_percent"])

        for _ in range(0, len(processes), batch_size):
            batch = processes[_:_ + batch_size]

            current_state = set()

            for process in batch:
                program_name = process.info.get("name", "")
                username = process.info.get("username", "")
                cpu_percent = process.info.get("cpu_percent", 0.0)
                memory_percent = process.info.get("memory_percent", 0.0)

                if self.filter_inappropriate_programs(program_name):
                    current_state.add(program_name.lower())

                    if program_name.lower() not in self.PREVIOUS_STATE:
                        self.log_program_execution(program_name, username, "started", cpu_percent, memory_percent)
                    else:
                        self.log_program_execution(program_name, username, "running", cpu_percent, memory_percent)

            self.PREVIOUS_STATE = current_state

            if self.location_monitor.is_outside_target_area():
                subject = "¡Alerta! Saliste del área designada"
                message = "Se detectó que has salido del área designada. Por favor, verifica tu ubicación."
                self.email_notifier.send_email(subject, message)

            time.sleep(10)

    def start_monitoring(self):
        try:
            while True:
                self.monitor_programs()
        except KeyboardInterrupt:
            print("Monitoring stopped.")
            self.client.close()  # Cierra la conexión al finalizar

if __name__ == "__main__":
    # Definir la ubicación objetivo
    target_location = (-0.2299, -78.5249)  # Sustituir con las coordenadas Quito-Ecuador
    monitor = ProgramMonitor(target_location)
    monitor.start_monitoring()
