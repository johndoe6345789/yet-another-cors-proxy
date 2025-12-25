
class Config(object):
	"""
	Configuration base, for all environments.
	"""
	DEBUG = False
	TESTING = False
	SQLALCHEMY_DATABASE_URI = 'sqlite:///application.db'
	BOOTSTRAP_FONTAWESOME = True
	SECRET_KEY = "MINHACHAVESECRETA"
	CSRF_ENABLED = True
	SQLALCHEMY_TRACK_MODIFICATIONS = True

	# CORS settings - permissive by default
	CORS_ORIGINS = "*"
	CORS_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
	CORS_ALLOW_HEADERS = "*"

	# Proxy endpoints configuration
	# Format: {'/api/proxy/name': 'https://target-url.com'}
	PROXY_ENDPOINTS = {}

	#Get your reCaptche key on: https://www.google.com/recaptcha/admin/create
	#RECAPTCHA_PUBLIC_KEY = "6LffFNwSAAAAAFcWVy__EnOCsNZcG2fVHFjTBvRP"
	#RECAPTCHA_PRIVATE_KEY = "6LffFNwSAAAAAO7UURCGI7qQ811SOSZlgU69rvv7"

class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = 'mysql://user@localhost/foo'
	SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
	DEBUG = True
	
	# Example proxy endpoints for testing
	PROXY_ENDPOINTS = {
		'/api/proxy/jsonplaceholder': 'https://jsonplaceholder.typicode.com'
	}

class TestingConfig(Config):
	TESTING = True
