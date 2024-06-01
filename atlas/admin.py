from admin_extra_buttons.api import ExtraButtonsMixin, button
from admin_extra_buttons.utils import HttpResponseRedirectToReferrer
from django.contrib import admin
from .models import Atlas
import atlas.atlascreator as atlascreator
import threading


class atlas(ExtraButtonsMixin, admin.ModelAdmin):
    list_display = ('unicodetld', 'stack', 'measurement', 'lastEdition')

    @button(change_form=True, html_attrs={'style': 'background-color:#88FF88;color:black'})
    def refresh(self, request):
        self.message_user(request, 'refresh called')
        t1 = threading.Thread(target=atlascreator.main())
        t1.start()
        # Optional: returns HttpResponse
        return HttpResponseRedirectToReferrer(request)


admin.site.register(Atlas, atlas)
