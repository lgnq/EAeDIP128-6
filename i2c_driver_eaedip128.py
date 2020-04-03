import smbus
from time import *

# LCD Address
# sudo i2cdetect -y 1
ADDRESS = 0x6F

ESC = 0x1B
DC1 = 0x11
ACK = 0x06
NAK = 0x15

ON = 1
OFF = 0

NUL = 0x00
LF = 0x0A
CR = 0x0D

LEFT = 0
RIGHT = 1
CENTER = 2

LCD_CLEAR_DISPLAY = [0x1B, 0x44, 0x4C, 0x1B, 0x47, 0x44, 0x00, 0x00, 0x7F, 0x3F]

# terminal commands
LCD_TERMINAL_CMD = 'T'

LCD_SAVE_CURSOR_POSITION = 'S'
LCD_RESTORE_CURSOR_POSITION = 'R'

LCD_TERMINAL_ON  = 'E'
LCD_TERMINAL_OFF = 'A'

LCD_OUTPUT_VERSION = 'V'
LCD_OUTPUT_PROJECT_NAME = 'J'
LCD_OUTPUT_INFORMATION = 'I'

# display commands
LCD_DISPLAY_CMD = 'D'

LCD_SET_DISPLAY_ORIENTATION = 'O'
LCD_SET_DISPLAY_CONTRAST = 'K'
LCD_DELETE_DISPLAY = 'L'
LCD_INVERT_DISPLAY = 'I'
LCD_FILL_DISPLAY = 'S'
LCD_SWITCH_DISPLAY_OFF = 'A'
LCD_SWITCH_DISPLAY_ON = 'E'
LCD_SHOW_CLIPBOARD = 'C'
LCD_SHOW_NORMAL_DISPLAY_CONTENT = 'N'

#TEXT COMMANDS
LCD_TEXT_CMD = 'Z'

LCD_SET_FONT = 'F'
LCD_SET_ZOOM_FACTOR = 'Z'
LCD_ADDITIONAL_LINE_SPACING = 'Y'
LCD_SPACEWIDTH = 'J'
LCD_TEXT_ANGLE = 'W'
LCD_TEXT_LINK_MODE = 'V'
LCD_TEXT_FLASHING_ATTRIBUTE = 'B'

#LCD BACKLIGHT
LCD_BACKLIGHT_CMD = 'Y'

LCD_ILLUMINATION_BRIGHTNESS = 'H'
LCD_ILLUMINATION_ONOFF = 'L'

class lcd(object):
    #initializes objects and lcd
    def __init__(self, brightness, port=1):
        self.addr = ADDRESS
        self.bus = smbus.SMBus(port)

        self.lcd_backlight_onoff(OFF)
        self.lcd_set_brightness(brightness)
        self.lcd_set_contrast(20)
        self.lcd_set_orientation(0)
        self.lcd_backlight_onoff(ON)

        sleep(0.2)   

    def send_data(self, dat, len):
        self.bus.write_byte(self.addr, DC1)
        bcc = DC1

        self.bus.write_byte(self.addr, len)
        bcc = bcc + len

        for i in range(0, len):
            self.bus.write_byte(self.addr, dat[i])
            bcc = bcc + dat[i]

        self.bus.write_byte(self.addr, bcc)

    def lcd_write_read(self, dat):
        while True:
            self.send_data(dat, len(dat))

            val = self.bus.read_byte(self.addr)
            if val == ACK:
                break
            elif val == NAK:
                print("NAK")
                continue

    def lcd_write_cmd(self, cmd1, cmd2, *codes):
        n = 0

        dat = [ESC, ord(cmd1), ord(cmd2)]
        for code in codes:
            dat.append(code)

        while True:
            n = n + 1
            if n == 10:
                print("lcd write cmd failed after try 10 times")
                break

            self.send_data(dat, len(dat))

            val = self.bus.read_byte(self.addr)
            if val == ACK:
                break
            elif val == NAK:
                print("NAK")
                continue

    def lcd_set_font(self, font = 0):
        if font > 15:
            print("wrong font value[0 - 15]")
            return

        dat = [ESC, ord('Z'), ord('F'), font]
        self.send_data(dat, len(dat))

    # put string function
    def lcd_display_string(self, str, x, y, align):
        dat = [ESC, ord('Z')]
        
        if align == LEFT:
            dat.append(ord('L'))
        elif align == RIGHT:
            dat.append(ord('R'))
        elif align == CENTER:
            dat.append(ord('C'))

        dat.append(x)
        dat.append(y)
        s = list(str)
        for i in range(0, len(s)):
            dat.append(ord(s[i]))
        dat.append(NUL)
                    
        self.send_data(dat, len(dat))

    # clear lcd and set to home
    def lcd_clear(self):
        dat = [ESC, ord('D'), ord('L')]
        self.send_data(dat, len(dat))

    def lcd_draw_point(self, x, y):
        # dat = [ESC, ord('D'), ord('L'), ESC, ord('G'), ord('D')]
        dat = [ESC, ord('G'), ord('P')]
        dat.append(x)
        dat.append(y)
        
        self.send_data(dat, len(dat))

    def lcd_draw_line(self, x1, y1, x2, y2):
        # dat = [ESC, ord('D'), ord('L'), ESC, ord('G'), ord('D')]
        dat = [ESC, ord('G'), ord('D')]
        dat.append(x1)
        dat.append(y1)
        dat.append(x2)
        dat.append(y2)
        
        self.send_data(dat, len(dat))

    def lcd_draw_rectangle(self, x1, y1, x2, y2):
        # dat = [ESC, ord('D'), ord('L'), ESC, ord('G'), ord('D')]
        dat = [ESC, ord('G'), ord('R')]
        dat.append(x1)
        dat.append(y1)
        dat.append(x2)
        dat.append(y2)
        
        self.send_data(dat, len(dat))

    def lcd_delete_area(self, x1, y1, x2, y2):
        dat = [ESC, ord('R'), ord('L')]
        dat.append(x1)
        dat.append(y1)
        dat.append(x2)
        dat.append(y2)
        
        self.send_data(dat, len(dat))

    def lcd_invert_area(self, x1, y1, x2, y2):
        dat = [ESC, ord('R'), ord('I')]
        dat.append(x1)
        dat.append(y1)
        dat.append(x2)
        dat.append(y2)
        
        self.send_data(dat, len(dat))

    def lcd_fill_area(self, x1, y1, x2, y2):
        dat = [ESC, ord('R'), ord('S')]
        dat.append(x1)
        dat.append(y1)
        dat.append(x2)
        dat.append(y2)
        
        self.send_data(dat, len(dat))

    def lcd_fill_area_pattern(self, x1, y1, x2, y2, n1):
        dat = [ESC, ord('R'), ord('M')]
        dat.append(x1)
        dat.append(y1)
        dat.append(x2)
        dat.append(y2)
        dat.append(n1)
        
        self.send_data(dat, len(dat))

    def lcd_draw_box(self, x1, y1, x2, y2, n1):
        dat = [ESC, ord('R'), ord('O')]
        dat.append(x1)
        dat.append(y1)
        dat.append(x2)
        dat.append(y2)
        dat.append(n1)
        
        self.send_data(dat, len(dat))

    def lcd_draw_frame(self, x1, y1, x2, y2, n1):
        dat = [ESC, ord('R'), ord('R')]
        dat.append(x1)
        dat.append(y1)
        dat.append(x2)
        dat.append(y2)
        dat.append(n1)
        
        self.send_data(dat, len(dat))

    def lcd_draw_frame_box(self, x1, y1, x2, y2, n1):
        dat = [ESC, ord('R'), ord('T')]
        dat.append(x1)
        dat.append(y1)
        dat.append(x2)
        dat.append(y2)
        dat.append(n1)
        
        self.send_data(dat, len(dat))

    def lcd_set_orientation(self, orientation):
        dat = [ESC, ord('D'), ord('O')]

        if orientation == 0:
            dat.append(0)
        elif orientation == 90:
            dat.append(1)
        elif orientation == 180:
            dat.append(2)
        elif orientation == 270:
            dat.append(3)            
        else:
            print("wrong value of orientation[0, 90, 180, 270]")
            return

        self.lcd_write_read(dat)

    def lcd_set_contrast(self, contrast):
        if (contrast >= 0) and (contrast <= 40):
            self.lcd_write_cmd(LCD_DISPLAY_CMD, LCD_SET_DISPLAY_CONTRAST, contrast)
        else:
            print("wrong value of contrast[0 - 40]")
            return

    def lcd_set_brightness(self, brightness):
        if (brightness >= 0) and (brightness <= 100):
            self.lcd_write_cmd(LCD_BACKLIGHT_CMD, LCD_ILLUMINATION_BRIGHTNESS, brightness)
        else:
            print("wrong value of brightness[0 - 100]")
            return

    def lcd_backlight_onoff(self, onoff):
        self.lcd_write_cmd(LCD_BACKLIGHT_CMD, LCD_ILLUMINATION_ONOFF, onoff)

if __name__ == '__main__':
    print("this is RPI I2C driver for EAeDIP128-6")

    l = lcd(2, 1)#设置背光开关，port=1

    l.lcd_write_cmd(LCD_TERMINAL_CMD, LCD_TERMINAL_ON)
    l.lcd_write_cmd(LCD_TERMINAL_CMD, LCD_OUTPUT_INFORMATION)
