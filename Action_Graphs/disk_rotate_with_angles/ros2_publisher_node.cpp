#include <rclcpp/rclcpp.hpp>
#include <std_msgs/msg/string.hpp>
#include <std_msgs/msg/float32.hpp>
#include <string>
#include <random>

int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<rclcpp::Node>("simple_node");

    // Publisher for Y value
    auto publisher = node->create_publisher<std_msgs::msg::String>("topic", 10);

    // Subscriber for disk angle
    // auto angle_sub = node->create_subscription<std_msgs::msg::Float32>(
    //     "pub_topic", 100,  // Increased queue size
    //     [](std_msgs::msg::Float32::SharedPtr msg) {
    //         if (msg) {
    //             float current_angle = msg->data;
    //             RCLCPP_INFO(rclcpp::get_logger("angle_subscriber"), "Current disk angle: %.2f", current_angle);
    //         } else {
    //             RCLCPP_WARN(rclcpp::get_logger("angle_subscriber"), "Received null message");
    //         }
    //     }
    // );

    rclcpp::Rate rate(0.5); // 1 Hz
    float y_value = 0.0F;

    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution <> distr(0, 359);


    while (rclcpp::ok())
    {
        // Publish Y value
        int y_value = distr(gen);
        auto msg = std_msgs::msg::String();
        msg.data = std::to_string(y_value);
        publisher->publish(msg);
        RCLCPP_INFO(node->get_logger(), "Publishing Y value: '%s'", msg.data.c_str());

        // Process subscriber callbacks
        rclcpp::spin_some(node);
        rate.sleep();
    }

    rclcpp::shutdown();
    return 0;
}

