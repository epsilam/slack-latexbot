# slack-latexbot
A project that uses the [slack-machine](https://slack-machine.readthedocs.io/) package and the [Slack Developer Kit for Python](https://slackapi.github.io/python-slackclient/) to provide a customizable LaTeX-rendering Slack bot.

## Quickstart
Install this project's dependencies with

`pip install slack-machine`

`pip install slackclient`

Also, make sure you have the `pdflatex` and `convert` commands available. `pdflatex` typically comes with any standard LaTeX distribution, and `convert` comes pre-installed in most Linux distros.

In `local-settings.py`, set the variable `SLACK_API_TOKEN` to the API token given to you by Slack in your bot's configuration.

The bot can be started by entering `slack-machine` into your shell.

## Alternative installation using Python virtual environments (highly recommended)
After you clone this repository, go into the repository's root directory with `cd slack-latexbot` and set the virtual environment's python version to at least Python 3.6 (`slack-machine` requires Python 3 and won't play nice with Python 2) and install the dependencies using the following commands:

`pipenv --python 3.6`

`pipenv install slack-machine`

`pipenv install slackclient`

Also, make sure you have the `pdflatex` and `convert` commands available. `pdflatex` typically comes with any standard LaTeX distribution, and `convert` comes pre-installed in most Linux distros.

In `local-settings.py`, set the variable `SLACK_API_TOKEN` to the API token given to you by Slack in your bot's configuration.

The bot can be started by entering `pipenv run slack-machine` into your shell while you are in the project's root directory.

## Running the bot as a background process

These instructions apply to GNU/Linux-based operating systems.

If you want the bot to keep running after you exit your shell or log out, you can use GNU Screen. If you have Screen installed, then `cd` into your local copy of this repository and run `screen`. Then dismiss the message that comes up by pressing space or enter. Now, start the bot with `slack-machine` or `pipenv run slack-machine` depending on if you used pipenv to install the dependencies or not, and then press `Ctrl`+`a`, and `d` to detach the screen instance. If you wish to kill all instances of the bot, you may do so with `killall slack-machine`.

If you wish to start a detached Screen instance with the bot automatically, simply enter `screen -dm slack-machine` or `screen -dm pipenv run slack-machine`. To re-attach to the Screen instance (e.g., if you want to view some output produced by the bot), enter `screen -r`.

## Using the bot in Slack
Whenever a user begins their message with `=tex`, the rest of the message is interpreted as if it were put between the standard `\begin{document}` and `\end{document}` tags. For example, entering the message
```
=tex $\int_{-\infty}^{\infty} e^{-x^2} \mathrm dx = \sqrt{\pi}$
```
in any channel which the bot is a member of (including DMs) will cause the bot to respond with the image below.

![Rendered LaTeX image](docs/outfile.png?raw=true "PNG image rendered by bot")

The `=t` command is a shorthand command that interprets the message text as if it were all one equation. No delimiters are required when using `=t`. An example usage would be `=t 1\neq 2`. This command takes the user's message and wraps it between two $ signs and then interprets the resulting string in the same way the `=tex` command would.

The `=help` command will cause the bot to send a help message with information about all of the available commands.

## To-do
- Allow users to import custom packages (e.g., by entering `=tex{packagename} <message>`)
- Remove dependency on slack-machine and rewrite using only SlackClient
- Send 'typing...' indicator when a request to convert LaTeX is received, so that users can know that their message was received and is being processed.
