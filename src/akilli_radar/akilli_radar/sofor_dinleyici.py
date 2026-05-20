import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class SoforDinleyici(Node):
    def __init__(self):
        super().__init__('sofor_dinleyici')
        self.subscription = self.create_subscription(
            Float32,
            'on_mesafe',
            self.karar_ver,
            10)

    def karar_ver(self, msg):
        mesafe = msg.data
        if mesafe < 3.0:
            # Buradaki warn kelimesini warning olarak düzelttik
            self.get_logger().warning(f'⚠️ DİKKAT! Engel {mesafe:.2f} metre yakında. FREN YAPILIYOR!')
        else:
            self.get_logger().info(f'✅ Yol temiz ({mesafe:.2f}m). Gaz vermeye devam.')

def main(args=None):
    rclpy.init(args=args)
    node = SoforDinleyici()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
