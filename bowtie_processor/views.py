
import time

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.http import JsonResponse

from bowtie_processor.processor import Processor
from bowtie_processor.places import GoogleMapsProcessor
from bowtie_processor.translate import GoogleTranslateProcessor
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

		response = maps.search(classified_image[0].get('word'), 
			{'lat':latitude, 'lng':longitude}
			)

		
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
		response = maps.search(
			word, 
			{'lat':latitude, 'lng':longitude}
			)

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