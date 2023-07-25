Amiran's test project.
=======

This application connects to both the users backend and the warhouse backend.

**THIS IS AN EXAMPLE WEBSITE**

Set it up
------

Use docker-compose to build the service

    $ docker-compose build

Configure the `environment.env` file to point to the users and warhouse backend. Use the
IP on your local machine.


Up the service

    $ docker-compose up


Test and login
------

There are two users created in the system, `bruce` and `stephen`, their password are "password".

You can log in as any of them, add more "beers", and search for all the beers in the system. No need to be logged to search.


Dependencies
------

This application uses Django as a web framework.
