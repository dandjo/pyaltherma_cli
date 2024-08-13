import asyncio
import aiohttp
import argparse
import json
import os

from pyaltherma.comm import DaikinWSConnection
from pyaltherma.controllers import AlthermaController
from pyaltherma.const import ClimateControlMode


ALTHERMA_HOST = os.environ.get('PYALTHERMA_HOST')


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
        for arg in args.prop:
            if arg[0] == 'dhw_power':
                try:
                    if arg[1].upper() == 'ON' or arg[1] == '1':
                        await device.hot_water_tank.turn_on()
                    if arg[1].upper() == 'OFF' or arg[1] == '0':
                        await device.hot_water_tank.turn_off()
                except IndexError:
                    pass
                json_data['dhw_power'] = 'ON' if await device.hot_water_tank.is_turned_on else 'OFF'
            if arg[0] == 'dhw_temp':
                json_data['dhw_temp'] = str(await device.hot_water_tank.tank_temperature)
            if arg[0] == 'dhw_target_temp':
                try:
                    await device.hot_water_tank.set_target_temperature(float(arg[1]))
                except IndexError:
                    pass
                json_data['dhw_target_temp'] = str(await device.hot_water_tank.target_temperature)
            if arg[0] == 'dhw_powerful':
                try:
                    await device.hot_water_tank.set_powerful(arg[1].upper() == 'ON' or arg[1] == '1')
                except IndexError:
                    pass
                json_data['dhw_powerful'] = 'ON' if await device.hot_water_tank.powerful else 'OFF'
            if arg[0] == 'indoor_temp':
                json_data['indoor_temp'] = str(await device.climate_control.indoor_temperature)
            if arg[0] == 'outdoor_temp':
                json_data['outdoor_temp'] = str(await device.climate_control.outdoor_temperature)
            if arg[0] == 'climate_control_heating_config':
                json_data['climate_control_heating_config'] = device.climate_control.climate_control_heating_configuration.value
            if arg[0] == 'climate_control_cooling_config':
                json_data['climate_control_cooling_config'] = device.climate_control.climate_control_cooling_configuration.value
            if arg[0] == 'climate_control_power':
                try:
                    if arg[1].upper() == 'ON' or arg[1] == '1':
                        await device.climate_control.turn_on()
                    if arg[1].upper() == 'OFF' or arg[1] == '0':
                        await device.climate_control.turn_off()
                except IndexError:
                    pass
                json_data['climate_control_power'] = 'ON' if await device.climate_control.is_turned_on else 'OFF'
            if arg[0] == 'climate_control_mode':
                try:
                    await device.climate_control.set_operation_mode(ClimateControlMode(arg[1]))
                except IndexError:
                    pass
                json_data['climate_control_mode'] = str((await device.climate_control.operation_mode).value)
            if arg[0] == 'leaving_water_temp_current':
                json_data['leaving_water_temp_current'] = str(await device.climate_control.leaving_water_temperature_current)
            if arg[0] == 'leaving_water_temp_offset_heating':
                try:
                    await device.climate_control.set_leaving_water_temperature_offset_heating(round(float(arg[1])))
                except IndexError:
                    pass
                json_data['leaving_water_temp_offset_heating'] = str(await device.climate_control.leaving_water_temperature_offset_heating)
            if arg[0] == 'leaving_water_temp_offset_cooling':
                try:
                    await device.climate_control.set_leaving_water_temperature_offset_cooling(round(float(arg[1])))
                except IndexError:
                    pass
                json_data['leaving_water_temp_offset_cooling'] = str(await device.climate_control.leaving_water_temperature_offset_cooling)
            if arg[0] == 'leaving_water_temp_offset_auto':
                try:
                    await device.climate_control.set_leaving_water_temperature_offset_auto(round(float(arg[1])))
                except IndexError:
                    pass
                json_data['leaving_water_temp_offset_auto'] = str(await device.climate_control.leaving_water_temperature_offset_auto)
            if arg[0] == 'leaving_water_temp_heating':
                try:
                    await device.climate_control.set_leaving_water_temperature_heating(round(float(arg[1])))
                except IndexError:
                    pass
                json_data['leaving_water_temp_heating'] = str(await device.climate_control.leaving_water_temperature_heating)
            if arg[0] == 'leaving_water_temp_cooling':
                try:
                    await device.climate_control.set_leaving_water_temperature_cooling(round(float(arg[1])))
                except IndexError:
                    pass
                json_data['leaving_water_temp_cooling'] = str(await device.climate_control.leaving_water_temperature_cooling)
            if arg[0] == 'leaving_water_temp_auto':
                json_data['leaving_water_temp_auto'] = str(await device.climate_control.leaving_water_temperature_auto)
        await device.get_current_state()
        await conn._client.close()
    print(json.dumps(json_data))


if __name__ == '__main__':
    asyncio.run(main())
