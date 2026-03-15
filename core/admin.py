from django.contrib import admin
from .models import Group, Member, Contribution, Cycle, Round


admin.site.register(Group)
admin.site.register(Member)
admin.site.register(Contribution)
admin.site.register(Cycle)
admin.site.register(Round)
