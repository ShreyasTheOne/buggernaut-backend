import email, smtplib, ssl
from  email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Mailer:

    def __init__(self):
        self.port = 587
        self.smtp_server = "smtp.gmail.com"
        self.password = "omniport123"
        self.sender_email = "buggernaut.testing@gmail.com"

    def sendMail(self, subject, from_user_name, to_user_name, receiver_email, text, html):
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = from_user_name
        message["To"] = to_user_name

        text_part = MIMEText(text, "plain")
        html_part = MIMEText(html, "html")

        message.attach(text_part)
        message.attach(html_part)

        context = ssl.create_default_context()
        with smtplib.SMTP(self.smtp_server, self.port) as server:
            server.starttls(context=context)
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, receiver_email, message.as_string())

    def newProjectUpdate(self, project_name, project_link, members=[]):
        for mem in members:
            name = mem.full_name
            email = mem.email

            text = f"""
                        Hi, {name}!

                        You have been added to the team of the project {project_name}!

                        Bon Testing!<br>
                        The Buggernaut Bot

                """

            html = f"""
                <html>
                    <head></head>
                    <body>
                            <h3>Hi, {name}!</h3>

                            <div>You have been added to the project <b>{project_name}</b>!<div>

                            <a href="{project_link}">Go to Project</a><br><br>
                            Bon Testing!<br>
                            The Buggernaut Bot
                    </body>
                </html>
            """

            # def sendMail(self, subject, from_user_name, to_user_name, receiver_email, text, html):
            self.sendMail("New Project Uploaded", "The Buggernaut Bot", name, email, text, html)



