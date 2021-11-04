import easygui as gui
import logging


class VGA_test:
    def test_content(self):
        logging.debug("\r\rVGA test start \r")
        VGA_result = gui.ccbox(msg='please check the vga screen display is light', title='VGA_check',
                               choices=(['light', 'not light']))
        if VGA_result:
            VGA_result = 'PASS'
            # print('The user choose light, VGA Test Pass')
            logging.debug("The user choose light, VGA Test Pass\r")
            return VGA_result
        else:
            VGA_result = 'FAIL'
            # print('The user choose not light, VGA Test failed, error code is 08001')
            logging.debug("The user choose not light, VGA Test failed, error code is 08001\r")
        return VGA_result