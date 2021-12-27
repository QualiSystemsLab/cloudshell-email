# cloudshell-email

[![CI](https://github.com/QualiSystemsLab/cloudshell-email/actions/workflows/ci.yml/badge.svg)](https://github.com/QualiSystemsLab/cloudshell-email/actions?query=workflow%3ACI)
[![Coverage Status](https://coveralls.io/repos/github/QualiSystemsLab/cloudshell-email/badge.svg?branch=master)](https://coveralls.io/github/QualiSystemsLab/cloudshell-email?branch=master)
[![PyPI version](https://badge.fury.io/py/cloudshell-email.svg)](https://badge.fury.io/py/cloudshell-email)
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)

![quali](quali.png)

Python package to easily add email functionality to orchestration scripts run from CloudShell.

## Why use cloudshell-email
- Send emails containing a link to the Sandbox
- Send emails based on html templates

## Installing
    $ python -m pip install cloudshell-email

## Basic Usage
### Initialize EmailService object
```
from cloudshell.workflow.orchestration.sandbox import Sandbox
from cloudshell.email import EmailConfig, EmailService

sandbox = Sandbox()
email_config = EmailConfig('SMTP Server hostname', 'username', 'password', 'Email_to_send_from')

email_service = EmailService(email_config, sandbox.logger)
```

### Send Emails
```python
send_email(self, to_email_address: List[str], 
                 subject: str,
                 template_name: str = 'default',
                 template_parameters: Dict[str, str] = {},
                 cc_email_address: List[str] = [])
```
Send emails using the above method of EmailService.
Default values added to the email config object will override these values.

- to_email_address: Email addresses to send email to
- subject: Subject line of email
- template_name: Path to local html file containing email template
- template_parameters: Parameter name:values to fill into html template
- cc_email_address: Email addresses to CC on email

### Validate Email Configuration
```python
import smtplib

email_service = EmailService(email_config, sandbox.logger)

try:
    email_service.validate_email_config()
except smtplib.SMTPHeloError:
    # error handling code
except smtplib.SMTPAuthenticationError:
    # error handling code
except smtplib.SMTPNotSupportedError:
    # error handling code
except smtplib.SMTPException:
    # error handling code
except RuntimeError:
    # error handling code
```
Validate email service configuration using validate_email_config() method.

### Html Templates
Html templates will be opened from the template_path on the machine running the orchestration scripts.

The default html template is if no template_name parameter is given:
```html
<!DOCTYPE html>
<html lang="en">
<div>
    <h2 style="text-align: center;"><span style="color: #F76723;"><strong>Welcome to cloudshell-email</strong></span></h2>
</div>
<div>
    <p><span style="color: #000000;">This is the default html template using the cloudshell-email package.</span></p>
</div>
<div>
    <p><span style="color: #000000;">The cloudshell-email package can be used to send emails to users from orchestration scripts.</span></p>
</div>
<div>
    <p><span style="color: #000000;"><strong>You can view cloudshell-email usage guide here:</strong></span></p>
</div>
<div>
    <span style="color: #000000;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        <a href="https://github.com/QualiSystemsLab/cloudshell-email"> Github Repo </a>
    </span>
</div>
</body>
</html>
```

Variables can be placed into the html to be replaced with the template_parameters input as so:
```html
<div>
    <p><span style="color: #000000;">Variable 1: {variable1}, Variable 2: {variable2}.</span></p>
</div>
```

template_parameters for the above html would be:
```python
{'variable1': 'Value 1', 'variable2': 'Value 2'}
```

### Email Configuration Shell

An email configuration resource can be added to Cloudshell blueprints using the driver included in the email-config-shell folder. 

To install the package: 
```commandline
cd shell-config-shell
shellfoundry install
```

This shell is useful to avoid hard coding the configurations and SMTP server authentication details when there is a need to send a custom email during setup/teardown (or any other orchestration flow). The information saved in the Email Configuration resource should be used to initialize the EmailConfig object in the script.

Orchestration script example:

```python
from cloudshell.workflow.orchestration.sandbox import Sandbox
from cloudshell.email import EmailConfig, EmailService

sandbox = Sandbox()

session = sandbox.automation_api

resource = session.GetResourceDetails('EmailConfigResource')

emailconfig = EmailConfig(
    session.GetAttributeValue(resource.Name, f'{resource.ResourceModelName}.SMTP Server').Value,
    session.GetAttributeValue(resource.Name, f'{resource.ResourceModelName}.User').Value,
    session.DecryptPassword(session.GetAttributeValue(resource.Name,
                                                      f'{resource.ResourceModelName}.Password').Value).Value,
    session.GetAttributeValue(resource.Name, f'{resource.ResourceModelName}.From Address').Value,
    session.GetAttributeValue(resource.Name, f'{resource.ResourceModelName}.SMTP Port').Value
)
emailservice = EmailService(emailconfig, sandbox.logger)
```


When adding this resource to the inventory, Cloudshell will validate the SMTP server configuration defined in its attributes.

## Troubleshooting and Help

For questions, bug reports or feature requests, please refer to the [Issue Tracker]. Also, make sure you check out our [Issue Template](.github/issue_template.md).

## Contributing


All your contributions are welcomed and encouraged.  We've compiled detailed information about:

* [Contributing](.github/contributing.md)
* [Creating Pull Requests](.github/pull_request_template.md)


## License
[Apache License 2.0](https://github.com/QualiSystems/shellfoundry/blob/master/LICENSE)
