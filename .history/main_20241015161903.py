# ---------------------------------------------------------------------------------------------
#  Copyright (c) Yunosuke Ohsugi. All rights reserved.
#  Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------*/

import sys

import qdarktheme
from qdarktheme.qtpy.QtCore import QDir, Qt, Slot
from qdarktheme.qtpy.QtGui import QFont
from qdarktheme.qtpy.QtWidgets import *
from qdarktheme.util import get_project_root_path
from main_ui import UI


class JobSimQt(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self._ui = UI()
        self._ui.setup_ui(self)

        # Signal
        self._ui.action_change_home.triggered.connect(self._change_page)
        self._ui.action_change_dock.triggered.connect(self._change_page)
        self._ui.action_open_folder.triggered.connect(
            lambda: QFileDialog.getOpenFileName(self, "Open File", options=QFileDialog.Option.DontUseNativeDialog)
        )
        self._ui.action_open_color_dialog.triggered.connect(
            lambda: QColorDialog.getColor(parent=self, options=QColorDialog.ColorDialogOption.DontUseNativeDialog)
        )
        self._ui.action_open_font_dialog.triggered.connect(
            lambda: QFontDialog.getFont(QFont(), parent=self, options=QFontDialog.FontDialogOption.DontUseNativeDialog)
        )
        self._ui.action_enable.triggered.connect(self._toggle_state)
        self._ui.action_disable.triggered.connect(self._toggle_state)
        for action in self._ui.actions_theme:
            action.triggered.connect(self._change_theme)

        self.initTreeView()

    @Slot()
    def _change_page(self) -> None:
        action_name = self.sender().text()
        self._ui.stack_widget.setCurrentIndex(0 if action_name == "Move to home" else 1)

    @Slot()
    def _toggle_state(self) -> None:
        state = self.sender().text()
        self._ui.central_window.centralWidget().setEnabled(state == "Enable")
        self._ui.action_enable.setEnabled(state == "Disable")
        self._ui.action_disable.setEnabled(state == "Enable")
        self.statusBar().showMessage(state)

    @Slot()
    def _change_theme(self) -> None:
        theme = self.sender().text()
        QApplication.instance().setStyleSheet(qdarktheme.load_stylesheet(theme))

    def setClicked(self):
        self._ui.homeui.add.clicked.connect(self._add)
        self._ui.homeui.pushButton.clicked.connect(self._delete)

    def initTreeView(self):
       QStandardItem *item1 = new QStandardItem("四年级");
 
    model->setItem(0,0,item1);
    QStandardItem *item00 = new QStandardItem("张三");
    QStandardItem *item10 = new QStandardItem("张四");
    QStandardItem *item20 = new QStandardItem("张五");
 
    QStandardItem *item01 = new QStandardItem("男");
    QStandardItem *item11 = new QStandardItem("女");
    QStandardItem *item21 = new QStandardItem("男");
 
    QStandardItem *item02 = new QStandardItem("15");
    QStandardItem *item12 = new QStandardItem("14");
    QStandardItem *item22 = new QStandardItem("16");
 
    model->item(0,0)->setChild(0,0,item00);
    model->item(0,0)->setChild(1,0,item10);
    model->item(0,0)->setChild(2,0,item20);
 
    model->item(0,0)->setChild(0,1,item01);
    model->item(0,0)->setChild(1,1,item11);
    model->item(0,0)->setChild(2,1,item21);
 
    model->item(0,0)->setChild(0,2,item02);
    model->item(0,0)->setChild(1,2,item12);
    model->item(0,0)->setChild(2,2,item22);



if __name__ == "__main__":
    app = QApplication(sys.argv)
    if hasattr(Qt.ApplicationAttribute, "AA_UseHighDpiPixmaps"):  # Enable High DPI display with Qt5
        app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)
    QDir.addSearchPath("icons", f"{get_project_root_path().as_posix()}/widget_gallery/ui/svg")
    win = JobSimQt()
    win.menuBar().setNativeMenuBar(False)
    app.setStyleSheet(qdarktheme.load_stylesheet())
    win.show()
    app.exec()
