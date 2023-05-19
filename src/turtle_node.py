import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

MAX_DIFF = 0.1
points = [(0.0, 0.5), (0.5, 0.0), (0.0, 0.5), (0.5, 0.0), (0.0, 1.0), (1.0, 0.0)]

class turtle(Node):
    def __init__(self, roadmap):
        super().__init__('turtle')
        self.publisher_ = self.create_publisher(Twist,'turtle1/cmd_vel', 10)
        self.twist_msg_ = Twist()
        self.pose_subscriber_ = self.create_subscription(Pose, '/turtle1/pose', self.handlePose, 10)
        self.position = {'x':0,'y':0}
        self.previous = (0.0, 0.0) 
        self.goal = None
        self.map = roadmap
        self.back = []
        self.newGoal()
    
    def moveTo(self):

        if abs(self.position['x'] - self.previous[0]) > abs(self.goal[0]) and abs(self.position['y'] - self.previous[1]) > abs(self.goal[1]):
            self.newGoal()

        self.twist_msg_.linear.x = self.goal[0]
        self.twist_msg_.linear.y = self.goal[1]
        self.publisher_.publish(self.twist_msg_)

    def newGoal(self):
        try:
            self.previous = (self.position['x'], self.position['y'])
            self.goal = self.map.pop(0)
            self.back.append(self.goal)
            print(self.goal)
        except IndexError:
            print('CABEI!!!')
            exit()
            # try:
            #     self.goal = self.back.pop(0)
            #     print(self.goal)
            # except IndexError:
            #     print('Acabei!')
    
    def handlePose(self, pose):
        self.position['x'] = pose.x
        self.position['y'] = pose.y

        self.moveTo()
        
        return self.position
    
    
        

def main(args=None):
    rclpy.init(args=args)

    turtle_node = turtle(points)

    rclpy.spin(turtle_node)

    rclpy.shutdown()

if __name__ == '__main__':

    main()
    
