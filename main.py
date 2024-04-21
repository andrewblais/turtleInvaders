from turtle import Screen, Turtle
import random
from screeninfo import get_monitors
import sys

from config.config import *
from modules.collision_check import *


class TurtleInvaders:
    def __init__(self):
        # GAME GENERAL ATTRIBUTES:
        self.game_is_paused = False
        self.game_is_on = True
        self.game_lives_object = None
        self.game_round_current = 1
        self.game_lives_left = 3
        self.game_score_object = None
        self.game_score_current = 0
        self.game_tracer_val = 20

        # INVADER ATTRIBUTES:
        self.invaders_y_limit = 50  # Higher val shifts formation up along y-axis
        self.invaders_vert_compress = 3  # Higher val to compress rows along y-axis
        self.invaders_all = []
        self.invader_formation_div_x = 6
        self.invader_formation_div_y = 4
        self.invader_gutter_factor = .7  # Smaller val = bigger L-R gutters
        self.invader_pos_all = []
        self.invaders_march_speed = 1
        self.invaders_march_speed_increase = .5
        self.invader_vert_init = 10
        self.invader_vert_now = self.invader_vert_init
        self.reversed = False  # Flag indicating invaders have changed direction
        self.invader_bombs = []
        self.invader_bomb_speed = 1
        self.invader_has_fired = False
        self.invader_bomb_barrage_begun = False
        self.invader_bomb_low_init = 500  # ~ 1/2 second (divide by 1000)
        self.invader_bomb_high_init = 5000  # ~5 seconds (divide by 1000)
        self.invader_bomb_low = self.invader_bomb_low_init
        self.invader_bomb_high = self.invader_bomb_high_init
        self.invader_bomb_freq = (self.invader_bomb_low, self.invader_bomb_high)

        # PLAYER ATTRIBUTES:
        self.player = None
        self.player_start_x = None
        self.player_start_y = None
        self.player_missiles_all = []
        self.player_has_fired = False
        self.player_reload_time_init = 1000  # 1 second
        self.player_reload_time = self.player_reload_time_init
        self.player_missile_speed = 15

        # SAUCER ATTRIBUTES:
        self.saucer = None
        self.saucer_x = None
        self.saucer_y = None
        self.saucer_shape_current = None
        self.saucer_flyby_speed = 5
        self.saucer_freq_tracker = 0
        # Allows variation in delay of saucer:
        self.saucer_freq_low = 10  # ~8-second SAUCER delay
        self.saucer_freq_high = 22  # ~20-second SAUCER delay
        self.saucer_freq = random.randint(self.saucer_freq_low, self.saucer_freq_high)

        # SCREEN ATTRIBUTES
        self.scr = None
        self.scr_stretch_x = .65
        self.scr_stretch_y = .8
        self.scr_w = None
        self.scr_h = None
        self.scr_w_half = None
        self.scr_h_half = None

        # SHIELDS ATTRIBUTES:
        self.shield_num = 3
        self.shield_blocks_num = 4
        self.shields_all = []
        self.shields_y_boundary = None

    # SCREEN METHODS:
    def screen_setup(self):
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

    # INVADER METHODS:
    def invaders_change_dir(self):
        """Reverses invaders direction on wall hit."""
        if self.invaders_march_speed < 1:
            self.invaders_march_speed -= 1
        else:
            self.invaders_march_speed += 1
        self.invaders_march_speed *= -self.invaders_march_speed_increase

    def reversed_flag_reset(self):
        """Resets reversed flag. Also slightly increases the invader_bomb
        frequency each time invaders have reversed."""
        # Keeps self.invader_bomb_low above 250:
        self.invader_bomb_low -= 50
        self.invader_bomb_low = max(self.invader_bomb_low, 250)

        # Keeps self.invader_bomb_high above 2500:
        self.invader_bomb_high -= 50
        self.invader_bomb_high = max(self.invader_bomb_high, 2500)

        self.invader_bomb_freq = (self.invader_bomb_low, self.invader_bomb_high)
        self.reversed = False

    def invaders_reverse(self):
        self.invaders_change_dir()
        self.invader_vert_now = self.invader_vert_init
        self.reversed = True
        self.scr.ontimer(self.reversed_flag_reset, 5)

    def invader_bomb_deploy(self, bomb_el):
        self.invader_has_fired = True
        invader_bomb = Turtle()
        invader_bomb.shape('square')
        invader_bomb.turtlesize(stretch_wid=.075, stretch_len=.8, outline=2)
        invader_bomb.penup()
        invader_bomb.setheading(270)
        invader_bomb.color(bomb_el.color()[0])
        invader_bomb.goto(bomb_el.xcor(), bomb_el.ycor() - 20)
        self.invader_bombs.append(invader_bomb)
        self.scr.ontimer(self.invader_has_fired_flag_reset,
                         random.randint(*self.invader_bomb_freq))

    def invaders_march(self):
        # Restart game if all invaders destroyed:
        if len(self.invaders_all) == 0:
            self.game_lives_left = 0  # Condition for end of game/restart

        # End game if invaders make contact with shields:
        if min([i.ycor() for i in self.invaders_all]) - 17.5 <= self.shields_y_boundary:
            self.game_lives_left = 0

        # `- 30` allows accuracy in left screen limit:
        min_x = min([i.xcor() for i in self.invaders_all]) - 30
        # `+ 35` allows accuracy in right screen limit:
        max_x = max([i.xcor() for i in self.invaders_all]) + 35
        if (min_x < -self.scr_w_half or max_x > self.scr_w_half) and not self.reversed:
            self.invaders_reverse()
        else:
            self.invader_vert_now = 0

        # Creates 'living' effect for invaders:
        rand_stretch = 1 + random.randint(71, 79) / 100
        for i in self.invaders_all:
            # SAUCER freq tied to invader marching:
            self.saucer_freq_tracker += self.game_tracer_val / 10000
            i.turtlesize(stretch_wid=rand_stretch, stretch_len=rand_stretch)
            i.teleport(i.xcor() - self.invaders_march_speed,
                       i.ycor() - self.invader_vert_now)

            # Chooses first to fire randomly from list:
            if not self.invader_bomb_barrage_begun:
                first = random.choice(self.invaders_all)
                self.invader_bomb_barrage_begun = True
                self.invader_bomb_deploy(first)
            elif not self.invader_has_fired:
                self.invader_bomb_deploy(i)

            for j in self.invader_bombs:
                j.goto(j.xcor(), j.ycor() - self.invader_bomb_speed)
                if j.ycor() < -self.scr_h_half:
                    j.goto(1500, 1500)
                    del_i = self.invader_bombs.pop(self.invader_bombs.index(j))  # noqa
                    del del_i
                if are_collision_x_y_cond_met(self.player, j, 40, 30):
                    self.player_destroyed()
                # Check friendly-fire and degrade shields accordingly:
                for shield in self.shields_all:
                    if are_collision_x_y_cond_met(shield, j, 20, 22.5):
                        j.goto(1500, 1500)
                        ind_j = self.invader_bombs.index(j)
                        del_i = self.invader_bombs.pop(ind_j)  # noqa
                        del del_i
                        new_ind = SHIELD_STAGES.index(shield.color()[0]) + 1
                        if new_ind <= len(SHIELD_STAGES) - 1:
                            shield.color(SHIELD_STAGES[new_ind])
                        else:
                            shield.goto(1500, 1500)
                            ind_shield = self.shields_all.index(shield)
                            del_s = self.shields_all.pop(ind_shield)  # noqa
                            del del_s

    def invader_has_fired_flag_reset(self):
        self.invader_has_fired = False

    def invader_get_positions(self):
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

    #    # #    # #  # #   # #    #
    #  # # #  RESUME HERE  # # #  #
    #    # #    # #  # #   # #    #
    def invader_formation(self):
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

    # PLAYER METHODS:
    def player_deploy(self):
        if not self.player:
            self.player = Turtle()
            self.player.shape('square')
            self.player.turtlesize(stretch_wid=2.75, stretch_len=2.5, outline=0)
            self.player.invader_width = self.player.shapesize()[0]  # Get player width
            self.player_start_x = -self.player.invader_width / 2  # Center player
            self.player_start_y = -self.scr_h_half + self.scr_h / 15
            self.player.color(PLAYER_COLOR)
            self.player.penup()
            self.player.setheading(90)
        self.player.goto(self.player_start_x, self.player_start_y)

    def player_destroyed(self):
        self.game_lives_left -= 1
        self.game_lives_update()
        self.player_deploy()

    def player_left(self):
        if self.player.xcor() > -self.scr_w_half + 50:
            x_pos = self.player.xcor() - 10
            self.player.goto(x_pos, self.player.ycor())

    def player_right(self):
        if self.player.xcor() < self.scr_w_half - 55:
            x_pos = self.player.xcor() + 10
            self.player.goto(x_pos, self.player.ycor())

    def reset_player_has_fired_flag(self):
        self.player_has_fired = False

    def player_fire_missile(self):
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
        for i in self.player_missiles_all:
            player_x, player_y = i.xcor(), i.ycor()
            i.goto(player_x, player_y + self.player_missile_speed)
            if player_y > self.scr_h_half:
                ind_i = self.player_missiles_all.index(i)
                to_del = self.player_missiles_all.pop(ind_i)  # noqa
                del to_del
            else:
                for j in self.invaders_all:
                    if are_collision_x_y_cond_met(j, i, 15, 10):
                        self.game_score_current += 10  # 10 points for hitting invader
                        self.game_score_update()
                        i.goto(1500, 1500)
                        j.goto(1500, 1500)
                        ind_i = self.player_missiles_all.index(i)
                        del_m = self.player_missiles_all.pop(ind_i)  # noqa
                        del del_m
                        ind_j = self.invaders_all.index(j)
                        del_t = self.invaders_all.pop(ind_j)  # noqa
                        del del_t
                if are_collision_x_y_cond_met(self.saucer, i, 35, 15):
                    i.goto(1500, 1500)
                    ind_i = self.player_missiles_all.index(i)
                    del_m = self.player_missiles_all.pop(ind_i)  # noqa
                    del del_m
                    # Get 100 points for SAUCER hit:
                    self.game_score_current += 100
                    self.game_score_update()
                    self.saucer_x = self.scr_w_half + 50
                    self.saucer.teleport(self.saucer_x, self.saucer_y)
                    # Heal shields for 'classic' SAUCER hit:
                    if self.saucer.shape() == 'classic':
                        for k in self.shields_all:
                            k.color(SHIELD_STAGES[0])
                    # Bonus 10 second rapid fire for 'circle' SAUCER hit:
                    elif self.saucer.shape() == 'circle':
                        self.player_reload_time = int(self.player_reload_time * .5)
                        self.scr.ontimer(self.player_reload_time_reset, 10000)
                    self.saucer_freq_tracker = 0
                    low = self.saucer_freq_low
                    high = self.saucer_freq_high
                    self.saucer_freq = random.randint(low, high)
                # Check for friendly-fire and degrade shields accordingly:
                for shield in self.shields_all:
                    if are_collision_x_y_cond_met(shield, i, 25, 20):
                        i.goto(1500, 1500)
                        ind_i = self.player_missiles_all.index(i)
                        to_del = self.player_missiles_all.pop(ind_i)  # noqa
                        del to_del
                        new_ind = SHIELD_STAGES.index(shield.color()[0]) + 1
                        if new_ind <= len(SHIELD_STAGES) - 1:
                            shield.color(SHIELD_STAGES[new_ind])
                        else:
                            shield.goto(1500, 1500)
                            ind_shield = self.shields_all.index(shield)
                            del_s = self.shields_all.pop(ind_shield)  # noqa
                            del del_s

    def player_reload_time_reset(self):
        self.player_reload_time = self.player_reload_time_init

    # SHIELDS METHODS:
    def shields_deploy(self):
        """To aid with memory clutter, instead of creating lots of shields bits,
        use fewer large shield blocks and degrade them with visual cue of less
        bright color when hit with enemy missile: let color fade on each hit until
        it's gone."""
        # Shield x stuff:
        shield_div_x = self.scr_w / (self.shield_num + 1)
        shield_grid_x = -self.scr_w_half + shield_div_x
        shield_bits_spacing = 46
        shield_width = self.shield_blocks_num * shield_bits_spacing

        # Create shield bits:
        stretch_length = 2.25
        stretch_factor = stretch_length * 20 / 2
        for i in range(self.shield_num):
            # Center each shield div:
            shield_x_begin = shield_grid_x - shield_width / 2 + stretch_factor
            for j in range(self.shield_blocks_num):
                shield = Turtle()
                shield.penup()
                shield.shape('square')
                shield.turtlesize(stretch_wid=2, stretch_len=stretch_length, outline=0)
                shield.color(SHIELD_STAGES[0])
                shield.goto(shield_x_begin, -self.scr_h_half + self.scr_h / 5.25)
                self.shields_all.append(shield)
                shield_x_begin += shield_bits_spacing
            shield_grid_x += shield_div_x

        # Get terminal y-limit for game over:
        self.shields_y_boundary = max([i.ycor() for i in self.shields_all]) + 20

    # SAUCER METHODS:
    def saucer_create(self):
        self.saucer = Turtle()
        self.saucer.penup()
        self.saucer.color(random.choice(TURTLE_COLORS))

        saucer_ind = random.randint(0, 1)

        self.saucer.setheading([0, 270][saucer_ind])

        self.saucer_shape_current = ['circle', 'classic'][saucer_ind]
        self.saucer.shape(self.saucer_shape_current)

        size_options = [(.6, 3.25, 10), (8.5, 2.5, 5)][saucer_ind]
        self.saucer.turtlesize(*size_options)

        self.saucer_x = self.scr_w_half + 50
        self.saucer_y = self.scr_h_half - self.scr_h / [10, 8.75][saucer_ind]
        self.saucer.goto(self.saucer_x, self.saucer_y)

    def saucer_flyby(self):
        if self.saucer_freq_tracker > self.saucer_freq:
            if self.saucer_x > -self.scr_w_half - 50:
                self.saucer_x -= self.saucer_flyby_speed
                self.saucer.teleport(self.saucer_x, self.saucer_y)
            else:
                self.saucer_x = self.scr_w_half + 50
                self.saucer.teleport(self.saucer_x, self.saucer_y)
                self.saucer_freq_tracker = 0
                self.saucer_freq = random.randint(self.saucer_freq_low,
                                                  self.saucer_freq_high)

    # GAME GENERAL METHODS:
    def game_restart(self):
        self.scr.clear()

        # Garbage collection
        del self.invaders_all
        del self.player
        del self.game_score_object
        del self.game_lives_object
        del self.saucer
        del self.player_missiles_all
        del self.shields_all
        del self.invader_bombs

        self.__init__()
        self.game_begin_invasion()

    def game_pause_toggle(self):
        self.game_is_paused = not self.game_is_paused

    def game_listeners(self):
        """Creates key listeners for movement/game_pause_toggle/game_quit/game_restart
        methods."""
        self.scr.listen()
        self.scr.onkeypress(self.player_fire_missile, 'space')
        self.scr.onkeypress(self.player_left, 'Left')
        self.scr.onkeypress(self.player_right, 'Right')
        self.scr.onkeypress(self.game_pause_toggle, 'p')
        self.scr.onkeypress(self.game_quit, 'q')
        self.scr.onkeypress(self.game_restart, 'r')

    def game_score_update(self):
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
        self.game_is_on = False
        self.scr.bye()

    def game_setup(self):
        self.game_score_update()
        self.game_lives_update()
        self.invader_get_positions()
        self.invader_formation()
        self.player_deploy()
        self.shields_deploy()
        self.saucer_create()

    def game_begin_invasion(self):
        self.screen_setup()
        self.scr.tracer(0)
        self.game_setup()
        self.scr.tracer(self.game_tracer_val)
        self.game_listeners()
        while self.game_is_on:
            if not self.game_is_paused and self.game_lives_left > 0:
                self.scr.update()
                self.invaders_march()
                self.player_missile_path()
                self.saucer_flyby()
            elif self.game_lives_left > 0:
                self.scr.update()
            else:
                self.game_lives_update()
                self.game_score_update()
                self.game_restart()
        self.scr.exitonclick()  # Is exitonclick() needed?


if __name__ == "__main__":
    try:
        turtle_invaders = TurtleInvaders()
        turtle_invaders.game_begin_invasion()
    except (KeyboardInterrupt, Exception):
        sys.exit(1)

# Things to do:
#  - Figure out anomalous cases where invaders march straight down, e.g. happens
#     first time invaders hit right wall if march initializes to the right.

# - Get setheading() for all objects aligned so stretch_len and stretch_wid mean
#      the same thing.

#  - Work on algo to see direct relation of tracer to seconds.

#  - Change player shape from square to triangle & make trig algo for collision
#     with player triangle. Use `print(self.player.get_shapepoly())` to see shape
#     boundaries -- returns: ((40.0, -11.54), (0.0, 23.1), (-40.0, -11.54)).

#  - Make one type of saucer provide points bonus, the other (more rare frequency)
#       have bonus of refreshing shields to max value/color.

#  - Consider healing shields one color stage for saucer hit:
#     curr_color_ind = SHIELD_STAGES.index(k.color()[0])
#     heal_color_ind = max(0, curr_color_ind - 1)
#     k.color(SHIELD_STAGES[heal_color_ind])

#  - Add functionality for subsequent rounds.

#  - Remedy names/concerns regarding game restart -- come up with better cases for
#     while loop, diversify functionality

#  - Add code for bonus lives at 1000s.

#  - Use get_shapepoly(), shapesize() for development analysis.

#  - For development, to identify invader indices easily:
#     invader.write(i, align="center", font=("Source Sans 3 Black", 24, "italic"))

#  - Rule out necessity of `self.scr.colormode(255)`

#  - Methods for future ref: self.scr.window_width(), self.scr.window_height()

#  - Display directions and indications of saucer bonuses on initial greet screen
