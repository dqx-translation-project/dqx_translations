from django.utils.translation import gettext_lazy as _
from weblate.checks.base import TargetCheck


class LineLength(TargetCheck):

    # Used as identifier for check, should be unique
    # Has to be shorter than 50 characters
    check_id = "LineLength"

    # Short name used to display failing check
    name = _("Line Length")

    # Description for failing check
    description = _("Line length check has failed. Each line must be <= 46 characters.")

    # Real check code
    # Return True if you want check to fail on match
    # Weblate assigns strings as unicode, so we need to encode first
    def check_single(self, source, target, unit):
        lines = target.split('\n')
        for line in lines:
            encoded_line = line.encode('utf-8')
            if len(encoded_line) > 46:
                return True
