from copy import deepcopy
from random import random
from celery import (
    group,
    subtask
)
from celery_scenarios.celery_app.celery import app

CAR_TYPES = ['sedan', 'suv']


@app.task
def get_cars(*, car_type: str, **kwargs):
    """Takes car_type and returns list of cars for that car_type.

    Args:
        car_type (str): car_type can currently only be sedan/suv

    Returns:
        list: list of cars
    """
    cars = []
    if car_type == 'sedan':
        cars = ['CT4', 'CT6']
    elif car_type == 'suv':
        cars = ['Escalade']
    return cars


@app.task
def get_profitable(car: str, *, car_type: str, **kwargs):
    """Takes car and car_type and determines if it's profitable in sales.

    Args:
        car (str): name of the car
        car_type (str): car_type can currently only be sedan/suv

    Returns:
        dict: dictionary with car_name and is_profitable
    """
    is_profitable = False
    if car_type == 'sedan':
        is_profitable = random() < 0.5
    elif car_type == 'suv':
        is_profitable = True
    return {'car_name': car, 'is_profitable': is_profitable}


@app.task
def final_task(car_details: dict, *args, **kwargs):
    """This is the final task in the workflow, which greets the user with a message depending on is_profitable flag from earlier tasks

    Args:
        car_details (dict): dictionary with car_name and is_profitable flag

    Returns:
        str: a message based on is_profitable flag
    """
    if car_details['is_profitable']:
        message = f"Continue current sales strategy for {car_details['car_name']}"
    else:
        message = f"Re-strategize sales for {car_details['car_name']}"
    return message


@app.task
def dmap(args_iter, celery_task):
    """
    Takes an iterator of argument tuples and queues them up for celery to run with the function.
    """
    callback = subtask(celery_task)
    if isinstance(args_iter, list):
        run_in_parallel = group(clone_signature(callback, args=(args,))
                                for args in args_iter)
    elif isinstance(args_iter, dict):
        run_in_parallel = group(clone_signature(callback, kwargs=args_iter))
    return run_in_parallel.delay()


def clone_signature(sig, args=(), kwargs=(), **opts):
    # Inspired from
    # https://stackoverflow.com/questions/59013002/how-to-recursively-chain-a-celery-task-that-returns-a-list-into-a-group
    # https://stackoverflow.com/questions/13271056/how-to-chain-a-celery-task-that-returns-a-list-into-a-group
    if sig.subtask_type and sig.subtask_type != "chain":
        raise NotImplementedError(
            "Cloning only supported for Tasks and chains, not {}".format(
                sig.subtask_type)
        )
    clone = sig.clone()
    # If the signature has multiple tasks in it.
    if hasattr(clone, "tasks"):
        task_to_apply_args_to = clone.tasks[0]
    else:
        task_to_apply_args_to = clone
    # Merge args, kwargs and options that we received with the ones the user provided earlier like `car_type`.
    args, kwargs, opts = task_to_apply_args_to._merge(
        args=args, kwargs=kwargs, options=opts)
    # Update the task with a deepcopy of options to ensure other tasks don't use the argument as reference.
    task_to_apply_args_to.update(
        args=args, kwargs=kwargs, options=deepcopy(opts))
    return clone


"""
This workflow showcases a lot of examples.
- The CAR_TYPE is a list which will start two tasks in parallel, one for 'sedan' and other for 'suv'.
- Since get_cars returns a list we can't apply singular tasks on it, we then use our custom dmap task that under the hood starts parallel tasks for each car 'CT4','CT6','Escalade'.
- Since dmap is a custom signature its result cannot be used directly hence I implemented clone_signature
NOTE: Consider get_cars, get_profitable as two endpoints on a 3rd party service(s) they don't have to be related and fianl_task our logic depending on the data gathered from earlier tasks.
"""
workflow = group(
    (
        get_cars.s(car_type=car_type)
        | dmap.s(
            get_profitable.s(car_type=car_type)
            | final_task.s()
        )
    ) for car_type in CAR_TYPES
)


@app.task
def my_workflow():
    return workflow.apply_async()
