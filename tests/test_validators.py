from django.test import TestCase
from django.test.utils import override_settings
from django.forms.utils import ValidationError
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string

from newsletter.validators import validate_email_no_user


class ValidatorTestCase(TestCase):
    """ Test case for validators. """
    def setUp(self):
        super().setUp()
        self.user = get_user_model().objects.create_user(
            'john', 'lennon@thebeatles.com', get_random_string(length=16))
        self.user.save()

    def test_validate_email_no_user_success(self):
        """ Test validate_email_no_user where no error is raised. """
        validate_email_no_user('test@nowhere.com')

    def test_validate_email_no_user_error(self):
        """ Test validate_email_no_user where error is raised. """
        with self.assertRaises(ValidationError):
            validate_email_no_user(self.user.email)

    @override_settings(NEWSLETTER_VALIDATE_NO_USER=False)
    def test_validate_email_no_user_disabled(self):
        """ With NEWSLETTER_VALIDATE_NO_USER=False the validator is a no-op. """
        validate_email_no_user('lennon@thebeatles.com')
