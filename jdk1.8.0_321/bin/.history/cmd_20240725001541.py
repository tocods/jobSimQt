import os



p = os.popen('java -jar ')
print("p.read(): {}\n".format(p.read()))
