from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Diagnosis
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# from .beanclassification import predictResult, test_dataset
class DiagoniseView(TemplateView):
	template_name = 'diagnosis/index.html'

@login_required(login_url = '/login/')
def resultsPage(request, crop_type):
	# form = DiagnosisImageForm()
	return render(request, 'diagnosis/fileUpload.html', {"crop":crop_type})


@login_required(login_url = '/login/')
def analyse(request):
	if request.method == 'POST':
		code = request.POST.get("code").lower()
		user = request.user
		mytype = "bn"
		disease = ""
		is_fine = False
		mydiagText = ""
		msg = ""
		if code == '#0brd':
			disease = "Bean rust"
			mydiagText = "Your bean sample has been infected with <b>Bean rust</b>. <br> Bean rust can be controlled by using a combination of management practices: Use clean bean seeds originating from non-diseased plants or from certified seed dealers. Using clean seeds prevents spreading of rust disease. We have found some solutions on <a href ='https://www.growveg.com/plant-diseases/us-and-canada/bean-rust/'/>here<a> and <a href='https://homeguides.sfgate.com/rid-rust-beans-28584.html'>here</a>"
			is_fine = True
		elif code == '#1alsd':
			disease = "Angular-leaf spot"			
			mydiagText = "Your bean sample has been diagnised with <b>Angular-leaf spot</b>.<br> It is characterised by: Leaves develop small, angular, brown or straw-colored spots with a yellow halo. Leaf spots dry and drop out, leaving irregularly shaped holes in the leaves. We found out useful resources on <a href ='https://extension.umn.edu/diseases/angular-leaf-spot'/>here<a> and <a href='https://www.gardeningknowhow.com/plant-problems/disease/treating-angular-leaf-spot.htm'>here</a>"
			is_fine = True
		elif code == '#2hl':
			disease = "Healthy"
			is_fine = True
			mydiagText = "Your bean sample has been found <b>healthy</b>."
		else:
			is_fine = False
			msg = "The code you sent is invalid, are you sure you tested?"
		if is_fine:
			save_diag = Diagnosis(
					farmer = user,
					predicate_disease = disease, 
					diagnosis_text = mydiagText,
					type_of_test = mytype, 
				)

			myresp = save_diag.save()
			all_tests = Diagnosis.objects.filter(farmer = request.user).order_by('-tested_on')
			respo = Diagnosis.objects.filter(farmer = user).order_by('-tested_on')[:1]
			context = {
				"resp": respo[0],
				"all_tests": all_tests
			}
			return render(request, 'diagnosis/feedback.html', context)
		else:
			context = {
				"msg": msg,
			}
			return render(request, 'diagnosis/index.html', context)


def resultsPage(request):
	context = {
		"all_tests" : Diagnosis.objects.filter(farmer = request.user).order_by('-tested_on')
		 }
	return render(request, 'diagnosis/feedback.html', context)
