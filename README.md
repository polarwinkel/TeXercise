# TeXercise

An auto-revising/correcting Exercise-Server

## What is this

TeXercise is an Exercise-Server offering Fill-in Worksheets created in mdTeX - MarkDown enriched with TeX formulas.

Fill-in elements can be either boolean (True/False), string (short text answers) or numbers with formula-variables generated at random in a given range.

The creation of an exercise-sheet is extremely easy and it can be stored on your personal devices as simple text-files - on in the [TeXerBase Exercise Database](https://github.com/polarwinkel/TeXerBase).

## How can I install this

A small computer like a Raspberry Pi will do just fine. Clone this repository, install the dependencies, and run `app.py`. Then point your browser to the IP of the machine to port 5000 (default at the moment - will still change).

It is strongly advised to use encryption to access the TeXercise-Server to protect the admin-password and other data! You can i.e. use nginx as a reverse proxy with Let's Encrypt certificates.

### Dependencies

All dependencies can be installed on a debian-besed system with `apt install`, on other systems with pip:

- `python3`
- `python-flask`
- `python3-jinja2`
- `python3-yaml`
- `python3-markdown`
- `python3-flask-login`
- `python3-unidecode`

## TODO

Features that may still come:

- Tolerance adjustable for calculated questions (default at the moment: 10%)
- List of possible answers in string-questions

## Contribute

If your like this: Spread the word, and give this project a star!

Help is needed in documentation as well. This `README.md` for example could be much better and contain i.e. examples for sheets or more/better documentation.

If you want to make translations please let me know, I'm planning to make one myself to german some day.

You are very welcome to report any issues you find! If you have any suggestions, just let me know by sending an eMail or filing an issiue, we'll se what can be done.

You can also submit pull-requests if you like.
