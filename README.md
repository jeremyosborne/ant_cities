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

- Entities
    * Data types and components
        * Refactor attr "current" into "val"
            * On "facing" and "heading" and in tests.
        * Combine velocityengine and velocity together. It's more complex
          keeping these things separate than just combining them. Things that
          should just have a constant velocity (bullets, sharks with lazers,
          small children with magnifying glasses) should just not augment
          the engine component of velocity. Outside forces (gravity, etc.)
          should apply additional force to our entities through separate
          means.
    * Ants
        * Ants are always moving and should manage their velocity engine and
          movement in the ant process, not the brain process.
          In particular move the chunk in the ant brains to the ant entity.
          UNLESS the brains should make a decision about the course or the
          speed.
    * Destination component.
        * Destination component has some niceties to handle entities and places
          in the world problematically.
- Spatial Index:
    - Keep the seeding of the expected index, but allow dynamic creation of cells
    outside of the world area if/when an entity travels outside the boundaries.
    - Add a togglable warning mechanism when entities travel outside of the
    boundaries.
- User Interface
    - Separate visual UI from logic simulation. Next step on path to multiprocess
      capable game (UI in one process, game in another).
        - Views should have: dirty rects and view entities (for tracking
        objects that are viewable).
    - Views should implement a View/Controller relationship between the UI and the
      game sim (separation of concerns, future availability of multi-core
      support).
    - Allow preservation of aspect ratio and auto scaling.
- Ant Entity
    - Adjust leaf carrying position from back to the mouth.
    - Add collision detection so that entities can not run over each other.
- Multi-Process, Sim and Render Thread
- Saving settings...
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

    nosetests -c nose.ini



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







