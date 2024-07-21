import asyncio
import aiohttp
import argparse
import json
import os

from pyaltherma.comm import DaikinWSConnection
from pyaltherma.controllers import AlthermaController, AlthermaClimateControlController, AlthermaUnitController, \
    AlthermaWaterTankController


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-get', metavar='item', nargs=1, action='append', type=str)
    parser.add_argument('-set', metavar=('item', 'value'), nargs=2, action='append', type=str)
    args = parser.parse_args()
    json_data = {}
    daikin_host = os.environ.get('PYALTHERMA_CLI_HOST')
    async with aiohttp.ClientSession() as session:
        conn = DaikinWSConnection(session, daikin_host)
        device = AlthermaController(conn)
        await device.discover_units()
        for arg in args.get:
            if arg[0] == 'dhw_power':
                json_data['dhw_power'] = '1' if device.hot_water_tank.is_turned_on() else '0'
            if arg[0] == 'dhw_temp':
                json_data['dhw_temp'] = str(device.hot_water_tank.tank_temperature)
            if arg[0] == 'dhw_target_temp':
                json_data['dhw_target_temp'] = str(device.hot_water_tank.target_temperature)
            if arg[0] == 'dhw_powerful':
                json_data['dhw_powerful'] = '1' if device.hot_water_tank.powerful else '0'
            if arg[0] == 'indoor_temp':
                json_data['indoor_temp'] = str(device.climate_control.indoor_temperature)
            if arg[0] == 'outdoor_temp':
                json_data['outdoor_temp'] = str(device.climate_control.outdoor_temperature)
            if arg[0] == 'climate_control_heating_config':
                json_data['climate_control_heating_config'] = device.climate_control.climate_control_heating_configuration
            if arg[0] == 'climate_control_cooling_config':
                json_data['climate_control_cooling_config'] = device.climate_control.climate_control_cooling_configuration
            if arg[0] == 'climate_control_power':
                json_data['climate_control_power'] = '1' if device.climate_control.is_turned_on() else '0'
            if arg[0] == 'climate_control_mode':
                json_data['climate_control_mode'] = str(device.climate_control.operation_mode)
            if arg[0] == 'leaving_water_temp_current':
                json_data['leaving_water_temp_current'] = str(device.climate_control.leaving_water_temperature_current)
            if arg[0] == 'leaving_water_temp_offset_heating':
                json_data['leaving_water_temp_offset_heating'] = str(device.climate_control.leaving_water_temperature_offset_heating)
            if arg[0] == 'leaving_water_temp_offset_cooling':
                json_data['leaving_water_temp_offset_cooling'] = str(device.climate_control.leaving_water_temperature_offset_cooling)
            if arg[0] == 'leaving_water_temp_offset_auto':
                json_data['leaving_water_temp_offset_auto'] = str(device.climate_control.leaving_water_temperature_offset_auto)
            if arg[0] == 'leaving_water_temp_heating':
                json_data['leaving_water_temp_heating'] = str(device.climate_control.leaving_water_temperature_heating)
            if arg[0] == 'leaving_water_temp_cooling':
                json_data['leaving_water_temp_cooling'] = str(device.climate_control.leaving_water_temperature_cooling)
            if arg[0] == 'leaving_water_temp_auto':
                json_data['leaving_water_temp_auto'] = str(device.climate_control.leaving_water_temperature_auto)
        for arg in args.set:
            if arg[0] == 'dhw_power':
                if arg[1] == '1':
                    device.hot_water_tank.turn_on()
                else:
                    device.hot_water_tank.turn_off()
                json_data['dhw_power'] = arg[1]
            if arg[0] == 'dhw_target_temp':
                device.hot_water_tank.set_target_temperature(float(arg[1]))
                json_data['dhw_target_temp'] = arg[1]
            if arg[0] == 'dhw_powerful':
                device.hot_water_tank.set_powerful(arg[1] == '1')
                json_data['dhw_powerful'] = arg[1]
            if arg[0] == 'climate_control_power':
                if arg[1] == '1':
                    device.climate_control.turn_on()
                else:
                    device.climate_control.turn_off()
                json_data['climate_control_power'] = arg[1]
            if arg[0] == 'climate_control_mode':
                device.climate_control.set_operation_mode(arg[1])
                json_data['climate_control_mode'] = arg[1]
            if arg[0] == 'leaving_water_temp_offset_heating':
                device.climate_control.set_leaving_water_temperature_offset_heating(round(float(arg[1])))
                json_data['leaving_water_temp_offset_heating'] = arg[1]
            if arg[0] == 'leaving_water_temp_offset_cooling':
                device.climate_control.set_leaving_water_temperature_offset_cooling(round(float(arg[1])))
                json_data['leaving_water_temp_offset_cooling'] = arg[1]
            if arg[0] == 'leaving_water_temp_offset_auto':
                device.climate_control.set_leaving_water_temperature_offset_auto(round(float(arg[1])))
                json_data['leaving_water_temp_offset_auto'] = arg[1]
            if arg[0] == 'leaving_water_temp_heating':
                device.climate_control.set_leaving_water_temperature_heating(round(float(arg[1])))
                json_data['leaving_water_temp_heating'] = arg[1]
            if arg[0] == 'leaving_water_temp_cooling':
                device.climate_control.set_leaving_water_temperature_cooling(round(float(arg[1])))
                json_data['leaving_water_temp_cooling'] = arg[1]
            if arg[0] == 'leaving_water_temp_auto':
                device.climate_control.set_leaving_water_temperature_auto(round(float(arg[1])))
                json_data['leaving_water_temp_auto'] = arg[1]
        await device.get_current_state()
        await conn._client.close()
    print(json.dumps(json_data))


if __name__ == '__main__':
    asyncio.run(main())