import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        


    def listener_callback(self, msg):
        # self.get_logger().info('I heard: "%s"' % msg)
        self.scan0 = msg.ranges[0]
        self.scan_msg  = min(msg.ranges)
        index  = msg.ranges.index(min(msg.ranges))
        self.step = msg.angle_increment
        self.angle= self.step*index
        # print((index) )
     
    def timer_callback(self):
        msg = Twist()
        if self.scan0>3.0:   #maijer
            if self.angle>1.57:

                msg.angular.z = 2.0
            
            else:
                msg.angular.z = -2.0
        else:
            msg.angular.z = 0.0
            msg.linear.x = -1.0
        self.publisher_.publish(msg)

        # self.publisher_.publish(msg)
        # self.get_logger().info('Publishing: "%s"' % msg.data)
        # self.i += 1
     

def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)


    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()