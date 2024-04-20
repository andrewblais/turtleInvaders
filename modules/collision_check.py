def is_collision_x_cond_met(obj, missile, space):
    obj_x = obj.xcor()
    half_w = obj.shapesize()[1] / 2
    x_cond = obj_x - (half_w + space) <= missile.xcor() <= obj_x + (half_w + space)
    return x_cond


def is_collision_y_cond_met(obj, missile, space):
    obj_y = obj.ycor()
    half_h = obj.shapesize()[0] / 2
    y_cond = obj_y - (half_h + space) <= missile.ycor() <= obj_y + (half_h + space)
    return y_cond


def are_collision_x_y_cond_met(obj, missile, space_x, space_y):
    x_cond_met = is_collision_x_cond_met(obj, missile, space_x)
    y_cond_met = is_collision_y_cond_met(obj, missile, space_y)
    return x_cond_met and y_cond_met

# Note: subtract/add half vertical shape length to get 'tip' of missile.
