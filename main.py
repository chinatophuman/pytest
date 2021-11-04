import pytest
import subprocess
import logging
import easygui as gui
from USB_test import USB_test
from PCIE_test import PCIE_test
from SATA_test import SATA_test
from SFP_test import SFP_test
from Memory_test import Memory_test
from SSD_test import SSD_test
from CONSOLE_test import CONSOLE_test
from ETH_test import ETH_test
from CPU_test import CPU_test

HOSTPORT = '10.168.1.124'
buildoption_type = 'Intel(R) Xeon(R) D-2177NT CPU @ 1.90GHz'
logname = 'ft_test_log.txt'
ETHPORT = 'enp3s0'
hostname = '10.168.1.213'
IPMIPORT = '10.168.1.214'
DEFGW = '10.168.1.1'
ETHPORT_IP = '10.168.1.215'
port = 22
username = 'root'
password = '1'
SFPPORT1 = 'enp184s0f0'
SFPPORT2 = 'enp184s0f1'
SFPPORT3 = 'enp184s0f2'
SFPPORT4 = 'enp184s0f3'
value2 = ''
mysql_host = 'localhost'
mysql_user = 'root'
mysql_password = 'joinus123'
mysql_database = 'ftdb'

sn = '123456789'
logging.basicConfig(level=logging.INFO)


def test_vga():
    logging.info("\rVGA test start \r")
    vga_result = gui.ccbox(msg='please check the vga screen display is light', title='VGA_check',
                           choices=(['light', 'not light']))
    if vga_result:
        # VGA_result = 'PASS'
        # print('The user choose light, VGA Test Pass')
        logging.info("\rThe user choose light, VGA Test Pass\r")
        assert 1
    else:
        # print('The user choose not light, VGA Test failed, error code is 08001')
        logging.info("\rThe user choose not light, VGA Test failed, error code is 08001\r")
        assert 0


def test_eth_local():
    ping_info = subprocess.getoutput("ping www.baidu.com")
    if "丢失 = 0" in ping_info:
        logging.info("\rno package loss，network is fine\r")
        assert 1
    else:
        print(ping_info)
        logging.info("\rthere is package loss, please check the network\r")
        assert 0


def test_cpu():
    cpu_result = CPU_test(logname, buildoption_type, hostname, port, username, password).test_content()
    if cpu_result == 'PASS':
        logging.info("\rCPU test Pass\r")
        assert 1
    else:
        logging.warning("\rCPU test Fail\r")
        assert 0


def test_usb():
    usb_result = USB_test(logname, hostname, port, username, password).test_content()
    if usb_result == 'PASS':
        logging.info("\rUSB test Pass\r")
        assert 1
    else:
        logging.warning("\rUSB test Fail\r")
        assert 0


def test_pcie():
    pcie_result = PCIE_test(logname, hostname, port, username, password).test_content()
    if pcie_result == 'PASS':
        logging.info("\rPCIE test Pass\r")
        assert 1
    else:
        logging.warning("\rPCIE test Fail\r")
        assert 0


def test_sata():
    sata_result = SATA_test(logname, hostname, port, username, password).test_content()
    if sata_result == 'PASS':
        logging.info("\rSATA test Pass\r")
        assert 1
    else:
        logging.warning("\rSATA test Fail\r")
        assert 0


def test_sfp():
    sfp_result = SFP_test(logname, hostname, port, username, password, SFPPORT1, SFPPORT2, SFPPORT3, SFPPORT4).\
        test_content()
    if sfp_result == 'PASS':
        logging.info("\rSFP test Pass\r")
        assert 1
    else:
        logging.warning("\rSFP test Fail\r")
        assert 0


def test_ssd():
    m2_result = SSD_test(logname, hostname, port, username, password).test_content()
    if m2_result == 'PASS':
        logging.info("\rM.2 test Pass\r")
        assert 1
    else:
        logging.warning("\rM.2 test Fail\r")
        assert 0


def test_memory():
    memory_result = Memory_test(logname, hostname, port, username, password).test_content()
    if memory_result == 'PASS':
        logging.info("\rMemory test Pass\r")
        assert 1
    else:
        logging.warning("\rMemory test Fail\r")
        assert 0


def test_console():
    console_result = CONSOLE_test(logname, hostname, port, username, password).test_content()
    if console_result == 'PASS':
        logging.info("\rCONSOLE test Pass\r")
        assert 1
    else:
        logging.warning("\rCONSOLE test Fail\r")
        assert 0


def test_eth():
    eth_result = ETH_test(logname, ETHPORT, HOSTPORT, IPMIPORT, DEFGW, ETHPORT_IP,
                          hostname, port, username, password).test_content()
    if eth_result == 'PASS':
        logging.info("\rETH test Pass\r")
        assert 1
    else:
        logging.warning("\rETH test Fail\r")
        assert 0


if __name__ == '__main__':
    arg = ["-s", "main.py", "--html=report/test_%s.html" % sn, "--capture=sys"]
    pytest.main(arg)
