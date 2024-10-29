import os



p = os.popen('java -jar gpuworkflow')
print("p.read(): {}\n".format(p.read()))
