# VolunteerX

VolunteerX is a lightweight platform for engaging local communities in volunteering.
Local people can sign up to become on-demand volunteers.
NGOs can easily manage the real time deployment of skilled volunteers.

## TODOs:

1) Sign up with LinkedIn, Facebook & OpenID
2) Volunteer members heatmap
3) Stats dashboard


## Prerequisites
----
These instructions have been tested with the following software:

* Python Flask = 0.10.0
* git
* gunicorn

## Dependency Setup
----
1.  `virtualenv venv`
1.  `source venv/bin/activate`
1.  `pip install -r requirements.txt`

## Configuration Setup
----
You need to provide configuration in config.py

* Twilio API credentials


## Scaffold Setup
----
These instructions assume a working directory of the repository root.


### Local Development
To run the app locally:

1.  `source venv/bin/activate`
1.  `python run.py`

The server will run on `localhost:5000`


### Deployment
To deploy to Heroku:

