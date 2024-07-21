# pyaltherma_cli
Provides a command-line interface for [pyaltherma](https://github.com/tadasdanielius/pyaltherma).

## Installation

This is just an example of how to install the module. You can install it in any way you like.

```bash
python3 -m venv ~/.venv/pyaltherma_cli
source ~/.venv/pyaltherma_cli/bin/activate
python3 -m pip install pyaltherma
deactivate
```

The module uses environment variables to configure the connection to the Altherma system.
You can set the environment variables in the shell or in a file that is sourced by the shell.

```bash
export PYALTHERMA_CLI_HOST=192.168.1.5
```

## Usage

The module provides a bash script that can be used to run the CLI. It uses the virtual env as created in the installation section.
Otherwise, you can run the CLI directly from the Python interpreter in an environment of your choice.
You can read and write defined items from the API via arguments. If you pass a value, it will be written. Mix them as you like. The output is a JSON object.

```bash
python3 -m pyaltherma_cli -item <item> -item <item> <value>
```

The following example shows how to run the CLI by setting the domestic hot water to "on" and the setpoint to 50 degrees. At the same time we request the current temperature of the domestic hot water.

```bash
python3 -m pyaltherma_cli -item dhw_power 1 -item dhw_target_temp 50 -item dhw_temp
```

This results in the following output.

```json
{
 "dhw_power": "1",
 "dhw_target_temp": "50",
 "dhw_temp": "33.4"
}
```

### Implemented items

| Item | Description | Read | Write | Values | Limitations |
|------|-------------|------|-------|--------|-------------|
| dhw_power | Domestic hot water power | X | X | "1" [On], "0" [Off] | |
| dhw_temp | Domestic hot water temperature | X | | | |
| dhw_target_temp | Domestic hot water target temperature | X | X | between "30" and "80" | only for "dhw_power" set to "1" |
| dhw_powerful | Domestic hot water powerful mode | X | X | "1" [On], "0" [Off] | |
| indoor_temp | Indoor temperature | X | | | |
| outdoor_temp | Outdoor temperature | X | | | |
| climate_control_heating_config | Climate control heating configuration | X | | "1" [WeatherDependent], "2" [Fixed] | |
| climate_control_cooling_config | Climate control cooling configuration | X | | "1" [WeatherDependent], "2" [Fixed] | |
| climate_control_power | Climate control power | X | X | "1" [On], "0" [Off] | |
| climate_control_mode | Climate control mode | X | X | "heating", "cooling", "auto", "heating_day", "heating_night" | |
| leaving_water_temp_offset_heating | Leaving water temperature offset for heating | X | X | between "-5" and "5" | only for "climate_control_mode" set to "heating" and "climate_control_heating_config" set to "1" |
| leaving_water_temp_offset_cooling | Leaving water temperature offset for cooling | X | X | between "-5" and "5" | only for "climate_control_mode" set to "cooling" and "climate_control_cooling_config" set to "1" |
| leaving_water_temp_offset_auto | Leaving water temperature offset for auto | X | X | between "-5" and "5" | only for "climate_control_mode" set to "auto" |
| leaving_water_temp_heating | Leaving water temperature for heating | X | | | only for "climate_control_mode" set to "heating" and "climate_control_heating_config" set to "2" |
| leaving_water_temp_cooling | Leaving water temperature for cooling | X | | | only for "climate_control_mode" set to "cooling" and "climate_control_cooling_config" set to "2" |
| leaving_water_temp_auto | Leaving water temperature for auto | X | | | only for "climate_control_mode" set to "auto" |
