import pandas as pd
import datetime as dt
import smtplib
import random
import os

my_email = ""
pass_word = os.environ['KEY']

today = (int(dt.datetime.now().strftime("%d")), int(dt.datetime.now().strftime("%m")))
today_date_string = dt.datetime.now().strftime("%d/%m/%Y")

data_list = pd.read_csv("LIST/Birthday_list.csv")
data = list(data_list.to_dict(orient="records"))

mail_list = []

# Creating Mailing List for a Day
for individual_data in data:
    date = individual_data["BIRTHDAY"]
    date_tuple = (int(date.split("/")[0]), int(date.split("/")[1]))
    if date_tuple == today:
        mail_list.append(individual_data)
    else:
        continue


# Mailing to recipients
for each in mail_list:
    message_text = ""
    if each["RELATION"] == "FRIEND":
        message_file = f"MESSAGES/FRIEND/{random.randint(1, 10)}.txt"
    elif each["RELATION"] == "TEACHER":
        message_file = f"MESSAGES/TEACHER/{random.randint(1, 10)}.txt"

    with open(message_file) as file:
        message_text = file.read()
        message_text = message_text.replace("[name]", each["FIRST NAME"].split()[0].lower().title())

    with smtplib.SMTP('smtp.gmail.com:587') as connection:
        connection.starttls()
        connection.login(user=my_email, password=pass_word)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=each["EMAIL"],
            msg=f"Subject:HAPPY BIRTHDAY ! \n\n{message_text}".encode("utf-8")
        )


# Information to yourselves mail
if len(mail_list) != 0:
    information = ""
    for each in mail_list:
        information += f'{each["NAME"]}, {each["EMAIL"]}, {each["BIRTHDAY"]}, {each["CONNECTION"]}, {each["RELATION"]} \n\n'
    with smtplib.SMTP('smtp.gmail.com:587') as connection:
        connection.starttls()
        connection.login(user=my_email, password=pass_word)
        connection.sendmail(
            from_addr=my_email,
            to_addrs="myemail@gmail.com",
            msg=f"Subject:TODAY'S BIRTHDAYS {today_date_string} \n\n{information}".encode("utf-8")
        )
