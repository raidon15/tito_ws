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
        self.publisher_ = self.create_publisher(Float64MultiArray, '/velocity_controller/commands', 10)
        self.subscription  # prevent unused variable warning

    def air_stage(self):
        msg = Float64MultiArray()
        msg.data = [2.5]  # Example velocity commands
        self.publisher_.publish(msg)
    def contact_stage(self):
        msg = Float64MultiArray()
        msg.data = [0.5]  # Example velocity commands
        self.publisher_.publish(msg)
    def multivalue(self,angle):
        if angle > 6.28318530718:
            angle = angle - 6.28318530718
            return(self.multivalue(angle))
        else:
            return(angle)
    def joint_state_callback(self, msg):
        #self.get_logger().info('Received joint state message:')
        angle = msg.position[0]
        angle = self.multivalue(angle)
        if angle < 1.0471975512 or angle > 5.23598775598 :
            self.contact_stage()
            print("contact stage")
        else:
            self.air_stage()
            print("air stage")
        
    

def main(args=None):
    rclpy.init(args=args)
    print("initializing subscriber")
    joint_state_subscriber = JointStateSubscriber()
    rclpy.spin(joint_state_subscriber)
    joint_state_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
