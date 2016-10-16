from django.conf import settings
from googleplaces import GooglePlaces, types, lang

class GoogleMapsProcessor(object):

	def __init__(self):
		self.google_places = GooglePlaces(settings.MAPS_API_KEY)
	
	def search(self, keyword, latlng):
		"""
		Search Google Places for Businesses
		"""
		# You may prefer to use the text_search API, instead.

		search_tokens = keyword.split(' ')

		response = []
		for token in search_tokens:
			query_result = self.google_places.nearby_search(
		        lat_lng=latlng, keyword=token,
		        radius=10000, types=[
		        types.TYPE_AMUSEMENT_PARK,
		        types.TYPE_BAKERY,
		        types.TYPE_BAR,
		        types.TYPE_BOOK_STORE,
		        types.TYPE_CAFE,
		        types.TYPE_CLOTHING_STORE,
		        types.TYPE_CONVENIENCE_STORE,
		        types.TYPE_DEPARTMENT_STORE,
		        types.TYPE_FOOD,
		        types.TYPE_GROCERY_OR_SUPERMARKET,
		        types.TYPE_HARDWARE_STORE,
		        types.TYPE_HEALTH,
		        types.TYPE_HOME_GOODS_STORE,
		        types.TYPE_LIBRARY,
		        types.TYPE_LIQUOR_STORE,
		        types.TYPE_MEAL_DELIVERY,
		        types.TYPE_MEAL_TAKEAWAY,
		        types.TYPE_MOVIE_THEATER,
		        types.TYPE_MUSEUM,
		        types.TYPE_NIGHT_CLUB,
		        types.TYPE_PARK,
		        types.TYPE_PHARMACY,
		        types.TYPE_RESTAURANT,
		        types.TYPE_SHOE_STORE,
		        types.TYPE_SHOPPING_MALL,
		        types.TYPE_STORE,

		        ])

			for place in query_result.places:
			    # Returned places from a query are place summaries.
			    cache = {}
			    place.get_details()
			    cache['id'] = place.place_id
			    cache['name'] = place.name
			    cache['address'] = place.formatted_address
			    cache['website'] = place.website
			    cache['phone'] = place.local_phone_number
			    cache['lat'] = float(place.geo_location.get('lat'))
			    cache['lng'] = float(place.geo_location.get('lng'))
			    cache['rating'] = place.rating
			    cache['types'] = place.types[0] if len(place.types) > 0 else 'Others'

			    for photo in place.photos:
			    	photo.get(maxheight=800, maxwidth=533)
			    	cache['photo'] = photo.url
			    	break;

			    response.append(cache)

		return response

		"""
		Search Expedia Hotels
		"""


		




