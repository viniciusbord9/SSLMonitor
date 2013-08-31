from django.contrib import admin
from certified.models import Server
from datetime import datetime
import time
import ssl
import OpenSSL

class AdminServer(admin.ModelAdmin):
	list_display = ('name','server','after_date')
	exclude = ['after_date','before_date']
	
		

admin.site.register(Server, AdminServer)



