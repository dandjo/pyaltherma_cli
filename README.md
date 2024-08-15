# pyaltherma_cli
Provides a command-line interface for [pyaltherma](https://github.com/tadasdanielius/pyaltherma).

## Installation

This is just an example of how to install the module with a virtual environment.

```bash
python3 -m venv ~/.venv/pyaltherma_cli
source ~/.venv/pyaltherma_cli/bin/activate
python3 -m pip install pyaltherma
```

The module uses environment variables to configure the connection to the Altherma system.
You can set the environment variables in the shell or in a file that is sourced by the shell.

```bash
export PYALTHERMA_HOST=192.168.1.5
```

## Usage

You can read and write defined properties from the API via arguments. If you
pass a value, it will be written. Mix them as you like. Providing no arguments,
all properties will be read. The output is a JSON object.

```bash
python3 -m pyaltherma_cli -prop <property> -prop <property> <value>
```

The following example shows how to run the CLI by setting the domestic hot water
to "on" and the setpoint to 50 degrees. At the same time we request the current
temperature of the domestic hot water.

```bash
python3 -m pyaltherma_cli -prop dhw_power ON -prop dhw_temp_heating 50 -prop dhw_temp
```

This results in the following output.

```json
{
 "dhw_power": "1",
 "dhw_temp_heating": "50",
 "dhw_temp": "33.4"
}
```

## Implemented properties

| Property                          | Description                                   | Read | Write | Values                                                       | Limitations                                                                                      |
|-----------------------------------|-----------------------------------------------|------|-------|--------------------------------------------------------------|--------------------------------------------------------------------------------------------------|
| dhw_power                         | Domestic hot water power                      | ✓    | ✓     | "ON", "OFF"                                                  |                                                                                                  |
| dhw_temp                          | Domestic hot water temperature                | ✓    |       |                                                              |                                                                                                  |
| dhw_target_temp                   | Domestic hot water target temperature         | ✓    | ✓     | between "30" and "80"                                        | only for "dhw_power" set to "ON"                                                                 |
| dhw_temp_heating                  | Domestic hot water target temperature heating | ✓    | ✓     | between "30" and "80"                                        | only for "dhw_power" set to "ON"                                                                 |
| dhw_powerful                      | Domestic hot water powerful mode              | ✓    | ✓     | "ON", "OFF"                                                  |                                                                                                  |
| indoor_temp                       | Indoor temperature                            | ✓    |       |                                                              |                                                                                                  |
| outdoor_temp                      | Outdoor temperature                           | ✓    |       |                                                              |                                                                                                  |
| climate_control_heating_config    | Climate control heating configuration         | ✓    |       | "1" (WeatherDependent), "2" (Fixed)                          |                                                                                                  |
| climate_control_cooling_config    | Climate control cooling configuration         | ✓    |       | "1" [WeatherDependent], "2" (Fixed)                          |                                                                                                  |
| climate_control_power             | Climate control power                         | ✓    | ✓     | "ON", "OFF"                                                  |                                                                                                  |
| climate_control_mode              | Climate control mode                          | ✓    | ✓     | "heating", "cooling", "auto", "heating_day", "heating_night" |                                                                                                  |
| leaving_water_temp_offset_heating | Leaving water temperature offset for heating  | ✓    | ✓     | between "-10" and "10"                                       | only for "climate_control_mode" set to "heating" and "climate_control_heating_config" set to "1" |
| leaving_water_temp_offset_cooling | Leaving water temperature offset for cooling  | ✓    | ✓     | between "-10" and "10"                                       | only for "climate_control_mode" set to "cooling" and "climate_control_cooling_config" set to "1" |
| leaving_water_temp_offset_auto    | Leaving water temperature offset for auto     | ✓    | ✓     | between "-10" and "10"                                       | only for "climate_control_mode" set to "auto"                                                    |
| leaving_water_temp_heating        | Leaving water temperature for heating         | ✓    | ✓     |                                                              | only for "climate_control_mode" set to "heating" and "climate_control_heating_config" set to "2" |
| leaving_water_temp_cooling        | Leaving water temperature for cooling         | ✓    | ✓     |                                                              | only for "climate_control_mode" set to "cooling" and "climate_control_cooling_config" set to "2" |
| leaving_water_temp_auto           | Leaving water temperature for auto            | ✓    |       |                                                              | only for "climate_control_mode" set to "auto"                                                    |
