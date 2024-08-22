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


async def create_coro(value, callback, output, prop):
    if inspect.iscoroutinefunction(value):
        v = await value()
    elif inspect.isawaitable(value):
        v = await value
    else:
        v = value
    output[prop] = callback(v)

def create_task(tasks, *args):
    tasks.append(asyncio.create_task(create_coro(*args)))

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-prop', metavar=('prop', 'value'), nargs='+', action='append', type=str)
    args = parser.parse_args()
    json_data = {}
    async with aiohttp.ClientSession() as session:
        conn = DaikinWSConnection(session, ALTHERMA_HOST)
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
        tasks = []
        for arg in args.prop:
            if arg[0] == 'dhw_power':
                try:
                    if arg[1].upper() == 'ON' or arg[1] == '1':
                        await device.hot_water_tank.turn_on()
                    if arg[1].upper() == 'OFF' or arg[1] == '0':
                        await device.hot_water_tank.turn_off()
                except IndexError:
                    pass
                create_task(tasks, device.hot_water_tank.is_turned_on, lambda v: 'ON' if v else 'OFF', json_data, arg[0])
            if arg[0] == 'dhw_temp':
                create_task(tasks, device.hot_water_tank.tank_temperature, lambda v: str(round(v)), json_data, arg[0])
            if arg[0] == 'dhw_target_temp':
                try:
                    await device.hot_water_tank.set_target_temperature(float(arg[1]))
                except IndexError:
                    pass
                create_task(tasks, device.hot_water_tank.target_temperature, lambda v: str(round(v)), json_data, arg[0])
            if arg[0] == 'dhw_temp_heating':
                try:
                    await device.hot_water_tank.set_domestic_hot_water_temperature_heating(float(arg[1]))
                except IndexError:
                    pass
                create_task(tasks, device.hot_water_tank.domestic_hot_water_temperature_heating, lambda v: str(round(v)), json_data, arg[0])
            if arg[0] == 'dhw_powerful':
                try:
                    await device.hot_water_tank.set_powerful(arg[1].upper() == 'ON' or arg[1] == '1')
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
                    if arg[1].upper() == 'ON' or arg[1] == '1':
                        await device.climate_control.turn_on()
                    if arg[1].upper() == 'OFF' or arg[1] == '0':
                        await device.climate_control.turn_off()
                except IndexError:
                    pass
                create_task(tasks, device.climate_control.is_turned_on, lambda v: 'ON' if v else 'OFF', json_data, arg[0])
            if arg[0] == 'climate_control_mode':
                try:
                    await device.climate_control.set_operation_mode(ClimateControlMode(arg[1]))
                except IndexError:
                    pass
                create_task(tasks, device.climate_control.operation_mode, lambda v: {'name': v.name, 'value': v.value}, json_data, arg[0])
            if arg[0] == 'leaving_water_temp_current':
                create_task(tasks, device.climate_control.leaving_water_temperature_current, lambda v: str(round(v, 1)), json_data, arg[0])
            if arg[0] == 'leaving_water_temp_offset_heating':
                try:
                    await device.climate_control.set_leaving_water_temperature_offset_heating(round(float(arg[1])))
                except IndexError:
                    pass
                create_task(tasks, device.climate_control.leaving_water_temperature_offset_heating, lambda v: str(round(v)), json_data, arg[0])
            if arg[0] == 'leaving_water_temp_offset_cooling':
                try:
                    await device.climate_control.set_leaving_water_temperature_offset_cooling(round(float(arg[1])))
                except IndexError:
                    pass
                create_task(tasks, device.climate_control.leaving_water_temperature_offset_cooling, lambda v: str(round(v)), json_data, arg[0])
            if arg[0] == 'leaving_water_temp_offset_auto':
                try:
                    await device.climate_control.set_leaving_water_temperature_offset_auto(round(float(arg[1])))
                except IndexError:
                    pass
                create_task(tasks, device.climate_control.leaving_water_temperature_offset_auto, lambda v: str(round(v)), json_data, arg[0])
            if arg[0] == 'leaving_water_temp_heating':
                try:
                    await device.climate_control.set_leaving_water_temperature_heating(round(float(arg[1])))
                except IndexError:
                    pass
                create_task(tasks, device.climate_control.leaving_water_temperature_heating, lambda v: str(round(v)), json_data, arg[0])
            if arg[0] == 'leaving_water_temp_cooling':
                try:
                    await device.climate_control.set_leaving_water_temperature_cooling(round(float(arg[1])))
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
