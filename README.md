
# Table of Contents
1. Task/Idea List
2. Changelog



## Task/Idea List

Prioritized in descending order.

Key
* In process
- Not Started or on hold.

- User Interface
    * Create control panel class
    - Add scrolling minimap on and off
    - experiment with full screen class
    - Enhance render code to use the spatial index.  This will speed things up
      considerably in the lower zoom levels.
    - If resolution changes are allowed, allow preservation of aspect ratio and/or
      auto scaling.
    - Cleanup mini-map like World_Viewport (version .15)
    - Add mini map scrolling back into the game.
    - Make something like surface effects that any display port can use.
- Ant Entity
    - Maybe add an ant destroy method that will allow ants to clean up their things,
      like spatial index or other references.
    - Fix ants going in circles next to a leaf.
    - Adjust leaf carrying position from back to the mouth.
    - Add collision detection so that entities can not run over each other.
    - Fix ant eating to be time based (like ant hunger.)
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




## Changelog

Version guesstimated with: git rev-list --count HEAD


Version 71 10/25/2013

- Started a bit of cleanup in the spatial_engine. Added an assert to watch
  for accidental double insertions into the spatial index. Asserts are
  removed when code is run in optimized mode so we don't have to delete them
  manually or during an explicit build process.

Version 70 10/25/2013

- Changed History.txt into README.md, since that's more of what it is. Changed
  the text formatting a tiny bit to be [markdown](http://github.github.com/github-flavored-markdown/) friendly.

Version 69 10/24/2013

- Moved previous ui_elements.py contents to ui.* files to ease multiple coders
  working on the same files.

Version 68 10/24/2013

- Moved entities to their own folder. For the sake of working around some Python
  import weirdness, assumed practice is to always:

        import entities.ant

  or:

        from entities.ant import Ant

  Not recommended, the simple:

        # both of these, while potentially valid, can cause module reload
        # and caching problems.
        import ant
        from ant import Ant

- Removed some extraneous module imports.

Version 67 10/24/2013

- Remove game3.py.

Version 65 10/24/2013

-  Modified spatial_engine's spatial_index to have padding.  Units can go off the screen
   when turning.
-  Added tracking button on the view unit info box.  By default tracking is off.  It's
   a crappy icon.

Version 64 (.33)  10/24/2013

-  Changed find_at_point to return the closest entity rather than the first entity
   found inside the cell.
-  Added more stuff to the view unit info box.

Version .32  10/23/2013
-  Added more functionality to the view unit info box.
-  Jeremy cleaned up the spatial_engine code.

Version .31  10/21/2013

-  Saw that ants typically cluster in the middle.  Adjusted how often they change direction.
   this helps a little bit.
-  Observed that on rare occasions, some ants would go around in circles next to a leaf.  I
   think this was due to me not allowing the ant to go below the speed of 5.  Adjusted lowest
   speed to 1.  After testing this did not resolve the problem.  I saw this months ago.
-  Started work on View_Unit_Info_Box in ui_elements.

Version .30  10/21/2013

-  Fixed bug that prevented the hunger bar from being rendered when at was roaming.

Version .29  10/21/2013

-  The game_world is now spatially indexed and performance for the sim process is way up.
   Most processing power now goes to rendering.  spatial_engine holds the new code.

Version .28  10/19/2013

-  Added the following key commands:
	tab - (Toggle) locks/unlocks cursor to screen.  Easy to scroll around now.
	esc - Exits the progra,
-  Rewrote ui_elements.World_Viewport.update_viewport_center to do valid input checking.
   this eliminated the need for the four methods staring with add_to_viewport_(whatever)
   and makes it easy to call from any other method that needs to change the view.  This
   change was part of being able to click the minimap to change view.
-  You can now click and hold and move on the minimap and it will update as the mouse moves.
   While the mouse button is down, all user input except for mouse location for the map scroll
   is exclusive to the minimap.

Version .27  10/19/2013

-  Clicking on the minimap now re-centers the game view.  Still need to add edge map detection
   and click and hold map movement on the minimap.
-  After thinking through what it would mean to do a click and drag/hold action, and how the
   current game loop doesn't support it, I reworked game loop code such that it's now an object
   and separate from the main user input loop.  Why is this needed?  Imagine dragging an item from
   a control panel to the world viewport.  You would want to negate the main user input code and
   stay inside the code managing the dragging, but you still want the simulation (game loop) to be
   executed.  So, now you can call the game loop from anywhere now.

Version .26  10/17/2013

-  Added rudimentary routing of mouse click events based on viewports.  You can now click on
   a viewport and see the description in the console output.

Version .25  8/30/2013

-  New zooming functionality finished.  Skipped implementing aspect ratio correction
   for the world view at the final zoomed out position.  Since it's mostly a problem
   for oblong worlds, not a priority now.  So:

   1.  Zoom levels are calculated at run time based on the world size.
   2.  Images are scaled to zoom level 5, then turn into squares.
   3.  Since the surface is screen size and not world size, memory consumption
       is fine.

Version .244 8/29/2013

-  Continuing rewrite.  New zooming method implemented.  Will be adding maintaining
   the aspect ratio and fixing a bug that seems to be cutting off the extreme left
   edge when zooming out.

Version .243 8/28/2013

-  Rewriting entity rendering in world viewport.

Version .242 8/28/2013

-  Added code to calculate the number and dimensions of zoom levels based on screen size
   and world size.

Version .241 8/27/2013

-Working on zooming.

Version .24 8/26/2013

-  Starting on new world viewport design to support new zoom methods and proper
   aspect ratios.

Version .23 8/26/2013

-  Modified minimap to keep aspect ratio of the world.  Did this in preparation of
   doing the same for the game viewport.

Version .22 8/25/2013

-  Done playing with hardware acceleration. It just doesn't work.  In the experiment
   folder, have determined the number of entities that can be rendered to the screen
   in a timely manner.
-  This commit represents the last time zooming is based on a digital zoom and cut
   of a single surface.  Will begin developing zoom based on rendering to the screen
   surface scaled objects.

Version .21 7/9/2013
-  Just playing around with hardware acceleration.  It appears that this program
   is not invoking hardware acceleration and that's the reason I thing the program
   is slow when rendering the whole world to the viewable screen.

Version .20 7/8/2013
-  Added border around minimap to help with implementation of movement based on
   interaction with the minimap.  I didn't want the minimap to overlap with
   scrolling around the map.

Version .19 7/7.2013
-  Added display box in the minimap.

Version .18 7/6/2013
-  More realistic motion added.

Version .17 7/6/2013
-  gameobjects removed; pymunk now used for 2d vector work.

Version .16 6/29/2013
-  FPS display is now a viewport inside of ui-elements.  It's also the first
   time I used colorkey.  This allowed me to pick the text on the screen
   with a transparent background.

Version .15 6/28/2013
-  Can now resize the game world view on the fly.  That's cool.  To make the
   change, just update the width or height.  New code added in ui_elements
   World_Viewport are setters that override those in Viewport.
-  Changed World_Viewport to no longer look at global variables.

Version .14 6/27/2013
- Fixed ant hunger to be time based (was based on time when rendered, meaning
  that ant consumed a set amount of food when the screen was rendered.

Version .13 6/25/2013
- Gameworld now appears to be self contained inside the world object.  All world init
  items are now inside the init of the world class.
- game module now cleaner.

Version .12 6/25/2013  Rewriting or re-organizing the code.
- Removed all statemachine and entities references to spiders.
- Started to move world init items into the world class.  I want the world
  to be completely self contained so I can play with python multiprocessing
  at a later date.


Version .11 6/20/2013

-Added class methods to viewport.

Version .10 6/19/2013

- General fixes and cleanup.
- Game_world class moved into it's own file.

Version .09 6/18/2013

- Screens now render with the Viewport Class render_viewports method  (That was
  Single functional call to render all viewports to single surface on the task
  list.)  Breaks the animated scrolling action of the minimap entrance and exit
  from the screen.


Version .08 6/16/2013

 - Added list data structure for managing viewports.
 - new experiments directory.

Version .07 6/15/2013

- Working on viewport class management code.

Version .06 6/15/2013

-  Bug Fixes.
-  Added comments in the area where the viewport class management code might be.

Version .05 6/14/2013

-  Changed Screen_Entity class name to Viewport
-  Made Viewport inherit from surface rather than being a general object (Jeremy suggestion.)  This begins us thinking of viewport as an extension to pygame.
-  Moved World Viewport out the the viewport module and into the ui_elements model.  The world viewport is too specific to this game to be general.
-  A little more code cleanup.

Version .04 6/13/2013

- Deleted old code segments no longer needed and copied to old-code.txt for reference if needed.
- Doing checkin now because I'm going to workout checking the Screen_Entity class names to Viewport.


Version .03 6/12/2013

- Changed top, left variable names to x_right and y_down.  I am less confused and feel smart again.
- Implemented mini map scroll onto the screen (key press m)
- Implemented mini map scrool off the screen (key press n

Version .02 6/11/2013

- Fixed minimap issue where right side was being cut off.  This was because I wasn't converting the numbers to calculate the scale to float.

Version .01 6/11/2013

Current Implemented Features.

1.  Strategic Zoom
2.  Panning
3.  Mini Map
4.  Generalized classes for windows/screens







