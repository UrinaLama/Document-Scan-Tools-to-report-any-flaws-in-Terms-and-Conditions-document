# Document-Scan
Application that scans the legal document in any website and provides their summary

### Project Structure

```

Flask Application

├───app
│   │   main.py
│   │   requirements.txt
│   │
│   ├───data
│   │       bad_privacy.txt
│   │       good_privacy.txt
│   │
│   ├───model
│   │       logistic_regression.pkl
│   │       vectorizer.pkl
│   │
│   ├───script
│   │   │   clean_data.py
│   │   │   model.py
│   │   │   scrape.py
│   │   │   __init__.py
│   │
│   ├───static
│   │   │   design.css
│   │   │
│   │   └───bootstrap
│   │       └───css
│   │               bootstrap.css
│   │               bootstrap.css.map
│   │               bootstrap.min.css
│   │               bootstrap.min.css.map
│   │
│   ├───templates
│   │       home.html

Jupyter Notebook
└───jupyter-notebooks
    │   Getting_Privacy_Text.ipynb
    │   privacy_policy_predictor.ipynb
    │
    │
    ├───Data
    │       bad_privacy.txt
    │       Data.csv
    │       good_privacy.txt
    │
    └───Model
            logistic_regression.pkl
            vectorizer.pkl
```


### Run the Flask Application

Make sure you have python3 and pip installed

1. Create a virtual environment
```
python -m venv python3-virtualenv
```

2. Activate a virtual environment
```
.\python3-virtualenv\Scripts\activate
```

3. Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all dependencies within activated environment

```
pip install -r requirements.txt
```

## Usage

Start flask server
```bash
set FLASK_APP=main.py
flask run
```
