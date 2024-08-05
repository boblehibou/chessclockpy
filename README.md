# Chess Clock

A simple, fullscreen, themable, modular, command line configured chess clock for PC, written in Python.

Although there is a multitude of chess clock applications for Android, PCs have to mostly rely on either web implementations or projects that are old or difficult to customise (single-file-blob-type projects). I am certain there must be brilliant equivalent or better implementations than this one out there; I simply had not found them by the time I started this small project.

This little project offers a functional chess clock that can be a starting point for building your ideal software clock. Configuration, logic, user interface and themes are all kept as separate as possible, so that it is easy enough to improve one aspect without having to know much about the inner workings of the other parts.

For now, development will not focus on adding functionalities but rather making it easy for users to customise the clock or to add their own functionalities to it.



# TLDR. How do I use this thing ?

## From source

The current entry point for the program is the `launch.py` file. However, if you want to take care of dependencies and run the code "just to get a feel of what it looks like", you can run `$ make run` and it will run the program with the default configuration.

## From a PyInstaller binary

A provided makefile target can turn the program into a single executable. To do that, simply run `$ make bin`.

## Configuration

The clock is configured using command line options. To see a list of them, pass the `-h` option to the program.

## Controls and Actions

- LCTRL : press the left button of the clock
- RCTRL : press the right button of the clock
- P : add 15 seconds to the timer of the player on the left
- Q : add 15 seconds to the timer of the player on the right
- SPACE : pause/resume countdown
- R : reset the clock to its starting state
- Z : (when paused) swap sides of the clock; useful in cases such as when moving the clock to the other side of the board



# Suitability

## Use this project if you ...

- Are playing with friends and want to turn your computer into a fully customisable chess clock.
- Want to contribute to a fun and somewhat useful (although quite niche) beginner level open source project.

## Do NOT use this project if you ...

- Are playing professionally and want a clock that will be accurate and regular to the nanosecond. The OS and Python simply won't allow it. If this is your case, I highly recommend using a good hardware clock, as advised by your chess federation.
- Want to use this project as a base for your next closed-source distribution. Sorry, you can't do that, as this code has been GPL-ed.



# For developers


## How do I ... ?

### Create a new theme for the clock

1. Subclass `chessclock.theme.Theme`.
2. Place the file containing the subclass definition in `chessclock/themes/extensions`.
3. Import the subclass in `chessclock/themes/extensions/__init__.py`.
4. The system should detect the new theme on startup. Use the appropriate command line option to load it.

The customisation options will grow in number and granularity as time goes on and the `Theme` class grows.

### Improve the clock logic

To change the clock logic, one should subclass `Interface` or `DefaultInterface` and pass an instance of the subclass to the constructor of `UI`.

Alternatively, in case you find a bug in the default core, you are welcome and encouraged to create an issue or a pull request.


## Issues and work in progress

### "I can see Fischer time controls but where on earth is Bronstein ?"

In your next pull request, perhaps? ;)

### "The project structure is a mess!"

I wish to make this code easy to grasp, improve and extend, in as few lines as possible but as many as required. Feedback on the matter, no matter how blunt, if constructive, is welcome and will receive some attention, as long as I am maintaining the project.
