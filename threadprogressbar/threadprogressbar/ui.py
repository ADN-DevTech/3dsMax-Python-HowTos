"""
    PySide2 dialog that launches a worker and monitors its progress.
"""
from PySide2.QtWidgets import QWidget, QDialog, QLabel, QProgressBar, QVBoxLayout, QPushButton
from PySide2.QtCore import QThread, Signal
import time

MINRANGE=1
MAXRANGE=100

class Worker(QThread):
    progress = Signal(int)
    aborted = False
    def __init__(self):
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
        super(PyMaxDialog, self).__init__(parent)
        self.setWindowTitle('Progress')

        main_layout = QVBoxLayout()
        label = QLabel("Progress so far")
        main_layout.addWidget(label)

        # progress bar
        pb = QProgressBar()
        pb.minimum = MINRANGE
        pb.maximum = MAXRANGE
        main_layout.addWidget(pb)

        # abort button
        btn = QPushButton("abort")
        main_layout.addWidget(btn)

        self.setLayout(main_layout)
        self.resize(250, 100)

        # start the worker
        self.worker = Worker()
        self.worker.progress.connect(pb.setValue)
        self.worker.start()

        # connect abort button
        btn.clicked.connect(self.worker.abort)
