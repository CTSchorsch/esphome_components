#include "mspawifi.h"
#include "esphome/core/log.h"

namespace esphome {
namespace mspawifi {

static const char *const TAG = "mspawifi";

bool MSPAWifi::processMessage( uint8_t *msg )
{
  //check checksum
  uint8_t csum = (msg[0] + msg[1] + msg[2]) % 256;
  uint8_t tcsum = msg[3];
  if (csum != tcsum) {
    ESP_LOGE(TAG, "Checksum mismatch: %02x != %02x", csum, tcsum);
    return false;
  }
  switch (msg[1]) {
    case 6: {
      float temp = msg[2] * 0.5;
      if (this->acttemp_sensor_ != nullptr) {
        if ( !this->acttemp_sensor_->has_state() || (this->acttemp_sensor_->state != temp ) )
          this->acttemp_sensor_->publish_state(temp);
      }
    } break;
    
   
    default: {
      ESP_LOGV(TAG, "unknown message type %02x, value %02x", msg[1], msg[2]);
    } break;
  }
  return true;
}

void MSPAWifi::loop() 
{
  uint8_t c;

  //pool -> remote
  if (this->pool_uart_ != nullptr) {
    while (this->pool_uart_->available()) {
      this->pool_uart_->read_byte(&c);
      //first relay to remote
      if (this->remote_uart_ != nullptr)
        this->remote_uart_->write_byte(c);
      
      //second process data
      if (!this->pool_rx_) {
        if (c != 0xa5)
          continue;
        this->pool_rx_ = true;
        this->pool_buffer_.push_back(c);
        continue;
      }
      this->pool_buffer_.push_back(c);
      if (this->pool_buffer_.size() < 4)
        continue;
      //Receive complete message
      this->pool_rx_ = false;
      uint8_t *d = this->pool_buffer_.data();
      //handle all the stuff
      processMessage( d);
      this->pool_buffer_.clear();
    }
  }
  //remote -> pool
  if (this->remote_uart_ != nullptr) {
    while (this->remote_uart_->available()) {
      this->remote_uart_->read_byte(&c);
      //relay to pool
      if (this->pool_uart_ != nullptr)
        this->pool_uart_->write_byte(c);

      if (!this->rem_rx_) {
        if (c != 0xa5)
          continue;
        this->rem_rx_ = true;
        this->rem_buffer_.push_back(c);
        continue;
      }
      this->rem_buffer_.push_back(c);
      if (this->rem_buffer_.size() < 4)
        continue;
      this->rem_rx_ = false;
      uint8_t *d = this->rem_buffer_.data();
      processMessage( d );
      this->rem_buffer_.clear();
    }
  }
}

void MSPAWifi::dump_config() {
  ESP_LOGCONFIG(TAG, "MSPAWifi");
  LOG_SENSOR("", "ActTemp", this->acttemp_sensor_);
}

}  // namespace mspawifi
}  // namespace esphome
