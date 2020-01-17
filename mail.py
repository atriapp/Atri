import smtplib

from string import Template
#from django.http import HttpResponse,JsonResponse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


MY_ADDRESS = 'user.support@davidpoc.co.in'#'info@davidpoc.co.in'#'tcsdatatool@gmail.com'
PASSWORD = 'Python@123'

def get_contacts(filename):
    """
    Return two lists names, emails containing names and email addresses
    read from a file specified by filename.
    """
    print("changed")
    names = []
    emails = []
   # with open(filename, mode='r', encoding='utf-8') as contacts_file:
        #for a_contact in contacts_file:
         #   names.append(a_contact.split()[0])
          #  emails.append(a_contact.split()[1])
    names = ["Netflix User"]
    emails = ["anjirwt8755@gmail.com"]
    return names, emails

def read_template(filename):
    """
    Returns a Template object comprising the contents of the
    file specified by filename.
    """

    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

def mailer(emails,body_temp,sub_temp):#emails,body_temp,sub_temp)
    print('@@@@@@@@@@@@@@@@inside main of mailer')
    #names, emails = get_contacts('mycontacts.txt') # read contacts
    #emails=email
    #names=username

    #emails = ["anjali.rawat1@tcs.com,anjirwt8755@gmail.com"]
    #sub_temp = "Ohayō gozaimasu"
    #body_temp = ["<p><span stlye = 'color:green; '>Ohayō gozaimasu Anjali </span><br><p>Hello and wish you a fresh and fruitful morning . I am now integrated with my own domain E-mail ! Ain't that Great ? </p><br><p><strong>DAVID</strong></p>"]
    # set up the SMTP server
    print(emails)
    print(body_temp)
    print(sub_temp)
    s = smtplib.SMTP(host='smtpout.secureserver.net', port=80)
    s.starttls()
    print(MY_ADDRESS)
    s.login(MY_ADDRESS, PASSWORD)
    print("########################email array is :#####################")
    print(emails)
    print("@@@@@@@@@@@@@@@@@@@@@@@@@appended email : ")
    #emails.append('pillaisunils@gmail.com')#pillai.sunil@tcs.com
    print(type(emails))
    # For each contact, send the email:
    for body, email in zip(body_temp, emails):
        msg = MIMEMultipart()       # create a mes
        #print(body)
        #print(email)
        msg = MIMEMultipart()       # create a message

        # add in the actual person name to the message template
        message = body #.substitute(PERSON_NAME=name.title())
        message+="<p style='font-weight':'bolder'>I'm excited to help you to better analyse and vizualize your data.<br>Explore more.<br>1. Use your own dashboard<br>2.	Use your document parser<br>I am continously working on making your experience enjoyable.<br>Give me a Pat, Oh I meant a good feedback if you like me and if you want to help me improve do share your suggestions. I am eagerly waiting.<br><>At your service.<br>DAVID Visit me at : <a href='www.davidpoc.co.in/login'>DAVID - Data Analysis Tool  </a></p>"
        # Prints out the message body for our sake
        #print(message)

        # setup the parameters of the message
        msg['From']=MY_ADDRESS
        print('#######sending email to: ',email)
        msg['To']=email
        msg['Cc'] ="pillai.sunil@tcs.com"# "anjirwt8755@gmail.com"
        msg['Subject']=sub_temp

        # add in the message body
        msg.attach(MIMEText(message, 'html'))
        print("#######################the message is #############################")
        #print(msg)
        # send the message via the server set up earlier.
        print('#########msg sent')
        #s.send_message(msg)
        #msg['To']="pillai.sunil@tcs.com"
        s.send_message(msg)
        print("############################sending message to : ",msg['Cc'])


        del msg

    # Terminate the SMTP session and close the connection

    s.quit()

    return True
if __name__ == '__main__':
    mailer()
