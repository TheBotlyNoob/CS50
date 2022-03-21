# an online terminal

This project is an online terminal that allows users to access a command prompt from anywhere, inside of their own temporary directory.

# safety

I have tried to make sure that the code is as safe and secure as possible, but, this website is for users to execute commands on the host machine it, so please, do not open this website to the world.

# running

To start the server, run the following command:

```bash
$ python3 manage.py runserver
```

# what's inside?

In [final_project/static/index.js](./final_project/static/index.js) is the client side code (it also contains jsx), it makes the requests to execute the command, and implements command history.

In [final_project/views.py](./final_project/views.py) is the server side code, it handles the requests from the client side, and executes the commands.

# distinctiveness and complexity

I believe this project satisfies the distinctiveness and complexity requirements of the project, because the idea of it has very little to do with previous projects. It has two Django models, one for an executed command, and one for a user.
