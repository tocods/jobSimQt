import os



p = os.popen('java -jar gpuworkflowsim')
print("p.read(): {}\n".format(p.read()))
