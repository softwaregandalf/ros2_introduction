from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    # 1. Orkestra Elemanı: Radar Düğümü
    radar_node = Node(
        package='gelismis_surus',
        executable='coklu_radar',
        name='radar_sistemi'
    )

    # 2. Orkestra Elemanı: Karar Merkezi (Şoför)
    # output='screen' diyerek şoförün uyarılarını ana ekranda görmek istediğimizi belirtiyoruz
    sofor_node = Node(
        package='gelismis_surus',
        executable='karar_merkezi',
        name='sofor_sistemi',
        output='screen'
    )

    # İkisini aynı anda sahneye sürüyoruz
    return LaunchDescription([radar_node, sofor_node])
