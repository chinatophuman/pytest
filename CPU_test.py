import paramiko
import logging


class CPU_test:
    def __init__(self, logname, buildoption_type, hostname, port, username, password):
        self.logname = logname
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.buildoption_type = buildoption_type

    def test_content(self):

        # create SSH item
        ssh = paramiko.SSHClient()
        # permit connect to remote host
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # connect
        ssh.connect(hostname=self.hostname, port=self.port, username=self.username, password=self.password)

        logging.info("\rCPU test start \r")
        CPU_result = 'FAIL'
        stdin, stdout, stderr = ssh.exec_command("cat /proc/cpuinfo | grep 'model name'")
        cpu_info = stdout.read()
        cpu_info_error = stderr.read()
        cpu_type = cpu_info.split(':'.encode())[-1]
        # print("The CPU type on board is:",cpu_type)
        stdin, stdout, stderr = ssh.exec_command("cat /proc/cpuinfo | grep process | wc -l")
        cpu_num = int(stdout.read())
        cpu_num_error = stderr.read()
        # print("The CPU core on board is:",cpu_num)
        logging.info("CPU info is:\r  '%s'\rCPU number is:\r  '%d'\r" % (cpu_info, cpu_num))
        if self.buildoption_type in cpu_type.decode():
            CPU_result = 'PASS'
            # print('CPU Test Pass')
            logging.info("CPU Test Pass\r")
        else:
            # print('CPU Test Failed, error code is 01001')
            logging.error("CPU Test Failed, CPU info check failed error code is 01001\r")

        # close connect
        ssh.close()
        return CPU_result
