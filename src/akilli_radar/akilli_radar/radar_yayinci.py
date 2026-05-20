import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32 # Sadece ondalıklı sayı göndereceğimiz için bu mesaj tipini seçtik
import random # Rastgele mesafe üretmek için

class RadarYayinci(Node):
    def __init__(self):
        super().__init__('radar_yayinci')
        
        # 'on_mesafe' adında bir kanaldan (topic) sayı (Float32) yayınlayacağımızı sisteme söylüyoruz
        self.publisher_ = self.create_publisher(Float32, 'on_mesafe', 10)
        
        # Her 1 saniyede bir ölçüm fonksiyonunu tetikliyoruz
        self.timer = self.create_timer(1.0, self.mesafe_olc)

    def mesafe_olc(self):
        msg = Float32()
        
        # Sanki gerçek bir sensörmüş gibi 0.5 metre ile 10.0 metre arası rastgele bir mesafe değeri üretiyoruz
        msg.data = random.uniform(0.5, 10.0)
        
        # Ürettiğimiz veriyi 'on_mesafe' kanalına aktarıyoruz
        self.publisher_.publish(msg)
        self.get_logger().info(f'📡 Radardan gelen veri: {msg.data:.2f} metre')

def main(args=None):
    rclpy.init(args=args)
    node = RadarYayinci()
    rclpy.spin(node) # Düğümü sürekli açık tut
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
