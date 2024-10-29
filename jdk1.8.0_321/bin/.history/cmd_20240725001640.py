import os



p = os.popen('java -jar gpuworkflowsim.jar D:\gpuworkflowsim\OutputFiles D:\gpuworkflowsim\input\Hosts.xml D:\gpuworkflowsim\input\Jobs.xml 1')
print("p.read(): {}\n".format(p.read()))
