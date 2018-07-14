from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse


class TestAccountEditView(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User(
            email='test@example.com',
            is_active=1
        )
        self.user.set_password('blah')
        self.user.save()

    def test_url_resolves(self):
        result = reverse('account.edit')

        self.assertEqual(result, '/account/')

    def test_not_logged_in(self):
        url = reverse('account.edit')

        result = self.client.get(url)

        self.assertEqual(result.status_code, 302)

    def test_loads_template(self):
        url = reverse('account.edit')
        self.client.login(email='test@example.com', password='blah')

        result = self.client.get(url)

        self.assertEqual(result.status_code, 200)
        self.assertTemplateUsed(result, 'account/account.html')
