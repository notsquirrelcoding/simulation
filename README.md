# Simulation

## Things to consider
- ~~The probability that someone will infect someone else and vice versa~~
- ~~Individual groups of people~~
- ~~How people will actually infect one another~~
- ~~How multiple groups will be managed asynchronously~~
- Options for starting the simulation

## Things to consider when making a group
- ~~Population~~
- ~~How resistant/contagious units are~~
- How long it takes for someone to recover/die
- How contagious a person is when they are in the state of recovering or something
- Probability that someone will die
- How the units will be connected (will connections be random?)
- How do the number of dead people affect the simulation
- **Interaction between groups**

## Todo
-  put all of the files in a folder. project structured very badly.
- Also refactor code by putting specific functionalities into their own functons
- Fix the bug where either all units in a group die or everyone is healthy. There is literally no in-between.
- Add an ID attribute to each unit to avoid naming collisions

## Changes
- Dead units now get their vertices deleted
- Added `utils.py`
- Units now generate without having an edge connecting themselves to themselves

## Known bugs
- Sometimes the numer of infected units is greater than the actual living population.