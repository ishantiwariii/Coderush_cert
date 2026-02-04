from django.contrib import admin
from .models import Participant


# 🎨 Branding
admin.site.site_header = "CodeRush Certificate Admin"
admin.site.site_title = "CodeRush Admin Portal"
admin.site.index_title = "Welcome to CodeRush Certificate Management"


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'position', 'certificate_generated')
    search_fields = ('email', 'name')
    list_filter = ('position', 'certificate_generated')
    ordering = ('email',)

    fieldsets = (
        ("Participant Information", {
            'fields': ('email', 'name')
        }),
        ("Certificate Details", {
            'fields': ('position', 'certificate_generated')
        }),
    )

    # 🔒 Prevent email from being changed after creation
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('email',)
        return ()
