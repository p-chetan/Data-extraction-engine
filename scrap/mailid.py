from django.core.mail import EmailMessage
from django.conf import settings

def mail(email,fname):
        subject = fname
        message = ''
        email = email
        
        with open(fname, "rb") as csvfile:
            email1 = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [email])
            email1.attach(fname, csvfile.read(), 'text/csv')
            print("\nSending email..")
            email1.send()
            print("Email sent successfully! ")
            print(email)
        csvfile.close()

#        except Exception as e:
 #           print("Sorry mail was not sent.") 

id="chetan.gpel@gmail.com"
fname="pands.py"
mail(id,fname)