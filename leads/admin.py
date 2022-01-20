from django.contrib import admin

from .models import User, Lead, Agent, UserProfile, Category, FollowUp, UserType, Department, Sale, Documents, SaleCategory



class LeadAdmin(admin.ModelAdmin):
    # fields = (
    #     'first_name',
    #     'last_name',
    # )

    list_display = ['First_Name', 'Last_Name']
    list_display_links = ['First_Name']
    list_editable = ['Last_Name']
    list_filter = ['category']
    search_fields = ['First_Name', 'Last_Name']

admin.site.register(Category)
admin.site.register(User)
admin.site.register(UserType)
admin.site.register(Sale)
admin.site.register(Documents)
admin.site.register(Department)
admin.site.register(UserProfile)
admin.site.register(Lead, LeadAdmin)
admin.site.register(Agent)
admin.site.register(FollowUp)
admin.site.register(SaleCategory)