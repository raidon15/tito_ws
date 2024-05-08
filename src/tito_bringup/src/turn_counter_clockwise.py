import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64MultiArray
import math
import time

class JointStateSubscriber(Node):
    def __init__(self):
        super().__init__('joint_state_subscriber')
        self.subscription = self.create_subscription(
            JointState,
            'joint_states',  # topic name
            self.joint_state_callback,  # callback function
            10  # QoS profile depth
        )
        self.publisher1_ = self.create_publisher(
            Float64MultiArray, '/leg1/commands', 1)
        self.publisher3_ = self.create_publisher(
            Float64MultiArray, '/leg3/commands', 1)
        self.publisher5_ = self.create_publisher(
            Float64MultiArray, '/leg5/commands', 1)
        self.publisher2_ = self.create_publisher(
            Float64MultiArray, '/leg2/commands', 1)
        self.publisher4_ = self.create_publisher(
            Float64MultiArray, '/leg4/commands', 1)
        self.publisher6_ = self.create_publisher(
            Float64MultiArray, '/leg6/commands', 1)
        self.publisher_position_tripod1 = self.create_publisher(
            Float64MultiArray, '/position_controller1/commands', 1)
        self.publisher_position_tripod2 = self.create_publisher(
            Float64MultiArray, '/position_controller2/commands', 1)
        
        self.acomodate_legs()
        time.sleep(3)
        self.subscription  # prevent unused variable warning

    def air_stage(self, publisher, velocity):
        msg = Float64MultiArray()
        msg.data = [-velocity*2.5]  # Example velocity commands
        publisher.publish(msg)

    def contact_stage(self, publisher, velocity):
        msg = Float64MultiArray()
        msg.data = [-velocity*0.5]  # Example velocity commands
        publisher.publish(msg)

    def multivalue(self, angle):
        
        if angle < 0:
            angle = angle + math.pi * 2
            return (self.multivalue(angle))
        if angle > 6.28318530718:
            angle = angle - 6.28318530718
            return (self.multivalue(angle))
        else:
            return (angle)

    def joint_state_callback(self, msg):
        # self.get_logger().info('Received joint state message:')
        angle1 = msg.position[0]
        angle1 = self.multivalue(angle1)
        angle2 = msg.position[3] + math.pi
        angle2 = self.multivalue(angle2)
        print(angle2)
        if angle1 < math.pi/3 or angle1 > 5*math.pi/3:
            self.contact_stage(self.publisher1_, 1)
            self.contact_stage(self.publisher3_, 1)
            self.contact_stage(self.publisher5_, 1)

        else:

            self.air_stage(self.publisher1_, 1)
            self.air_stage(self.publisher3_, 1)
            self.air_stage(self.publisher5_, 1)

        if angle2 < math.pi/3 or angle2 > 5*math.pi/3:

            self.contact_stage(self.publisher2_, 1)
            self.contact_stage(self.publisher4_, 1)
            self.contact_stage(self.publisher6_, 1)

            print("air stage")
        else:
            self.air_stage(self.publisher2_, 1)
            self.air_stage(self.publisher4_, 1)
            self.air_stage(self.publisher6_, 1)
            print("contact stage")

    def acomodate_legs(self):
        print("acomodating legs")
        msg = Float64MultiArray()
        msg.data = [0.0,0.0,0.0]
        self.publisher_position_tripod1.publish(msg)
        self.publisher_position_tripod2.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    print("initializing subscriber")
    joint_state_subscriber = JointStateSubscriber()
    rclpy.spin(joint_state_subscriber)
    joint_state_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
