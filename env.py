import os

# Development mode
os.environ['DEV'] = '1'

# Django secret key
os.environ['SECRET_KEY'] = "django-insecure-it3fboer&t(#=(050uy(9@obq^un%9+06ps^a22c=wvj4x$@+e7"

# Database URL
os.environ['DATABASE_URL'] = "postgres://neondb_owner:aRhc4OdmXS0q@ep-fancy-surf-a24q678d.eu-central-1.aws.neon.tech/wife_trek_yelp_808895"

# Cloudinary settings 
os.environ['CLOUDINARY_CLOUD_NAME'] = 'dpw2txejq'
os.environ['CLOUDINARY_API_KEY'] = '173578923717674'
os.environ['CLOUDINARY_API_SECRET'] = 'VVp4fYWkDGWKRYVzq4KDIhGgEck'