from celery_scenarios.celery_app.celery import app


@app.task
def add(x, y): return x+y
