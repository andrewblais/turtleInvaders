# This module contains functions for detecting collisions between game elements.

def is_collision_x_cond_met(obj, missile, space):
    """
    Determines if a collision occurs along the x-axis within a specified buffer space.

    :param obj: The game object, typically an invader or shield.
    :type obj: Turtle
    :param missile: The projectile object, usually a player missile or invader bomb.
    :type missile: Turtle
    :param space: The buffer space around the object's x-coordinate.
    :type space: float
    :return: True if a collision is detected, False otherwise.
    :rtype: bool
    """
    obj_x = obj.xcor()
    half_w = obj.shapesize()[1] / 2
    x_cond = obj_x - (half_w + space) <= missile.xcor() <= obj_x + (half_w + space)
    return x_cond


def is_collision_y_cond_met(obj, missile, space):
    """
    Determines if a collision occurs along the y-axis within a specified buffer space.

    :param obj: The game object, typically an invader or shield.
    :type obj: Turtle
    :param missile: The projectile object, usually a player missile or invader bomb.
    :type missile: Turtle
    :param space: The buffer space around the object's y-coordinate.
    :type space: float
    :return: True if a collision is detected, False otherwise.
    :rtype: bool
    """
    obj_y = obj.ycor()
    half_h = obj.shapesize()[0] / 2
    y_cond = obj_y - (half_h + space) <= missile.ycor() <= obj_y + (half_h + space)
    return y_cond


def are_collision_x_y_cond_met(obj, missile, space_x, space_y):
    """
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
    """
    x_cond_met = is_collision_x_cond_met(obj, missile, space_x)
    y_cond_met = is_collision_y_cond_met(obj, missile, space_y)
    return x_cond_met and y_cond_met
