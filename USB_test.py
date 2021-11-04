import paramiko
import logging



class USB_test:
    def __init__(self, logname, hostname, port, username, password):
        self.logname = logname
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password

    def test_content(self):
        # create SSH item
        ssh = paramiko.SSHClient()
        # permit connect to remote host
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # connect
        ssh.connect(hostname=self.hostname, port=self.port, username=self.username, password=self.password)

        logging.info("\rUSB test start \r")
        USB_result = 'FAIL'

        stdin, stdout, stderr = ssh.exec_command("lsusb -v | grep Mouse | wc -l")
        mouse_num=int(stdout.read())
        # print(mouse_num)
        mouse_num_error=stderr.read()
        stdin, stdout, stderr = ssh.exec_command("lsusb -v | grep Mouse")
        mouse_info=stdout.read()
        # print(mouse_num)
        mouse_info_error=stderr.read()
        stdin, stdout, stderr = ssh.exec_command("lsusb -v | grep Keyboard | wc -l")
        keybaord_num = int(stdout.read())
        keyboard_num_error = stderr.read()
        stdin, stdout, stderr = ssh.exec_command("lsusb -v | grep Keyboard")
        keybaord_info = stdout.read()
        keyboard_info_error = stderr.read()
        stdin, stdout, stderr = ssh.exec_command("lsusb -v | grep Bulk-Only | wc -l")
        usb_num = int(stdout.read())
        usb_num_error = stderr.read()
        stdin, stdout, stderr = ssh.exec_command("lsusb -v | grep Bulk-Only")
        usb_info = stdout.read()
        usb_info_error = stderr.read()
        logging.info("Mouse info is:\r  '%s'\rKeyboard info is:\r  '%s'\rUSB info is:\r  '%s'\r"
                     % (mouse_info, keybaord_info, usb_info))

        if mouse_num != 6:
            # print('Mouse Test failed, error code is 04003')
            logging.error("Mouse Test failed, error code is 04003\r")
        elif keybaord_num != 6:
            # print('Keyboard Test failed, error code is 04002')
            logging.error("Keyboard Test failed, error code is 04002\r")
        elif usb_num != 1:
            # print('USB Test failed, error code is 04001')
            logging.error("USB Test failed,detect %d USB device error code is 04001\r" % usb_num)
        else:
            # print('USB Test Pass')
            USB_result = 'PASS'
            logging.info("USB Test Pass\r")

        # close connect
        ssh.close()
        return USB_result
