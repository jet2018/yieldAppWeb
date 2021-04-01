from django.contrib import admin
from .models import Diagnosis
# Register your models here.
class DiagnosisAdmin(admin.ModelAdmin):
	list_display = ("farmer","predicate_disease", "did_work", "diagnosis_text", "type_of_test", "feedbacks")
admin.site.register(Diagnosis, DiagnosisAdmin)