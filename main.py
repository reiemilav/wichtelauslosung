from random import shuffle
import smtplib
from email.mime.text import MIMEText
import json


class SecretSantaDraw:
    def __init__(self, config: str):
        with open(config, "r") as config_file:
            config_dict = json.load(config_file)

            self.app_pw = config_dict["app_pw"]
            self.subject = config_dict["subject"]
            self.body = config_dict["body"]
            self.sender = config_dict["sender"]

            self.participants:dict = config_dict["participants"]

            self.restricted_pairs:dict = config_dict["restricted_pairs"]


    def get_vars(self):
        print(f"app_pw = {self.app_pw}\nsubject = {self.subject}\nbody = {self.body}\nsender = {self.sender}")
        print("participants = ", end="")
        print(json.dumps(self.participants, indent=4))
        print("restricted_pairs = ", end="")
        print(json.dumps(self.restricted_pairs, indent=4))


    def send_email(self, message, receiver):
        msg = MIMEText(message)
        msg['Subject'] = self.subject
        msg['From'] = self.sender
        msg['To'] = receiver

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(self.sender, self.app_pw)
            smtp_server.sendmail(self.sender, [self.participants[receiver]], msg.as_string())

        print(f"Message sent to {self.participants[receiver]}!")
        print(f"{message}!\n")


    @staticmethod
    def is_valid_assignment(givers, receivers, restricted):
        """Checks that no giver is assigned to themselves and restricted pairs are avoided."""
        return all(
            giver != receiver and (giver, receiver) not in restricted
            for giver, receiver in zip(givers, receivers)
        )


    def run(self):
        wichtel = list(self.participants.keys())
        receivers = list(self.participants.keys())
        shuffle(receivers)

        while not self.is_valid_assignment(wichtel, receivers, self.restricted_pairs):
            shuffle(receivers)

        for giver, receiver in zip(wichtel, receivers):
            message = f"Hallo {receiver},\n{self.body}{giver}"
            self.send_email(message, receiver)

        

if __name__ == "__main__":
    wpl = SecretSantaDraw("config.json")
    wpl.run()