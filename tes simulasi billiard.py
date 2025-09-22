from coppeliasim_zmqremoteapi_client import RemoteAPIClient
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtCore import QCoreApplication
import sys
import math

# Inisialisasi klien CoppeliaSim di luar kelas
client = RemoteAPIClient()
sim = client.getObject('sim')
sim.setStepping(False)
sim.startSimulation()

class BilliardApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.b2_Handle = sim.getObject("/Sphere[6]")

    def init_ui(self):
        self.setWindowTitle("Kontrol Bola Putih")
        self.setGeometry(10, 10, 20, 15)
        
        # Buat tombol-tombol
        self.btn_up = QPushButton("Atas (W)")
        self.btn_down = QPushButton("Bawah (S)")
        self.btn_left = QPushButton("Kiri (A)")
        self.btn_right = QPushButton("Kanan (D)")
        
        # Hubungkan tombol dengan fungsi kontrol
        self.btn_up.clicked.connect(lambda: self.apply_force(10))
        self.btn_down.clicked.connect(lambda: self.apply_force(30))
        self.btn_left.clicked.connect(lambda: self.apply_force(20))
        self.btn_right.clicked.connect(lambda: self.apply_force(0))
        
        # Atur tata letak
        layout = QVBoxLayout()
        layout.addWidget(self.btn_up)
        layout.addWidget(self.btn_down)
        layout.addWidget(self.btn_left)
        layout.addWidget(self.btn_right)
        self.setLayout(layout)

    def apply_force(self, direction_angle_deg):
        force_magnitude = 5
        direction_angle_rad = math.radians(direction_angle_deg)
        force_x = force_magnitude * math.cos(direction_angle_rad)
        force_y = force_magnitude * math.sin(direction_angle_rad)
        force_vector = [force_x, force_y, 0]
        
        sim.addForce(self.b2_Handle, sim.getObjectPosition(self.b2_Handle, -1), force_vector)
        sim.addStatusbarMessage(f"Gaya diterapkan. Arah: {direction_angle_deg}°, Kekuatan: {force_magnitude} N")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BilliardApp()
    ex.show()
    sys.exit(app.exec_())