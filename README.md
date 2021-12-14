# DAA Project single

## How to setup the environment

```
python -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

## How to test

```
pytest -W ignore::DeprecationWarning
```

Note: We ignore the deprecation warning from the daa_collections package

