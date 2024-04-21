# Turtle Invaders

```
      # # # # #  # #                             # #  # # # # #
      #   # #                                           # #   #
      # # #                     #####                     # # #
      # #                    ## # # # ##                      #
      #                     # #  ###  # #                     #
      # #                  #  ## # # ##   #                  # #
      # # #              # # #   # #   # # #              # # #
      #   # #           # #     TURTLE    # #           # #   #
      # # # # # # # # # # #    INVADERS   # # # # # # # # # # #
      #   #   #  # #  # # # #   # # #   # # # #  # #  #   #   #
      # # # #            # ##### # # ##### #            # # # #
      # # #               #     #####    #               # # #
      #                    # # ##   ## # #                    #
      #                      #### # ####                      #
      # # #                     #   #                     # # #
      # #   #                    # #                    #   # #
      # # # # #  ###  ##  #  #   ###   #  #  ##  ###  # # # # #
      # #        # #             # #             # #        # #
      # #        # #             # #             # #        # #
      # #         #               #               #         # #
      # #         #               #               #         # #
```

## Project in progress.

A class to create a Space Invaders clone. Completed for Professional Portfolio Project:
Assignment 14: Angela Yu 100 Days of Code -- "GUI Automation: Space Invaders".

A huge goal of this project is to create a responsive design. As many values as possible
are based on the user's screen size rather than being hard-coded. Some work still to
be done on this issue, but the game should work fairly well on computers of varying
resolutions/dimensions.

Aliens are turtles of course, because that's why.

### Resources Utilized

- [Python](https://www.python.org/)

- [PythonTurtle Website](https://pythonturtle.org/)

- [PythonTurtle GitHub](https://github.com/PythonTurtle/PythonTurtle)

- [PythonTurtle Documentation](https://docs.python.org/3/library/turtle.html)

- [screeninfo](https://github.com/rr-/screeninfo)

_MIT License: Copyright (c) 2024- Andrew Blais_

---

### Future Updates

#### Hugely important next step is to separate Invaders/Player/Screen/Shields methods into separate modules!!

- Figure out anomalous cases where invaders march straight down, e.g. happens
  first time invaders hit right wall if march initializes to the right.

- Get setheading() for all objects aligned so stretch_len and stretch_wid mean
  the same thing.

- Work on algo to see direct relation of tracer to seconds.

- Change player shape from square to triangle & make trig algo for collision
  with player triangle. Use `print(self.player.get_shapepoly())` to see shape
  boundaries -- returns: ((40.0, -11.54), (0.0, 23.1), (-40.0, -11.54)).

- Add functionality for subsequent rounds.

- Remedy names/concerns regarding game restart -- come up with better cases for
  while loop, diversify functionality

- Add code for bonus lives at 1000s.

- Use get_shapepoly(), shapesize() for development analysis.

- For development, to identify invader indices easily:
  invader.write(i, align="center", font=("Source Sans 3 Black", 24, "italic"))

- Methods for future development ref: self.scr.window_width(), self.scr.window_height()

- Display directions and indications of saucer bonuses on initial greet screen

- Subtract/add half vertical shape length to get 'tip' of missile for more precise
  collision detection.

---

### Documentation:

```requirements
screeninfo>=0.8.1
```

_Docstrings for `main.py`:

```
Help on class TurtleInvaders in module __main__:

class TurtleInvaders(builtins.object)
 |  A class to manage the overall game logic and state for Turtle Invaders.
 |
 |  :ivar game_is_paused (bool): Indicates if the game is currently paused.
 |  :ivar game_is_on (bool): Indicates if the game is active.
 |  :ivar game_lives_object (Turtle): Turtle object to display remaining lives.
 |  :ivar game_round_current (int): Tracks the current round of the game.
 |  :ivar game_lives_left (int): Represents the number of lives left.
 |  :ivar game_score_object (Turtle): Turtle object to display current score.
 |  :ivar game_score_current (int): Tracks the current score.
 |  :ivar game_tracer_val (int): Controls the screen update rate for animations.
 |  :ivar invaders_y_limit (int): Sets the upper y-axis limit for invaders' initial position.
 |  :ivar invaders_vert_compress (int): Compresses invader rows closer vertically.
 |  :ivar invaders_all (list) of Turtle: Contains all invader Turtle objects.
 |  :ivar invader_formation_div_x (int): Divides the screen width for invader formation.
 |  :ivar invader_formation_div_y (int): Divides the screen height for invader formation.
 |  :ivar invader_gutter_factor (float): Represents left-right gutter size factor; smaller values result in larger gutters.
 |  :ivar invader_pos_all (list) of tuple: Stores calculated invader positions.
 |  :ivar invaders_main_march_speed (float): Controls the speed of invaders' movement.
 |  :ivar invaders_main_march_speed_increase (float): Increases the speed of invaders when direction changes.
 |  :ivar invader_vert_init (int): Initial vertical position adjustment for invaders.
 |  :ivar invader_vert_now (int): Current vertical position of invaders.
 |  :ivar lr_rl (bool): Indicates if invaders have changed direction.
 |  :ivar invader_bombs (list) of Turtle: Contains all active invader bomb Turtle objects.
 |  :ivar invader_bomb_speed (int): Controls the speed of invader bombs.
 |  :ivar invader_has_fired (bool): Tracks if an invader has fired a bomb.
 |  :ivar invader_bomb_barrage_begun (bool): Indicates if the invader bomb barrage has started.
 |  :ivar invader_bomb_low_init (int): Initial lowest frequency of invader bombs.
 |  :ivar invader_bomb_high_init (int): Initial highest frequency of invader bombs.
 |  :ivar invader_bomb_low (int): Current lowest frequency of invader bombs.
 |  :ivar invader_bomb_high (int): Current highest frequency of invader bombs.
 |  :ivar invader_bomb_freq (tuple): Stores the current frequency range of invader bombs.
 |  :ivar player (Turtle): Turtle object representing the player.
 |  :ivar player_start_x (float): Initial x-coordinate of the player.
 |  :ivar player_start_y (float): Initial y-coordinate of the player.
 |  :ivar player_missiles_all (list) of Turtle: Contains all active player missile Turtle objects.
 |  :ivar player_has_fired (bool): Tracks if the player has fired a missile.
 |  :ivar player_reload_time_init (int): Sets initial reload time for player firing.
 |  :ivar player_reload_time (int): Current reload time for player firing.
 |  :ivar player_missile_speed (int): Controls the speed of player's missiles.
 |  :ivar saucer (Turtle): Turtle object representing the flying saucer.
 |  :ivar saucer_x (float): Current x-coordinate of the saucer.
 |  :ivar saucer_y (float): Current y-coordinate of the saucer.
 |  :ivar saucer_shape_current (str): Represents the current shape of the saucer.
 |  :ivar saucer_flyby_speed (int): Controls the speed of the saucer's flyby.
 |  :ivar saucer_freq_tracker (float): Tracks the time until next saucer appearance.
 |  :ivar saucer_freq_low (int): Sets the minimum delay for saucer appearances.
 |  :ivar saucer_freq_high (int): Sets the maximum delay for saucer appearances.
 |  :ivar saucer_freq (int): Sets the current delay for the next saucer appearance.
 |  :ivar scr (Screen): Turtle Screen object for the game display.
 |  :ivar scr_stretch_x (float): Sets the horizontal stretch factor of the game screen.
 |  :ivar scr_stretch_y (float): Sets the vertical stretch factor of the game screen.
 |  :ivar scr_w (int): Calculated width of the game screen.
 |  :ivar scr_h (int): Calculated height of the game screen.
 |  :ivar scr_w_half (float): Half the width of the game screen.
 |  :ivar scr_h_half (float): Half the height of the game screen.
 |  :ivar shield_num (int): Sets the number of shields.
 |  :ivar shield_blocks_num (int): Sets the number of blocks per shield.
 |  :ivar shields_all (list) of Turtle: Contains all shield Turtle objects.
 |  :ivar shields_y_boundary (float): Determines the y-coordinate boundary for shields.
 |
 |  Methods defined here:
 |
 |  __init__(self)
 |      Initializes the game, setting up the screen, player, invaders, shields,
 |       and other game elements.
 |
 |  game_begin_invasion(self)
 |      Starts the main game loop. Sets up the screen, initializes the game, and
 |       continues the loop until the game is either paused, ended, or exited.
 |
 |  game_listeners(self)
 |      Sets up the key listeners for the game, binding specific game actions to
 |       keyboard keys. This allows player interaction using the keyboard.
 |
 |      :return: None
 |
 |  game_lives_update(self)
 |      Updates the display of player lives. Each life is represented as a square
 |       block in the game's UI. If the lives display object does not exist, it
 |       creates one, otherwise it updates the existing display.
 |
 |  game_pause_toggle(self)
 |      Toggles the pause state of the game. This method is bound to a keypress and
 |       can be used to pause/resume the game.
 |
 |      Example:
 |          game_instance.game_pause_toggle()  # This would toggle the pause state
 |                                                based on the current state.
 |
 |      :return: None
 |
 |  game_quit(self)
 |      Quits the game immediately. This method is bound to a keypress allowing the
 |      player to exit the game.
 |
 |  game_restart(self)
 |      Clears the game screen and resets all game elements to start a new game.
 |       This method is invoked typically after a game over or when the player
 |       chooses to restart the game.
 |
 |  game_score_update(self)
 |      Updates the game score display. If the score display object does not exist,
 |       it creates one, otherwise it updates the existing score display.
 |
 |  game_setup(self)
 |      Initializes all components of the game, setting up the game board, player,
 |       invaders, saucer, shields, and initial game settings.
 |
 |  invader_bomb_deploy(self, bomb_element)
 |      Deploys a bomb from an invader's position, initializing and configuring a
 |       new bomb Turtle object. This method is typically called when an invader is
 |       eligible to drop a bomb based on game logic defined in `invaders_main_march`.
 |
 |      :param bomb_element: The invader Turtle object from which the bomb is deployed.
 |      :type bomb_element: Turtle
 |      :return: None
 |
 |  invader_formation(self)
 |      Creates the initial formation of invaders based on pre-calculated positions.
 |
 |  invader_get_positions(self)
 |      Calculates and stores the starting positions for all invaders based on screen
 |       dimensions and configuration settings.
 |
 |  invader_has_fired_flag_reset(self)
 |      Resets the flag that an invader has fired, allowing another bomb to be deployed.
 |
 |  invaders_change_dir(self)
 |      Reverses the direction of invader movement when they reach the screen edge.
 |      The movement speed also slightly increases.
 |
 |  invaders_main(self)
 |      Manages the primary behavior of invaders during gameplay, including their
 |       movement across the screen, and interactions with player defenses and
 |       game boundaries.
 |
 |      Invaders move in formation and this method checks to restart the game if
 |       all invaders are destroyed or if they reach the shield boundary. It also
 |       handles directional changes when invaders reach screen edges.
 |
 |      :return: None
 |
 |  invaders_main_march(self)
 |      Manages the movement of all invaders on the screen, giving a 'living' effect
 |       with a slight random stretch. This method also triggers the deployment of
 |       bombs by invaders, starting with a random invader if no bombs have been
 |       deployed yet.
 |
 |      This method also updates the saucer frequency tracker based on the invader
 |       movement, affecting the timing of saucer appearances.
 |
 |      :return: None
 |
 |  invaders_main_march_bomb(self)
 |      Handles the movement and collision checking of bombs dropped by the invaders.
 |       This method moves each bomb downward, removes bombs that have left the screen,
 |       and checks for collisions with the player and shields.
 |
 |      If a bomb hits the player, the `player_destroyed` method is triggered. Bomb
 |       collisions with shields trigger damage to the shield.
 |
 |      :return: None
 |
 |  invaders_main_march_bomb_shields(self, bomb)
 |      Checks for and handles collisions between invader bombs and player shields.
 |       If a bomb hits a shield, the shield's integrity is reduced or the shield is
 |       removed if fully degraded.
 |
 |      :param bomb: The bomb to check for collisions with shields.
 |      :type bomb: Turtle
 |      :return: None
 |
 |  invaders_reverse(self)
 |      Handles the logic when invaders need to reverse direction due to hitting
 |       a screen edge or other trigger.
 |
 |  lr_rl_flag_reset(self)
 |      Resets the left-right flag indicating a recent reversal in invader direction,
 |       and adjusts the frequency range for dropping bombs. Use of `max` ensures the
 |       bomb drop frequency does not become too fast.
 |
 |  player_deploy(self)
 |      Deploys or repositions the player on the game screen.
 |      Initializes the player if not already created.
 |
 |  player_destroyed(self)
 |      Handles the event of the player being destroyed by an invader bomb.
 |      Decreases life count and resets the player's position.
 |
 |  player_fire_missile(self)
 |      Fires a missile from the player if not already fired.
 |      Sets a timer to reset the fire capability using `reset_player_has_fired_flag`.
 |
 |  player_left(self)
 |      Moves the player to the left if within the screen boundaries.
 |
 |  player_missile_path(self)
 |      Controls the movement and collision detection of missiles fired by the player.
 |       This method updates the position of each missile, checks for screen boundaries,
 |       and handles collisions with invaders, saucers, and shields.
 |
 |      Missiles are moved upwards from their current position, and checks are performed
 |       to remove missiles that exceed the game screen or hit a target. Collisions with
 |       different game elements like invaders or saucers affect the game score or player
 |       capabilities.
 |
 |      :return: None
 |
 |  player_missile_path_invader_collision(self, missile)
 |      Handles collisions between the player's missiles and invaders. When a collision
 |       is detected, the invader is removed from the game, the player's score is
 |       updated, and the missile is removed from play.
 |
 |      :param missile: The missile to check for collisions with invaders.
 |      :type missile: Turtle
 |      :return: None
 |
 |  player_missile_path_saucer_collision(self, missile)
 |      Handles collisions between the player's missiles and the saucer. A successful
 |       hit results in a significant increase in the player's score and triggers
 |       specific effects depending on the saucer's type. This method also handles the
 |       removal of the missile from play and updates the saucer's position.
 |
 |      :param missile: The missile to check for collisions with the saucer.
 |      :type missile: Turtle
 |      :return: None
 |
 |  player_missile_path_shields_collision(self, missile)
 |      Manages the interaction between player-fired missiles and the defensive shields.
 |       If a missile hits a shield, the shield's integrity is reduced, changing its
 |       color. If the shield's integrity is fully depleted, the shield is removed from
 |       the game.
 |
 |      :param missile: The missile to check for collisions with shields.
 |      :type missile: Turtle
 |      :return: None
 |
 |  player_reload_time_reset(self)
 |      Resets the player's missile firing reload time to the initial setting.
 |
 |  player_right(self)
 |      Moves the player to the right if within the screen boundaries.
 |
 |  reset_player_has_fired_flag(self)
 |      Resets the flag that prevents the player from firing multiple missiles at once.
 |
 |  saucer_create(self)
 |      Initializes the saucer that flies over the screen, providing bonus points
 |       when hit. The type of saucer and its effects on hit are randomized.
 |
 |  saucer_flyby(self)
 |      Manages the movement of the saucer across the screen. Resets its position
 |       and frequency of appearance after it passes.
 |
 |  screen_setup(self)
 |      Sets up the game screen using the dimensions of the primary monitor or defaults
 |       to hardcoded values in case of an error. This method attempts to dynamically
 |       determine the monitor resolution but will revert to defaults if any issues occur.
 |
 |      :raises Exception: Describes what kind of exceptions can be expected if monitor
 |               information cannot be retrieved.
 |      :return: None
 |
 |  shields_deploy(self)
 |      Creates defensive shields on the game screen. Each shield can degrade upon
 |       being hit by enemy fire, indicated by a gradual change in color until it
 |       disappears.
 |
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |
 |  __dict__
 |      dictionary for instance variables
 |
 |  __weakref__
 |      list of weak references to the object
```

__Docstrings for `modules/collisions.py`:_

```
# This module contains functions for detecting collisions between game elements.

Help on function is_collision_x_cond_met in module __main__:

is_collision_x_cond_met(obj, missile, space)
    Determines if a collision occurs along the x-axis within a specified buffer space.

    :param obj: The game object, typically an invader or shield.
    :type obj: Turtle
    :param missile: The projectile object, usually a player missile or invader bomb.
    :type missile: Turtle
    :param space: The buffer space around the object's x-coordinate.
    :type space: float
    :return: True if a collision is detected, False otherwise.
    :rtype: bool

Help on function is_collision_y_cond_met in module __main__:

is_collision_y_cond_met(obj, missile, space)
    Determines if a collision occurs along the y-axis within a specified buffer space.

    :param obj: The game object, typically an invader or shield.
    :type obj: Turtle
    :param missile: The projectile object, usually a player missile or invader bomb.
    :type missile: Turtle
    :param space: The buffer space around the object's y-coordinate.
    :type space: float
    :return: True if a collision is detected, False otherwise.
    :rtype: bool

Help on function are_collision_x_y_cond_met in module __main__:

are_collision_x_y_cond_met(obj, missile, space_x, space_y)
    Checks if a collision occurs within specified buffer spaces along both the x and y axes.

    :param obj: The game object involved in the collision, e.g., an invader or shield.
    :type obj: Turtle
    :param missile: The missile object that might be colliding with the obj.
    :type missile: Turtle
    :param space_x: The buffer space around the object's x-coordinate for collision detection.
    :type space_x: float
    :param space_y: The buffer space around the object's y-coordinate for collision detection.
    :type space_y: float
    :return: True if a collision is detected on both axes, False otherwise.
    :rtype: bool
```

__Docstrings for `config/colors.py`:_

```
This module defines color constants used throughout the game for easy theme
  management including variables/lists indicating:
  - Background color for the game screen:
  - Primary color for player elements:
  - Progressive damage stages for shields, represented by decreasing lightness:
  - Colors used for different invader types, which might change per game round:
    Maps invader positions to color indices, facilitating changes in invader
     color by game round:

Help on function invader_get_row_index in module __main__:

invader_get_row_index(number, game_round_current)
    Determines the color index for an invader based on its position and current game round.

    :param number: The position number of the invader in its formation.
    :type number: int
    :param game_round_current: The current round of the game, affecting color selection.
    :type game_round_current: int
    :return: An index to the TURTLE_COLORS list, cycling through colors as rounds advance.
    :rtype: int
```

---

## Created in completing an assignment for Angela Yu Course:

### **Day 94, Professional Portfolio Project [GUI Automation]**

#### **_Assignment 14: "Space Invaders"_**

Build the classic arcade game where you shoot down alien ships.

- _assignment
  for [Angela Yu 100 Days of Code](https://www.udemy.com/course/100-days-of-code/)_

### **Assignment instructions:**

Using Python Turtle, build the classic shoot 'em up game - space invaders game.

[Space Invaders Wikipedia Page](https://en.wikipedia.org/wiki/Space_Invaders)

Your space ship can move left and right and it can hit some alien ships. Every second the
aliens will move closer to your ship. Once the aliens touch your ship then it's game
over. There are usually some barriers between you and the aliens which offers you
defensive positions.

You can play the game here:

https://elgoog.im/space-invaders/

---

### My Submission:

My project is viewable here: https://github.com/andrewblais/turtleInvaders

---

### **Questions for this assignment**

#### _Reflection Time:_

**_Write down how you approached the project._**

After taking a close look at my previous turtle game projects like the Pong, BreakOut
and Frogger clones, as well as lessons about the subject from Angela Yu's course, I got
to work with the basics: outlining what aspects of the game I wanted to create and how
to separate them. This included figuring out functionality for the invaders objects,
player object, shields and flying saucer, as well as the scoreboard. The most simple and
direct way for me to proceed from there is to create a class and instantiate the Screen
object. Lots of hard work followed. This was by far the most challenging project for me
yet.

**_What was hard?_**

The most difficult aspect of this project was getting all the pieces of the game to work
together smoothly. There are so many dependencies, for instance the missiles might come
in contact with lots of different objects and I had to figure out how to create the
movement and order the collision conditional functions. Still lots of work to do to make
this more efficient, to be honest...

**_What was easy?_**

Creating a class and its methods -- this has become much more natural for me as the
course and Projects section have progressed. I'm getting a lot more comfortable with
OOP.

**_How might you improve for the next project?_**

Since the most glaring problem with the project as it stands is that the class is simply
too long, I should think about separating out concerns and methods into different modules
at a much earlier stage. It becomes more difficult once the class is built and there are
so many inter-dependencies. So I'd try have more classes and .py files going on from the
outset.

**_What was your biggest learning from today?_**

Game design wasn't the point of this project for me -- rather, I think what was most
educational was getting a grip on the inter-workings of all the different objects in the
application, and trying to make them work smoothly together and for the overall thing
to be as efficient as possible.

Memory management, in particular the `del` keyword, was a new concept that I picked up
during this project. Especially with all the missiles which are just temporary objects,
this was very important to consider and implement.

**_What would you do differently if you were to tackle this project again?_**

Trying not to get to fancy with the application until after the building-blocks are in
place. It's easy to get ahead of myself with creative ideas, but core-functionality and
logic are paramount.

What a challenging, helpful project. I did not expect to work quite so hard, and was
pleasantly surprised with how much I learned.