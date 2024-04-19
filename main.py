from turtle import Screen, Turtle
import random
from screeninfo import get_monitors
import sys

from config.config import *
from util.util import *


class TurtleInvaders:
    def __init__(self,
                 turtle_march_speed: int | float = 1,
                 turtle_march_speed_increase: int | float = .5,
                 turtle_movement_vert: int = 10,
                 patriot_reload_time: int = 1000,
                 uap_flyby_speed: int = 5,
                 sam_speed: int = 10):
        self.screen = None
        self.formation_div_x = 6
        self.formation_div_y = 4
        self.monitor_width = 1920
        self.monitor_height = 1080
        self.screen_stretch_x = .65
        self.screen_stretch_y = .8
        self.screen_width = 1248
        self.screen_height = 810
        self.turtle_formation_width = 1440
        self.formation_gutter_factor = .7  # Smaller val = bigger L-R gutters
        self.patriot = None
        self.patriot_start_x = -2
        self.patriot_start_y = -350
        self.turtle_positions = []
        self.all_turtles = []
        self.score_object = None
        self.score_current = 0
        self.lives_object = None
        self.lives_left = 3
        self.uap = None
        self.uap_x = 0
        self.uap_y = 0
        self.round_number = 1
        self.uap_freq_tracker = 0
        # Note...work on math to see direct relation of tracer to seconds:
        self.uap_freq_low = 10  # Means about an 8-second UAP delay
        self.uap_freq_high = 22  # Means about a 20-second UAP delay
        # Allow variation in delay of UAPs:
        self.uap_freq = random.randint(self.uap_freq_low, self.uap_freq_high)
        self.turtle_march_speed = turtle_march_speed
        self.turtle_march_speed_increase = turtle_march_speed_increase
        self.turtle_movement_vert = turtle_movement_vert
        self.uap_flyby_speed = uap_flyby_speed
        self.turtles_have_reversed = False  # Flag indicating turtles have changed direction
        self.pause_game = False
        self.game_on = True
        self.patriot_sams = []
        self.sam_has_fired = False
        self.patriot_reload_time_init = patriot_reload_time
        self.patriot_reload_time = self.patriot_reload_time_init
        self.sam_speed = sam_speed
        self.turtles_to_pop_ind = []
        self.shields = []
        self.tracer_val = 25
        self.turtle_hellfires = []
        self.hellfire_speed = 15
        self.turtle_has_fired = False
        self.hellfire_barrage_begun = False
        self.hellfire_freq = (500, 5000)  # Divide by 1000 for seconds

    #  #  #  #  #  #
    # SCREEN STUFF #
    #  #  #  #  #  #
    def setup_screen(self):
        self.screen = Screen()
        self.screen.title("Turtle Invaders")
        self.screen.colormode(255)
        self.screen.bgcolor('gray0')

        monitor = get_monitors()[0]
        self.monitor_width = monitor.width
        self.monitor_height = monitor.height
        self.screen_width = int(self.monitor_width * self.screen_stretch_x)
        self.screen_height = int(self.monitor_height * self.screen_stretch_y)
        screen_pos_x = (self.monitor_width - self.screen_width) // 2
        screen_pos_y = (self.monitor_height - self.screen_height) // 2

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
    def get_turtle_row_index(number, round_number):
        for key, value in TURTLE_COLOR_INDEX_DICT.items():
            if number in key:
                return (value + round_number) % len(TURTLE_COLORS)
        raise ValueError(f"Number {number} not in any range key.")

    def turtle_change_dir(self):
        if self.turtle_march_speed < 1:
            self.turtle_march_speed -= 1
        else:
            self.turtle_march_speed += 1
        self.turtle_march_speed *= -self.turtle_march_speed_increase

    def reset_turtle_flag(self):
        self.turtles_have_reversed = False

    def turtle_march(self):
        right_limit = self.screen_width / 2
        left_limit = -right_limit

        min_turtle = min([i.xcor() for i in self.all_turtles])
        max_turtle = max([i.xcor() for i in self.all_turtles])

        if min_turtle - 30 < left_limit and not self.turtles_have_reversed:
            self.turtle_change_dir()
            turtle_movement_vert = self.turtle_movement_vert
            self.turtles_have_reversed = True
            self.screen.ontimer(self.reset_turtle_flag, 5)
        elif max_turtle + 35 > right_limit and not self.turtles_have_reversed:
            self.turtle_change_dir()
            turtle_movement_vert = self.turtle_movement_vert
            self.turtles_have_reversed = True
            self.screen.ontimer(self.reset_turtle_flag, 5)
        else:
            turtle_movement_vert = 0

        rand_dec = random.randint(71, 79) / 100
        rand_stretch = 1 + rand_dec

        for i in self.all_turtles:
            # UAP freq tied to turtle marching. The following equation makes
            #  self.uap_freq_tracker increment approx 1.0 per second:
            self.uap_freq_tracker += self.tracer_val / 10000
            i.turtlesize(stretch_wid=rand_stretch, stretch_len=rand_stretch)
            i.teleport(i.xcor() - self.turtle_march_speed,
                       i.ycor() - turtle_movement_vert)
            # Random first turtle to fire:
            if not self.hellfire_barrage_begun:
                self.hellfire_barrage_begun = True
                self.turtle_has_fired = True
                first = random.choice(self.all_turtles)
                hellfire = self.deploy_turtle_hellfire()
                hellfire.color(first.color()[0])
                hellfire.goto(first.xcor(), first.ycor() - 20)
                self.turtle_hellfires.append(hellfire)
                delay = random.randint(*self.hellfire_freq)
                self.screen.ontimer(self.reset_turtle_has_fired_flag, delay)
            elif not self.turtle_has_fired:
                self.turtle_has_fired = True
                hellfire = self.deploy_turtle_hellfire()
                hellfire.color(i.color()[0])
                hellfire.goto(i.xcor(), i.ycor() - 20)
                self.turtle_hellfires.append(hellfire)
                delay = random.randint(*self.hellfire_freq)
                self.screen.ontimer(self.reset_turtle_has_fired_flag, delay)
            for j in self.turtle_hellfires:
                j.goto(j.xcor(), j.ycor() - 1)
                if j.ycor() < -self.screen_height / 2:
                    j.goto(-1500, 0)
                    self.turtle_hellfires.pop(self.turtle_hellfires.index(j))

    def reset_turtle_has_fired_flag(self):
        self.turtle_has_fired = False

    @staticmethod
    def deploy_turtle_hellfire():
        hellfire = Turtle()
        hellfire.shape('square')
        hellfire.turtlesize(stretch_wid=.075, stretch_len=.8, outline=2)
        hellfire.penup()
        hellfire.setheading(270)
        return hellfire

    def get_turtle_positions(self):
        self.turtle_formation_width = self.screen_width * self.formation_gutter_factor
        turtle_grid_width = self.turtle_formation_width / self.formation_div_x
        turtle_grid_height = self.screen_height / self.formation_div_y

        for x in range(self.formation_div_x):
            for y in range(self.formation_div_y):
                start_x = -self.turtle_formation_width / 2
                spacing_x = turtle_grid_width * x
                center_x = turtle_grid_width / 2
                pos_x = start_x + spacing_x + center_x

                # Add higher number to shift formation higher along y-axis:
                start_y = -turtle_grid_height / 2 + 50
                # Make divisor larger to compress rows along on y-axis:
                spacing_y = turtle_grid_height * y / 3
                center_y = turtle_grid_height / 2
                pos_y = start_y + spacing_y + center_y

                self.turtle_positions.append((pos_x, pos_y))

    def turtle_formation(self):
        for i in range(len(self.turtle_positions)):
            single_turtle = Turtle()
            single_turtle.shape('turtle')
            single_turtle.speed('slowest')
            single_turtle.turtlesize(stretch_wid=1.75, stretch_len=1.75)
            color_ind = self.get_turtle_row_index(i, self.round_number)
            single_turtle.color(TURTLE_COLORS[color_ind])
            single_turtle.penup()
            single_turtle.setheading(270)
            single_turtle.goto(self.turtle_positions[i][0], self.turtle_positions[i][1])
            self.all_turtles.append(single_turtle)
            # For development only, to identify turtle indices easily:
            # turtle.write(i, align="center", font=("Source Sans 3 Black", 24, "italic"))

    #  #  #  #   #  #  #  #
    #  PATRIOT SAM STUFF  #
    #  #  #  #   #  #  #  #
    def patriot_left(self):
        if self.patriot.xcor() > -self.screen_width / 2 + 50:
            x_pos = self.patriot.xcor() - 10
            self.patriot.goto(x_pos, self.patriot.ycor())

    def patriot_right(self):
        if self.patriot.xcor() < self.screen_width / 2 - 55:
            x_pos = self.patriot.xcor() + 10
            self.patriot.goto(x_pos, self.patriot.ycor())

    def reset_sam_has_fired_flag(self):
        self.sam_has_fired = False

    def patriot_fire_sam(self):
        if not self.sam_has_fired:
            patriot_sam = Turtle()
            patriot_sam.shape('square')
            patriot_sam.turtlesize(stretch_wid=.1, stretch_len=1.05, outline=2.5)
            patriot_sam.penup()
            patriot_sam.color(PLAYER_COLOR)
            patriot_sam.setheading(90)
            patriot_sam.goto(self.patriot.xcor(), self.patriot.ycor() + 35)
            self.patriot_sams.append(patriot_sam)
            self.sam_has_fired = True
            self.screen.ontimer(self.reset_sam_has_fired_flag, self.patriot_reload_time)

    def sam_path(self):
        for i in self.patriot_sams:
            patriot_x, patriot_y = i.xcor(), i.ycor()
            i.goto(patriot_x, patriot_y + self.sam_speed)
            if patriot_y > self.screen_height / 2:
                self.patriot_sams.pop(self.patriot_sams.index(i))
            else:
                for j in self.all_turtles:
                    if are_collision_x_y_cond_met(j, i, 15, 10):
                        self.score_current += 10
                        self.update_scoreboard()
                        i.goto(-1500, 0)
                        j.goto(-1500, 0)
                        self.patriot_sams.pop(self.patriot_sams.index(i))
                        self.all_turtles.pop(self.all_turtles.index(j))
                if are_collision_x_y_cond_met(self.uap, i, 35, 15):
                    i.goto(-1500, 0)
                    self.patriot_sams.pop(self.patriot_sams.index(i))
                    self.score_current += 50
                    self.update_scoreboard()
                    self.uap_x = self.screen_width / 2 + 50
                    self.uap.teleport(self.uap_x, self.uap_y)
                    # Bonus rapid fire for UAP hit:
                    self.patriot_reload_time = int(self.patriot_reload_time * .5)
                    self.screen.ontimer(self.patriot_reload_time_reset, 5000)
                    self.uap_freq_tracker = 0
                    low = self.uap_freq_low
                    high = self.uap_freq_high
                    self.uap_freq = random.randint(low, high) * .01
                # Check for friendly-fire and degrade shields accordingly:
                for shield in self.shields:
                    if are_collision_x_y_cond_met(shield, i, 25, 20):
                        i.goto(-1500, 0)
                        self.patriot_sams.pop(self.patriot_sams.index(i))
                        curr_ind = SHIELD_STAGES.index(shield.color()[0])
                        new_ind = curr_ind + 1
                        if new_ind <= len(SHIELD_STAGES) - 1:
                            new_color = SHIELD_STAGES[new_ind]
                            shield.color(new_color)
                        else:
                            shield.goto(-1500, 0)
                            self.shields.pop(self.shields.index(shield))

    def patriot_reload_time_reset(self):
        self.patriot_reload_time = self.patriot_reload_time_init

    def deploy_patriot(self):
        self.patriot = Turtle()
        self.patriot.shape('triangle')
        self.patriot.turtlesize(stretch_wid=4, stretch_len=2, outline=5)
        self.patriot.turtle_width = self.patriot.shapesize()[0]  # Get patriot width
        self.patriot_start_x = -self.patriot.turtle_width / 2  # Center patriot
        # Position patriot at comfortable y-coordinate:
        self.patriot_start_y = -self.screen_height / 2 + self.screen_height / 15
        self.patriot.color(PLAYER_COLOR)
        self.patriot.penup()
        self.patriot.setheading(90)
        self.patriot.goto(self.patriot_start_x, self.patriot_start_y)

    #  #  #  #  #  #
    # SHIELD STUFF #
    #  #  #  #  #  #
    def deploy_shields(self):
        """Instead of creating lots of shield turtles, create fewer and degrade them
        with visual cue when hit with enemy sam: let color fade on each hit until
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
                shield.color(SHIELD_STAGES[0])
                shield.goto(shield_x_begin, shield_grid_y)
                self.shields.append(shield)
                shield_x_begin += shield_bits_spacing
            shield_grid_x += shield_div_x

    #  #  #   #  #  #  #
    # SCOREBOARD STUFF #
    #  #  #   #  #  #  #
    def inititalize_score(self):
        self.score_object = Turtle()
        self.score_object.penup()
        self.score_object.hideturtle()
        self.score_object.color(PLAYER_COLOR)
        pos_x = -self.screen_width / 2 + self.screen_width / 20
        pos_y = self.screen_height / 2 - self.screen_height / 15
        self.score_object.goto(pos_x, pos_y)
        self.score_object.write(f"{self.score_current:04d}",
                                align="center",
                                font=("Source Sans 3 Black", 32, "italic"))

    def inititalize_lives(self):
        self.lives_object = Turtle()
        self.lives_object.penup()
        self.lives_object.hideturtle()
        self.lives_object.color(PLAYER_COLOR)

        shift_factor = (self.lives_left - 1) * self.screen_width / 95
        pos_x = self.screen_width / 2 - self.screen_width / 50 - shift_factor
        pos_y = self.screen_height / 2 - self.screen_height / 15
        self.lives_object.goto(pos_x, pos_y)

        self.lives_object.write("▲" * (self.lives_left - 1),
                                align="center",
                                font=("Source Sans 3 Black", 32, "italic"))

    def update_scoreboard(self):
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

    #  #  #  #  #
    # UAP STUFF #
    #  #  #  #  #
    def uap_sighting(self):
        self.uap = Turtle()
        self.uap.penup()
        self.uap.color(random.choice(TURTLE_COLORS))

        uap_ind = random.randint(0, 1)

        heading_uptions = [0, 270]
        self.uap.setheading(heading_uptions[uap_ind])

        shape_options = ['circle', 'classic']
        self.uap.shape(shape_options[uap_ind])

        size_options = [(.6, 3.25, 10), (8.5, 2.5, 5)][uap_ind]
        self.uap.turtlesize(*size_options)

        # pos_x = random.randint(int(-self.screen_width / 2), int(self.screen_width / 2))
        self.uap_x = self.screen_width / 2 + 50
        pos_y_divs = [10, 8.75]
        self.uap_y = self.screen_height / 2 - self.screen_height / pos_y_divs[uap_ind]
        self.uap.goto(self.uap_x, self.uap_y)

    def uap_flyby(self):
        # print(self.uap_freq_tracker, self.uap_freq)  # Uncomment for development/testing
        if self.uap_freq_tracker > self.uap_freq:
            if self.uap_x > -self.screen_width / 2 - 50:
                self.uap_x -= self.uap_flyby_speed
                self.uap.teleport(self.uap_x, self.uap_y)
            else:
                self.uap_x = self.screen_width / 2 + 50
                self.uap.teleport(self.uap_x, self.uap_y)
                self.uap_freq_tracker = 0
                self.uap_freq = random.randint(self.uap_freq_low,
                                               self.uap_freq_high) * .01

    #  #   #  #   #  #
    # GAME UTILITIES #
    #  #   #  #   #  #
    def restart_game(self):
        self.screen.clear()
        self.__init__()
        self.begin_invasion()

    def pause_toggle(self):
        self.pause_game = not self.pause_game

    def key_listeners(self):
        """Creates key listeners for movement/pause_toggle/quit_game/restart_game methods."""
        self.screen.listen()
        self.screen.onkeypress(self.patriot_fire_sam, 'space')
        self.screen.onkeypress(self.patriot_left, 'Left')
        self.screen.onkeypress(self.patriot_right, 'Right')
        self.screen.onkeypress(self.pause_toggle, 'p')
        self.screen.onkeypress(self.quit_game, 'q')
        self.screen.onkeypress(self.restart_game, 'r')

    def quit_game(self):
        self.screen.bye()

    def setup_pieces(self):
        self.inititalize_score()
        self.inititalize_lives()
        self.get_turtle_positions()
        self.turtle_formation()
        self.deploy_patriot()
        self.deploy_shields()
        self.uap_sighting()

    def begin_invasion(self):
        self.setup_screen()
        self.screen.tracer(0)
        self.get_screen_width()
        self.setup_pieces()
        # self.screen.tracer(20)
        self.screen.tracer(self.tracer_val)
        self.key_listeners()
        while self.lives_left > 0:
            while self.game_on:
                if not self.pause_game:
                    self.screen.update()
                    self.turtle_march()
                    self.sam_path()
                    self.uap_flyby()
                else:
                    self.screen.update()
        self.screen.exitonclick()


if __name__ == "__main__":
    try:
        turtle_invaders = TurtleInvaders()
        turtle_invaders.begin_invasion()
    except (KeyboardInterrupt, Exception) as e:
        print(f"Error: {e}")
        sys.exit(1)
