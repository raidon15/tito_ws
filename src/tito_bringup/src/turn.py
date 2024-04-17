import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64MultiArray


class JointStateSubscriber(Node):
    def __init__(self):
        super().__init__('joint_state_subscriber')
        self.subscription = self.create_subscription(
            JointState,
            'joint_states',  # topic name
            self.joint_state_callback,  # callback function
            10  # QoS profile depth
        )
        self.publisher1_ = self.create_publisher(Float64MultiArray, '/velocity_controller1/commands', 10)
        self.publisher2_ = self.create_publisher(Float64MultiArray, '/velocity_controller2/commands', 10)
        self.position_publisher_ = self.create_publisher(Float64MultiArray, '/position_controller/commands', 10)
        self.subscription  # prevent unused variable warning

    def air_stage(self,publisher,velocity):
        msg = Float64MultiArray()
        msg.data = [velocity*7.5]  # Example velocity commands
        publisher.publish(msg)
    def contact_stage(self,publisher,velocity):
        msg = Float64MultiArray()
        msg.data = [velocity*1.5]  # Example velocity commands
        publisher.publish(msg)
    def multivalue(self,angle):
        if angle > 6.28318530718:
            angle = angle - 6.28318530718
            return(self.multivalue(angle))
        else:
            return(angle)
    def joint_state_callback(self, msg):
        #self.get_logger().info('Received joint state message:')
        angle1 = msg.position[0]
        angle2 = msg.position[3]+3.14159265359
        angle1 = self.multivalue(angle1)
        angle2 = self.multivalue(angle2)
        if angle1 < 1.0471975512 or angle1 > 5.23598775598 :
            self.contact_stage(self.publisher1_,1)
            print("contact stage")
        else:
            self.air_stage(self.publisher1_,1)
            print("air stage")
        
        if angle2 < 1.0471975512 or angle2 > 5.23598775598 :
            self.contact_stage(self.publisher2_,-1)
            print("contact stage")
        else:
            self.air_stage(self.publisher2_,-1)
            print("air stage")
    def acomodate_legs(self):
        pass

def main(args=None):
    rclpy.init(args=args)
    print("initializing subscriber")
    joint_state_subscriber = JointStateSubscriber()
    rclpy.spin(joint_state_subscriber)
    joint_state_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
