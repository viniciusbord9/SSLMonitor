#!/usr/bin/env python
import sys
import os
import ssl
import OpenSSL
import time
import datetime
import pytz
from django.core.mail import EmailMessage
from django.core.mail import send_mail

sys.path.append('/var/www/monitor/')

import manage

if __name__ == "__main__":
	utc = pytz.utc
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "monitor.settings")
	from certified.models import Server
	servers = Server.objects.all()
	_today = datetime.datetime.today()
	today = datetime.datetime(_today.year, _today.month, _today.day, _today.hour, _today.minute, _today.second,tzinfo=utc)
	for server in servers:

		expiration = server.after_date
		date_expiration = datetime.datetime(expiration.year, expiration.month, expiration.day, expiration.hour, expiration.minute, expiration.second, tzinfo=utc)
		time_expiration = date_expiration - today
		if time_expiration.days <= 90:
			cert = ssl.get_server_certificate((server.server, 443))
			certificado = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM,cert)
			_after = certificado.get_notAfter()
			_before = certificado.get_notBefore()
			_date = _after[0:8]
			_time = _after[8:14]
			after = time.strptime(_date+" "+_time,"%Y%m%d %H%M%S")
			_date = _before[0:8]
			_time = _before[8:14]
			before = time.strptime(_date+" "+_time,"%Y%m%d %H%M%S")
			after_date= datetime.datetime(after.tm_year, after.tm_mon, after.tm_mday, after.tm_hour, after.tm_min, after.tm_sec,tzinfo=utc)
			before_date= datetime.datetime(before.tm_year, before.tm_mon, before.tm_mday, before.tm_hour, before.tm_min, before.tm_sec,tzinfo=utc)
			dt = after_date - today
			days = dt.days
			if dt.days <= 90:
				text = 'O Certificado do servidor '+server.name+' expira em '+str(days)+' dias'
				email = EmailMessage("Cerficado SSL",text, to=['thiago@agenciadeinternet.com'])
				email.send()


			server.before_date = before_date
			server.after_date = after_date
			server.save()
