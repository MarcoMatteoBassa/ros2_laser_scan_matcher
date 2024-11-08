#include "ros2_laser_scan_matcher/filter.hpp"

#include <algorithm>
#include <cmath>
#include <numeric>

double FilterBase::update(double time, double current_value) {
  if (!is_initialized_) {
    is_initialized_ = true;
    return current_value;
  }
  return filterImpl(time, current_value);
}

// Low-pass filter
LowPassFilter::LowPassFilter(double alpha) : alpha_(alpha) {}

double LowPassFilter::filterImpl(double time, double current_value) {
  if (last_time_ != 0) {
    double dt = time - last_time_;
    double effective_alpha = 1.0 - std::exp(-dt / alpha_);
    filtered_value_ = effective_alpha * current_value + (1.0 - effective_alpha) * filtered_value_;
  } else {
    // First measurement
    filtered_value_ = current_value;
  }

  last_time_ = time;
  return filtered_value_;
}

// Moving average filter
MovingAverageFilter::MovingAverageFilter(double time_window, double weight_factor)
    : time_window_(time_window), weight_factor_(weight_factor) {}

double MovingAverageFilter::filterImpl(double time, double current_value) {
  buffer_.emplace_back(time, current_value);

  while (!buffer_.empty() && (time - buffer_.front().first) > time_window_) {
    buffer_.pop_front();
  }

  double sum = 0.0;
  double total_weight = 0.0;

  for (const auto& [sample_time, value] : buffer_) {
    double dt = time - sample_time;
    double weight = std::exp(-weight_factor_ * dt / time_window_);
    sum += value * weight;
    total_weight += weight;
  }

  return total_weight > 0.0 ? sum / total_weight : current_value;
}
