import subprocess

a = subprocess.getoutput('ping www.baidu.com')
print (a)