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


def are_collision_x_y_cond_met(obj, missile, space_x, space_y):
    x_cond_met = is_collision_x_cond_met(obj, missile, space_x)
    y_cond_met = is_collision_y_cond_met(obj, missile, space_y)
    return x_cond_met and y_cond_met
