# An Online Terminal

---

This project is an online terminal that allows users to access a command prompt from anywhere, inside of their own temporary directory.

# Safety

---

I have tried to make sure that the code is as safe and secure as possible, but, this website is for users to execute commands on the host machine it, so please, do not open this website to the world.

# Running

---

To start the server, run the following command:

```bash
$ python3 manage.py runserver
```

# What's Inside?

---

This project uses Django, which has a lot of extra files that I haven't edited. So, I'm not going to include them in this overview of files.

In [final_project/static/index.js](./final_project/static/index.js) is the main JavaScript code. It uses ReactJS and BabelJS to render the webpage. When the user wants to execute a command, it sends the command to the server at `/execute`, which then executes it.

In [final_project/views.py](./final_project/views.py) is the server side code, it handles the requests from the client side, and executes the commands. It only contains 2 custom functions: `execute` and `command_history`. `execute` is the function that executes the command in a shell, using `subprocess`, and `command_history` is a function that allows you to get the command history.

In [final_project/static/styles.css](./final_project/static/styles.css) is the CSS code. It contains the styles for the webpage. It uses a black background, white text, and Source Code Pro as the font to give the complete look of the terminal.

# API

---

The api to execute commands and get the command history for a user.

> ### `POST` /execute
>
> Executes a command and returns the output. User must be authenticated.

Expected request (`multipart/form-data`):

```yaml
command:
    type: string
    required: true
```

Expected response (`application/json`):

```json
{
    "output": string,
    "success": boolean,
    "command_history": list<string>
}
```

Example response:

```json
{
    "output": "Hello, World!",
    "success": true,
    "command_history": ["echo Hello, World!"]
}
```

> ### `POST` /command_history
>
> Gets a user's command history. User must be authenticated.

Expected response (`application/json`):

```json
{
    "commands": list<string>
}
```

Example response:

```json
{
    "commands": ["echo Hello, World!"]
}
```

# Distinctiveness and Complexity

---

I believe this project satisfies the distinctiveness and complexity requirements of the project, because the idea of it has very little to do with previous projects, and because it utilizes `subprocess.run()`, ReactJS, and BabelJS. It has two Django models, one for an executed command, and one for a user.
