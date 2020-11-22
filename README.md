# `wihparse`

Parser for HN's "Who is hiring" threads.


## Overview

On the first business day of every month, [Hacker News] has a "Who is hiring?" thread, e.g., [November 2020]. These threads have useful information, but reach quite a hefty size—819 posts for the aforemenetioned one—making them a bit challenging to handle manually. Various tools for browsing them already exist, but I've never found any particularly pleasant to use, so I made my own.

Thus `wihparse` came to be. It's a tool for parsing these threads and generating reports based on keywords. My use case is wanting every post mentioning "Python", for example.


## Setup

Note: These instructions assume a Unix-like OS, like macOS or Linux, with a POSIX-like shell.


### Requirements

You'll need the following:
- [Python 3.6+]
- [Poetry]
- [GNU Make]


### Installation

- `make install`


## Usage

Running `make` will show all available commands. Here's the current output:

```
help                          this help dialog
install                       set up project locally (requires Python 3.6+ and Poetry)
update                        update DB from API
report                        generate report from DB
hide                          hide specific post
export                        export report
all                           update and export
shell                         open Python REPL with application loaded
```

More details about various commands:

- `make install` runs `poetry install` to set up the project and make the other commands possible.
- `make update` accesses the HN thread via API and updates the local `posts.json` database.
- `make hide` marks posts as invisible. E.g., `make hide ids=8,14`.
- `make report` queries the local database and outputs results.
- `make export` stores the output of `make report` into `report.txt`.
- `make all` runs `make update` and `make export`, essentially refreshing the local database and report.
- `make shell` drops you into the program so you can do whatever you need to do that it doesn't support out of the box.

In reality, you'll probably mostly run `make all` and look at `report.txt`.


### Example Workflow

```
# ensure THREAD_ID in wihparse.py is the one you want
# ensure Python 3.6, Poetry, and GNU Make are present
$ make install          # install everything
$ make all              # run the whole process
$ less report.txt       # look at the report
# decide jobs with IDs 13 and 42 aren't interesting
$ make hide ids=13,42   # hide them
$ make export           # regenerate the report
$ less report.txt       # look at the report again
# rinse and repeat, occasionally running make all to update from API as well
```


## License

This project is released into the public domain via the [Unlicense].


## Contributing and Future

Unlike most of my projects, contributions are not explicitly encouraged, though they're not discouraged, either.

If there's enough interest, I might be open to turning this into an installable tool for easier use. However, I sincerely doubt that's the case, and I don't have the need for it myself, so this is it.

Big thanks to [John Mitchell] for the [reality check].


[Hacker News]:https://news.ycombinator.com/
[November 2020]: https://news.ycombinator.com/item?id=24969524
[Python 3.6+]: https://www.python.org/
[Poetry]: https://python-poetry.org/
[GNU Make]: https://www.gnu.org/software/make/
[Unlicense]: https://unlicense.org/
[John Mitchell]: https://www.johntellsall.com/
[reality check]: https://twitter.com/JohnTellsAll/status/1330231638878531587
