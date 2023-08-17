
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QSpinBox, QLabel, QDoubleSpinBox
import sys

LABEL_ENERGY = "Energy (keV)"
LABEL_WAVELENGTH = "Wavelength (nm)"
LABEL_DISTANCE = "Distance (mm)"
LABEL_RADIUS_BS = "Beamstop radius (mm)"

ENERGY_DEFAULT = 12.4
ENERGY_STEP = 0.1
ENERGY_RANGE = (0, 1000)
DISTANCE_DEFAULT = 200
DISTANCE_STEP = 1
DISTANCE_RANGE = (0, 1E4)
BEAMSTOP_RADIUS_DEFAULT = 5
BEAMSTOP_RADIUS_STEP = 1
BEAMSTOP_RADIUS_RANGE = (0, 1E2)


class QCalcWidgetLayOut(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._build()

    def _build(self):
        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)

        self.input_grid = QGridLayout()
        self.result_grid = QGridLayout()

        self.grid_layout.addLayout(self.input_grid, 1, 1)
        self.grid_layout.addLayout(self.result_grid, 2, 1)

        self.label_energy = QLabel(LABEL_ENERGY)
        self.spinbox_energy = QDoubleSpinBox()
        self.spinbox_energy.setSingleStep(ENERGY_STEP)
        self.spinbox_energy.setValue(ENERGY_DEFAULT)
        self.spinbox_energy.setRange(ENERGY_RANGE[0], ENERGY_RANGE[1])
        self.label_wavelength = QLabel(LABEL_WAVELENGTH)
        self.spinbox_wavelength = QDoubleSpinBox()
        self.label_distance = QLabel(LABEL_DISTANCE)
        self.spinbox_distance = QDoubleSpinBox()
        self.spinbox_distance.setSingleStep(DISTANCE_STEP)
        self.spinbox_distance.setRange(DISTANCE_RANGE[0], DISTANCE_RANGE[1])
        self.spinbox_distance.setValue(DISTANCE_DEFAULT)
        self.label_radius = QLabel(LABEL_RADIUS_BS)
        self.spinbox_radius = QDoubleSpinBox()
        self.spinbox_radius.setRange(BEAMSTOP_RADIUS_RANGE[0], BEAMSTOP_RADIUS_RANGE[1])
        self.spinbox_radius.setSingleStep(BEAMSTOP_RADIUS_STEP)
        self.spinbox_radius.setValue(BEAMSTOP_RADIUS_DEFAULT)

        self.input_grid.addWidget(self.label_energy, 1, 1)
        self.input_grid.addWidget(self.spinbox_energy, 1, 2)
        self.input_grid.addWidget(self.label_wavelength, 2, 1)
        self.input_grid.addWidget(self.spinbox_wavelength, 2, 2)
        self.input_grid.addWidget(self.label_distance, 3, 1)
        self.input_grid.addWidget(self.spinbox_distance, 3, 2)
        self.input_grid.addWidget(self.label_radius, 4, 1)
        self.input_grid.addWidget(self.spinbox_radius, 4, 2)


class QCalcWidget(QCalcWidgetLayOut):
    def __init__(self) -> None:
        super().__init__()


class QCalcWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self._guiwidget = QCalcWidget()
        self.setCentralWidget(self._guiwidget)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = QCalcWindow()

    main_window.show()
    app.exec_()