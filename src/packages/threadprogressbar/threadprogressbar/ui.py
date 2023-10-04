"""
    qtpy dialog that launches a worker and monitors its progress.
"""
#pylint: disable=no-name-in-module
#pylint: disable=too-few-public-methods
import time
from qtpy.QtWidgets import QWidget, QDialog, QLabel, QProgressBar, QVBoxLayout, QPushButton
from qtpy.QtCore import QThread, Signal
from pymxs import runtime as rt

MINRANGE = 1
MAXRANGE = 100

class Worker(QThread):
    """
    Worker thread
    """
    progress = Signal(int)
    aborted = False
    def __init__(self):
        """
        Construct the worker
        """
        QThread.__init__(self)

    def run(self):
        """
        Increment a counter an notify progress.
        Abort if aborted is True
        """
        for i in range(MINRANGE, MAXRANGE):
            self.progress.emit(i)
            time.sleep(0.5)
            if self.aborted:
                return
        self.progress.emit(MAXRANGE)


    def abort(self):
        """
        Make the worker terminate before it's done.
        """
        self.aborted = True

class PyMaxDialog(QDialog):
    """
    Custom dialog attached to the 3ds Max main window
    """
    def __init__(self, parent=QWidget.find(rt.windows.getMAXHWND())):
        super().__init__(parent)
        self.setWindowTitle('Progress')

        main_layout = QVBoxLayout()
        label = QLabel("Progress so far")
        main_layout.addWidget(label)

        # progress bar
        progb = QProgressBar()
        progb.minimum = MINRANGE
        progb.maximum = MAXRANGE
        main_layout.addWidget(progb)

        # abort button
        btn = QPushButton("abort")
        main_layout.addWidget(btn)

        self.setLayout(main_layout)
        self.resize(250, 100)

        # start the worker
        self.worker = Worker()
        self.worker.progress.connect(progb.setValue)
        self.worker.start()

        # connect abort button
        btn.clicked.connect(self.worker.abort)
