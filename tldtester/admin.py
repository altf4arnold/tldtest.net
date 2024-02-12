from django.contrib import admin
from .models import TLD

class tlds(admin.ModelAdmin):
    list_display = ('tld', 'inet', 'dnssec', 'lastEdition')


admin.site.register(TLD, tlds)
# Register your models here.
