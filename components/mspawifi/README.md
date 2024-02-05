# UART in the middle - wifi bridge - for MSPA whirpools

Two configured uarts are required for full function.

Example:
```yaml
mspawifi:
  id: my_mspa
  pool_uart: pool_bus
  remote_uart: remote_bus
  act_temp:
    name: Actual temperature
```

`act_temp` is a `sensor`

