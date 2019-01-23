"""
Failures of AAA01: no Act block found in test
"""

from applications.models import MembershipApplication


def test(db):
    """
    Database starts with an application
    """
    assert MembershipApplication.objects.count() == 1
