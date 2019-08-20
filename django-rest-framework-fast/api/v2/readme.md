# v2 - Django REST Framework Generic Views

By using Django REST Framework views, you can consolidate the examples from the api.v1 into more succinct views that handle all the API based actions for you.

In this example, our views no longer mimic the browser-based views used in our webapp frontend, but are now their own thing and handle all the API verbs one would expect. On top of that, the endpoints automatically return the serialized data in the format expected. If accessed via a browser, the browsable API is returned.

Our urls.py is also much smaller and easier to maintain.

