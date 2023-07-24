from binaryninja import *
from binaryninjaui import *
from PySide6 import QtCore
import subprocess
import sys
from PySide6.QtCore import Qt, QRectF
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from colored import fore, style

filepath = ""


class PwnAssistantbarWidget(SidebarWidget):
    # Your custom code for handling the button click goes here
    def __init__(self, name, frame, data):
        global instance_id
        global filepath
        SidebarWidget.__init__(self, name)
        self.actionHandler = UIActionHandler()
        self.actionHandler.setupActionHandler(self)

        offset_layout = QHBoxLayout()
        offset_layout.addWidget(QLabel("Offset: "))
        self.offset = QLabel(hex(0))
        offset_layout.addWidget(self.offset)
        offset_layout.setAlignment(QtCore.Qt.AlignCenter)

        datatype_layout = QHBoxLayout()
        datatype_layout.addWidget(QLabel("Data Type: "))
        self.datatype = QLabel("")
        datatype_layout.addWidget(self.datatype)
        datatype_layout.setAlignment(QtCore.Qt.AlignCenter)

        layout = QVBoxLayout()
        # button1 = QPushButton("Run")
        checksec = QLabel("checksec:", self)
        serifFont = QFont("Times", 16, QFont.Bold)
        checksec.setFont(serifFont)

        layout.addWidget(checksec)
        # button1.clicked.connect(self.button_clicked)
        # layout.addWidget(button1)

        instance = QLabel("Instance: " + str(instance_id), self)
        instance.setAlignment(QtCore.Qt.AlignCenter)

        checksec_cmd = ["checksec", filepath]
        try:
            # Run the checksec command and capture its output with ANSI escape codes
            print("Running checksec on", filepath)
            result = subprocess.run(
                checksec_cmd, capture_output=True, text=True, check=True
            )
            txt_edit = QPlainTextEdit("\n".join(result.stderr.splitlines()[1:]))
            txt_edit.setReadOnly(True)
            layout.addWidget(txt_edit)
            
        except FileNotFoundError:
            txt_edit = QTextEdit("error during analysis")
            layout.addWidget(txt_edit)

        layout.addWidget(instance)
        layout.addLayout(datatype_layout)
        layout.addLayout(offset_layout)
        layout.addStretch()
        self.setLayout(layout)
        instance_id += 1
        self.data = data

    # def button_clicked(self):
    #    print("clicked")

    def notifyOffsetChanged(self, offset):
        self.offset.setText(hex(offset))

    def notifyViewChanged(self, view_frame):
        if view_frame is None:
            self.datatype.setText("None")
            self.data = None
        else:
            self.datatype.setText(view_frame.getCurrentView())
            view = view_frame.getCurrentViewInterface()
            self.data = view.getData()

    def contextMenuEvent(self, event):
        self.m_contextMenuManager.show(self.m_menu, self.actionHandler)


class PwnAssistantbarWidgetType(SidebarWidgetType):
    def __init__(self, bv):
        self.current_view = bv
        global filepath
        filepath = bv.file.original_filename
        # Sidebar icons are 28x28 points. Should be at least 56x56 pixels for
        # HiDPI display compatibility. They will be automatically made theme
        # aware, so you need only provide a grayscale image, where white is
        # the color of the shape.
        icon = QImage(56, 56, QImage.Format_RGB32)
        icon.fill(0)

        # Render an "H" as the example icon
        p = QPainter()
        p.begin(icon)
        p.setFont(QFont("Open Sans", 20))
        p.setPen(QColor(255, 255, 255, 255))
        p.drawText(QRectF(0, 0, 56, 56), Qt.AlignCenter, "PWN")
        p.end()

        SidebarWidgetType.__init__(self, icon, "PWN")

    def createWidget(self, frame, data):
        # This callback is called when a widget needs to be created for a given context. Different
        # widgets are created for each unique BinaryView. They are created on demand when the sidebar
        # widget is visible and the BinaryView becomes active.
        return PwnAssistantbarWidget("PWN Assistant", frame, data)


# Register the sidebar widget type with Binary Ninja. This will make it appear as an icon in the
# sidebar and the `createWidget` method will be called when a widget is required.
# Sidebar.addSidebarWidgetType(PwnAssistantbarWidgetType())
instance_id = 0
