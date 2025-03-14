import os

class CorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Get allowed origins from environment or use default
        self.allowed_origins = []
        if 'CLIENT_ORIGIN' in os.environ:
            self.allowed_origins.append(os.environ.get('CLIENT_ORIGIN'))
        if 'CLIENT_ORIGIN_DEV' in os.environ:
            self.allowed_origins.append(os.environ.get('CLIENT_ORIGIN_DEV'))
        
        # Add fallbacks if no environment variables are set
        if not self.allowed_origins:
            self.allowed_origins = [
                'http://localhost:3000',
                'https://eventify-front-e281c9a84c02.herokuapp.com',
            ]

    def __call__(self, request):
        response = self.get_response(request)
        
        # Get the origin from the request
        origin = request.headers.get('Origin')
        
        # If the origin is in our allowed list, set the CORS headers
        if origin and (origin in self.allowed_origins or '*' in self.allowed_origins):
            response["Access-Control-Allow-Origin"] = origin
            response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
            response["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
            response["Access-Control-Allow-Credentials"] = "true"
        
        return response
