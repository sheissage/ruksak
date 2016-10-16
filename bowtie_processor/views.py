
import time

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.http import JsonResponse

from bowtie_processor.processor import Processor
from bowtie_processor.places import GoogleMapsProcessor
from bowtie_processor.translate import GoogleTranslateProcessor
from bowtie_processor.expedia import ExpediaProcessor
# Create your views here.

def index(request):
	return render(request, 'bowtie_processor/main.html', {},
        content_type="text/html")


def process(request):
	if request.method == 'POST':
		latitude = request.POST.get('lat')
		longitude = request.POST.get('lng')

		image = request.FILES.get('raw_image')
		processor = Processor()
		raw_image = image.read()
		classified_image = processor.run(raw_image)

		maps = GoogleMapsProcessor()
		response = {}

		try:

			response = maps.search(classified_image[0].get('word'), 
				{'lat':latitude, 'lng':longitude}
				)
		except:
			return HttpResponseNotFound('<h1>Please allow locations!</h1>')

		
		data = {
			'stores': response,
			'word': classified_image[0].get('word')
		}

		if response:
			return render(request, 'bowtie_processor/main.html', data)
		else:
			return HttpResponse(400)
	else:
		return HttpResponseNotFound('<h1>Page not found</h1>')

def process_text(request):
	if request.method == 'POST':
		term = request.POST.get('search')
		latitude = request.POST.get('lat')
		longitude = request.POST.get('lng')

		translate = GoogleTranslateProcessor()
		word = translate.translate(term)

		if not word:
			word = term 
		
		maps = GoogleMapsProcessor()

		try:
			response = maps.search(
				word, 
				{'lat':latitude, 'lng':longitude}
				)
		except:
			return HttpResponseNotFound('<h1>Please allow locations!</h1>')

		data = {
			'stores': response,
			'word': term
		}

		if response:
			return render(request, 'bowtie_processor/main.html', data)
		else:
			return HttpResponse(400)
	else:
		return HttpResponseNotFound('<h1>Page not found</h1>')

def process_details(request, place_id):
	if request.method == 'GET':
		maps = GoogleMapsProcessor()
		details = maps.get_place(place_id)

		expedia = ExpediaProcessor()
		results = expedia.search(details.get('lat'), details.get('lng'))
		

		for result in results:
			print result
			print '--------------------'
		data = {
			'store': details,
			'recommendations': results
		}

		return render(request, 'bowtie_processor/details.html', data)
	else:
		return HttpResponseNotFound('<h1>Page not found</h1>')