from turtle import Screen, Turtle
import random
from screeninfo import get_monitors
import sys

from config.config import *
from modules.collision_check import *


class TurtleInvaders:
    def __init__(self):
        self.screen = None
        self.formation_div_x = 6
        self.formation_div_y = 4
        self.screen_stretch_x = .65
        self.screen_stretch_y = .8
        self.screen_width = None
        self.screen_height = None
        self.formation_gutter_factor = .7  # Smaller val = bigger L-R gutters
        self.player = None
        self.player_start_x = -2
        self.player_start_y = -350
        self.invader_positions = []
        self.all_invaders = []
        self.score_object = None
        self.score_current = 0
        self.lives_object = None
        self.lives_left = 3
        self.saucer = None
        self.saucer_x = 0
        self.saucer_y = 0
        self.round_number = 1
        self.current_saucer_shape = None
        self.saucer_freq_tracker = 0
        # Allow variation in delay of UAPs:
        self.saucer_freq_low = 10  # Means about an 8-second UAP delay
        self.saucer_freq_high = 22  # Means about a 20-second UAP delay
        self.saucer_freq = random.randint(self.saucer_freq_low, self.saucer_freq_high)
        self.invader_march_speed = 1
        self.invader_march_speed_increase = .5
        self.invader_movement_vert = 10
        self.saucer_flyby_speed = 5
        self.invaders_have_reversed = False  # Flag indicating invaders have changed direction
        self.pause_game = False
        self.game_on = True
        self.player_missiles = []
        self.missile_has_fired = False
        self.player_reload_time_init = 1000
        self.player_reload_time = self.player_reload_time_init
        self.missile_speed = 10
        self.shields = []
        self.terminal_y = None
        self.tracer_val = 20
        self.invader_missiles = []
        self.invader_missile_speed = 1
        self.invader_has_fired = False
        self.invader_missile_barrage_begun = False
        self.invader_missile_low_init = 500  # Divide by 1000 = .5 seconds/5 seconds
        self.invader_missile_high_init = 5000  # Divide by 1000 = 5 seconds
        self.invader_missile_low = self.invader_missile_low_init
        self.invader_missile_high = self.invader_missile_high_init
        self.invader_missile_freq = (self.invader_missile_low, self.invader_missile_high)

    #  #  #  #  #  #
    # SCREEN STUFF #
    #  #  #  #  #  #
    def setup_screen(self):
        self.screen = Screen()
        self.screen.title("Turtle Invaders")
        # self.screen.colormode(255)
        self.screen.bgcolor(SCREEN_COLOR)

        monitor = get_monitors()[0]
        monitor_width = monitor.width
        monitor_height = monitor.height
        self.screen_width = int(monitor_width * self.screen_stretch_x)
        self.screen_height = int(monitor_height * self.screen_stretch_y)
        screen_pos_x = (monitor_width - self.screen_width) // 2
        screen_pos_y = (monitor_height - self.screen_height) // 2

        self.screen.setup(width=self.screen_width,
                          height=self.screen_height,
                          startx=screen_pos_x,
                          starty=screen_pos_y)

    def get_screen_width(self):
        self.screen_width = self.screen.window_width()
        self.screen_height = self.screen.window_height()

    #  #  #  #  #  #
    # TURTLE STUFF #
    #  #  #  #  #  #
    @staticmethod
    def get_invader_row_index(number, round_number):
        for key, value in TURTLE_COLOR_INDEX_DICT.items():
            if number in key:
                return (value + round_number) % len(TURTLE_COLORS)
        raise ValueError(f"Number {number} not in any range key.")

    def invader_change_dir(self):
        if self.invader_march_speed < 1:
            self.invader_march_speed -= 1
        else:
            self.invader_march_speed += 1
        self.invader_march_speed *= -self.invader_march_speed_increase

    def reset_invader_flag(self):
        """Resets invaders_have_reversed flag. Also slightly increases the invader_missile
        frequency each time invaders have reversed."""
        self.invader_missile_low -= 50
        self.invader_missile_low = max(self.invader_missile_low, 250)
        self.invader_missile_high -= 50
        self.invader_missile_high = max(self.invader_missile_high, 2500)
        self.invader_missile_freq = (self.invader_missile_low, self.invader_missile_high)
        self.invaders_have_reversed = False

    def invader_march(self):
        # Restart game if all invaders destroyed:
        if len(self.all_invaders) == 0:
            self.lives_left = 0

        # End game if invaders make contact with shields:
        min_invader_y = min([i.ycor() for i in self.all_invaders]) - 17.5
        if min_invader_y <= self.terminal_y:
            self.lives_left = 0

        right_limit = self.screen_width / 2
        left_limit = -right_limit

        min_invader_x = min([i.xcor() for i in self.all_invaders])
        max_invader_x = max([i.xcor() for i in self.all_invaders])

        if min_invader_x - 30 < left_limit and not self.invaders_have_reversed:
            self.invader_change_dir()
            invader_movement_vert = self.invader_movement_vert
            self.invaders_have_reversed = True
            self.screen.ontimer(self.reset_invader_flag, 5)
        elif max_invader_x + 35 > right_limit and not self.invaders_have_reversed:
            self.invader_change_dir()
            invader_movement_vert = self.invader_movement_vert
            self.invaders_have_reversed = True
            self.screen.ontimer(self.reset_invader_flag, 5)
        else:
            invader_movement_vert = 0

        rand_dec = random.randint(71, 79) / 100
        rand_stretch = 1 + rand_dec

        for i in self.all_invaders:
            # UAP freq tied to invader marching. The following equation makes
            #  self.saucer_freq_tracker increment approx 1.0 per second:
            self.saucer_freq_tracker += self.tracer_val / 10000
            i.turtlesize(stretch_wid=rand_stretch, stretch_len=rand_stretch)
            i.teleport(i.xcor() - self.invader_march_speed,
                       i.ycor() - invader_movement_vert)
            # Random first invader to fire:
            if not self.invader_missile_barrage_begun:
                self.invader_missile_barrage_begun = True
                self.invader_has_fired = True
                first = random.choice(self.all_invaders)
                invader_missile = self.deploy_invader_invader_missile()
                invader_missile.color(first.color()[0])
                invader_missile.goto(first.xcor(), first.ycor() - 20)
                self.invader_missiles.append(invader_missile)
                delay = random.randint(*self.invader_missile_freq)
                self.screen.ontimer(self.reset_invader_has_fired_flag, delay)
            elif not self.invader_has_fired:
                self.invader_has_fired = True
                invader_missile = self.deploy_invader_invader_missile()
                invader_missile.color(i.color()[0])
                invader_missile.goto(i.xcor(), i.ycor() - 20)
                self.invader_missiles.append(invader_missile)
                delay = random.randint(*self.invader_missile_freq)
                self.screen.ontimer(self.reset_invader_has_fired_flag, delay)
            for j in self.invader_missiles:
                j.goto(j.xcor(), j.ycor() - self.invader_missile_speed)
                if j.ycor() < -self.screen_height / 2:
                    j.goto(1500, 1500)
                    # noinspection PyUnusedLocal
                    del_i = self.invader_missiles.pop(self.invader_missiles.index(j))
                    del del_i
                # ((40.0, -30.0), (40.0, 30.0), (-40.0, 30.0), (-40.0, -30.0))
                if are_collision_x_y_cond_met(self.player, j, 40, 30):
                    self.player_destroyed()
                # Check friendly-fire and degrade shields accordingly:
                for shield in self.shields:
                    # poly: ((20.0, -22.5), (20.0, 22.5), (-20.0, 22.5), (-20.0, -22.5))
                    if are_collision_x_y_cond_met(shield, j, 20, 22.5):
                        j.goto(1500, 1500)
                        # noinspection PyUnusedLocal
                        del_i = self.invader_missiles.pop(self.invader_missiles.index(j))
                        del del_i
                        curr_ind = SHIELD_STAGES.index(shield.color()[0])
                        new_ind = curr_ind + 1
                        if new_ind <= len(SHIELD_STAGES) - 1:
                            new_color = SHIELD_STAGES[new_ind]
                            shield.color(new_color)
                        else:
                            shield.goto(1500, 1500)
                            # noinspection PyUnusedLocal
                            del_s = self.shields.pop(self.shields.index(shield))
                            del del_s

    def player_redeploy(self):
        self.player.color(SCREEN_COLOR)
        self.player.goto(self.player_start_x, self.player_start_y)
        self.player.color(PLAYER_COLOR)

    def player_destroyed(self):
        self.lives_left -= 1
        self.update_lives()
        self.player_redeploy()

    def reset_invader_has_fired_flag(self):
        self.invader_has_fired = False

    @staticmethod
    def deploy_invader_invader_missile():
        invader_missile = Turtle()
        invader_missile.shape('square')
        invader_missile.turtlesize(stretch_wid=.075, stretch_len=.8, outline=2)
        # print(invader_missile.get_shapepoly())  # For development
        # print(invader_missile.shapesize())  # For development
        invader_missile.penup()
        invader_missile.setheading(270)
        return invader_missile

    def get_invader_positions(self):
        invader_formation_width = self.screen_width * self.formation_gutter_factor
        invader_grid_width = invader_formation_width / self.formation_div_x
        invader_grid_height = self.screen_height / self.formation_div_y

        for x in range(self.formation_div_x):
            for y in range(self.formation_div_y):
                start_x = -invader_formation_width / 2
                spacing_x = invader_grid_width * x
                center_x = invader_grid_width / 2
                pos_x = start_x + spacing_x + center_x

                # Add higher number to shift formation higher along y-axis:
                start_y = -invader_grid_height / 2 + 50
                # Make divisor larger to compress rows along on y-axis:
                spacing_y = invader_grid_height * y / 3
                center_y = invader_grid_height / 2
                pos_y = start_y + spacing_y + center_y

                self.invader_positions.append((pos_x, pos_y))

    def invader_formation(self):
        for i in range(len(self.invader_positions)):
            single_invader = Turtle()
            single_invader.shape('turtle')
            single_invader.speed('slowest')
            single_invader.turtlesize(stretch_wid=1.75, stretch_len=1.75)
            color_ind = self.get_invader_row_index(i, self.round_number)
            single_invader.color(TURTLE_COLORS[color_ind])
            single_invader.penup()
            single_invader.setheading(270)
            single_invader.goto(self.invader_positions[i][0],
                                self.invader_positions[i][1])
            self.all_invaders.append(single_invader)
            # For development only, to identify invader indices easily:
            # invader.write(i, align="center", font=("Source Sans 3 Black", 24, "italic"))

    #  #  #  #  #  #  #
    #  PLAYER  STUFF  #
    #  #  #  #  #  #  #
    def player_left(self):
        if self.player.xcor() > -self.screen_width / 2 + 50:
            x_pos = self.player.xcor() - 10
            self.player.goto(x_pos, self.player.ycor())

    def player_right(self):
        if self.player.xcor() < self.screen_width / 2 - 55:
            x_pos = self.player.xcor() + 10
            self.player.goto(x_pos, self.player.ycor())

    def reset_missile_has_fired_flag(self):
        self.missile_has_fired = False

    def player_fire_missile(self):
        if not self.missile_has_fired:
            player_missile = Turtle()
            player_missile.shape('square')
            player_missile.turtlesize(stretch_wid=.1, stretch_len=1.05, outline=2.5)
            # print(self.player_missile.get_shapepoly())  # For development
            # print(self.player_missile.shapesize())  # For development
            player_missile.penup()
            player_missile.color(PLAYER_COLOR)
            player_missile.setheading(90)
            player_missile.goto(self.player.xcor(), self.player.ycor() + 35)
            self.player_missiles.append(player_missile)
            self.missile_has_fired = True
            self.screen.ontimer(self.reset_missile_has_fired_flag,
                                self.player_reload_time)

    def player_missile_path(self):
        for i in self.player_missiles:
            player_x, player_y = i.xcor(), i.ycor()
            i.goto(player_x, player_y + self.missile_speed)
            if player_y > self.screen_height / 2:
                # noinspection PyUnusedLocal
                to_del = self.player_missiles.pop(self.player_missiles.index(i))
                del to_del
            else:
                for j in self.all_invaders:
                    if are_collision_x_y_cond_met(j, i, 15, 10):
                        # 10 points for hitting invader:
                        self.score_current += 10
                        self.update_score()
                        i.goto(1500, 1500)
                        j.goto(1500, 1500)
                        # noinspection PyUnusedLocal
                        del_m = self.player_missiles.pop(self.player_missiles.index(i))
                        del del_m
                        # noinspection PyUnusedLocal
                        del_t = self.all_invaders.pop(self.all_invaders.index(j))
                        del del_t
                if are_collision_x_y_cond_met(self.saucer, i, 35, 15):
                    i.goto(1500, 1500)
                    # noinspection PyUnusedLocal
                    del_m = self.player_missiles.pop(self.player_missiles.index(i))
                    del del_m
                    # Get 100 points for UAP hit:
                    self.score_current += 100
                    self.update_score()
                    self.saucer_x = self.screen_width / 2 + 50
                    self.saucer.teleport(self.saucer_x, self.saucer_y)
                    # Heal shields for 'classic' UAP hit:
                    if self.saucer.shape() == 'classic':
                        for k in self.shields:
                            k.color(SHIELD_STAGES[0])
                    # Bonus 10 second rapid fire for 'circle' UAP hit:
                    elif self.saucer.shape() == 'circle':
                        self.player_reload_time = int(self.player_reload_time * .5)
                        self.screen.ontimer(self.player_reload_time_reset, 10000)
                    self.saucer_freq_tracker = 0
                    low = self.saucer_freq_low
                    high = self.saucer_freq_high
                    self.saucer_freq = random.randint(low, high)
                # Check for friendly-fire and degrade shields accordingly:
                for shield in self.shields:
                    if are_collision_x_y_cond_met(shield, i, 25, 20):
                        i.goto(1500, 1500)
                        # noinspection PyUnusedLocal
                        to_del = self.player_missiles.pop(self.player_missiles.index(i))
                        del to_del
                        curr_ind = SHIELD_STAGES.index(shield.color()[0])
                        new_ind = curr_ind + 1
                        if new_ind <= len(SHIELD_STAGES) - 1:
                            new_color = SHIELD_STAGES[new_ind]
                            shield.color(new_color)
                        else:
                            shield.goto(1500, 1500)
                            # noinspection PyUnusedLocal
                            del_s = self.shields.pop(self.shields.index(shield))
                            del del_s

    def player_reload_time_reset(self):
        self.player_reload_time = self.player_reload_time_init

    def deploy_player(self):
        self.player = Turtle()
        self.player.shape('square')
        self.player.turtlesize(stretch_wid=2.75, stretch_len=2.5, outline=0)
        # print(self.player.get_shapepoly())  # For development
        # print(self.player.shapesize())  # For development
        self.player.invader_width = self.player.shapesize()[0]  # Get player width
        self.player_start_x = -self.player.invader_width / 2  # Center player
        # Position player at comfortable y-coordinate:
        self.player_start_y = -self.screen_height / 2 + self.screen_height / 15
        self.player.color(PLAYER_COLOR)
        self.player.penup()
        self.player.setheading(90)
        self.player.goto(self.player_start_x, self.player_start_y)

    #  #  #  #  #  #
    # SHIELD STUFF #
    #  #  #  #  #  #
    def deploy_shields(self):
        """Instead of creating lots of shield invaders, create fewer and degrade them
        with visual cue when hit with enemy missile: let color fade on each hit until
        it's gone."""
        shield_num = 3

        # Shield x stuff:
        shield_div_x = self.screen_width / (shield_num + 1)
        shield_grid_x = -self.screen_width / 2 + shield_div_x
        shield_bits_spacing = 46
        shield_bits_x_num = 4
        shield_width = shield_bits_x_num * shield_bits_spacing

        # Shield y stuff:
        shield_grid_y = -self.screen_height / 2 + self.screen_height / 5.25

        # Create shield bits:
        stretch_length = 2.25
        stretch_factor = stretch_length * 20 / 2
        for i in range(shield_num):
            # Center each shield div:
            shield_x_begin = shield_grid_x - shield_width / 2 + stretch_factor
            for j in range(shield_bits_x_num):
                shield = Turtle()
                shield.penup()
                shield.shape('square')
                shield.turtlesize(stretch_wid=2, stretch_len=stretch_length, outline=0)
                # print(shield.get_shapepoly())  # For development
                # print(shield.shapesize())  # For development
                shield.color(SHIELD_STAGES[0])
                shield.goto(shield_x_begin, shield_grid_y)
                self.shields.append(shield)
                shield_x_begin += shield_bits_spacing
            shield_grid_x += shield_div_x

        # Get terminal y-limit for game over:
        self.terminal_y = max([i.ycor() for i in self.shields]) + 20

    #  #  #   #  #  #  #
    # SCOREBOARD STUFF #
    #  #  #   #  #  #  #
    def update_score(self):
        if not self.score_object:
            self.score_object = Turtle()
        else:
            self.score_object.clear()
        self.score_object.penup()
        self.score_object.hideturtle()
        self.score_object.color(PLAYER_COLOR)
        pos_x = -self.screen_width / 2 + self.screen_width / 20
        pos_y = self.screen_height / 2 - self.screen_height / 15
        self.score_object.goto(pos_x, pos_y)
        self.score_object.write(f"{self.score_current:04d}",
                                align="center",
                                font=("Source Sans 3 Black", 32, "italic"))

    def update_lives(self):
        if not self.lives_object:
            self.lives_object = Turtle()
        else:
            self.lives_object.clear()
        self.lives_object.penup()
        self.lives_object.hideturtle()
        self.lives_object.color(PLAYER_COLOR)
        shift_factor = (self.lives_left - 1) * self.screen_width / 95
        pos_x = self.screen_width / 2 - self.screen_width / 50 - shift_factor
        pos_y = self.screen_height / 2 - self.screen_height / 15
        self.lives_object.goto(pos_x, pos_y)
        self.lives_object.write("■" * (self.lives_left - 1),
                                align="center",
                                font=("Source Sans 3 Black", 32, "italic"))

    #  #  #  #  #
    # UAP STUFF #
    #  #  #  #  #
    def deploy_saucer(self):
        self.saucer = Turtle()
        self.saucer.penup()
        self.saucer.color(random.choice(TURTLE_COLORS))

        saucer_ind = random.randint(0, 1)

        heading_uptions = [0, 270]
        self.saucer.setheading(heading_uptions[saucer_ind])

        shape_options = ['circle', 'classic']
        self.current_saucer_shape = shape_options[saucer_ind]
        self.saucer.shape(self.current_saucer_shape)

        size_options = [(.6, 3.25, 10), (8.5, 2.5, 5)][saucer_ind]
        self.saucer.turtlesize(*size_options)

        self.saucer_x = self.screen_width / 2 + 50
        pos_y_divs = [10, 8.75]
        self.saucer_y = self.screen_height / 2 - self.screen_height / pos_y_divs[
            saucer_ind]
        self.saucer.goto(self.saucer_x, self.saucer_y)

    def saucer_flyby(self):
        if self.saucer_freq_tracker > self.saucer_freq:
            if self.saucer_x > -self.screen_width / 2 - 50:
                self.saucer_x -= self.saucer_flyby_speed
                self.saucer.teleport(self.saucer_x, self.saucer_y)
            else:
                self.saucer_x = self.screen_width / 2 + 50
                self.saucer.teleport(self.saucer_x, self.saucer_y)
                self.saucer_freq_tracker = 0
                self.saucer_freq = random.randint(self.saucer_freq_low,
                                                  self.saucer_freq_high)

    #  #   #  #   #  #
    # GAME UTILITIES #
    #  #   #  #   #  #
    def restart_game(self):
        self.screen.clear()

        # Garbage collection
        del self.all_invaders
        del self.player
        del self.score_object
        del self.lives_object
        del self.saucer
        del self.player_missiles
        del self.shields
        del self.invader_missiles

        self.__init__()
        self.begin_invasion()

    def pause_toggle(self):
        self.pause_game = not self.pause_game

    def key_listeners(self):
        """Creates key listeners for movement/pause_toggle/quit_game/restart_game
        methods."""
        self.screen.listen()
        self.screen.onkeypress(self.player_fire_missile, 'space')
        self.screen.onkeypress(self.player_left, 'Left')
        self.screen.onkeypress(self.player_right, 'Right')
        self.screen.onkeypress(self.pause_toggle, 'p')
        self.screen.onkeypress(self.quit_game, 'q')
        self.screen.onkeypress(self.restart_game, 'r')

    def quit_game(self):
        self.game_on = False
        self.screen.bye()

    def setup_pieces(self):
        self.update_score()
        self.update_lives()
        self.get_invader_positions()
        self.invader_formation()
        self.deploy_player()
        self.deploy_shields()
        self.deploy_saucer()

    def begin_invasion(self):
        self.setup_screen()
        self.screen.tracer(0)
        self.get_screen_width()
        self.setup_pieces()
        self.screen.tracer(self.tracer_val)
        self.key_listeners()
        while self.game_on:
            if not self.pause_game and self.lives_left > 0:
                self.screen.update()
                self.invader_march()
                self.player_missile_path()
                self.saucer_flyby()
            elif self.lives_left > 0:
                self.screen.update()
            else:
                self.update_lives()
                self.update_score()
                self.restart_game()
        self.screen.exitonclick()


if __name__ == "__main__":
    try:
        turtle_invaders = TurtleInvaders()
        turtle_invaders.begin_invasion()
    except (KeyboardInterrupt, Exception):
        sys.exit(1)

# Todos:
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

#  - Consider healing shields one color stage for UAP hit:
#     curr_color_ind = SHIELD_STAGES.index(k.color()[0])
#     heal_color_ind = max(0, curr_color_ind - 1)
#     k.color(SHIELD_STAGES[heal_color_ind])

#  - Add functionality for subsequent rounds.

#  - Remedy names/concerns regarding game restart -- come up with better cases for
#     while loop, diversify functionality
