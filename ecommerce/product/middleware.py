# # middleware.py

# from django.utils.deprecation import MiddlewareMixin
# from ipware import get_client_ip
# import geoip2.database
# from django.conf import settings

# class GeoIPMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         if 'country' not in request.session:
#             client_ip, is_routable = get_client_ip(request)
#             if client_ip:
#                 reader = geoip2.database.Reader(settings.GEOIP_PATH)
#                 response = reader.country(client_ip)
#                 request.session['country'] = response.country.iso_code
#             else:
#                 request.session['country'] = 'US'  # Default country if IP detection fails
