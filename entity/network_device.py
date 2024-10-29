class NetworkDevice:
    # 所有NerworkDevice的名字注册表，任何一个NetWorkDevice的名字都不能重名
    name_registry = {}

    def __init__(self, name, device_type):
        self.set_name(name)
        self.type = device_type

    def set_name(self, name):
        # TODO: 检查名字是否符合omnet规范
        # 检查是否重名
        if name in NetworkDevice.name_registry:
            NetworkDevice.name_registry[name] += 1
            if not name + str(NetworkDevice.name_registry[name]) in NetworkDevice.name_registry:
                self.name = name + str(NetworkDevice.name_registry[name])
                NetworkDevice.name_registry.update({name + str(NetworkDevice.name_registry[name]): 1})
            else:
                # 若添加编号后依然重名，则继续添加编号，递归调用
                self.set_name(name)
        else:
            self.name = name
            NetworkDevice.name_registry.update({name: 1})

    def __str__(self):
        return f"{self.__class__.__name__}(name={self.name}, Type={self.type})"

    def setXMLElement(self, element):
        print("no impl")

    def readXMLElement(self, element):
        print("no impl")