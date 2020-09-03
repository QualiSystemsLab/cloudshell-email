import logging
import re
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Dict, List

from cloudshell.orch.training.models.email_config import EmailConfig
from cloudshell.orch.training.services.sandbox_output import SandboxOutputService

default_html = '''
<!DOCTYPE html>
<html lang="en">
<div>
    <h2 style="text-align: center;"><span style="color: #F76723;"><strong>Welcome to Training</strong></span></h2>
</div>
<div>
    <p><span style="color: #000000;">Please retain this email as it is how you will access your online lab environment. It also contains your credentials (if needed) and links to helpful materials.</span></p>
</div>
<div>
    <p><span style="color: #000000;">I&rsquo;m looking forward to our class together</span></p>
</div>
<div>
    <p><span style="color: #000000;"><strong>To access your CloudShell Environment please use the following:</strong></span></p>
</div>
<div>
    <span style="color: #000000;"><span style="color: #F76723;"><strong>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Environment details:</strong></span></span><br>
</div>
<div>
    <span style="color: #000000;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        <a href="{sandbox_link}"> Environment Link </a>
    </span>
</div>
</body>
</html>
'''


class EmailService:

    def __init__(self, email_config: EmailConfig, sandbox_output_service: SandboxOutputService, logger: logging.Logger):
        self._email_config = email_config
        self._sandbox_output = sandbox_output_service
        self._logger = logger

    def send_email(self, to_email_address: List[str], subject: str, link: str, template_parameters: Dict[str, str],
                   template_name: str = 'default',
                   cc_email_address: List[str] = None):

        for email_address in to_email_address:
            if not self._is_valid_email_address(email_address):
                self._sandbox_output.notify(f'{email_address} is not a valid email address')
                return

        message = self._load_and_format_template(template_name, link, **template_parameters)

        self._send(to_email_address, subject, message, cc_email_address)

    def _is_valid_email_address(self, email):
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        return re.search(regex, email)

    def _send(self, to_address, subject, message, cc=None):
        from_address = self._email_config.from_address
        msg = MIMEMultipart('alternative')
        msg['From'] = ';'.join(from_address) if isinstance(from_address, list) else from_address
        msg['To'] = ';'.join(to_address) if isinstance(to_address, list) else to_address
        msg['Subject'] = subject
        if cc:
            msg["Cc"] = ';'.join(cc) if isinstance(cc, list) else cc
        mess = MIMEText(message, 'html')
        msg.attach(mess)

        try:
            smtp = smtplib.SMTP(
                host=self._email_config.smtp_server,
                port=self._email_config.smtp_port
            )
            smtp.ehlo()
            smtp.starttls()
            smtp.login(self._email_config.user, self._email_config.password)
            smtp.sendmail(
                from_addr=from_address,
                to_addrs=[to_address, cc] if cc else to_address,
                msg=msg.as_string()
            )
            smtp.close()
        except Exception:
            self._logger.exception(f'Failed to send email to {to_address}')
            raise

    def _load_and_format_template(self, template_name, sandbox_link, **extra_args):
        content = None

        try:
            if os.path.isfile(template_name):
                with open(template_name, 'r') as f:
                    html_string = f.read()
                    content = html_string.format(sandbox_link=sandbox_link, **extra_args)
            else:
                content = default_html.format(sandbox_link=sandbox_link)
        except Exception:
            self._logger.exception('Failed loading email template')
            raise

        return content