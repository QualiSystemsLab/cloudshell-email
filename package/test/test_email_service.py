import unittest
from unittest.mock import patch, mock_open

from mock import Mock, ANY

from cloudshell.orch.training.services.email import EmailService


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

not_default_html = '''
{sandbox_link}
'''

args_html = '''
{sandbox_link}
{arg1}
{arg2}
{arg3}
'''


class TestEmailService(unittest.TestCase):

    def setUp(self) -> None:
        self.email_config = Mock()
        self.sandbox_output_service = Mock()
        self.logger = Mock()
        self.email_service = EmailService(self.email_config, self.sandbox_output_service, self.logger)

    def test_send_no_email_address(self):
        # arrange
        self.email_service._send = Mock()

        # act
        self.email_service.send_email([], Mock(), Mock(), Mock())

        # assert
        self.sandbox_output_service.notify.assert_called_once_with('Empty list of email addresses')
        self.email_service._send.aseert_not_called()

    def test_send_email_invalid_address(self):
        # arrange
        self.email_service._send = Mock()
        invalid_email = 'aaa@bbb'

        # act
        self.email_service.send_email([invalid_email], Mock(), Mock(), Mock())

        # assert
        self.sandbox_output_service.notify.assert_called_once_with(f'{invalid_email} is not a valid email address')
        self.email_service._send.aseert_not_called()

    def test_send_email_valid_and_invalid_address(self):
        # arrange
        self.email_service._send = Mock()
        valid_email = 'aaa@bbb.com'
        invalid_email = 'aaa@bbb'

        # act
        self.email_service.send_email([valid_email, invalid_email], Mock(), Mock(), Mock())

        # assert
        self.sandbox_output_service.notify.assert_called_once_with(f'{invalid_email} is not a valid email address')
        self.email_service._send.aseert_not_called()

    def test_send_email_mulitple_valid_and_invalid_address(self):
        # arrange
        self.email_service._send = Mock()
        valid_email = 'aaa@bbb.com'
        valid_email2 = 'aaa2@bbb.com'
        valid_email3 = 'aaa3@bbb.com'
        invalid_email = 'aaa@bbb'
        invalid_email2 = 'aaa2@bbb'
        invalid_email3 = 'aaa3@bbb'

        emails = [invalid_email, invalid_email2, valid_email, valid_email2, invalid_email3, valid_email3]

        # act
        self.email_service.send_email(emails, Mock(), Mock(), Mock())

        # assert
        self.sandbox_output_service.notify.assert_called_once_with(f'{invalid_email},{invalid_email2},{invalid_email3} are not valid email addresses')
        self.email_service._send.aseert_not_called()

    def test_cc_send_email_mulitple_valid_and_invalid_address(self):
        # arrange
        self.email_service._send = Mock()
        valid_email = 'aaa@bbb.com'
        valid_email2 = 'aaa2@bbb.com'
        valid_email3 = 'aaa3@bbb.com'
        invalid_email = 'aaa@bbb'
        invalid_email2 = 'aaa2@bbb'
        invalid_email3 = 'aaa3@bbb'

        emails = [invalid_email, invalid_email2, valid_email, valid_email2, invalid_email3, valid_email3]

        # act
        self.email_service.send_email([valid_email], Mock(), Mock(), Mock(), cc_email_address=emails)

        # assert
        self.sandbox_output_service.notify.assert_called_once_with(f'{invalid_email},{invalid_email2},{invalid_email3} are not valid email addresses')
        self.email_service._send.aseert_not_called()

    @patch('os.path.isfile')
    def test_load_default_template(self, mock_isfile):
        # arrange
        self.email_service._send = Mock()
        valid_email = 'aaa@bbb.com'
        link = 'Default Link'

        mock_isfile.return_value = False

        # act
        content = self.email_service._load_and_format_template('', link)

        # assert
        self.assertEqual(content, default_html.format(sandbox_link=link))

    @patch('os.path.isfile')
    def test_load_template(self, mock_isfile):
        # arrange
        self.email_service._send = Mock()
        valid_email = 'aaa@bbb.com'
        link = 'Default Link'

        mock_isfile.return_value = True

        # act
        with patch("builtins.open", mock_open(read_data=not_default_html)) as mock_file:
            content = self.email_service._load_and_format_template('', link)

        # assert
        self.assertEqual(content, not_default_html.format(sandbox_link=link))

    @patch('os.path.isfile')
    def test_load_template_with_args(self, mock_isfile):
        # arrange
        self.email_service._send = Mock()
        valid_email = 'aaa@bbb.com'
        link = 'Default Link'

        extra_args = dict()
        extra_args['arg1'] = 'argument1'
        extra_args['arg2'] = 'argument2'
        extra_args['arg3'] = 'argument3'

        mock_isfile.return_value = True

        # act
        with patch("builtins.open", mock_open(read_data=args_html)) as mock_file:
            content = self.email_service._load_and_format_template('', link, **extra_args)

        # assert
        self.assertEqual(content, args_html.format(sandbox_link=link, **extra_args))

    @patch('os.path.isfile')
    def test_send_email(self, mock_isfile):
        # arrange
        self.email_service._send = Mock()
        email = 'aaa@bbb.com'
        link = 'Default Link'

        mock_isfile.return_value = False

        # act
        self.email_service.send_email([email], 'Default Subject', link, cc_email_address=[email])

        # assert
        self.email_service._send.assert_called_once_with([email], 'Default Subject', default_html.format(sandbox_link=link), [email])