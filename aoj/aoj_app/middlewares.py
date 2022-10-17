from django.utils.deprecation import MiddlewareMixin


class RequestLogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        print("%s GET: %s POST: %s") % (request.path, request.GET, request.POST)
