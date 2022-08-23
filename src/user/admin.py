from django.contrib import admin

# Register your models here.
from user.models import (
    User,
    State,
    City,
    BloodCamp,
    RBC,
    Platelets,
    Plasma,
    CryoAHF,
    Granulocytes
)

admin.site.register(City)
admin.site.register(State)
admin.site.register(BloodCamp)
admin.site.register(User)
admin.site.register(RBC)
admin.site.register(Platelets)
admin.site.register(Plasma)
admin.site.register(CryoAHF)
admin.site.register(Granulocytes)
