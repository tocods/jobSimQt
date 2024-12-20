# ---------------------------------------------------------------------------------------------
#  Copyright (c) Yunosuke Ohsugi. All rights reserved.
#  Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------*/

from qdarktheme.qtpy.QtCore import Qt
from qdarktheme.qtpy.QtGui import QAction, QActionGroup, QIcon, QFont
from qdarktheme.qtpy.QtWidgets import (
    QMainWindow,
    QMenuBar,
    QSizePolicy,
    QStackedWidget,
    QStatusBar,
    QToolBar,
    QToolButton,
    QWidget,
    QTabWidget
)
from component.home import Ui_home
from component.result import Ui_Result
from Window.NetworkEditorWindow import NetworkEditorWindow

class UI:
    def setup_ui(self, main_win: QMainWindow) -> None:
        f = QFont()
        f.setPointSize(15)
        # Actions
        self.action_change_home = QAction("建模与仿真")
        self.action_change_dock = QAction("系统管理评估平台")
        self.action_software = QAction("系统管理集成开发平台")
        self.action_open_folder = QAction(QIcon("img/打开文件.png"), "打开项目")
        self.action_open_color_dialog = QAction(QIcon("img/保存文件.png"), "保存项目")
        self.action_open_font_dialog = QAction(QIcon("img/设置时间.png"), "设置仿真时间")
        # self.action_enable = QAction(QIcon("icons:circle_24dp.svg"), "Enable")
        # self.action_disable = QAction(QIcon("icons:clear_24dp.svg"), "Disable")
        self.actions_theme = [QAction(theme, main_win) for theme in ["黑色", "白色"]]
        self.action_out = QAction("退出")
        action_group_toolbar = QActionGroup(main_win)

        # Widgets
        self.central_window = QMainWindow()
        self.stack_widget = QStackedWidget()

        activitybar = QToolBar("activitybar")
        toolbar = QToolBar("Toolbar")
        statusbar = QStatusBar()
        menubar = QMenuBar()
        tool_btn_settings, tool_btn_theme, tool_btn_enable, tool_btn_disable = [QToolButton() for _ in range(4)]

        spacer = QToolButton()

        # Setup Actions
        self.action_change_home.setCheckable(True)
        self.action_change_dock.setCheckable(True)
        self.action_software.setCheckable(True)
        self.action_change_home.setChecked(True)
        #action_group_toolbar.addAction(self.action_change_home)
        action_group_toolbar.addAction(self.action_change_dock)
        action_group_toolbar.addAction(self.action_software)

        # Setup Widgets
        spacer.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        spacer.setEnabled(False)

        activitybar.setMovable(False)
        activitybar.addActions((self.action_change_dock, self.action_software))
        activitybar.addWidget(spacer)
        #activitybar.addWidget(tool_btn_settings)

        # tool_btn_settings.setIcon(QIcon("icons:settings_24dp.svg"))
        # tool_btn_settings.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        # tool_btn_enable.setDefaultAction(self.action_enable)
        # tool_btn_disable.setDefaultAction(self.action_disable)
        tool_btn_theme.setIcon(QIcon("img/样式设置.png"))
        tool_btn_theme.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)

        toolbar.addActions((self.action_open_folder, self.action_open_color_dialog, self.action_open_font_dialog))
        toolbar.addSeparator()
        toolbar.addWidget(tool_btn_theme)

        # statusbar.addPermanentWidget(tool_btn_enable)
        # statusbar.addPermanentWidget(tool_btn_disable)
        # statusbar.showMessage("Enable")

        menu_toggle = menubar.addMenu("系统管理建模和仿真工具")
        menu_toggle.setFont(f)
        # menu_toggle.addActions((self.action_enable, self.action_disable))
        menu_toggle.addActions((self.action_out,))
        menu_theme = menubar.addMenu("")
        menu_theme.addActions(self.actions_theme)
     
        
        # menu_dialog = menubar.addMenu("&Dialog")
        # menu_dialog.addActions((self.action_open_folder, self.action_open_color_dialog, self.action_open_font_dialog))

        tool_btn_settings.setMenu(menu_toggle)

       
        tool_btn_theme.setMenu(menu_theme)

        #self.action_enable.setEnabled(False)

        # setup custom property
        activitybar.setProperty("type", "activitybar")

        # layout
        stack1 = QTabWidget()
        stack_1 = QWidget()
        self.homeui = Ui_home()
        #HomeUI().setup_ui(stack_1)
        self.homeui.setupUi(stack_1)
        stack1.addTab(stack_1, "系统仿真")
        self.network_editor = NetworkEditorWindow()
        stack1.addTab(self.network_editor, "网络仿真")
        self.stack_widget.addWidget(stack1)
        stack2 = QWidget()
        self.resultui = Ui_Result()
        #ResultUI().setup_ui(stack2)
        self.resultui.setupUi(stack2)
        #DockUI().setup_ui(stack2)
        self.stack_widget.addWidget(stack2)

        self.central_window.setCentralWidget(self.stack_widget)
        self.central_window.addToolBar(toolbar)

        main_win.setCentralWidget(self.central_window)
        main_win.addToolBar(Qt.ToolBarArea.LeftToolBarArea, activitybar)
        main_win.setMenuBar(menubar)
        main_win.setStatusBar(statusbar)
