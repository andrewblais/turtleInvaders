from turtle import Screen, Turtle
import random
from screeninfo import get_monitors
import sys

from config.config import *


def is_collision_x_cond_met(obj, missile, space):
    obj_x = obj.xcor()
    obj_w = obj.shapesize()[1] * 1
    x_cond = obj_x - (obj_w / 2 + space) <= missile.xcor() <= obj_x + (obj_w / 2 + space)
    return x_cond


def is_collision_y_cond_met(obj, missile, space):
    obj_y = obj.ycor()
    obj_h = obj.shapesize()[0] * 1
    y_cond = obj_y - (obj_h / 2 + space) <= missile.ycor() <= obj_y + (obj_h / 2 + space)
    return y_cond


def are_collision_x_y_cond_met(obj, missile, space):
    x_cond_met = is_collision_x_cond_met(obj, missile, space)
    y_cond_met = is_collision_y_cond_met(obj, missile, space)
    return x_cond_met and y_cond_met


class TurtleInvaders:
    def __init__(self):
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
        self.formation_gutter_factor = .7  # Smaller val for bigger L-R gutters
        self.turtle_grid_width = 208
        self.turtle_grid_height = 208
        self.player = None
        self.player_start_x = -2
        self.player_start_y = -350
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
        self.time_tracker = 0
        self.uap_sec_low = 1000
        self.uap_sec_high = 3000
        self.uap_freq = random.randint(self.uap_sec_low, self.uap_sec_high) * .01
        self.turtle_movement_horiz = -5
        self.turtles_have_reversed = False  # Flag indicating turtles have changed direction
        self.pause_game = False
        self.game_on = True
        self.player_missiles = []
        self.player_has_fired = False
        # self.player_reload_time = random.randint(2000, 5000)
        self.player_reload_time = 2500
        self.turtles_to_pop_ind = []

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

    def get_turtle_positions(self):
        self.turtle_formation_width = self.screen_width * self.formation_gutter_factor
        self.turtle_grid_width = self.turtle_formation_width / self.formation_div_x
        self.turtle_grid_height = self.screen_height / self.formation_div_y

        for x in range(self.formation_div_x):
            for y in range(self.formation_div_y):
                start_x = -self.turtle_formation_width / 2
                spacing_x = self.turtle_grid_width * x
                center_x = self.turtle_grid_width / 2
                pos_x = start_x + spacing_x + center_x

                # Add higher number to shift formation higher along y-axis:
                start_y = -self.turtle_grid_height / 2 + 50
                # Make divisor larger to compress rows along on y-axis:
                spacing_y = self.turtle_grid_height * y / 3
                center_y = self.turtle_grid_height / 2
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

    @staticmethod
    def get_turtle_row_index(number, round_number):
        for key, value in TURTLE_COLOR_INDEX_DICT.items():
            if number in key:
                return (value + round_number) % len(TURTLE_COLORS)
        raise ValueError(f"Number {number} not in any range key.")

    def deploy_player(self):
        self.player = Turtle()
        self.player.shape('triangle')
        self.player.turtlesize(stretch_wid=4, stretch_len=2, outline=5)
        self.player.turtle_width = self.player.shapesize()[0]  # Get player width
        self.player_start_x = -self.player.turtle_width / 2  # Center player
        # Position player at comfortable y-coordinate:
        self.player_start_y = -self.screen_height / 2 + self.screen_height / 15
        self.player.color(PLAYER_COLOR)
        self.player.penup()
        self.player.setheading(90)
        self.player.goto(self.player_start_x, self.player_start_y)

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

    # 'arrow', 'turtle', 'circle', 'square', 'triangle', 'classic'
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
        # print(self.time_tracker, self.uap_freq)
        if self.time_tracker > self.uap_freq:
            if self.uap_x > -self.screen_width / 2 - 50:
                self.uap_x -= 10
                self.uap.teleport(self.uap_x, self.uap_y)
            else:
                self.uap_x = self.screen_width / 2 + 50
                self.uap.teleport(self.uap_x, self.uap_y)
                self.time_tracker = 0
                self.uap_freq = random.randint(self.uap_sec_low, self.uap_sec_high) * .01

    def player_left(self):
        if self.player.xcor() > -self.screen_width / 2 + 50:
            x_pos = self.player.xcor() - 10
            self.player.goto(x_pos, self.player.ycor())

    def player_right(self):
        if self.player.xcor() < self.screen_width / 2 - 55:
            x_pos = self.player.xcor() + 10
            self.player.goto(x_pos, self.player.ycor())

    def reset_player_has_fired_flag(self):
        self.player_has_fired = False

    def player_fire(self):
        if not self.player_has_fired:
            player_missile = Turtle()
            player_missile.shape('square')
            player_missile.turtlesize(stretch_wid=.1, stretch_len=1.05, outline=2.5)
            player_missile.penup()
            player_missile.color(PLAYER_COLOR)
            player_missile.setheading(90)
            player_missile.goto(self.player.xcor(), self.player.ycor() + 35)
            self.player_missiles.append(player_missile)
            self.player_has_fired = True
            self.screen.ontimer(self.reset_player_has_fired_flag,
                                self.player_reload_time)

    def player_missile_path(self):
        for i in self.player_missiles:
            player_x, player_y = i.xcor(), i.ycor()
            i.goto(player_x, player_y + 30)
            if player_y > self.screen_height / 2:
                self.player_missiles.pop(self.player_missiles.index(i))
            # # # # # # # # #
            # # # # # # # # #
            # # # # # # # # #
            # # # # # # # # #
            # # # # # # # # #
            # # # # # # # # #
            # # # # # # # # #
            # # # # # # # # #
            # # # # # # # # #
            else:
                for j in self.all_turtles:
                    if are_collision_x_y_cond_met(j, i, 15):
                        i.goto(-1500, 0)
                        j.goto(-1500, 0)
                        self.player_missiles.pop(self.player_missiles.index(i))
                        self.all_turtles.pop(self.all_turtles.index(j))

    def check_player_destroyed(self):
        pass

    def restart_game(self):
        self.screen.clear()
        self.__init__()
        self.begin_invasion()

    def pause_toggle(self):
        self.pause_game = not self.pause_game

    def key_listeners(self):
        """Creates key listeners for movement/pause_toggle/quit_game/restart_game methods."""
        self.screen.listen()
        self.screen.onkeypress(self.player_fire, 'space')
        self.screen.onkeypress(self.player_left, 'Left')
        self.screen.onkeypress(self.player_right, 'Right')
        self.screen.onkeypress(self.pause_toggle, 'p')
        self.screen.onkeypress(self.quit_game, 'q')
        self.screen.onkeypress(self.restart_game, 'r')

    def turtle_change_dir(self):
        self.turtle_movement_horiz *= -1

    def reset_turtle_flag(self):
        self.turtles_have_reversed = False

    def turtle_march(self):
        right_limit = self.screen_width / 2
        left_limit = -right_limit

        min_turtle = min([i.xcor() for i in self.all_turtles])
        max_turtle = max([i.xcor() for i in self.all_turtles])

        if min_turtle - 30 < left_limit and not self.turtles_have_reversed:
            self.turtle_change_dir()
            turtle_movement_vert = -10
            self.turtles_have_reversed = True
            self.screen.ontimer(self.reset_turtle_flag, 5)
        elif max_turtle + 35 > right_limit and not self.turtles_have_reversed:
            self.turtle_change_dir()
            turtle_movement_vert = -10
            self.turtles_have_reversed = True
            self.screen.ontimer(self.reset_turtle_flag, 5)
        else:
            turtle_movement_vert = 0

        rand_dec = random.randint(50, 75) / 100
        rand_stretch = 1 + rand_dec

        for i in self.all_turtles:
            self.time_tracker += .01
            i.turtlesize(stretch_wid=rand_stretch, stretch_len=rand_stretch)
            i.teleport(i.xcor() + self.turtle_movement_horiz,
                       i.ycor() + turtle_movement_vert)

    def check_turtle_destroyed(self):
        pass

    def quit_game(self):
        self.screen.bye()

    def setup_pieces(self):
        self.inititalize_score()
        self.inititalize_lives()
        self.get_turtle_positions()
        self.turtle_formation()
        self.deploy_player()
        self.uap_sighting()

    def begin_invasion(self):
        self.setup_screen()
        self.screen.tracer(0)
        self.get_screen_width()
        self.setup_pieces()
        self.screen.tracer(2)
        self.key_listeners()
        while self.lives_left > 0:
            while self.game_on:
                if not self.pause_game:
                    self.screen.update()
                    self.turtle_march()
                    self.player_missile_path()
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
