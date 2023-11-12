#!/usr/bin/env bash
echo "Check convention ..."
python3 -m flake8 && python3 -m pylint services airflow_dags common services
echo "Unit tests ..."
python3 -m pytest -vv --cov ./ --cov-report term-missing --cov-fail-under=100
