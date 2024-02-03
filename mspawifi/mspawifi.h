#pragma once

#include "esphome/core/component.h"
#include "esphome/components/sensor/sensor.h"
#include "esphome/components/uart/uart.h"

namespace esphome {
namespace mspawifi {


class MSPAWifi : public Component {
 
 public:
  float get_setup_priority() const override { return setup_priority::LATE; }
  void loop() override;
  void dump_config() override;
  void set_remote_uart(uart::UARTComponent *uart) { this->remote_uart_ = uart; }
  void set_pool_uart(uart::UARTComponent *uart) { this->pool_uart_ = uart; }
  void set_acttemp_sensor(sensor::Sensor *sensor) { acttemp_sensor_ = sensor; }
 

 protected:
  bool processMessage( uint8_t *msg );
  uart::UARTComponent *remote_uart_{nullptr};
  uart::UARTComponent *pool_uart_{nullptr};
  sensor::Sensor *acttemp_sensor_{nullptr};

  std::vector<uint8_t> rem_buffer_;
  std::vector<uint8_t> pool_buffer_;
  bool rem_rx_{false};
  bool pool_rx_{false};
};

}  // namespace mspawifi
}  // namespace esphome
