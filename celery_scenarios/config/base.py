# Broker settings.
broker_url = 'redis://localhost:6379/'

# List of modules to import when the Celery worker starts.
imports = ('celery_scenarios.workflow',)

# Using the database to store task state and results.
# result_backend = 'db+sqlite:///results.db'
