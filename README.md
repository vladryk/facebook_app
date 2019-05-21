# Facebook Application

To run this application please create your own `Social applications` in django-admin or change current that is present:
Add `Client id`, `Secret key`, `Name` then please add this `Name` for `SOCIAL_APP_NAME` in `settings.py`
You can use current (or create your own) admin-user name:`test`, pswd:`Testzei0`. 
SQLite is used by default (it's enough for current task), there are some data for runnig project more easly.
Url/View for DeAuth callback is implemented. Long living access token is implemented by `django-allauth` libirary.

Need to be implemented: Tests and docker-compose