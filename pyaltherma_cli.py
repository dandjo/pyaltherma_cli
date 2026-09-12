import asyncio
import aiohttp
import argparse
import inspect
import json
import os

from pyaltherma.comm import DaikinWSConnection
from pyaltherma.controllers import AlthermaController
from pyaltherma.const import ClimateControlMode


ALTHERMA_HOST = os.environ.get('PYALTHERMA_HOST')
ALTHERMA_TIMEOUT = float(os.environ.get('PYALTHERMA_TIMEOUT', 3))


async def resolve(value):
    if inspect.iscoroutinefunction(value):
        return await value()
    if inspect.isawaitable(value):
        return await value
    return value

async def create_coro(value, callback, output, prop):
    output[prop] = callback(await resolve(value))

def create_task(tasks, *args):
    tasks.append(asyncio.create_task(create_coro(*args)))

def parse_switch(value):
    if value.upper() == 'ON' or value == '1':
        return True
    if value.upper() == 'OFF' or value == '0':
        return False
    return None

async def write(current, normalize, value, operation):
    """Calls the write operation only if the normalized current state of the unit differs from the value."""
    try:
        if normalize(await resolve(current)) == value:
            return
    except Exception:
        pass  # current state unknown, write anyway
    await operation()

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-prop', metavar=('prop', 'value'), nargs='+', action='append', type=str)
    args = parser.parse_args()
    json_data = {}
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(ALTHERMA_TIMEOUT)) as session:
        conn = DaikinWSConnection(session, ALTHERMA_HOST, ALTHERMA_TIMEOUT)
        device = AlthermaController(conn)
        await device.discover_units()
        if not args.prop:
            args.prop = [
                ['dhw_power'],
                ['dhw_temp'],
                ['dhw_target_temp'],
                ['dhw_temp_heating'],
                ['dhw_powerful'],
                ['indoor_temp'],
                ['outdoor_temp'],
                ['climate_control_heating_config'],
                ['climate_control_cooling_config'],
                ['climate_control_power'],
                ['climate_control_mode'],
                ['leaving_water_temp_current'],
                ['leaving_water_temp_offset_heating'],
                ['leaving_water_temp_offset_cooling'],
                ['leaving_water_temp_offset_auto'],
                ['leaving_water_temp_heating'],
                ['leaving_water_temp_cooling'],
                ['leaving_water_temp_auto'],
            ]
        tank = device.hot_water_tank
        climate = device.climate_control
        tasks = []
        for arg in args.prop:
            if arg[0] == 'dhw_power':
                try:
                    switch = parse_switch(arg[1])
                    if switch is True:
                        await write(tank.is_turned_on, bool, True, tank.turn_on)
                    if switch is False:
                        await write(tank.is_turned_on, bool, False, tank.turn_off)
                except IndexError:
                    pass
                create_task(tasks, device.hot_water_tank.is_turned_on, lambda v: 'ON' if v else 'OFF', json_data, arg[0])
            if arg[0] == 'dhw_temp':
                create_task(tasks, device.hot_water_tank.tank_temperature, lambda v: str(round(v)), json_data, arg[0])
            if arg[0] == 'dhw_target_temp':
                try:
                    value = round(float(arg[1]))
                    await write(tank.target_temperature, round, value, lambda: tank.set_target_temperature(value))
                except IndexError:
                    pass
                create_task(tasks, device.hot_water_tank.target_temperature, lambda v: str(round(v)), json_data, arg[0])
            if arg[0] == 'dhw_temp_heating':
                try:
                    value = round(float(arg[1]))
                    await write(tank.domestic_hot_water_temperature_heating, round, value, lambda: tank.set_domestic_hot_water_temperature_heating(value))
                except IndexError:
                    pass
                create_task(tasks, device.hot_water_tank.domestic_hot_water_temperature_heating, lambda v: str(round(v)), json_data, arg[0])
            if arg[0] == 'dhw_powerful':
                try:
                    value = parse_switch(arg[1]) is True
                    await write(tank.powerful, bool, value, lambda: tank.set_powerful(value))
                except IndexError:
                    pass
                create_task(tasks, device.hot_water_tank.powerful, lambda v: 'ON' if v else 'OFF', json_data, arg[0])
            if arg[0] == 'indoor_temp':
                create_task(tasks, device.climate_control.indoor_temperature, lambda v: str(round(v, 1)), json_data, arg[0])
            if arg[0] == 'outdoor_temp':
                create_task(tasks, device.climate_control.outdoor_temperature, lambda v: str(round(v)), json_data, arg[0])
            if arg[0] == 'climate_control_heating_config':
                config = device.climate_control.climate_control_heating_configuration
                json_data[arg[0]] = {'name': config.name, 'value': str(config.value)}
            if arg[0] == 'climate_control_cooling_config':
                config = device.climate_control.climate_control_cooling_configuration
                json_data[arg[0]] = {'name': config.name, 'value': str(config.value)}
            if arg[0] == 'climate_control_power':
                try:
                    switch = parse_switch(arg[1])
                    if switch is True:
                        await write(climate.is_turned_on, bool, True, climate.turn_on)
                    if switch is False:
                        await write(climate.is_turned_on, bool, False, climate.turn_off)
                except IndexError:
                    pass
                create_task(tasks, device.climate_control.is_turned_on, lambda v: 'ON' if v else 'OFF', json_data, arg[0])
            if arg[0] == 'climate_control_mode':
                try:
                    mode = ClimateControlMode(arg[1])
                    await write(climate.operation_mode, lambda v: v, mode, lambda: climate.set_operation_mode(mode))
                except IndexError:
                    pass
                create_task(tasks, device.climate_control.operation_mode, lambda v: {'name': v.name, 'value': v.value}, json_data, arg[0])
            if arg[0] == 'leaving_water_temp_current':
                create_task(tasks, device.climate_control.leaving_water_temperature_current, lambda v: str(round(v, 1)), json_data, arg[0])
            if arg[0] == 'leaving_water_temp_offset_heating':
                try:
                    value = round(float(arg[1]))
                    await write(climate.leaving_water_temperature_offset_heating, round, value, lambda: climate.set_leaving_water_temperature_offset_heating(value))
                except IndexError:
                    pass
                create_task(tasks, device.climate_control.leaving_water_temperature_offset_heating, lambda v: str(round(v)), json_data, arg[0])
            if arg[0] == 'leaving_water_temp_offset_cooling':
                try:
                    value = round(float(arg[1]))
                    await write(climate.leaving_water_temperature_offset_cooling, round, value, lambda: climate.set_leaving_water_temperature_offset_cooling(value))
                except IndexError:
                    pass
                create_task(tasks, device.climate_control.leaving_water_temperature_offset_cooling, lambda v: str(round(v)), json_data, arg[0])
            if arg[0] == 'leaving_water_temp_offset_auto':
                try:
                    value = round(float(arg[1]))
                    await write(climate.leaving_water_temperature_offset_auto, round, value, lambda: climate.set_leaving_water_temperature_offset_auto(value))
                except IndexError:
                    pass
                create_task(tasks, device.climate_control.leaving_water_temperature_offset_auto, lambda v: str(round(v)), json_data, arg[0])
            if arg[0] == 'leaving_water_temp_heating':
                try:
                    value = round(float(arg[1]))
                    await write(climate.leaving_water_temperature_heating, round, value, lambda: climate.set_leaving_water_temperature_heating(value))
                except IndexError:
                    pass
                create_task(tasks, device.climate_control.leaving_water_temperature_heating, lambda v: str(round(v)), json_data, arg[0])
            if arg[0] == 'leaving_water_temp_cooling':
                try:
                    value = round(float(arg[1]))
                    await write(climate.leaving_water_temperature_cooling, round, value, lambda: climate.set_leaving_water_temperature_cooling(value))
                except IndexError:
                    pass
                create_task(tasks, device.climate_control.leaving_water_temperature_cooling, lambda v: str(round(v)), json_data, arg[0])
            if arg[0] == 'leaving_water_temp_auto':
                create_task(tasks, device.climate_control.leaving_water_temperature_auto, lambda v: str(round(v)), json_data, arg[0])
            if arg[0] == 'dhw_consumptions':
                create_task(tasks, device.hot_water_tank.read_consumptions, lambda v: v, json_data, arg[0])
            if arg[0] == 'climate_control_consumptions':
                create_task(tasks, device.climate_control.read_consumptions, lambda v: v, json_data, arg[0])
        await asyncio.wait(tasks)
        await conn._client.close()
    print(json.dumps(json_data, indent=4))


if __name__ == '__main__':
    asyncio.run(main())
