## Superhero Storyboard

This is a tutorial project for checking out Django REST Framework and comparing some of the ways to create an API using the framework, as well as a popular method of using stock Django to create the same API

This project can be run with Docker. To get started:

1. `$ docker-compose build`
2. `$ docker-compose up`

Afterward, you should be able to access the different versions of the API at:

`0.0.0.0:8009/api/v{1,2,3}/characters`

The different versions of the API each have a readme.md to explain what they are and why they exist.
A brief explanation is:

1: [v1 represents one of the popular stock Django ways to build APIs](/api/v1/readme.md)

2: [v2 is an example of a basic implementation of Django REST Framework API endpoints](/api/v2/readme.md)

3: [v3 uses DRF a ViewSet to automatically generate the API endpoints](/api/v3/readme.md)
