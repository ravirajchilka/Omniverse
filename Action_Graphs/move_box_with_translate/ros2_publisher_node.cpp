#include <rclcpp/rclcpp.hpp>
#include <std_msgs/msg/string.hpp>
#include <string>

int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<rclcpp::Node>("simple_node");
    auto publisher = node->create_publisher<std_msgs::msg::String>("topic", 10);
    rclcpp::Rate rate(10); // 1 Hz
    double y_value = 0.0;

    while (rclcpp::ok())
    {
        auto msg = std_msgs::msg::String();
        msg.data = std::to_string(y_value);  // Send numeric value as string
        publisher->publish(msg);

        RCLCPP_INFO(node->get_logger(), "Publishing Y value: '%s'", msg.data.c_str());

        y_value += 0.2;  // increment Y each tick
        if (y_value > 30.0) y_value = 0.0;  // reset after 15 units

        rclcpp::spin_some(node);
        rate.sleep();
    }

    rclcpp::shutdown();
    return 0;
}
