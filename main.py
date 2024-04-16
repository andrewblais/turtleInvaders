from turtle import Screen, Turtle
import random
from screeninfo import get_monitors

from config.config import *


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
        self.cannon = None
        self.cannon_start_x = -2
        self.cannon_start_y = -350
        self.turtle = None
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

    def deploy_cannon(self):
        self.cannon = Turtle()
        self.cannon.shape('triangle')
        self.cannon.turtlesize(stretch_wid=4, stretch_len=2, outline=5)
        self.cannon.turtle_width = self.cannon.shapesize()[0]  # Get cannon width
        self.cannon_start_x = -self.cannon.turtle_width / 2  # Center cannon
        # Position cannon at comfortable y-coordinate:
        self.cannon_start_y = -self.screen_height / 2 + self.screen_height / 15
        self.cannon.color(PLAYER_COLOR)
        self.cannon.penup()
        self.cannon.setheading(90)
        self.cannon.goto(self.cannon_start_x, self.cannon_start_y)

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
        print(self.time_tracker, self.uap_freq)
        if self.time_tracker > self.uap_freq:
            if self.uap_x > -self.screen_width / 2 - 50:
                self.uap_x -= 10
                self.uap.teleport(self.uap_x, self.uap_y)
            else:
                self.uap_x = self.screen_width / 2 + 50
                self.uap.teleport(self.uap_x, self.uap_y)
                self.time_tracker = 0
                self.uap_freq = random.randint(self.uap_sec_low, self.uap_sec_high) * .01

    def cannon_fire(self):
        pass

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

    def check_cannon_destroyed(self):
        pass

    def setup_pieces(self):
        self.inititalize_score()
        self.inititalize_lives()
        self.get_turtle_positions()
        self.turtle_formation()
        self.deploy_cannon()
        self.uap_sighting()

    def begin_invasion(self):
        self.setup_screen()
        self.screen.tracer(0)
        self.get_screen_width()
        self.setup_pieces()
        self.screen.tracer(2)
        while self.lives_left > 0:
            self.turtle_march()
            self.uap_flyby()
        self.screen.exitonclick()


if __name__ == "__main__":
    turtle_invaders = TurtleInvaders()
    turtle_invaders.begin_invasion()
