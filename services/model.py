from ai import loaded_model as model

LIGHT_THRESHOLD = 2000
HUMIDITY_THRESHOLD = 700

def can_turn_on_pump(humidity: float):
    return humidity >= HUMIDITY_THRESHOLD


def can_turn_on_light(light: float):
    return light >= LIGHT_THRESHOLD

def is_turn_on_pump(humidity: float, light: float):
    return model.predict(humidity, light)