from django.forms import ModelForm
from .models import Profile

class ImageUploadForm(ModelForm):
	class Meta:
		model = Profile
		fields = ['profile_pik']