from django.core.mail import send_mail, send_mass_mail

class Mailer:
    def __init__(self):
        pass


    def newProjectUpdate(self, project_name, project_link, team_members=[]):
        for mem in team_members:
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
                        <body style="max-width:350px;">
                                <h3>Hi, {name}!</h3>
                
                                <div>You have been added to the project <b>{project_name}</b>!<div>
                
                                <center>
                                    <div style="margin-top:30px; border-radius:5px; border-width:0px; text-align:center; background:#5390d9; width:50%; height:fit-content; padding:13px; display: table;">
                                        <center>
                                            <div style="display:table-cell; vertical-align:middle;"> 
                                                <a style="color:white; font-size:16px;" href="{project_link}">Go to Project</a>
                                            </div>
                                        </center>
                                    </div>
                                </center>
                                <br><br>
                                Bon Testing!<br>
                                The Buggernaut Bot
                        </body>
                    </html>
               """

            # def sendMail(self, subject, from_user_name, to_user_name, receiver_email, text, html):
            send_mail(subject="New Project Uploaded", message=text, from_email="The Buggernaut Bot", recipient_list= [email,], html_message=html)


    def newBugReported(self, project_name, project_link, reported_by, issue_subject, team_members=[]):
        for mem in team_members:
            name = mem.full_name
            email = mem.email

            text = f"""
                            Hi, {name}!

                            {reported_by} has reported an issue for the project {project_name}:

                            Issue:    
                            {issue_subject}

                            Bon Testing!<br>
                            The Buggernaut Bot

                   """

            html = f"""
                   <html>
                        <head></head>
                        <body style="max-width:350px;">
                                <h3>Hi, {name}!</h3>

                                <div>{reported_by} has reported an issue for the project <b>{project_name}</b>:<div>
                                <br>
                                <b>Issue:</b><br>
                                <b>{issue_subject}</b>
                                <br>
                                <center>
                                    <div style="margin-top:30px; border-radius:5px; border-width:0px; text-align:center; background:#5390d9; width:50%; height:fit-content; padding:13px; display: table;">
                                        <center>
                                            <div style="display:table-cell; vertical-align:middle;"> 
                                                <a style="color:white; font-size:16px;" href="{project_link}">Check it out!</a>
                                            </div>
                                        </center>
                                    </div>
                                </center>
                                <br>
                                Bon Testing!<br>
                                The Buggernaut Bot
                        </body>
                    </html>
               """

            # def sendMail(self, subject, from_user_name, to_user_name, receiver_email, text, html):
            send_mail(subject=f"New Bug Reported in {project_name}", message=text, from_email="The Buggernaut Bot", recipient_list=[email, ], html_message=html)

    def bugAssigned(self, project_name, assignment_link, issue_subject, assigned_to_name, assigned_to_email):

        text = f"""
                        Hi, {assigned_to_name}!

                        You have been assigned an issue for the project {project_name}.

                        Issue:
                        {issue_subject}

                        Bon Testing!<br>
                        The Buggernaut Bot

               """

        html = f"""
               <html>
                    <head></head>
                    <body style="max-width:350px;">
                            <h3>Hi, {assigned_to_name}!</h3>

                            <div>You have been assigned an issue for the project <b>{project_name}</b>.<div>
                            
                            <br>
                            <b>Issue:</b><br>
                            <b>{issue_subject}</b>
                            <br>

                            <center>
                                <div style="margin-top:30px; border-radius:5px; border-width:0px; text-align:center; background:#5390d9; width:50%; height:fit-content; padding:13px; display: table;">
                                    <center>
                                        <div style="display:table-cell; vertical-align:middle;"> 
                                            <a style="color:white; font-size:16px;" href="{assignment_link}">Check it out!</a>
                                        </div>
                                    </center>
                                </div>
                            </center>
                            <br><br>
                            Bon Testing!<br>
                            The Buggernaut Bot
                    </body>
                </html>
           """

        # def sendMail(self, subject, from_user_name, to_user_name, receiver_email, text, html):
        send_mail(subject=f"New assignment for {project_name}", message=text, from_email="The Buggernaut Bot",
                  recipient_list=[assigned_to_email, ], html_message=html)

    def bugResolved(self, project_name, project_link, resolved_by, issue_subject, team_members=[]):
        for mem in team_members:
            name = mem.full_name
            email = mem.email

            text = f"""
                            Hi, {name}!

                            {resolved_by} has resolved an issue for the project {project_name}:

                            Issue:    
                            {issue_subject}

                            Bon Testing!<br>
                            The Buggernaut Bot

                   """

            html = f"""
                   <html>
                        <head></head>
                        <body style="max-width:350px;">
                                <h3>Hi, {name}!</h3>

                                <div>{resolved_by} has resolved an issue for the project <b>{project_name}</b>:<div>
                                <br>
                                <b>Issue:</b><br>
                                <b>{issue_subject}</b>
                                <br>
                                <center>
                                    <div style="margin-top:30px; border-radius:5px; border-width:0px; text-align:center; background:#5390d9; width:50%; height:fit-content; padding:13px; display: table;">
                                        <center>
                                            <div style="display:table-cell; vertical-align:middle;"> 
                                                <a style="color:white; font-size:16px;" href="{project_link}">Go to Project</a>
                                            </div>
                                        </center>
                                    </div>
                                </center>
                                <br>
                                Bon Testing!<br>
                                The Buggernaut Bot
                        </body>
                    </html>
               """

            # def sendMail(self, subject, from_user_name, to_user_name, receiver_email, text, html):
            send_mail(subject=f"Bug Resolved in {project_name}!", message=text, from_email="The Buggernaut Bot",
                      recipient_list=[email, ], html_message=html)

    # get user name from request.user and send who reopened the issue
    def bugStatusChanged(self, project_name, project_link, issue_subject, action, doer, team_members=[]):
        for mem in team_members:
            name = mem.full_name
            email = mem.email

            text = f"""
                        Hi, {name}!

                        The following issue for the project {project_name} has been {action} by {doer}:

                        {issue_subject}

                        Bon Testing!<br>
                        The Buggernaut Bot

                       """

            html = f"""
                       <html>
                            <head></head>
                            <body style="max-width:350px;">
                                    <h3>Hi, {name}!</h3>

                                    <div>The following issue for the project <b>{project_name}</b> has been {action} by {doer}:<div>
                                    <br>
                                    
                                    <b>{issue_subject}</b>
                                    <br>
                                    <center>
                                        <div style="margin-top:30px; border-radius:5px; border-width:0px; text-align:center; background:#5390d9; width:50%; height:fit-content; padding:13px; display: table;">
                                            <center>
                                                <div style="display:table-cell; vertical-align:middle;"> 
                                                    <a style="color:white; font-size:16px;" href="{project_link}">Go to Project</a>
                                                </div>
                                            </center>
                                        </div>
                                    </center>
                                    <br>
                                    Bon Testing!<br>
                                    The Buggernaut Bot
                            </body>
                        </html>
                   """

            subject = ""
            if action == "reopened":
                subject = "Reopened"
            elif action == "resolved":
                subject = "Resolved"
            elif action == "deleted":
                subject = "Deleted"

            # def sendMail(self, subject, from_user_name, to_user_name, receiver_email, text, html):
            send_mail(subject=f"Bug {subject} in {project_name}!", message=text, from_email="The Buggernaut Bot",
                      recipient_list=[email, ], html_message=html)

    def statusUpdate(self, user_email, user_name, change, changer):
        if change == "promote":
            text = f"""
                        Hi, {user_name}!

                        You have been promoted to the role of <b>ADMIN</b> by {changer}!

                        Bon Testing!<br>
                        The Buggernaut Bot

                           """
            html = f"""
                       <html>
                            <head></head>
                            <body>
                                    <h3>Hi, {user_name}!</h3>

                                    <div>You have been promoted to the role of <b>ADMIN</b> by {changer}!<div>

                                    <br>
                                    Bon Testing!<br>
                                    The Buggernaut Bot
                            </body>
                        </html>
                       """
        elif change == "demote":
            text = f"""
                        Hi, {user_name}!

                        You have been demoted to the role of <b>USER</b> by {changer}.

                        Bon Testing!<br>
                        The Buggernaut Bot

                           """

            html = f"""
                       <html>
                            <head></head>
                            <body>
                                    <h3>Hi, {user_name}!</h3>

                                    <div>You have been demoted to the role of <b>USER</b> by {changer}.<div>

                                    <br>
                                    Bon Testing!<br>
                                    The Buggernaut Bot
                            </body>
                        </html>
                       """

        send_mail(subject=f"Buggernaut Role Update", message=text, from_email="The Buggernaut Bot",
                  recipient_list=[user_email, ], html_message=html)

    def banOrAdmitUser(self, user_email, user_name, change, changer):
        if change == "banned":
            text = f"""
                        Dear {user_name},

                        You have been banned from Buggernaut by {changer}.

                        The Buggernaut Bot

                           """
            html = f"""
                       <html>
                            <head></head>
                            <body>
                                    <h3>Dear {user_name},</h3>

                                    <div>You have been banned from Buggernaut by {changer}.<div>

                                    <br>
                                    The Buggernaut Bot
                            </body>
                        </html>
                       """
        elif change == "admit":
            text = f"""
                        Dear {user_name},

                        You have been readmitted Buggernaut by {changer}.

                        The Buggernaut Bot

                           """

            html = f"""
                       <html>
                            <head></head>
                            <body>
                                    <h3>Dear {user_name},</h3>

                                    <div>You have been readmitted Buggernaut by {changer}.<div>

                                    <br>
                                    The Buggernaut Bot
                            </body>
                        </html>
                       """
        subject = ""
        if change == "banned":
            subject = "BANNED!"
        elif change == "admit":
            subject = "Welcome Back!"

        send_mail(subject=subject, message=text, from_email="The Buggernaut Bot",
                  recipient_list=[user_email, ], html_message=html)