'''
Demonstrates combining the mesh of two scene nodes
'''
from qtpy.QtWidgets import QVBoxLayout, QPushButton, QLabel, QDialog, QMessageBox
from pymxs import runtime as rt # pylint: disable=import-error
from qtmax import GetQMaxMainWindow

def combine_two_meshes():
    """
    Convert the two provided objects to meshes and merges them as a single editable mesh.
    """
    if len(rt.getCurrentSelection()) != 2:
        msg = "Please select 2 nodes to combine."
        show_alert(msg)
    else:
        first_item_selected = rt.convertToMesh(rt.getCurrentSelection()[0])
        second_item_selected = rt.convertToMesh(rt.getCurrentSelection()[1])
        # create a new, empty editable mesh for the combined meshes
        new_obj = rt.Editable_mesh()
        # combine 'first_item_selected' and 'second_item_selected' into the new mesh
        mesh_operation = rt.meshOp
        mesh_operation.attach(new_obj, first_item_selected, deleteSourceNode=False)
        mesh_operation.attach(new_obj, second_item_selected, deleteSourceNode=False)

def show_alert(message):
    """
    Display a message using a Qt Message Box.
    """
    msg_box = QMessageBox()
    msg_box.setText(message)
    msg_box.exec_()

def demo_combine_meshes():
    """
    Demonstrates combining the mesh of two scene nodes
    Prompt user to select two nodes to be merged and merge them.
    """
    dialog = QDialog(GetQMaxMainWindow())
    dialog.resize(250, 100)
    dialog.setWindowTitle('DEMO - Combine 2 Nodes')

    main_layout = QVBoxLayout()
    label = QLabel("Combine 2 Nodes")
    main_layout.addWidget(label)

    combine_btn = QPushButton("Combine")
    combine_btn.clicked.connect(combine_two_meshes)
    main_layout.addWidget(combine_btn)

    dialog.setLayout(main_layout)
    dialog.show()

demo_combine_meshes()
