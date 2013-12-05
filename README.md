# Table of Contents
1. Goals
2. Task/Idea List
3. Dev Notes
4. Changelog


## Goals
* Meta Goals
    * Basic UI widgets that can be reused.
    * Separation of concerns.
    * Multi-processing: simulation separate from UI.
* Game Goals
    * 2 teams on the field.
        * 1 player
        * 1 AI
    * Each team has one base and N number of ants.
    * "Energy" is the main resource.
    * Every N leaves brought in gives you E energy.
    * Every 1 ant carcass gives you aE energy.
    * Energy can be used to create new ants.
    * Energy can be used to create DNA.
    * User has no direct control over the ants. User only directly controls
      the queen.
    * Queen ants, represented by the base, produce ants on a button click.
    * The ant produced is determined by the current DNA makeup which is
      also determined by the player.
    * Producing an Ant costs N base amount + kD amount based on additional
      DNA changes.
    * Win condition: other teams have no energy and no ants.
* Game Physics/Rules
    * Ants can't climb over each other.
        * Ants perform a short-sighted A* pathing because that's how ants behave in real life.
    * Simple terrain generation: passable and impassible.
    * Simple visual background procedurally generated.



## Task/Idea List

Prioritized in descending order.

Key
* In process
- Not Started or on hold.

- User Interface
    * Update views to allow nesting and setup a View/Controller relationship
      between the UI and the game sim (separation of concerns).
    * UI elements need to have the ability to convert a screen coordinate to a
      UI equivalent element, and also determine if the collision happened inside
      of them.
    * UI elements need to receive pygame events, and respond back to a controller
      with messages/events when something significant was clicked.
    - If resolution changes are allowed, allow preservation of aspect ratio and/or
      auto scaling.
    - Correct aspect ratio when world completely zoomed out.
    - Add scrolling minimap on and off.
    - Make something like surface effects that any display port can use.
- Ant Entity
    - Adjust leaf carrying position from back to the mouth.
    - Add collision detection so that entities can not run over each other.
- Multi-Process, Sim and Render Thread
- Saving settings...
    - Option: JSON, csv, ini... lots of choices. I'd prefer JSON in general only
      for the reason that JSON can preserve numbers and numbers distinct from
      strings so our in game code won't need to convert numbers.
- Ant-god controls:
    - Hostility level
    - Friendly index
    - Helpful level
    - Health minded ants or self sacrifice?
    - Expansionn oriented or homebodies?
    - Conversion or kill?
- Food as economy:
    - feed existing ants
    - new ants
    - evolutionary advancements
    - New food types
- Evolutionary advancements
    - vision increase (see food and enemies better)
    - conversion capability
    - Different Ant types
    - The Swarm
- Game World
    - Procedural world generation.



## Dev Notes

### Third party dependencies
Dependencies are managed by [pip](http://www.pip-installer.org/en/latest/index.html)
and are stored in the `requirements.txt` file. To install dependencies on a
new system, do:

    pip install -r requirements.txt

### Testing
To run the tests with [nose](http://nose.readthedocs.org/en/latest/index.html),
use the following command from the main directory.

    nosetests -v test/*.py



## Changelog

It's difficult to map git to a traditional changelog. Logging entries should
be stored with the commit:

    # short entries
    git commit -m "My log entry."

    # long entries...
    git commit
    # ...and use vi or whatnot to enter the log entry.

A quick way to generate a changelog like format to standard out:

    git log --oneline --decorate







