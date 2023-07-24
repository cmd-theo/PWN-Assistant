from binaryninja import *
from binaryninjaui import *
from PySide6 import QtCore
import subprocess
import sys
from PySide6.QtCore import Qt, QRectF
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from .pwnassistant import *

pwnState = 0


def version(bv):
    show_message_box(
        "Version",
        "1.1- Alpha.\n\n" + "Pat yourself on the back.",
        MessageBoxButtonSet.OKButtonSet,
        MessageBoxIcon.InformationIcon,
    )


def run(bv):
    global pwnState
    pwnState += 1
    if pwnState == 1:
        Sidebar.addSidebarWidgetType(PwnAssistantbarWidgetType(bv))
        instance_id = 0
        # filename = bv.file.original_filename
        # print(filename)
    else:
        print("PWN Assistant already launched")


PluginCommand.register("PWN Assistant\\Version", "Show current version", version)
PluginCommand.register(
    "PWN Assistant\\Run", "Highlights parameters with color highlights", run
)
