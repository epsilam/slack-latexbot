# slack-latexbot
A project that uses the `slack-machine` package and the Slack Developer Kit for Python to provide a customizable LaTeX-rendering Slack bot.

## Quickstart
Install this project's dependencies with

`pip install slack-machine`

`pip install slackclient`

In `local-settings.py`, set the variable `SLACK_API_TOKEN` to the API token given to you by Slack in your bot's configuration.

The bot can be started by entering `slack-machine` into your shell.


## Alternative installation using Python virtual environments (highly recommended)
After you `git clone` this repo, go into the root directory with `cd slack-latexbot` and then locally install the dependencies with

`pipenv install slack-machine`

`pipenv install slackclient`

In `local-settings.py`, set the variable `SLACK_API_TOKEN` to the API token given to you by Slack in your bot's configuration.

The bot can be started by entering `pipenv run slack-machine` into your shell while you are in the project's root directory.

## Using the bot in Slack
Whenever a user begins their message with `=tex`, the rest of the message is interpreted as if it were put between the standard `\begin{document}` and `\end{document}` tags. For example, entering the message
```
=tex $\int_{-\infty}^{\infty} e^{-x^2} \mathrm dx = \sqrt{\pi}$
```
in any channel which the bot is a member of will cause the bot to respond with
![Rendered LaTeX image](docs/outfile.png?raw=true "PNG image rendered by bot")

The `=t` command is a shorthand command that interprets the message text as if it were all one equation. No delimiters are required when using `=t`. An example usage would be `=t 1\neq 2`. This command takes the user's message and wraps it between two $ signs and then interprets the resulting string in the same way the `=tex` command would.

## To-do
- Make an inline version of `render_latex()` that prints several images (one for each pair of math-mode delimiters). It should not return any text outside these delimiters. Triggered on detection of "=inline" or a similar command.
