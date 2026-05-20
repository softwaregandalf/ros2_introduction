import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import random

class CokluRadar(Node):
    def __init__(self):
        super().__init__('coklu_radar')
        
        # Üç farklı kanal (topic) oluşturuyoruz
        self.pub_on = self.create_publisher(Float32, 'sensor/on', 10)
        self.pub_sag = self.create_publisher(Float32, 'sensor/sag', 10)
        self.pub_sol = self.create_publisher(Float32, 'sensor/sol', 10)
        
        self.timer = self.create_timer(1.0, self.veri_yayinla)

    def veri_yayinla(self):
        msg_on = Float32()
        msg_sag = Float32()
        msg_sol = Float32()

        # Sensörlerden rastgele veriler üretiliyor (1.0 ile 8.0 metre arası)
        msg_on.data = random.uniform(1.0, 8.0)
        msg_sag.data = random.uniform(1.0, 8.0)
        msg_sol.data = random.uniform(1.0, 8.0)

        # Kanallara yayınlanıyor
        self.pub_on.publish(msg_on)
        self.pub_sag.publish(msg_sag)
        self.pub_sol.publish(msg_sol)

        self.get_logger().info(f'📡 Yayında | Ön: {msg_on.data:.1f}m | Sağ: {msg_sag.data:.1f}m | Sol: {msg_sol.data:.1f}m')

def main(args=None):
    rclpy.init(args=args)
    node = CokluRadar()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
