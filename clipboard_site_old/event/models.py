# from django.db import models

# class Category(models.Model):
# 	name = models.CharField(max_length = 255)

# 	def __str__(self):
# 		return self.name

# class Event(models.Model):
# 	eventId = models.AutoField(primary_key=True)
# 	id = models.CharField(max_length = 255)
# 	title = models.CharField(max_length = 255)
# 	description = models.CharField(max_length = 500)
# 	organization = models.CharField(max_length = 255)
# 	start_date = models.DateTimeField()
# 	end_date = models.DateTimeField()
# 	location = models.CharField(max_length = 255)
# 	address = models.CharField(max_length = 255)
# 	start_time = models.DateTimeField()
# 	end_time = models.DateTimeField()
# 	price = models.FloatField()
# 	url = models.CharField(max_length = 255)
# 	# category = models.ForeignKey(
# 	# 	Category,
# 	# 	on_delete=models.DO_NOTHING,
# 	# )
# 	category = models.CharField(max_length = 255)
# 	source = models.CharField(max_length = 255)

# 	def __str__(self):
# 		return self.title
