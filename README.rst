================
celery_scenarios
================


.. image:: https://img.shields.io/pypi/v/celery_scenarios.svg
        :target: https://pypi.python.org/pypi/celery_scenarios

.. image:: https://img.shields.io/travis/S-Mann/celery_scenarios.svg
        :target: https://travis-ci.com/S-Mann/celery_scenarios

.. image:: https://readthedocs.org/projects/celery-scenarios/badge/?version=latest
        :target: https://celery-scenarios.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status




Celery workflows and scenarios


* Free software: GNU General Public License v3
* Documentation: https://celery-scenarios.readthedocs.io.


Features
--------

- This application is a sandbox for my crazy celery workflow designs.
- This is also very helpful for some who is looking to implement a workflow based on my learnings.

Setup
--------

- Use `venv` in `Python3` and install Redis_
- Install the necessary packages
  ```sh
  $ pip install -r requirements_dev.txt
  ```
- Start `beat` scheduler, this will periodically schedule the whole workflow within certain mins.
  ```sh
  $ celery -A celery_scenarios.celery_app beat --loglevel=INFO
  ```
- Start `worker`, this is where your workflow and tasks run.
  ```sh
  $ celery -A celery_scenarios.celery_app worker --loglevel=INFO
  ```

Configs
--------

- If you don't want to use `Redis`you can go ahead can change the configs in config.py_ and install and setup dependencies accordingly.
- Don't like the periodic scheduler's schedule? You can configure it under the app's beat_schedule_.

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _Redis: https://redis.io/topics/quickstart
.. _beat_schedule: ./celery_scenarios/celery_app/celery.py#L12
.. _config.py: ./celery_scenarios/config/base.py