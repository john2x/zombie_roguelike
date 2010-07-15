
def get_area_around_entity(entity, area_w, area_h, total_w, total_h):
    """ Gets area within the map around an entity. """
    start_y = entity.y - area_h / 2
    end_y = entity.y + area_h / 2
    start_x = entity.x - area_w / 2
    end_x = entity.x + area_w / 2

    if start_y < 0:
        start_y = 0
        end_y = area_h
    elif end_y >= total_h:
        start_y = total_h - area_h
        end_y = total_h
    if start_x < 0:
        start_x = 0
        end_x = area_w
    elif end_x >= total_w:
        start_x = total_w - area_w
        end_x = total_w

    return {'start_x':start_x, 'start_y':start_y,
            'end_x':end_x, 'end_y':end_y}

def get_tile_distance(entity1, entity2):
    pass
def get_area(area_w, area_h, total_w, total_h):
    pass

