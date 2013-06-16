from django.core import mail
from django.test import TestCase
from django.contrib.auth import models as auth_models

from userprofiles.contrib.emailverification import models


class ModelTests(TestCase):
    def setUp(self):
        self.user = auth_models.User.objects.create(
            username="test", password="test", email="old@test.com")

    def tearDown(self):
        models.EmailVerification.objects.all().delete()
        self.user.delete()

    def test_unicode(self):
        """Unicode rendering should contain the user, the old email and the new email"""
        rendering = unicode(models.EmailVerification(user=self.user, new_email="new@email.com", old_email="old@email.com"))
        self.assertEquals(rendering, "test - old@email.com/new@email.com")

    def test_get_pending(self):
        """Tests that get_pending really only returns pending items."""
        models.EmailVerification.objects.create_new_verification(
            self.user, 'new@email.com')
        pending = models.EmailVerification.objects.create_new_verification(
            self.user, 'newer@email.com')
        self.assertEquals(
            list(models.EmailVerification.objects.get_pending(self.user)),
            [pending])

    def test_create_sends_mail(self):
        """Tests that the create manager method sends an activation email."""
        models.EmailVerification.objects.create_new_verification(
            self.user, "test@test.com")
        self.assertEquals(len(mail.outbox), 1)
        self.assertEquals(mail.outbox[0].to, ["test@test.com"])

    def test_old_expired(self):
        """Tests that the creation of a new verification expired pending old
        ones."""
        first = models.EmailVerification.objects.create_new_verification(
            self.user, "test@test.com")
        second = models.EmailVerification.objects.create_new_verification(
            self.user, "test@test.com")

        self.assertTrue(models.EmailVerification.objects.get(pk=first.pk).is_expired)
        self.assertFalse(models.EmailVerification.objects.get(pk=second.pk).is_expired)
