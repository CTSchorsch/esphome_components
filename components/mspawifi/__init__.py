import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import (sensor, uart, switch, text_sensor, number)
from esphome.const import (CONF_ID, CONF_NAME)


DEPENDENCIES = ['uart']

AUTO_LOAD = ['sensor', 'switch', 'text_sensor', 'number']

mspawifi_ns = cg.esphome_ns.namespace('mspawifi')

MSPAWifi = mspawifi_ns.class_('MSPAWifi', cg.Component)
MSPAWifiHeaterSwitch = mspawifi_ns.class_('MSPAWifiHeaterSwitch', switch.Switch, cg.Component)
MSPAWifiFilterSwitch = mspawifi_ns.class_('MSPAWifiFilterSwitch', switch.Switch, cg.Component)
MSPAWifiSollTempNumber = mspawifi_ns.class_('MSPAWifiSollTempNumber', number.Number, cg.Component)

CONF_REMOTE_UART = "remote_uart"
CONF_POOL_UART = "pool_uart"
CONF_ACTTEMP = "act_temp"
CONF_FILTERHOURS = "filter_hours"
CONF_HEATER_SWITCH = "heater_sw"
CONF_FILTER_SWITCH = "filter_sw"
CONF_STATUS_TEXT = "status_text"
CONF_SOLLTEMP_NUMBER = "solltemp"

CONFIG_SCHEMA = cv.component_schema(MSPAWifi).extend({
#    cv.GenerateID(): cv.declare_id(MSPAWifi),
    cv.Required(CONF_REMOTE_UART): cv.use_id(uart.UARTComponent),
    cv.Required(CONF_POOL_UART): cv.use_id(uart.UARTComponent),
    cv.Optional(CONF_STATUS_TEXT): text_sensor.text_sensor_schema(text_sensor.TextSensor),
    cv.Optional(CONF_ACTTEMP): sensor.sensor_schema(
        accuracy_decimals = 1
    ),
    cv.Optional(CONF_FILTERHOURS): sensor.sensor_schema(
        accuracy_decimals = 0
    ),
#    cv.Optional(CONF_HEATER_SWITCH): switch.SWITCH_SCHEMA.extend({cv.GenerateID(): cv.declare_id(MSPAWifiHeaterSwitch)}),
    cv.Optional(CONF_HEATER_SWITCH): switch.switch_schema(MSPAWifiHeaterSwitch).extend({}),
#    cv.Optional(CONF_FILTER_SWITCH): switch.SWITCH_SCHEMA.extend({cv.GenerateID(): cv.declare_id(MSPAWifiFilterSwitch)}),
    cv.Optional(CONF_FILTER_SWITCH): switch.switch_schema(MSPAWifiFilterSwitch).extend({}),
#    cv.Optional(CONF_SOLLTEMP_NUMBER): number.NUMBER_SCHEMA.extend({cv.GenerateID(): cv.declare_id(MSPAWifiSollTempNumber)}),
    cv.Optional(CONF_SOLLTEMP_NUMBER): switch.number_schema(MSPAWifiSollTempNumber).extend({}),
})


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)

    if CONF_STATUS_TEXT in config:
       status_text = await text_sensor.new_text_sensor(config[CONF_STATUS_TEXT])
       cg.add(var.set_status_text(status_text))

    if CONF_REMOTE_UART in config:
        remote_uart = await cg.get_variable(config[CONF_REMOTE_UART])
        cg.add(var.set_remote_uart(remote_uart))

    if CONF_POOL_UART in config:
        pool_uart = await cg.get_variable(config[CONF_POOL_UART])
        cg.add(var.set_pool_uart(pool_uart))

    if CONF_ACTTEMP in config:
        sens = await sensor.new_sensor(config[CONF_ACTTEMP])
        cg.add(var.set_acttemp_sensor(sens))

    if CONF_FILTERHOURS in config:
        filter_hours = await sensor.new_sensor(config[CONF_FILTERHOURS])
        cg.add(var.set_filterhours_sensor(filter_hours))

    if CONF_HEATER_SWITCH in config:
        heater_sw = await switch.new_switch(config[CONF_HEATER_SWITCH])
        cg.add(heater_sw.set_parent(var))

    if CONF_FILTER_SWITCH in config:
        filter_sw = await switch.new_switch(config[CONF_FILTER_SWITCH])
        cg.add(var.setFilterSw(filter_sw))

    if CONF_SOLLTEMP_NUMBER in config:
        solltemp_number = await number.new_number(config[CONF_SOLLTEMP_NUMBER],min_value=20,max_value=40,step=0.5)
        cg.add(var.set_solltemp_number(solltemp_number))
