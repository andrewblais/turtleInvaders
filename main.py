# Main module for the Turtle Invaders game. This module initializes the game
#  environment, manages game events, and processes all game logic and interactions.

import random
from screeninfo import get_monitors
import sys
from turtle import Screen, Turtle

from config.colors import *
from modules.collisions import *


class TurtleInvaders:
    """
    A class to manage the overall game logic and state for Turtle Invaders.

    :ivar game_is_paused (bool): Indicates if the game is currently paused.
    :ivar game_is_on (bool): Indicates if the game is active.
    :ivar game_lives_object (Turtle): Turtle object to display remaining lives.
    :ivar game_round_current (int): Tracks the current round of the game.
    :ivar game_lives_left (int): Represents the number of lives left.
    :ivar game_score_object (Turtle): Turtle object to display current score.
    :ivar game_score_current (int): Tracks the current score.
    :ivar game_tracer_val (int): Controls the screen update rate for animations.
    :ivar invaders_y_limit (int): Sets the upper y-axis limit for invaders' initial position.
    :ivar invaders_vert_compress (int): Compresses invader rows closer vertically.
    :ivar invaders_all (list) of Turtle: Contains all invader Turtle objects.
    :ivar invader_formation_div_x (int): Divides the screen width for invader formation.
    :ivar invader_formation_div_y (int): Divides the screen height for invader formation.
    :ivar invader_gutter_factor (float): Represents left-right gutter size factor; smaller values result in larger gutters.
    :ivar invader_pos_all (list) of tuple: Stores calculated invader positions.
    :ivar invaders_main_march_speed (float): Controls the speed of invaders' movement.
    :ivar invaders_main_march_speed_increase (float): Increases the speed of invaders when direction changes.
    :ivar invader_vert_init (int): Initial vertical position adjustment for invaders.
    :ivar invader_vert_now (int): Current vertical position of invaders.
    :ivar lr_rl (bool): Indicates if invaders have changed direction.
    :ivar invader_bombs (list) of Turtle: Contains all active invader bomb Turtle objects.
    :ivar invader_bomb_speed (int): Controls the speed of invader bombs.
    :ivar invader_has_fired (bool): Tracks if an invader has fired a bomb.
    :ivar invader_bomb_barrage_begun (bool): Indicates if the invader bomb barrage has started.
    :ivar invader_bomb_low_init (int): Initial lowest frequency of invader bombs.
    :ivar invader_bomb_high_init (int): Initial highest frequency of invader bombs.
    :ivar invader_bomb_low (int): Current lowest frequency of invader bombs.
    :ivar invader_bomb_high (int): Current highest frequency of invader bombs.
    :ivar invader_bomb_freq (tuple): Stores the current frequency range of invader bombs.
    :ivar player (Turtle): Turtle object representing the player.
    :ivar player_start_x (float): Initial x-coordinate of the player.
    :ivar player_start_y (float): Initial y-coordinate of the player.
    :ivar player_missiles_all (list) of Turtle: Contains all active player missile Turtle objects.
    :ivar player_has_fired (bool): Tracks if the player has fired a missile.
    :ivar player_reload_time_init (int): Sets initial reload time for player firing.
    :ivar player_reload_time (int): Current reload time for player firing.
    :ivar player_missile_speed (int): Controls the speed of player's missiles.
    :ivar saucer (Turtle): Turtle object representing the flying saucer.
    :ivar saucer_x (float): Current x-coordinate of the saucer.
    :ivar saucer_y (float): Current y-coordinate of the saucer.
    :ivar saucer_shape_current (str): Represents the current shape of the saucer.
    :ivar saucer_flyby_speed (int): Controls the speed of the saucer's flyby.
    :ivar saucer_freq_tracker (float): Tracks the time until next saucer appearance.
    :ivar saucer_freq_low (int): Sets the minimum delay for saucer appearances.
    :ivar saucer_freq_high (int): Sets the maximum delay for saucer appearances.
    :ivar saucer_freq (int): Sets the current delay for the next saucer appearance.
    :ivar scr (Screen): Turtle Screen object for the game display.
    :ivar scr_stretch_x (float): Sets the horizontal stretch factor of the game screen.
    :ivar scr_stretch_y (float): Sets the vertical stretch factor of the game screen.
    :ivar scr_w (int): Calculated width of the game screen.
    :ivar scr_h (int): Calculated height of the game screen.
    :ivar scr_w_half (float): Half the width of the game screen.
    :ivar scr_h_half (float): Half the height of the game screen.
    :ivar shield_num (int): Sets the number of shields.
    :ivar shield_blocks_num (int): Sets the number of blocks per shield.
    :ivar shields_all (list) of Turtle: Contains all shield Turtle objects.
    :ivar shields_y_boundary (float): Determines the y-coordinate boundary for shields.
    """

    def __init__(self):
        """
        Initializes the game, setting up the screen, player, invaders, shields,
         and other game elements.
        """
        # Game General Attributes:
        self.game_is_paused = False
        self.game_is_on = True
        self.game_lives_object = None
        self.game_round_current = 1
        self.game_lives_left = 3
        self.game_score_object = None
        self.game_score_current = 0
        self.game_tracer_val = 20

        # Invader Attributes:
        self.invaders_y_limit = 50  # Higher val shifts formation up along y-axis
        self.invaders_vert_compress = 3  # Higher val to compress rows along y-axis
        self.invaders_all = []
        self.invader_formation_div_x = 6
        self.invader_formation_div_y = 4
        self.invader_gutter_factor = .7  # Smaller val = bigger L-R gutters
        self.invader_pos_all = []
        self.invaders_main_march_speed = 1
        self.invaders_main_march_speed_increase = .5
        self.invader_vert_init = 10
        self.invader_vert_now = self.invader_vert_init
        self.lr_rl = False  # Flag indicating invaders have changed direction
        self.invader_bombs = []
        self.invader_bomb_speed = 1
        self.invader_has_fired = False
        self.invader_bomb_barrage_begun = False
        self.invader_bomb_low_init = 500  # ~ 1/2 second (divide by 1000)
        self.invader_bomb_high_init = 5000  # ~5 seconds (divide by 1000)
        self.invader_bomb_low = self.invader_bomb_low_init
        self.invader_bomb_high = self.invader_bomb_high_init
        self.invader_bomb_freq = (self.invader_bomb_low, self.invader_bomb_high)

        # Player Attributes:
        self.player = None
        self.player_start_x = None
        self.player_start_y = None
        self.player_missiles_all = []
        self.player_has_fired = False
        self.player_reload_time_init = 1000  # 1 second
        self.player_reload_time = self.player_reload_time_init
        self.player_missile_speed = 15

        # Saucer Attributes:
        self.saucer = None
        self.saucer_x = None
        self.saucer_y = None
        self.saucer_shape_current = None
        self.saucer_flyby_speed = 5
        self.saucer_freq_tracker = 0
        self.saucer_freq_low = 10  # ~8-second SAUCER delay
        self.saucer_freq_high = 22  # ~20-second SAUCER delay
        self.saucer_freq = random.randint(self.saucer_freq_low, self.saucer_freq_high)

        # Screen Attributes:
        self.scr = None
        self.scr_stretch_x = .65
        self.scr_stretch_y = .8
        self.scr_w = None
        self.scr_h = None
        self.scr_w_half = None
        self.scr_h_half = None

        # Shields Attributes:
        self.shield_num = 3
        self.shield_blocks_num = 4
        self.shields_all = []
        self.shields_y_boundary = None

    # SCREEN METHODS (separation into separate module in the works):
    def screen_setup(self):
        """
        Sets up the game screen using the dimensions of the primary monitor or defaults
         to hardcoded values in case of an error. This method attempts to dynamically
         determine the monitor resolution but will revert to defaults if any issues occur.

        :raises Exception: Describes what kind of exceptions can be expected if monitor
                 information cannot be retrieved.
        :return: None
        """
        self.scr = Screen()
        self.scr.title("Turtle Invaders")
        self.scr.bgcolor(SCREEN_COLOR)
        try:
            monitors = get_monitors()[0]
            monitor_width = monitors.width
            monitor_height = monitors.height
            self.scr_w = int(monitor_width * self.scr_stretch_x)
            self.scr_w_half = self.scr_w / 2
            self.scr_h = int(monitor_height * self.scr_stretch_y)
            self.scr_h_half = self.scr_h / 2
            pos_x = (monitor_width - self.scr_w) // 2
            pos_y = (monitor_height - self.scr_h) // 2
        except (Exception,) as e:
            print(f"get_monitors() error: {e}")
            # Hard code in case of error:
            self.scr_w = 1920
            self.scr_w_half = 960
            self.scr_h = 1080
            self.scr_h_half = 540
            pos_x = 336
            pos_y = 108
        self.scr.setup(width=self.scr_w, height=self.scr_h, startx=pos_x, starty=pos_y)

    # INVADER METHODS (separation into separate module coming soon):
    def invaders_change_dir(self):
        """
        Reverses the direction of invader movement when they reach the screen edge.
        The movement speed also slightly increases.
        """
        if self.invaders_main_march_speed < 1:
            self.invaders_main_march_speed -= 1
        else:
            self.invaders_main_march_speed += 1
        self.invaders_main_march_speed *= -self.invaders_main_march_speed_increase

    def lr_rl_flag_reset(self):
        """
        Resets the left-right flag indicating a recent reversal in invader direction,
         and adjusts the frequency range for dropping bombs. Use of `max` ensures the
         bomb drop frequency does not become too fast.
        """
        self.invader_bomb_low -= 50
        self.invader_bomb_low = max(self.invader_bomb_low, 250)
        self.invader_bomb_high -= 50
        self.invader_bomb_high = max(self.invader_bomb_high, 2500)
        self.invader_bomb_freq = (self.invader_bomb_low, self.invader_bomb_high)
        self.lr_rl = False

    def invaders_reverse(self):
        """
        Handles the logic when invaders need to reverse direction due to hitting
         a screen edge or other trigger.
        """
        self.invaders_change_dir()
        self.invader_vert_now = self.invader_vert_init
        self.lr_rl = True
        self.scr.ontimer(self.lr_rl_flag_reset, 5)

    def invader_bomb_deploy(self, bomb_element):
        """
        Deploys a bomb from an invader's position, initializing and configuring a
         new bomb Turtle object. This method is typically called when an invader is
         eligible to drop a bomb based on game logic defined in `invaders_main_march`.

        :param bomb_element: The invader Turtle object from which the bomb is deployed.
        :type bomb_element: Turtle
        :return: None
        """
        self.invader_has_fired = True
        invader_bomb = Turtle()
        invader_bomb.shape('square')
        invader_bomb.turtlesize(stretch_wid=.075, stretch_len=.8, outline=2)
        invader_bomb.penup()
        invader_bomb.setheading(270)
        invader_bomb.color(bomb_element.color()[0])
        invader_bomb.goto(bomb_element.xcor(), bomb_element.ycor() - 20)
        self.invader_bombs.append(invader_bomb)
        self.scr.ontimer(self.invader_has_fired_flag_reset,
                         random.randint(*self.invader_bomb_freq))

    def invaders_main(self):
        """
        Manages the primary behavior of invaders during gameplay, including their
         movement across the screen, and interactions with player defenses and
         game boundaries.

        Invaders move in formation and this method checks to restart the game if
         all invaders are destroyed or if they reach the shield boundary. It also
         handles directional changes when invaders reach screen edges.

        :return: None
        """
        if len(self.invaders_all) == 0:  # Restart game if all invaders destroyed
            self.game_lives_left = 0  # Condition for end of game/restart
        # Restart game if invaders make contact with shields:
        if min([i.ycor() for i in self.invaders_all]) - 17.5 <= self.shields_y_boundary:
            self.game_lives_left = 0
        min_x = min([i.xcor() for i in self.invaders_all]) - 30  # `30` for fine-tuning
        max_x = max([i.xcor() for i in self.invaders_all]) + 35  # `35` for fine-tuning
        if (min_x < -self.scr_w_half or max_x > self.scr_w_half) and not self.lr_rl:
            self.invaders_reverse()
        else:
            self.invader_vert_now = 0
        self.invaders_main_march()  # Iterates over each invader

    def invaders_main_march(self):
        """
        Manages the movement of all invaders on the screen, giving a 'living' effect
         with a slight random stretch. This method also triggers the deployment of
         bombs by invaders, starting with a random invader if no bombs have been
         deployed yet.

        This method also updates the saucer frequency tracker based on the invader
         movement, affecting the timing of saucer appearances.

        :return: None
        """
        # Random stretch creates 'living' effect for invaders:
        rand_stretch = 1 + random.randint(71, 79) / 100
        for invader in self.invaders_all:
            # saucer freq tied to invader marching:
            self.saucer_freq_tracker += self.game_tracer_val / 10000
            invader.turtlesize(stretch_wid=rand_stretch, stretch_len=rand_stretch)
            invader.teleport(invader.xcor() - self.invaders_main_march_speed,
                             invader.ycor() - self.invader_vert_now)
            if not self.invader_bomb_barrage_begun:  # Random invader fires first
                first = random.choice(self.invaders_all)
                self.invader_bomb_barrage_begun = True
                self.invader_bomb_deploy(first)
            elif not self.invader_has_fired:
                self.invader_bomb_deploy(invader)
            self.invaders_main_march_bomb()  # Handles bomb iteration/functionality

    def invaders_main_march_bomb(self):
        """
        Handles the movement and collision checking of bombs dropped by the invaders.
         This method moves each bomb downward, removes bombs that have left the screen,
         and checks for collisions with the player and shields.

        If a bomb hits the player, the `player_destroyed` method is triggered. Bomb
         collisions with shields trigger damage to the shield.

        :return: None
        """
        for bomb in self.invader_bombs:
            bomb.goto(bomb.xcor(), bomb.ycor() - self.invader_bomb_speed)
            if bomb.ycor() < -self.scr_h_half:
                bomb.goto(1500, 1500)
                self.invader_bombs.remove(bomb)
                del bomb
            elif are_collision_x_y_cond_met(self.player, bomb, 40, 30):
                self.player_destroyed()
            # Check friendly-fire and degrade shields accordingly:
            else:
                self.invaders_main_march_bomb_shields(bomb)

    def invaders_main_march_bomb_shields(self, bomb):
        """
        Checks for and handles collisions between invader bombs and player shields.
         If a bomb hits a shield, the shield's integrity is reduced or the shield is
         removed if fully degraded.

        :param bomb: The bomb to check for collisions with shields.
        :type bomb: Turtle
        :return: None
        """
        for shield in self.shields_all:
            if are_collision_x_y_cond_met(shield, bomb, 20, 22.5):
                bomb.goto(1500, 1500)
                ind_j = self.invader_bombs.index(bomb)
                del_i = self.invader_bombs.pop(ind_j)  # noqa
                del del_i
                new_ind = SHIELD_STAGES.index(shield.color()[0]) + 1
                if new_ind <= len(SHIELD_STAGES) - 1:
                    shield.color(SHIELD_STAGES[new_ind])
                else:
                    shield.goto(1500, 1500)
                    self.shields_all.remove(shield)
                    del shield

    def invader_has_fired_flag_reset(self):
        """
        Resets the flag that an invader has fired, allowing another bomb to be deployed.
        """
        self.invader_has_fired = False

    def invader_get_positions(self):
        """
        Calculates and stores the starting positions for all invaders based on screen
         dimensions and configuration settings.
        """
        invader_formation_width = self.scr_w * self.invader_gutter_factor
        invader_grid_width = invader_formation_width / self.invader_formation_div_x
        invader_grid_height = self.scr_h / self.invader_formation_div_y
        for x in range(self.invader_formation_div_x):
            for y in range(self.invader_formation_div_y):
                start_x = -invader_formation_width / 2
                spacing_x = invader_grid_width * x
                center_x = invader_grid_width / 2
                pos_x = start_x + spacing_x + center_x

                start_y = -invader_grid_height / 2 + self.invaders_y_limit
                spacing_y = invader_grid_height * y / self.invaders_vert_compress
                center_y = invader_grid_height / 2
                pos_y = start_y + spacing_y + center_y

                self.invader_pos_all.append((pos_x, pos_y))

    def invader_formation(self):
        """
        Creates the initial formation of invaders based on pre-calculated positions.
        """
        for i in range(len(self.invader_pos_all)):
            single_invader = Turtle()
            single_invader.shape('turtle')
            single_invader.turtlesize(stretch_wid=1.75, stretch_len=1.75)
            color_ind = invader_get_row_index(i, self.game_round_current)
            single_invader.color(TURTLE_COLORS[color_ind])
            single_invader.penup()
            single_invader.setheading(270)
            single_invader.goto(self.invader_pos_all[i][0], self.invader_pos_all[i][1])
            self.invaders_all.append(single_invader)

    # PLAYER METHODS (separation into separate module in next refactor):
    def player_deploy(self):
        """
        Deploys or repositions the player on the game screen.
        Initializes the player if not already created.
        """
        if not self.player:
            self.player = Turtle()
            self.player.shape('square')
            self.player.turtlesize(stretch_wid=2.75, stretch_len=2.5, outline=0)
            # Calculate player width from its shape size:
            self.player.invader_width = self.player.shapesize()[0]
            # Center player horizontally:
            self.player_start_x = -self.player.invader_width / 2
            # Position player vertically:
            self.player_start_y = -self.scr_h_half + self.scr_h / 15
            self.player.color(PLAYER_COLOR)
            self.player.penup()
            self.player.setheading(90)  # Facing upwards
        self.player.goto(self.player_start_x, self.player_start_y)

    def player_destroyed(self):
        """
        Handles the event of the player being destroyed by an invader bomb.
        Decreases life count and resets the player's position.
        """
        self.game_lives_left -= 1
        self.game_lives_update()
        self.player_deploy()

    def player_left(self):
        """
        Moves the player to the left if within the screen boundaries.
        """
        if self.player.xcor() > -self.scr_w_half + 50:
            x_pos = self.player.xcor() - 10
            self.player.goto(x_pos, self.player.ycor())

    def player_right(self):
        """
        Moves the player to the right if within the screen boundaries.
        """
        if self.player.xcor() < self.scr_w_half - 55:
            x_pos = self.player.xcor() + 10
            self.player.goto(x_pos, self.player.ycor())

    def reset_player_has_fired_flag(self):
        """
        Resets the flag that prevents the player from firing multiple missiles at once.
        """
        self.player_has_fired = False

    def player_fire_missile(self):
        """
        Fires a missile from the player if not already fired.
        Sets a timer to reset the fire capability using `reset_player_has_fired_flag`.
        """
        if not self.player_has_fired:
            player_missile = Turtle()
            player_missile.shape('square')
            player_missile.turtlesize(stretch_wid=.1, stretch_len=1.05, outline=2.5)
            player_missile.penup()
            player_missile.color(PLAYER_COLOR)
            player_missile.setheading(90)
            player_missile.goto(self.player.xcor(), self.player.ycor() + 35)
            self.player_missiles_all.append(player_missile)
            self.player_has_fired = True
            self.scr.ontimer(self.reset_player_has_fired_flag, self.player_reload_time)

    def player_missile_path(self):
        """
        Controls the movement and collision detection of missiles fired by the player.
         This method updates the position of each missile, checks for screen boundaries,
         and handles collisions with invaders, saucers, and shields.

        Missiles are moved upwards from their current position, and checks are performed
         to remove missiles that exceed the game screen or hit a target. Collisions with
         different game elements like invaders or saucers affect the game score or player
         capabilities.

        :return: None
        """
        for missile in self.player_missiles_all:
            player_x, player_y = missile.xcor(), missile.ycor()
            missile.goto(player_x, player_y + self.player_missile_speed)
            if player_y > self.scr_h_half:
                self.player_missiles_all.remove(missile)
                del missile
            else:
                self.player_missile_path_invader_collision(missile)
                self.player_missile_path_saucer_collision(missile)
                self.player_missile_path_shields_collision(missile)

    def player_missile_path_invader_collision(self, missile):
        """
        Handles collisions between the player's missiles and invaders. When a collision
         is detected, the invader is removed from the game, the player's score is
         updated, and the missile is removed from play.

        :param missile: The missile to check for collisions with invaders.
        :type missile: Turtle
        :return: None
        """
        for invader in self.invaders_all:
            if are_collision_x_y_cond_met(invader, missile, 15, 10):
                self.game_score_current += 10  # 10 points for hitting invader
                self.game_score_update()
                missile.goto(1500, 1500)
                ind_i = self.player_missiles_all.index(missile)
                del_m = self.player_missiles_all.pop(ind_i)  # noqa
                del del_m
                invader.goto(1500, 1500)
                self.invaders_all.remove(invader)
                del invader

    def player_missile_path_saucer_collision(self, missile):
        """
        Handles collisions between the player's missiles and the saucer. A successful
         hit results in a significant increase in the player's score and triggers
         specific effects depending on the saucer's type. This method also handles the
         removal of the missile from play and updates the saucer's position.

        :param missile: The missile to check for collisions with the saucer.
        :type missile: Turtle
        :return: None
        """
        if are_collision_x_y_cond_met(self.saucer, missile, 35, 15):
            missile.goto(1500, 1500)
            ind_i = self.player_missiles_all.index(missile)
            del_m = self.player_missiles_all.pop(ind_i)  # noqa
            del del_m
            self.game_score_current += 100  # Get 100 points for saucer hit
            self.game_score_update()
            self.saucer_x = self.scr_w_half + 50
            self.saucer.teleport(self.saucer_x, self.saucer_y)
            # Heal shields for 'classic' saucer hit:
            if self.saucer.shape() == 'classic':
                for k in self.shields_all:
                    k.color(SHIELD_STAGES[0])
            # Bonus 10 second rapid fire for 'circle' saucer hit:
            elif self.saucer.shape() == 'circle':
                self.player_reload_time = int(self.player_reload_time * .5)
                self.scr.ontimer(self.player_reload_time_reset, 10000)
            self.saucer_freq_tracker = 0
            self.saucer_freq = random.randint(self.saucer_freq_low,
                                              self.saucer_freq_high)

    def player_missile_path_shields_collision(self, missile):
        """
        Manages the interaction between player-fired missiles and the defensive shields.
         If a missile hits a shield, the shield's integrity is reduced, changing its
         color. If the shield's integrity is fully depleted, the shield is removed from
         the game.

        :param missile: The missile to check for collisions with shields.
        :type missile: Turtle
        :return: None
        """
        # Check for friendly-fire and degrade shields accordingly:
        for shield in self.shields_all:
            if are_collision_x_y_cond_met(shield, missile, 25, 20):
                missile.goto(1500, 1500)
                ind_i = self.player_missiles_all.index(missile)
                to_del = self.player_missiles_all.pop(ind_i)  # noqa
                del to_del
                new_ind = SHIELD_STAGES.index(shield.color()[0]) + 1
                if new_ind <= len(SHIELD_STAGES) - 1:
                    shield.color(SHIELD_STAGES[new_ind])
                else:
                    shield.goto(1500, 1500)
                    self.shields_all.remove(shield)
                    del shield

    def player_reload_time_reset(self):
        """
        Resets the player's missile firing reload time to the initial setting.
        """
        self.player_reload_time = self.player_reload_time_init

    # SHIELDS METHODS:
    def shields_deploy(self):
        """
        Creates defensive shields on the game screen. Each shield can degrade upon
         being hit by enemy fire, indicated by a gradual change in color until it
         disappears.
        """
        # Shield x stuff:
        shield_div_x = self.scr_w / (self.shield_num + 1)  # Grid for shield bits
        shield_grid_x = -self.scr_w_half + shield_div_x
        shield_bits_spacing = 46
        shield_width = self.shield_blocks_num * shield_bits_spacing

        # Create shield bits:
        stretch_length = 2.25  # Controls width of shield bit
        stretch_factor = stretch_length * 20 / 2  # Since 1 Turtle unit is 20px
        for i in range(self.shield_num):
            # Center each shield div:
            shield_x_begin = shield_grid_x - shield_width / 2 + stretch_factor
            for j in range(self.shield_blocks_num):
                shield = Turtle()
                shield.penup()
                shield.shape('square')
                shield.turtlesize(stretch_wid=2, stretch_len=stretch_length, outline=0)
                shield.color(SHIELD_STAGES[0])  # Start at the brightest color
                shield.goto(shield_x_begin, -self.scr_h_half + self.scr_h / 5.25)
                self.shields_all.append(shield)
                shield_x_begin += shield_bits_spacing
            shield_grid_x += shield_div_x  # Move to position for the next shield

        # Get terminal y-limit for game over:
        self.shields_y_boundary = max([i.ycor() for i in self.shields_all]) + 20

    # SAUCER METHODS:
    def saucer_create(self):
        """
        Initializes the saucer that flies over the screen, providing bonus points
         when hit. The type of saucer and its effects on hit are randomized.
        """
        self.saucer = Turtle()
        self.saucer.penup()
        self.saucer.color(random.choice(TURTLE_COLORS))
        saucer_ind = random.randint(0, 1)  # Randomly decide saucer type
        self.saucer.setheading([0, 270][saucer_ind])
        self.saucer_shape_current = ['circle', 'classic'][saucer_ind]
        self.saucer.shape(self.saucer_shape_current)
        size_options = [(.6, 3.25, 10), (8.5, 2.5, 5)][saucer_ind]
        self.saucer.turtlesize(*size_options)
        self.saucer_x = self.scr_w_half + 50  # Initial position off-screen
        self.saucer_y = self.scr_h_half - self.scr_h / [10, 8.75][saucer_ind]
        self.saucer.goto(self.saucer_x, self.saucer_y)

    def saucer_flyby(self):
        """
        Manages the movement of the saucer across the screen. Resets its position
         and frequency of appearance after it passes.
        """
        if self.saucer_freq_tracker > self.saucer_freq:
            if self.saucer_x > -self.scr_w_half - 50:
                self.saucer_x -= self.saucer_flyby_speed
                self.saucer.teleport(self.saucer_x, self.saucer_y)
            else:
                self.saucer_x = self.scr_w_half + 50  # Reset position to other side
                self.saucer.teleport(self.saucer_x, self.saucer_y)
                self.saucer_freq_tracker = 0  # Reset frequency tracker
                self.saucer_freq = random.randint(self.saucer_freq_low,
                                                  self.saucer_freq_high)

    # GAME GENERAL METHODS:
    def game_restart(self):
        """
        Clears the game screen and resets all game elements to start a new game.
         This method is invoked typically after a game over or when the player
         chooses to restart the game.
        """
        self.scr.clear()

        # Garbage collection, removing all game objects to start fresh:
        del self.invaders_all
        del self.player
        del self.game_score_object
        del self.game_lives_object
        del self.saucer
        del self.player_missiles_all
        del self.shields_all
        del self.invader_bombs

        self.__init__()  # Re-initialize the game setup
        self.game_begin_invasion()  # Begin the game loop

    def game_pause_toggle(self):
        """
        Toggles the pause state of the game. This method is bound to a keypress and
         can be used to pause/resume the game.

        Example:
            game_instance.game_pause_toggle()  # This would toggle the pause state
                                                  based on the current state.

        :return: None
        """
        self.game_is_paused = not self.game_is_paused

    def game_listeners(self):
        """
        Sets up the key listeners for the game, binding specific game actions to
         keyboard keys. This allows player interaction using the keyboard.

        :return: None
        """
        self.scr.listen()
        self.scr.onkeypress(self.player_fire_missile, 'space')
        self.scr.onkeypress(self.player_left, 'Left')
        self.scr.onkeypress(self.player_right, 'Right')
        self.scr.onkeypress(self.game_pause_toggle, 'p')
        self.scr.onkeypress(self.game_quit, 'q')
        self.scr.onkeypress(self.game_restart, 'r')

    def game_score_update(self):
        """
        Updates the game score display. If the score display object does not exist,
         it creates one, otherwise it updates the existing score display.
        """
        if not self.game_score_object:
            self.game_score_object = Turtle()
        else:
            self.game_score_object.clear()
        self.game_score_object.penup()
        self.game_score_object.hideturtle()
        self.game_score_object.color(PLAYER_COLOR)
        self.game_score_object.goto(-self.scr_w_half + self.scr_w / 20,
                                    self.scr_h_half - self.scr_h / 15)
        self.game_score_object.write(f"{self.game_score_current:04d}",
                                     align="center",
                                     font=("Source Sans 3 Black", 32, "italic"))

    def game_lives_update(self):
        """
        Updates the display of player lives. Each life is represented as a square
         block in the game's UI. If the lives display object does not exist, it
         creates one, otherwise it updates the existing display.
        """
        if not self.game_lives_object:
            self.game_lives_object = Turtle()
        else:
            self.game_lives_object.clear()

        self.game_lives_object.penup()
        self.game_lives_object.hideturtle()
        self.game_lives_object.color(PLAYER_COLOR)
        shift_factor = (self.game_lives_left - 1) * self.scr_w / 95
        self.game_lives_object.goto(self.scr_w_half - self.scr_w / 50 - shift_factor,
                                    self.scr_h_half - self.scr_h / 15)
        self.game_lives_object.write("■" * (self.game_lives_left - 1),
                                     align="center",
                                     font=("Source Sans 3 Black", 32, "italic"))

    def game_quit(self):
        """
        Quits the game immediately. This method is bound to a keypress allowing the
        player to exit the game.
        """
        self.game_is_on = False
        self.scr.bye()

    def game_setup(self):
        """
        Initializes all components of the game, setting up the game board, player,
         invaders, saucer, shields, and initial game settings.
        """
        self.game_score_update()
        self.game_lives_update()
        self.invader_get_positions()
        self.invader_formation()
        self.player_deploy()
        self.shields_deploy()
        self.saucer_create()

    def game_begin_invasion(self):
        """
        Starts the main game loop. Sets up the screen, initializes the game, and
         continues the loop until the game is either paused, ended, or exited.
        """
        self.screen_setup()
        self.scr.tracer(0)
        self.game_setup()
        self.scr.tracer(self.game_tracer_val)
        self.game_listeners()
        while self.game_is_on:
            if not self.game_is_paused and self.game_lives_left > 0:
                self.scr.update()
                self.invaders_main()
                self.player_missile_path()
                self.saucer_flyby()
            elif self.game_lives_left > 0:
                self.scr.update()
            else:
                self.game_lives_update()
                self.game_score_update()
                self.game_restart()


if __name__ == "__main__":
    try:
        turtle_invaders = TurtleInvaders()
        turtle_invaders.game_begin_invasion()
    except (KeyboardInterrupt, Exception):
        sys.exit(1)  # Properly handle unexpected exits.

# Things to do:
#  - Separate Invaders/Player/Screen/Shields methods into separate modules!!

#  - Figure out anomalous cases where invaders march straight down, e.g. happens
#     first time invaders hit right wall if march initializes to the right.

# - Get setheading() for all objects aligned so stretch_len and stretch_wid mean
#      the same thing.

#  - Work on algo to see direct relation of tracer to seconds.

#  - Change player shape from square to triangle & make trig algo for collision
#     with player triangle. Use `print(self.player.get_shapepoly())` to see shape
#     boundaries -- returns: ((40.0, -11.54), (0.0, 23.1), (-40.0, -11.54)).

#  - Add functionality for subsequent rounds.

#  - Remedy names/concerns regarding game restart -- come up with better cases for
#     while loop, diversify functionality

#  - Add code for bonus lives at 1000s.

#  - Use get_shapepoly(), shapesize() for development analysis.

#  - For development, to identify invader indices easily:
#     invader.write(i, align="center", font=("Source Sans 3 Black", 24, "italic"))

#  - Methods for future development ref: self.scr.window_width(), self.scr.window_height()

#  - Display directions and indications of saucer bonuses on initial greet screen
