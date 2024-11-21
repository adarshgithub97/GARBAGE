from django.contrib import admin
from .models import Garbage,Contact,Plant,Booking,PasswordResetToken

# Register your models here.
admin.site.register(Garbage)
admin.site.register(Contact)
admin.site.register(Plant)
admin.site.register(PasswordResetToken)

class BookingAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'place', 'selected_plant', 'date')
admin.site.register(Booking, BookingAdmin)


