from django.utils.translation import gettext_lazy as _
from weblate.checks.base import TargetCheck


class ByteCheck(TargetCheck):

    # Used as identifier for check, should be unique
    # Has to be shorter than 50 characters
    check_id = "ByteCheck"

    # Short name used to display failing check
    name = _("Byte Check")

    # Description for failing check
    description = _("Byte check has failed. Translation string bytes are longer than source string bytes.")

    # Real check code
    # Return True if you want check to fail on match
    # Weblate assigns strings as unicode, so we need to encode first
    def check_single(self, source, target, unit):
        encoded_source = source.encode('utf-8')
        encoded_target = target.encode('utf-8')
        if len(encoded_target) > len(encoded_source):
            return True
