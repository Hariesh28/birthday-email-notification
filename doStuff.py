import datetime
import json
import smtplib
import os
import email
import imaplib
import threading
import schedule
import time
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

class BirthDay:

    @staticmethod
    def get_student_info(dataframe: pd.DataFrame) -> list[dict] | None:

        try:
            result = []

            for student in list(dataframe[['dob', 'name', 'section', 'student_id']].values): #df.values: <class 'numpy.ndarray'>

                dob, name, section, student_id = list(student) # student: <class 'numpy.ndarray'>

                course = 'AIDS' if student_id.startswith('BA') else 'IOT'

                # create a datetime object
                birthday = datetime.datetime.strptime(dob, '%d-%m-%Y')
                birthyear = birthday.year
                birthday = birthday.replace(year=datetime.datetime.now().year)

                today = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                # today = today.replace(day=28, month=6) # if we want to change today's date

                if today == birthday:
                    result.append({'name' : name.title(), 'birth_year' : birthyear, 'section': section, 'course': course})


            if result == []: return None
            return result

        except Exception:
            return None


class mail:

    @staticmethod
    def load_constants():
        with open('constants.json') as file:
            return json.load(file)

    @staticmethod
    def get_message(data: list[dict] | None) -> str:

        if not data:
            message = '''Hi,
Just a quick note to let you know that there are no birthdays to celebrate today.

Best regards,
Myself'''

            return message

        constant_data = mail.load_constants()

        message = f'''Date: {datetime.datetime.now().date().strftime('%d-%m-%Y')}
Day: {constant_data["days"][datetime.datetime.now().weekday()]}

Dear Myself,
I hope this message finds you well. Today, we have some special occasions to celebrate as it's the birthday of the following colleagues:


Birthday List:

'''

        for index, student in enumerate(data):
            message += f"{index+1}. {student['name']} ({student['birth_year']}) -> {student['course']} - {student['section']}\n"

        message += '\n\nBest Regards, Myself 💀'

        return message

    @staticmethod
    def send_mail(data:list[dict] | None, receivers_address:list[str]) -> bool:

        constant_data = mail.load_constants()

        try:
            # Create Message
            message = MIMEMultipart()
            message['Subject'] = f"Birthday Celebrations - {datetime.datetime.now().date().strftime('%d-%m-%Y')}"
            message['From'] = constant_data['sender_mail_id']
            message['To'] = ', '.join(receivers_address)

            # Add body
            message.attach(payload=MIMEText(mail.get_message(data=data)))

            image_path = 'hawk_tuah_girl.png'

            # Add image
            with open(image_path, 'rb') as file:

                image = MIMEApplication(file.read(), name = os.path.basename(image_path))
                image['Content-Disposition'] = f'attachment; filename="{os.path.basename(image_path)}"'

                message.attach(payload=image)

            # Send mail
            with smtplib.SMTP('smtp.gmail.com', 587) as server:

                server.starttls()
                server.login(user=constant_data['sender_mail_id'], password=os.environ.get('SPAM_G_ACC_APP_PASSWORD'))

                server.sendmail(from_addr=constant_data['sender_mail_id'], to_addrs=receivers_address, msg=message.as_string())

        except Exception as e:
            return False

        else:
            return True


class readEmail:

    @staticmethod
    def get_constant_data():

        with open('constants.json') as file:
            return json.load(file)

    @staticmethod
    def sign_in():

        constant_data = readEmail.get_constant_data()

        mail_con.login(constant_data['sender_mail_id'], os.environ.get('SPAM_G_ACC_APP_PASSWORD'))
        mail_con.select("INBOX")


    @staticmethod
    def sign_out():
        mail_con.close()
        mail_con.logout()

    @staticmethod
    def get_no_of_emails() -> int:

        mail_con.noop() # Refresh the connection

        _, no_of_msg = mail_con.search(None, 'ALL')
        no_of_messages = int(no_of_msg[0].split()[-1])

        return no_of_messages

    @staticmethod
    def check_for_new_email():

        print("Checking...")

        global total
        result = []

        new_total = readEmail.get_no_of_emails()

        if new_total > total:

            print("Found new messages")

            for i in range(total+1, new_total+1):

                print(f'Checking message: {i}')

                _, msg = mail_con.fetch(str(i), '(RFC822)')

                try:
                    message = email.message_from_bytes(msg[0][1])

                except Exception:

                    # here we get some kind of seen message thingy and the format is changed, so we change accordingly
                    # still if we get multiple message, i think we should probably check [2][1], [3][1] and so on...
                    # we can solve this by checking until msg[smth][1] is out of range, but i'm too lazy
                    # here i am hoping not more than three/four (idk) ppl will message at the same time in one check, works in most cases ;)
                    # very bad code here

                    try:
                        message = email.message_from_bytes(msg[1][1])

                    except Exception:

                        try:
                            message = email.message_from_bytes(msg[2][1])

                        except Exception:
                            message = email.message_from_bytes(msg[3][1])


                for part in message.walk():

                    if part.get_content_type() == 'text/plain':
                        message_content = part.get_payload(decode=True).decode()

                        if message_content.strip().lower() == 'birthday list':

                            print(f"Requested for birthday list: {message['From']}")
                            result.append(message['From'].split('"')[-1].strip()[1:-1])

                        elif message_content.strip().lower() == 'stop' and message['From'] == '"Hariesh .R" <hariesh28606@gmail.com>':
                            global stop
                            stop = True

                        else:
                            print(f"Random message by: {message['From']}")
                            print(f"Contains: {message_content}")

            print(f'Sending to: {result}')

            if result != []:

                df = pd.read_csv('data.txt', sep=', ', engine='python')
                students = BirthDay.get_student_info(dataframe=df)
                status = mail.send_mail(data=students, receivers_address=result)

                if status: print(f"Sent to: {result}")
                else: print(f"Error Sending to: {result}")

        total = new_total

# IMAP Connection
mail_con = imaplib.IMAP4_SSL('imap.gmail.com')
readEmail.sign_in()
total = readEmail.get_no_of_emails()
stop = False

class master:

    @staticmethod
    def start_thread(func):
        job = threading.Thread(target=func)
        job.start()

    @staticmethod
    def start_program():

        df = pd.read_csv('data.txt', sep=', ', engine='python')
        student_data = BirthDay.get_student_info(dataframe=df)
        constant_data = mail.load_constants()

        schedule.every(7).seconds.do(master.start_thread, readEmail.check_for_new_email)
        schedule.run_all() # if we want to run all the functions immediately

        schedule.every().day.at('15:32:30').do(mail.send_mail, student_data, constant_data['receiver_mail_ids'])

        while True:
            schedule.run_pending()
            time.sleep(1)

            if stop:
                readEmail.sign_out()
                print("EXITING !")
                break