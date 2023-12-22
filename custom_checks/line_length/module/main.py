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

    def replace_with_placeholder(self, text: str):
        # these are the maximum lengths we've decided these strings should be
        text = text.replace("<pc_hiryu>", "<&13_aaaaaaa>")
        text = text.replace("<cs_pchero_hiryu>", "<&13_aaaaaab>")
        text = text.replace("<cs_pchero_race>", "<&8_aaa>")
        text = text.replace("<cs_pchero>", "<13_aaaaaac>")
        text = text.replace("<kyodai_rel1>", "<&7_aa>")
        text = text.replace("<kyodai_rel2>", "<&7_ab>")
        text = text.replace("<kyodai_rel3>", "<&7_ac>")
        text = text.replace("<pc_hometown>", "<&8_aab>")
        text = text.replace("<pc_race>", "<&8_aac>")
        text = text.replace("<pc_rel1>", "<&7_ad>")
        text = text.replace("<pc_rel2>", "<&7_ae>")
        text = text.replace("<pc_rel3>", "<&7_af")
        text = text.replace("<kyodai>", "<&13_aaaaaac>")
        text = text.replace("<pc>", "<&13_aaaaaad>")
        text = text.replace("<client_pcname>", "<&13_aaaaaae>")
        text = text.replace("<heart>", "<&2a>")
        text = text.replace("<diamond>", "<&2b>")
        text = text.replace("<spade>", "<&2c>")
        text = text.replace("<clover>", "<&2d>")
        text = text.replace("<r_triangle>", "<&2e>")
        text = text.replace("<l_triangle>", "<&2f>")
        text = text.replace("<half_star>", "<&2g>")
        text = text.replace("<null_star>", "<&2h>")
        text = text.replace("<npc>", "<&13_aaaaaaf>")
        text = text.replace("<pc_syokugyo>", "<&13_aaaaaag>")
        text = text.replace("<pc_original>", "<&13_aaaaaah>")
        text = text.replace("<log_pc>", "<&13_aaaaaai>")
        text = text.replace("<1st_title>", "<&20_aaaaaaaaaaaaaa>")
        text = text.replace("<2nd_title>", "<&20_aaaaaaaaaaaaab>")
        text = text.replace("<3rd_title>", "<&20_aaaaaaaaaaaaac>")
        text = text.replace("<4th_title>", "<&20_aaaaaaaaaaaaad>")
        text = text.replace("<5th_title>", "<&20_aaaaaaaaaaaaae>")
        text = text.replace("<6th_title>", "<&20_aaaaaaaaaaaaaf>")
        text = text.replace("<7th_title>", "<&20_aaaaaaaaaaaaag>")

        # remove strings we dont want to evaluate
        text = text.replace("<yesno>", "")
        text = text.replace("<yesno 2>", "")
        text = text.replace("<yesno2>", "")
        text = text.replace("<yesno_nc>", "")
        text = text.replace("<break>", "")
        text = text.replace("<case 1>", "")
        text = text.replace("<case 2>", "")
        text = text.replace("<case 3>", "")
        text = text.replace("<case 4>", "")
        text = text.replace("<case 5>", "")
        text = text.replace("<close>", "")
        text = text.replace("<case_end>", "")
        text = text.replace("<yesno_se_off>", "")
        text = text.replace("<if_woman>", "")
        text = text.replace("<if_man>", "")
        text = text.replace("<endif>", "")
        text = text.replace("<else>", "")

        return text

    def check_single(self, source, target, unit):
        lines = target.split('\n')
        for line in lines:
            line = self.replace_with_placeholder(text=line)
            encoded_line = line.encode('utf-8')
            if len(encoded_line) > 46:
                return True
