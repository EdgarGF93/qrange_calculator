
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QSpinBox, QLabel, QDoubleSpinBox, QComboBox
from PyQt5.QtGui import QFont
from scipy.constants import h, c, e
import numpy as np
import sys

LABEL_ENERGY = "Energy (keV)"
LABEL_WAVELENGTH = "Wavelength (nm)"
LABEL_DISTANCE = "Distance (mm)"
LABEL_RADIUS_BS = "Beamstop radius (mm)"
LABEL_DETECTOR = "Detector"
RESULTS_DEFAULT = "HOLA"

DICT_DETECTOR_SIZE = {
    "MarCCD" : {
        "Shape" : np.array([2048, 2048]),
        "Pixel" : 0.079,
    },
    "Pilatus1M" :{
        "Shape" : np.array([981, 1043]),
        "Pixel" : 0.172,
    },
    "Pilatus300k" :{
        "Shape" : np.array([487, 619]),
        "Pixel" : 0.172,
    },
}

ENERGY_DEFAULT = 12.4
WAVELENGTH_DEFAULT = 0.1
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
        self.label_energy_result = QLabel()
        self.label_wavelength = QLabel(LABEL_WAVELENGTH)
        self.spinbox_wavelength = QDoubleSpinBox()
        self.spinbox_wavelength.setValue(WAVELENGTH_DEFAULT)
        self.label_wavelength_result = QLabel()
        self.label_distance = QLabel(LABEL_DISTANCE)
        self.spinbox_distance = QDoubleSpinBox()
        self.spinbox_distance.setSingleStep(DISTANCE_STEP)
        self.spinbox_distance.setRange(DISTANCE_RANGE[0], DISTANCE_RANGE[1])
        self.spinbox_distance.setValue(DISTANCE_DEFAULT)
        self.label_distance_result = QLabel()
        self.label_radius = QLabel(LABEL_RADIUS_BS)
        self.spinbox_radius = QDoubleSpinBox()
        self.spinbox_radius.setRange(BEAMSTOP_RADIUS_RANGE[0], BEAMSTOP_RADIUS_RANGE[1])
        self.spinbox_radius.setSingleStep(BEAMSTOP_RADIUS_STEP)
        self.spinbox_radius.setValue(BEAMSTOP_RADIUS_DEFAULT)
        self.label_radius_result = QLabel()
        self.label_detector = QLabel(LABEL_DETECTOR)
        self.combobox_detector =QComboBox()
        for detector in DICT_DETECTOR_SIZE.keys():
            self.combobox_detector.addItem(detector)
        self.label_detector_result = QLabel()
        
        self.input_grid.addWidget(self.label_energy, 1, 1)
        self.input_grid.addWidget(self.spinbox_energy, 1, 2)
        self.input_grid.addWidget(self.label_energy_result, 1, 3)
        self.input_grid.addWidget(self.label_wavelength, 2, 1)
        self.input_grid.addWidget(self.spinbox_wavelength, 2, 2)
        self.input_grid.addWidget(self.label_wavelength_result, 2, 3)
        self.input_grid.addWidget(self.label_distance, 3, 1)
        self.input_grid.addWidget(self.spinbox_distance, 3, 2)
        self.input_grid.addWidget(self.label_distance_result, 3, 3)
        self.input_grid.addWidget(self.label_radius, 4, 1)
        self.input_grid.addWidget(self.spinbox_radius, 4, 2)
        self.input_grid.addWidget(self.label_radius_result, 4, 3)
        self.input_grid.addWidget(self.label_detector, 5, 1)
        self.input_grid.addWidget(self.combobox_detector, 5, 2)
        self.input_grid.addWidget(self.label_detector_result, 5, 3)

        self.label_results = QLabel(RESULTS_DEFAULT)
        self.result_grid.addWidget(self.label_results)
        self.label_results.setFont(QFont('Arial', 20))


class QCalcWidget(QCalcWidgetLayOut):
    def __init__(self) -> None:
        super().__init__()
        self.start_callbacks()
        self.update_distance()
        self.update_energy()
        self.update_wavelength()
        self.update_radius()
        self.update_detector()
        self.update_results()
    
    def update_distance(self):
        self.distance = self.spinbox_distance.value()
        self.label_distance_result.setText(f"Distance: {str(self.distance)} mm")
        
    def update_energy(self):
        self.energy = self.spinbox_energy.value()
        self.label_energy_result.setText(f"Energy: {str(self.energy)} keV")
        energy_J = self.energy * 1e3 * e
        self.wavelength = h * c / energy_J * 1e9
        self.label_wavelength_result.setText(f"Wavelength: {str(self.wavelength)} nm")

    def update_wavelength(self):
        self.wavelength = self.spinbox_wavelength.value()
        self.label_wavelength_result.setText(f"Wavelength: {str(self.wavelength)} nm")
        wav_m = self.wavelength / 1e9
        self.energy = h * c / wav_m / e
        self.label_energy_result.setText(f"Energy: {str(self.energy)} keV")

    def update_radius(self):
        self.radius = self.spinbox_radius.value()
        self.label_radius_result.setText(f"Beamstop radius: {str(self.radius)} mm")

    def update_detector(self):
        self.detector = DICT_DETECTOR_SIZE.get(self.combobox_detector.currentText())
        self.detector_shape = self.detector.get("Shape")
        self.detector_pixel = self.detector.get("Pixel")
        self.label_detector_result.setText(f"Detector shape: [{self.detector_shape[0]}, {self.detector_shape[1]}]")
        self.detector_diagonal = np.sqrt((self.detector_shape[0] * self.detector_pixel) ** 2 + (self.detector_shape[1] * self.detector_pixel) ** 2)
        self.detector_radius = self.detector_diagonal / 2

    def start_callbacks(self):
        self.spinbox_distance.valueChanged.connect(
            lambda:
            (
                self.update_distance(),
                self.update_results(),
            )
        )
        self.spinbox_energy.valueChanged.connect(
            lambda:
            (
                self.update_energy(),
                self.update_results(),
            )
        )
        self.spinbox_wavelength.valueChanged.connect(
            lambda:
            (
                self.update_wavelength(),
                self.update_results(),
            )
        )
        self.spinbox_radius.valueChanged.connect(
            lambda:
            (
                self.update_radius(),
                self.update_results(),
            )
        )
        self.combobox_detector.currentTextChanged.connect(
            lambda:
            (
                self.update_detector(),
                self.update_results(),
            )
        )

    def tth_to_q(self, tth, wavelength):
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
            wavelength=self.wavelength,
        )
        return q_min

    def get_max_2theta(self, distance, diagonal):
        tth_max = np.arctan(diagonal / distance)
        return tth_max

    def get_max_q(self, distance, diagonal):
        tth_max = np.arctan(diagonal / distance)
        q_max = self.tth_to_q(
            tth=tth_max, 
            wavelength=self.wavelength,
        )
        return q_max

    def update_results(self):

        tth_min = self.get_min_2theta(
            beamstop_radius=self.radius,
            distance=self.distance,
        )
        tth_min_degs = np.rad2deg(tth_min)

        q_min = self.get_min_q(
            beamstop_radius=self.radius,
            distance=self.distance,
            energy=self.energy,
        )
        q_min_A = q_min / 10
        d_max = 1 / q_min

        tth_max_full = self.get_max_2theta(
            diagonal=self.detector_diagonal,
            distance=self.distance,
        )
        tth_max_full_degs = np.rad2deg(tth_max_full)

        tth_max_half = self.get_max_2theta(
            diagonal=self.detector_radius,
            distance=self.distance,
        )
        tth_max_half_degs = np.rad2deg(tth_max_half)

        q_max_full = self.tth_to_q(
            tth=tth_max_full, 
            wavelength=self.wavelength,
        )
        q_max_half = self.tth_to_q(
            tth=tth_max_half, 
            wavelength=self.wavelength,
        )

        q_label = "$nm^{-1}$"
        cmd_th = f"2\u03b8 = {tth_min_degs:.2f}\u00b0 - {tth_max_half_degs:.2f}\u00b0 (from center) - {tth_max_full_degs:.2f}\u00b0 (full diagonal)"
        cmd_q = f"q = {q_min:.2f}nm-1 - {q_max_half:.2f}nm-1 (from center) - {q_max_full:.2f}nm-1 (full diagonal)."
        cmd = f"{cmd_th}\n{cmd_q}"

        self.label_results.setText(cmd)





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