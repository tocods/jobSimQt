from qdarktheme.qtpy.QtWidgets import QDialog
from UI.Network.Host.set_host_args_ui import Ui_Dialog
from entity.host import *


class SetHostArgsWindow(QDialog):

    def __init__(self, parent=None, jobSim=None):
        QDialog.__init__(self)
        self.parent = parent
        self.jobSim = jobSim
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle("设置主机属性")
        # 编辑对象名称
        self.ui.lineEdit_name.textEdited.connect(self.lineEdit_name_cb)
        # 编辑网络属性
        self.ui.netButton.clicked.connect(self.netButton_cb)

        # 用于保存当前配置的主机
        self.hostGraphicItem = None

        self.hide()

    def setHostGraphicItem(self, hostGraphicItem):
        self.hostGraphicItem = hostGraphicItem
        # 将当前主机名显示在界面上
        self.ui.lineEdit_name.setText(self.hostGraphicItem.hostAttr.name)

    def binGraphicsItem(self, item):
        self.item = item
        self.ui.lineEdit_name.setText(self.jobSim.hosts[item].name)

    def lineEdit_name_cb(self):
        name = self.ui.lineEdit_name.text()

        # 网络属性，更新主机名称
        if name != self.hostGraphicItem.hostAttr.name:
            #self.hostGraphicItem.hostAttr.del_name(self.hostGraphicItem.hostAttr.name)
            self.hostGraphicItem.hostAttr.set_name(name)

            # 若重名自动添加编号后缀时，更新画布上的主机名称
            self.ui.lineEdit_name.setText(self.hostGraphicItem.hostAttr.name)

        print("Host name: " + self.hostGraphicItem.hostAttr.name)
        self.hostGraphicItem.setName(name)

        # 主机属性
        self.jobSim.hosts[self.item].name = name
        print("名称：" + name)

        self.parent.parent.update_tree_view()

    def netButton_cb(self):
        self.hide()
        if isinstance(self.hostGraphicItem.hostAttr, NormalHost):
            self.parent.editHostNetargsWindowNormal.setHostGraphicItem(
                self.hostGraphicItem
            )
            self.parent.editHostNetargsWindowNormal.show()
        if isinstance(self.hostGraphicItem.hostAttr, UdpHost):
            self.parent.editHostNetargsWindowUdp.setHostGraphicItem(
                self.hostGraphicItem
            )
            self.parent.editHostNetargsWindowUdp.show()
        if isinstance(self.hostGraphicItem.hostAttr, TsnHost):
            self.parent.editHostNetargsWindowTsn.setHostGraphicItem(
                self.hostGraphicItem
            )
            self.parent.editHostNetargsWindowTsn.show()
        if isinstance(self.hostGraphicItem.hostAttr, TcpHost):
            self.parent.editHostNetargsWindowTcp.setHostGraphicItem(
                self.hostGraphicItem
            )
            self.parent.editHostNetargsWindowTcp.show()
        if isinstance(self.hostGraphicItem.hostAttr, DdsHost):
            self.parent.editHostNetargsWindowDds.setHostGraphicItem(
                self.hostGraphicItem
            )
            self.parent.editHostNetargsWindowDds.show()
        if isinstance(self.hostGraphicItem.hostAttr, RdmaHost):
            self.parent.editHostNetargsWindowRdma.setHostGraphicItem(
                self.hostGraphicItem
            )
            self.parent.editHostNetargsWindowRdma.show()
        # self.hide()

    def sysButton_cb(self):
        # print("sysbutton")
        self.parent.hostInform.showItem(self.item)
        # self.parent.hostInform.show()
        self.hide()


# if __name__ == '__main__':

#     app = QApplication(sys.argv)
#     window = NewProjectWindow()
#     sys.exit(app.exec())
