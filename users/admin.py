from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, SearchLog, AdminConsumptionLimit

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Civil Registry Info'

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'profile__national_code', 'profile__phone_number')

    # Registering a profile model in the admin (for hidden access).
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'national_code', 'phone_number', 'daily_limit', 'monthly_limit', 'get_daily_usage', 'get_monthly_usage')
    list_filter = ('daily_limit', 'monthly_limit')
    search_fields = ('user__username', 'national_code', 'phone_number')
    
    def get_daily_usage(self, obj):
        return obj.get_daily_usage()
    get_daily_usage.short_description = "Daily Usage"

    def get_monthly_usage(self, obj):
        return obj.get_monthly_usage()
    get_monthly_usage.short_description = "Monthly Usage"

@admin.register(SearchLog)
class SearchLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'query_text', 'results_count', 'duration', 'timestamp')
    list_filter = ('timestamp', 'user')
    search_fields = ('query_text', 'user__username')
    readonly_fields = ('user', 'query_text', 'results_count', 'duration', 'timestamp')




