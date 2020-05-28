from django.contrib import admin
from Pages.models import country_team,match_user,user_team,choosen_players,user,match_performance

admin.site.register(country_team)
admin.site.register(match_user)
admin.site.register(user_team)
admin.site.register(choosen_players)
admin.site.register(user)
admin.site.register(match_performance)
