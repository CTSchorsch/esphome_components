# UART in the middle - wifi bridge - for MSPA whirpools

Two configured uarts are required for full function.

Example:
```yaml
spawifi:
  pool_uart: uartPool
  remote_uart: uartRemote
  act_temp:
    name: Aktuelle Temperatur
  heater_sw:
    name: Heizung
  filter_sw:
    name: Filterpumpe
  status_text:
    name: Status
  sollemp:
    name: Solltemperatur
```
`status_text` is a `text_sensor` with the pool status
`act_temp` is a `sensor`for the actual water temperatur
`filter_sw` is a `switch` to enable the filterpump
`heater_sw` is a `switch` to enable the heater and implicit the filterpump with 2 minuts overrun after haeter is switched off
`solltemp` is a `number` input to set the target temperature
 

