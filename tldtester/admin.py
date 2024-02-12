from admin_extra_buttons.api import ExtraButtonsMixin, button
from admin_extra_buttons.utils import HttpResponseRedirectToReferrer
from django.contrib import admin
from .models import TLD
from .models import zonecontent
import tldtester.sorter as sorter


class tlds(admin.ModelAdmin):
    list_display = ('tld', 'inet', 'dnssec', 'lastEdition')


class zone(ExtraButtonsMixin, admin.ModelAdmin):
    list_display = ('name', 'rtype', 'rclass', 'ttl', 'data', 'lastEdition')

    @button(change_form=True, html_attrs={'style': 'background-color:#88FF88;color:black'})
    def refresh(self, request):
        self.message_user(request, 'refresh called')
        sorter.main()
        # Optional: returns HttpResponse
        return HttpResponseRedirectToReferrer(request)


admin.site.register(TLD, tlds)
admin.site.register(zonecontent,zone)
