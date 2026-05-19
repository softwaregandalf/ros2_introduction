import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class ZamanliSofor(Node):
    def __init__(self):
        super().__init__('zamanli_sofor')
        # Sadece çalışan hız kütüphanesini kullanıyoruz
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.timer = self.create_timer(1.0, self.hareket_et) # Her 1 saniyede bir tetiklenir
        self.adim = 0

    def hareket_et(self):
        msg = Twist()
        
        if self.adim % 2 == 0:
            # Çift sayılarda (0, 2, 4...) düz git
            msg.linear.x = 2.0
            msg.angular.z = 0.0
            self.get_logger().info('Düz ilerliyorum...')
        else:
            # Tek sayılarda (1, 3, 5...) yerinde dön
            msg.linear.x = 0.0
            msg.angular.z = 1.57 # Yaklaşık 90 derece dönüş
            self.get_logger().info('Dönüş yapıyorum...')
            
        self.publisher_.publish(msg)
        self.adim += 1

def main(args=None):
    rclpy.init(args=args)
    node = ZamanliSofor()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
