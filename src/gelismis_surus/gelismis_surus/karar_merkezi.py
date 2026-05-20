import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from std_srvs.srv import SetBool # ROS 2'nin standart True/False servis kütüphanesi

class KararMerkezi(Node):
    def __init__(self):
        super().__init__('karar_merkezi')
        
        self.mesafe_on = 8.0
        self.mesafe_sag = 8.0
        self.mesafe_sol = 8.0
        
        # Aracın kilitli olup olmadığını tutan ana güvenlik anahtarı
        self.sistem_kilitli = False

        self.create_subscription(Float32, 'sensor/on', self.cb_on, 10)
        self.create_subscription(Float32, 'sensor/sag', self.cb_sag, 10)
        self.create_subscription(Float32, 'sensor/sol', self.cb_sol, 10)

        # 'acil_stop' adında bir servis sunucusu (Server) oluşturuyoruz
        self.srv = self.create_service(SetBool, 'acil_stop', self.acil_stop_callback)

        self.create_timer(1.0, self.manevra_yap)

    def acil_stop_callback(self, request, response):
        # Dışarıdan gelen isteğe (True/False) göre sistemi kilitle veya aç
        if request.data == True:
            self.sistem_kilitli = True
            response.success = True
            response.message = "SİSTEM KİLİTLENDİ!"
            self.get_logger().error('🚨 DIŞARIDAN MÜDAHALE: MOTORLAR KİLİTLENDİ!')
        else:
            self.sistem_kilitli = False
            response.success = True
            response.message = "Otonom sürüş devrede."
            self.get_logger().info('🟢 KİLİT AÇILDI. Sistem normale döndü.')
        return response

    def cb_on(self, msg): self.mesafe_on = msg.data
    def cb_sag(self, msg): self.mesafe_sag = msg.data
    def cb_sol(self, msg): self.mesafe_sol = msg.data

    def manevra_yap(self):
        # Eğer sistem kilitliyse sensörlere hiç bakma, doğrudan çık!
        if self.sistem_kilitli:
            self.get_logger().error('Sistem kilitli... Bekleniyor.')
            return

        # Kilitli değilse normal otonom karar mekanizması
        if self.mesafe_on < 3.0:
            self.get_logger().warning(f'⚠️ ÖN KAPALI ({self.mesafe_on:.1f}m)!')
            if self.mesafe_sag > 3.0:
                self.get_logger().info('↪️ Sağ boş, sağa kırılıyor!')
            elif self.mesafe_sol > 3.0:
                self.get_logger().info('↩️ Sol boş, sola kırılıyor!')
            else:
                self.get_logger().warning('🛑 HER YER KAPALI! TAM FREN YAPILDI!')
        else:
            self.get_logger().info(f'✅ Rota temiz ({self.mesafe_on:.1f}m), düz devam.')

def main(args=None):
    rclpy.init(args=args)
    node = KararMerkezi()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
