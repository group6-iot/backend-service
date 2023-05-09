from actions import Device as DeviceAction
from helpers import parse_enviroment_capture
from models.device import DeviceMode, DeviceStatus
from repositories import Device, Enviroment
from services.model import can_turn_on_light, can_turn_on_pump, is_turn_on_pump
from services.cache import CACHE
from services.logging import LOGGER


def capture(raw_payload: str):
    enviroment = parse_enviroment_capture(raw_payload)
    CACHE.set("enviroment:latest", enviroment)
    pump = Device.find_one({"name": "Pump"})
    light = Device.find_one({"name": "Light"})

    if pump["mode"] == DeviceMode.AUTO:
        humidity = enviroment["humidity"]
        light_value = enviroment["light"]
        # status = DeviceStatus.ON if can_turn_on_pump(humidity) else DeviceStatus.OFF
        status = DeviceStatus.ON if is_turn_on_pump(humidity, light_value) else DeviceStatus.OFF
        LOGGER.info(f"status {status}")
        if pump["status"] != status:
            DeviceAction.set_status(pump, status, must_be_manual=False)

    if light["mode"] == DeviceMode.AUTO:
        status = DeviceStatus.ON if can_turn_on_light(enviroment["light"]) else DeviceStatus.OFF
        if light["status"] != status:
            DeviceAction.set_status(light, status, must_be_manual=False)

    return Enviroment.create(enviroment)


def get_latest_capture():
    return CACHE.get("enviroment:latest", {})
