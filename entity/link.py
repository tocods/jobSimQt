class Link:
    name_registry = {}
    def __init__(self, endpoint1, endpoint2, type):
        self.name = ""
        self.set_name('Link')

        # 连接属性，初始化为默认值
        self.link_bandwidth = 100
        self.error_rate = 0

        self.endpoint1 = endpoint1  # 连接一端
        self.endpoint2 = endpoint2  # 连接另一端
        self.type = type

    def applyAttr(self, data):
        self.link_bandwidth = data["link_bandwidth"]
        self.error_rate = data["error_rate"]

    def set_name(self, name):
        # TODO: 检查名字是否符合omnet规范
        # 检查是否重名
        if self.name in Link.name_registry:
            self.del_name(self.name)
        if name in Link.name_registry:         
            Link.name_registry[name] += 1
            # 当重名时，自动加上编号

            # 如果加编号后不重名了
            if not name + str(Link.name_registry[name]) in Link.name_registry:
                self.name = name + str(Link.name_registry[name])
                Link.name_registry.update({name + str(Link.name_registry[name]): 1})
            # 如果加编号后还是重名，继续加编号，递归调用
            else:
                self.set_name(name)

        else:
            self.name = name
            Link.name_registry.update({name: 1})
