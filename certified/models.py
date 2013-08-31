from django.db import models

class Server(models.Model):
	name = models.CharField(max_length=20)
	server = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')
	before_date = models.DateTimeField(null=True)
	after_date = models.DateTimeField(null=True )

	def __unicode__(self):
		return self.name


# Create your models here.
