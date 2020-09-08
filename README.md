

![quali](quali.png)

## cloudshell-email
Python package to easily add email functionality to orchestration scripts run from CloudShell.

## Why use cloudshell-email
- Send emails containing a link to the Sandbox
- Send emails based html templates

## Installing
    $ python -m pip install cloudshell-email

## Basic Usage
### Initialize EmailService object
```
import logging
from cloudshell.workflow.orchestration.sandbox import Sandbox
from cloudshell.orch.email_service.sandbox_output import SandboxOutputService
from cloudshell.orch.email_service.email_config import EmailConfig
from cloudshell.orch.email_service.email import EmailService

sandbox = Sandbox()
email_config = EmailConfig('SMTP Server hostname', 'username', 'password', 'Email_to_send_from', SMTP_Port = 587)
sandbox_output_service = SandboxOutputService(sandbox, debug_enabled)

email_service = EmailService(email_config, sandbox_output_service, sandbox.logger)
```

### Send Emails
```
send_email(self, to_email_address: List[str], subject: str, link: str,
                 template_name: str = 'default',
                 template_parameters: Dict[str, str] = {},
                 cc_email_address: List[str] = [])
```
Send emails using the above method of EmailService.

- to_email_address: Email addresses to send email to
- subject: Subject line of email
- link: Sandbox link to add to email
- template_name: Path to html file containing email template
- template_parameters: Parameter name:values to fill into html template
- cc_email_address: Email addresses to CC on email

## Troubleshooting and Help

For questions, bug reports or feature requests, please refer to the [Issue Tracker]. Also, make sure you check out our [Issue Template](.github/issue_template.md).

## Contributing


All your contributions are welcomed and encouraged.  We've compiled detailed information about:

* [Contributing](.github/contributing.md)
* [Creating Pull Requests](.github/pull_request_template.md)


## License
[Apache License 2.0](https://github.com/QualiSystems/shellfoundry/blob/master/LICENSE)