import re

from django.utils.translation import gettext_lazy as _
from weblate.checks.base import TargetCheck


class SpaceChecker(TargetCheck):

    # Used as identifier for check, should be unique
    # Has to be shorter than 50 characters
    check_id = "SpaceChecker"

    # Short name used to display failing check
    name = _("Space Checker")

    # Description for failing check
    description = _("Space checker has failed. Make sure you aren't double spacing, leaving spaces at the beginning or end of your lines, or using full-width spaces. Look for vertical red rectangles!")

    # Real check code
    # Return True if you want check to fail on match
    # Weblate assigns strings as unicode, so we need to encode first
    def check_single(self, source, target, unit):
        lines = target.split('\n')
        for line in lines:
            # check for double spaces
            if re.search(r' {2,}', line):
                return True

            # check for lines that start with a space
            if line.startswith(" "):
                return True

            # check for lines that end with a space
            if line.endswith(" "):
                return True

            # check for usage of full width spaces
            if line.contains("　"):
                return True
