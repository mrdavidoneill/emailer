import smtplib
import imaplib
from email.mime.text import MIMEText


from .logger import logger


class Emailer:
    """ Utility emailer
        args: from_address, to_address, pwd, server, in_port=993, out_port=587, intervalMins=10
    """

    def __init__(self, message, subject, from_address, to_address, pwd, server, in_port=993, out_port=587):
        self.__message = message
        self.__subject = subject
        self.__from_address = from_address
        self.__to_address = to_address
        self.__pwd = pwd
        self.__server = server
        self.__in_port = in_port
        self.__out_port = out_port
        self.mailbox = None
        self.is_logged_in = self.login()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        logger.debug("Deleting sent messages...")
        self.delete_sent_emails()
        logger.debug("Expunging...")
        self.mailbox.expunge()
        logger.debug("Closing...")
        self.mailbox.close()
        logger.debug("Mailbox closed")
        self.mailbox.logout()
        logger.debug("Mailbox logged out")

    def login(self):
        """ Log in to server and select inbox.
            Return true if successful
            Else return false
        """
        try:
            logger.debug("Logging in...")
            self.mailbox = imaplib.IMAP4_SSL(self.__server)
            self.mailbox.login(self.__from_address, self.__pwd)
            self.mailbox.select('inbox')
            logger.debug("Logged in...")
            return True
        except Exception as e:
            logger.critical(str(e))
            return False

    def mark_delete_msg(self, msg_id):
        """ Marks single email message for deletion """
        self.mailbox.store(msg_id, "+FLAGS", "\\Deleted")

    def delete_sent_emails(self):
        """ Delete all emails from sent folder """
        self.mailbox.select('"[Gmail]/Sent Mail"')
        typ, data = self.mailbox.search(None, "ALL")
        mail_ids = data[0]
        id_list = mail_ids.split()
        for i in id_list:
            self.mark_delete_msg(i)

    def send_email(self):
        """ Send email """
        server = None
        try:
            logger.info("*** Sending email ***")
            msg = MIMEText(self.__message, "plain")
            msg['Subject'] = self.__subject
            msg['From'] = self.__from_address
            msg['To'] = self.__to_address
            server = smtplib.SMTP(self.__server, self.__out_port)
            logger.debug("Starting TLS server")
            server.starttls()
            logger.debug("Logging in to TLS server")
            server.login(self.__from_address, self.__pwd)
            logger.debug("Sending mail")
            server.sendmail(self.__from_address, [
                self.__to_address], msg.as_string())
            logger.debug("*** Email sent ***")
        except Exception as e:
            logger.critical(e)
        finally:
            if server:
                logger.debug("Server quitting...")
                server.quit()
                logger.debug("Server quit successful")
            else:
                logger.debug("No server to quit")
