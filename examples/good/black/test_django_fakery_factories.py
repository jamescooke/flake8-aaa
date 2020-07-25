from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.utils import IntegrityError
from django.test import TestCase

from .django_fakery_factories import ItemFactory, UserFactory
from .models import Item


class TestItemFactory(TestCase):
    def test_default(self):
        """
        Django Fakery: Plant.Item: RED (creates invalid items)
        """
        result = ItemFactory()

        self.assertEqual(Item.objects.count(), 1)
        with self.assertRaises(ValidationError) as cm:
            result.full_clean()
        self.assertIn("has at most 1 character", str(cm.exception))


class TestUserFactory(TestCase):

    user_model = get_user_model()

    def test_default(self):
        """
        Django Fakery: User Model: YELLOW (raises IntegrityError)

        We have to push the number of Users created, but since Django Fakery
        has no collision protection and uses a small number of latin words it
        will always fail sooner or later. Sometimes on the second user.

        However, instances created are valid if they are able to enter the
        database.
        """
        with self.assertRaises(IntegrityError) as cm:
            for expected_num_created in range(1, 100):
                with transaction.atomic():
                    UserFactory()

        self.assertEqual(self.user_model.objects.count(), expected_num_created - 1)
        self.assertIn("unique", str(cm.exception).lower())
        for u in self.user_model.objects.all():
            u.full_clean()
