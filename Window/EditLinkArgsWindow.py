from qdarktheme.qtpy.QtWidgets import (
    QDialog,
)
from UI.Network.edit_link_args_ui import Ui_Dialog


class EditLinkArgsWindow(QDialog):

    def __init__(self, parent=None):
        QDialog.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("编辑连接属性")

        # 用于保存当前配置的连接
        self.linkGraphicItem = None

        # # 编辑对象名称
        # self.ui.lineEdit_bw_2.returnPressed.connect(self.lineEdit_name_cb)

        # # 编辑链路带宽
        # self.ui.lineEdit_bw.returnPressed.connect(self.lineEdit_bw_cb)

        # 确定
        self.ui.applyButton.clicked.connect(self.apply_link)

        self.hide()

    def setLinkGraphicItem(self, linkGraphicItem):
        self.linkGraphicItem = linkGraphicItem
        # 将当前连接的属性显示在界面上
        self.ui.lineEdit_bw_2.setText(self.linkGraphicItem.edge_wrap.linkAttr.name)
        self.ui.lineEdit_bw.setText(
            str(self.linkGraphicItem.edge_wrap.linkAttr.link_bandwidth)
        )

    def lineEdit_name_cb(self):
        return

    def lineEdit_bw_cb(self):
        return

    def apply_link(self):
        # 更新连接名称
        name = self.ui.lineEdit_bw_2.text()
        if name != self.linkGraphicItem.edge_wrap.linkAttr.name:
            self.linkGraphicItem.edge_wrap.linkAttr.set_name(name)
            # 更新画布上的连接名称
            # self.ui.lineEdit_bw_2.setText(self.linkGraphicItem.edge_wrap.linkAttr.name)
            print("Link name: " + self.linkGraphicItem.edge_wrap.linkAttr.name)
        # 更新连接带宽
        bw = self.ui.lineEdit_bw.text()
        """ TODO: 有风险，带宽可能是小数 """
        if not bw.isdigit():
            print(f"Link 带宽非数字")
            self.ui.lineEdit_bw.setText("0")
            return
        else:
            self.linkGraphicItem.edge_wrap.linkAttr.link_bandwidth = int(bw)
            print(
                f"Link {self.linkGraphicItem.edge_wrap.linkAttr.name} link_bandwidth change to {bw}"
            )
        self.hide()
