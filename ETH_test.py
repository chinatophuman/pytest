import paramiko
import logging
import subprocess


class ETH_test:
    def __init__(self, logname, ETHPORT, HOSTPORT, IPMIPORT, DEFGW, ETHPORT_IP, hostname, port, username, password):
        self.logname = logname
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.ETHPORT = ETHPORT
        self.HOSTPORT = HOSTPORT
        self.IPMIPORT = IPMIPORT
        self.DEFGW = DEFGW
        self.ETHPORT_IP = ETHPORT_IP

    def test_content(self):

        # create SSH item
        ssh = paramiko.SSHClient()
        # permit connect to remote host
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # connect
        ssh.connect(hostname=self.hostname, port=self.port, username=self.username, password=self.password)

        with open(self.logname, 'a+') as f:
            f.write("\rETH test start \r")
        ETH_result = 'FAIL'
        fail_cnt = 0
        cnt = 0

        # get eth info
        stdin, stdout, stderr = ssh.exec_command("ethtool %s" % self.ETHPORT)
        ethinfo = stdout.read()
        # set ipmi LAN network
        ssh.exec_command("ipmitool lan set 1 ipsrc static")
        ssh.exec_command("ipmitool lan set 1 ipaddr %s" % self.IPMIPORT)
        ssh.exec_command("ipmitool lan set 1 netmask 255.255.255.0")
        ssh.exec_command("ipmitool lan set 1 defgw ipaddr %s" % self.DEFGW)
        ssh.exec_command("ifconfig %s %s/24 up" % (self.ETHPORT, self.ETHPORT_IP))
        logging.info("The ETH info is:\r  '%s'\r" % ethinfo)
        logging.info("set ipmi lan 1 ipaddr is: %s \r" % self.IPMIPORT)
        logging.info("set ipmi lan 1 netmask is: 255.255.255.0 \r")
        logging.info("set ipmi lan 1 defgw ipaddr is: %s \r" % self.DEFGW)
        logging.info("set %s ipaddr is: %s \r" % (self.ETHPORT, self.ETHPORT_IP))
        # get ipmi LAN network info
        IPMI_Info = subprocess.getoutput("ipmitool -H %s -U aaa -P joinus123 -I lanplus lan print 1" % self.IPMIPORT)
        logging.info("The IPMI info get is:\r  '%s'\r" % IPMI_Info)

        if (not('Speed: 1000Mb/s'.encode() in ethinfo)):
            # print('ETH Test fail, error code 05002')
            logging.error("ETH Test fail, ethinfo check failed, error code 05002\r")
        elif (not (self.IPMIPORT in IPMI_Info)):
            logging.error("ETH Test fail, IPMIinfo check failed, error code 05003\r")
        else:
            while cnt < 6:
                # print('ethinfo is:', ethinfo)
                pinginfo = subprocess.getoutput("ping -c 15 %s" % self.ETHPORT_IP)
                # print('pinginfo is:', pinginfo)
                # print(pinginfo)
                logging.info("The '%d' ping info is:\r  '%s'\r" % (cnt+1, pinginfo))
                if (not('Link detected: yes'.encode() in ethinfo) or not('0% packet loss' in pinginfo) or
                        ('10% packet loss' in pinginfo) or ('100% packet loss' in pinginfo)):
                    fail_cnt += 1
                    cnt += 1
                else:
                    # print('Test Pass')
                    cnt += 1
            if fail_cnt < 3:
                ETH_result = 'PASS'
                # print('ETH Test Pass')
                logging.info("ETH Test Pass\r")
            else:
                # print('ETH Test fail, error code 05001')
                logging.error("ETH Test fail, error code 05001\r")

        # close connect
        ssh.close()
        return ETH_result