
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QSpinBox, QLabel, QDoubleSpinBox, QComboBox
import numpy as np
import sys

LABEL_ENERGY = "Energy (keV)"
LABEL_WAVELENGTH = "Wavelength (nm)"
LABEL_DISTANCE = "Distance (mm)"
LABEL_RADIUS_BS = "Beamstop radius (mm)"
LABEL_DETECTOR = "Detector"
RESULTS_DEFAULT = "HOLA"

DICT_DETECTOR_SIZE = {
    "MarCCD" : np.array([2048, 2048]),
    "Pilatus1M" : np.array([981, 1043]),
    "Pilatus300k" : np.array([487, 619])
}


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
        self.label_detector = QLabel(LABEL_DETECTOR)
        self.combobox_detector =QComboBox()
        for detector in DICT_DETECTOR_SIZE.keys():
            self.combobox_detector.addItem(detector)

        self.input_grid.addWidget(self.label_energy, 1, 1)
        self.input_grid.addWidget(self.spinbox_energy, 1, 2)
        self.input_grid.addWidget(self.label_wavelength, 2, 1)
        self.input_grid.addWidget(self.spinbox_wavelength, 2, 2)
        self.input_grid.addWidget(self.label_distance, 3, 1)
        self.input_grid.addWidget(self.spinbox_distance, 3, 2)
        self.input_grid.addWidget(self.label_radius, 4, 1)
        self.input_grid.addWidget(self.spinbox_radius, 4, 2)
        self.input_grid.addWidget(self.label_detector, 5, 1)
        self.input_grid.addWidget(self.combobox_detector, 5, 2)

        self.label_results = QLabel(RESULTS_DEFAULT)
        self.result_grid.addWidget(self.label_results)


class QCalcWidget(QCalcWidgetLayOut):
    def __init__(self) -> None:
        super().__init__()
        self.update_parameters()
        self.start_callbacks()
    
    def update_parameters(self):
        self.distance = self.spinbox_distance.getValue()
        self.distance = float(self.distance)
        self.energy = self.spinbox_energy.getValue()
        self.energy = float(self.energy)
        self.bs_radius = self.bs_radius.getValue()
        self.bs_radius = float(self.bs_radius)
        self.detector = self.combobox_detector.currentText()

    def start_callback(self):
        self.spinbox_distance.valueChanged.connect(
            lambda:
            (
                self.update_parameters(),
                self.update_results(),
            )
        )


    def tth_to_q(self, tth, energy):
        wavelength = 1.2398 / energy
        q = 4 * np.pi / wavelength * np.sin(tth / 2)
        return q

    def q_to_tth(self, q, energy):
        wavelength = 1.2398 / energy
        tth = 2 * np.arcsin(wavelength * q / (4 * np.pi))
        return tth

    def get_min_2theta(self, beamstop_radius, distance):
        min_2theta = np.arctan(beamstop_radius / distance)
        return min_2theta
    
    def get_min_q(self, beamstop_radius, distance, energy):
        min_2theta = self.get_min_2theta(
            beamstop_radius=beamstop_radius,
            distance=distance,
        )
        q_min = self.tth_to_q(
            tth=min_2theta,
            energy=energy,
        )

    def get_max_d(self):
        pass

    def update_results(self):
        min_2theta
        print('The minimum 2theta is %f rads (%f degrees)' % (min_2theta, (min_2theta*180/np.pi)))
        print('The minimum q is %f nm-1 (%f A-1)' % (q_min, q_min/10))
        print('The maximum d is %f nanometers\n' % d_max)




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