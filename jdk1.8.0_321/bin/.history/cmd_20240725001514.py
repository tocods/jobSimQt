import os



p = os.popen('ipconfig')
print("p.read(): {}\n".format(p.read()))
