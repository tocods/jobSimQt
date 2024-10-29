import os



p = os.popen('java -jar gpuworkflowsi')
print("p.read(): {}\n".format(p.read()))
