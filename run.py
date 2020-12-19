from emailer.emailer import Emailer
from settings import MESSAGE, SUBJECT, FROM_PWD, FROM_ADDRESS, TO_ADDRESS, SMTP_SERVER


if __name__ == "__main__":
    with Emailer(message=MESSAGE, subject=SUBJECT,
                 from_address=FROM_ADDRESS, pwd=FROM_PWD,
                 server=SMTP_SERVER, to_address=TO_ADDRESS) as casa:
        casa.send_email()
