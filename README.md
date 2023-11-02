# Great Expectations Research

Table of Contents:

1. [Reference links](#1-reference-links)

2. [Create GX project]()

## 1. Reference links
- [Official website](https://greatexpectations.io/integrations/)
- [Github](https://github.com/great-expectations/great_expectations)
- [Orchestrate Great Expectations with Airflow](https://docs.astronomer.io/learn/airflow-great-expectations)
- [DataHubValidationAction](https://datahubproject.io/docs/metadata-ingestion/integration_docs/great-expectations/)
- [Expectations Gallery](https://greatexpectations.io/expectations/)

## 2. Create GX Project
1. Create gx folder: `mkdir -p great_expectations`
2. Run python script below to initial project:
```python
import great_expections as gx
context = gx.get_context()
context = context.convert_to_file_context()
```

