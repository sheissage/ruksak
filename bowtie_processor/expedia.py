import requests
from django.conf import settings

from bowtie_processor.places import GoogleMapsProcessor

class ExpediaProcessor(object):

	def __init__(self):
		self.api_key = settings.EXPEDIA_API_KEY

	def search(self, lat, lng):
		query = "http://terminal2.expedia.com/x/geo/features?within=5km&lng={0}&lat={1}&type=point_of_interest&apikey={2}".format(lng, lat, self.api_key)
		r = requests.get(query)
		results = r.json()

		response = []

		counter = 0
		for result in results:
			name = result.get('name')
			position = result.get('position')
			latitude = position.get('coordinates')[0]
			longitude = position.get('coordinates')[1]

			cache = {}
			cache['name'] = name
			cache['lat'] = latitude
			cache['lng'] = longitude
			cache['maps'] = "http://maps.google.com/maps?z=12&t=m&q=loc:{0}+{1}".format(longitude, latitude)

			response.append(cache)

			counter = counter + 1
			if counter > 2:
				break

		return response
