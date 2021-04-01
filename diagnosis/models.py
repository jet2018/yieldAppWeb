from django.db import models
from django.contrib.auth.models import User
from django.core.validators import validate_image_file_extension

# Create your models here.
class Diagnosis(models.Model):
    crop_type = [
        ("cs", "Cassava"),
        ("bn", "Bean"),
    ]
    farmer = models.ForeignKey(User, on_delete=models.CASCADE)
    predicate_disease = models.CharField(max_length = 100,  blank=True, null=True)
    did_work = models.BooleanField(default = False)
    diagnosis_text = models.TextField(blank=True, null=True)
    type_of_test = models.CharField(max_length = 10, choices = crop_type)
    feedbacks = models.TextField(max_length = 1000, null = True, blank = True)
    tested_on = models.DateTimeField(auto_now_add = True)
    def __str__(self):
        self.farmer.username