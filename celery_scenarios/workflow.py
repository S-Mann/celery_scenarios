from random import random
from celery import (
    chain,
    group,
    subtask
)
from celery_scenarios.celery_app.celery import app

CAR_TYPES = ['sedan', 'suv']


@app.task
def get_cars(prev_result=None, *, car_type, **kwargs):
    cars = []
    if car_type == 'sedan':
        cars = ['CT4', 'CT6']
    elif car_type == 'suv':
        cars = ['Escalade']
    return cars


@app.task
def get_profitable(car, *, car_type, **kwargs):
    sales = {'name': car}
    if car_type == 'sedan':
        sales['is_profitable'] = random() < 0.5
    elif car_type == 'suv':
        sales['is_profitable'] = True
    return sales


@app.task
def dmap(it, callback):
    # https://stackoverflow.com/a/13569873/8243326
    # ?: This takes a partial as an argument with the result from the earlier task and converts it into subtasks so that the result from this group can be used in the workflow.
    callback = subtask(callback)
    return group(callback.clone([arg, ]) for arg in it).apply_async()


workflow = group(
    [chain([
        get_cars.s(car_type=car_type),
        dmap.s(get_profitable.s(car_type=car_type))
    ]) for car_type in CAR_TYPES]
)


@app.task
def my_workflow():
    return workflow.apply_async()
