import os



p = os.popen('java -jar gpuworkflowsim.jar')
print("p.read(): {}\n".format(p.read()))
