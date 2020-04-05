import smbus
from time import *
import time

# LCD Address
# sudo i2cdetect -y 1
I2C_ADDRESS = 0x6F

# LCD size
XPIXEL = 128
YPIXEL = 64
XMAX = XPIXEL - 1
YMAX = YPIXEL - 1

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

# fonts
FONT4_6 = 1
FONT6_8 = 2
FONT7_12 = 3
GENEVA10 = 4
CHICAGO14 = 5
SWISS30B = 6
BIGZIF50 = 7
BIGZIF100 = 8

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

#DRAW LINES and POINTS
LCD_DRAW_CMD = 'G'

LCD_POINT_SIZE = 'Z'
LCD_DRAW_POINT = 'P'
LCD_DRAW_STRAIGHT_LINE = 'D'
LCD_CONTINUE_STRAIGHT_LINE = 'W'
LCD_DRAW_RECTANGLE = 'R'

#DRAW RECTANGULAR AREA
LCD_DRAW_RECTANGULAR_CMD = 'R'

LCD_DELETE_AREA = 'L'
LCD_INVERT_AREA = 'I'
LCD_FILL_AREA = 'S'

LCD_AREA_WITH_FILL_PATTERN = 'M'
LCD_DRAW_BOX = 'O'
LCD_DRAW_FRAME = 'R'
LCD_DRAW_FRAME_BOX = 'T'

#BARGRAPH
LCD_BARGRAPH_CMD = 'B'
LCD_BARGRAPH_R = 'R'
LCD_BARGRAPH_L = 'L'
LCD_BARGRAPH_O = 'O'
LCD_BARGRAPH_U = 'U'
LCD_DELETE_BARGRAPH = 'D'
LCD_UPDATE_BARGRAPH = 'A'
LCD_REDRAW_BARGRAPH = 'Z'
LCD_SEND_BARGRAPH_VALUE = 'S'

#BITMAT
LCD_BITMAP_CMD = 'U'

LCD_LOAD_INTERNAL_IMAGE = 'I'
LCD_LOAD_IMAGE = 'L'

BLH = [64, 64,
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    0, 31,255,248,  0,  0,  0,  0,  0,224,  0,  7,  0,  0,  0,  0,
    0,  0,  0,  1,128,  0,  0,  0,  0,  0,  0,  0,128,  0, 32,  0,
    0,  0,  0,  0, 64,  0, 32,  0,  0,  0,  0,  0, 64,  0, 16,  0,
    0,  0,  0,  0, 32,  0, 16,  0,  0,  0,  0,  0, 32,  0, 16,  0,
    0,  0,  0,  0, 32,  0, 16,  0,  0,  0,  0,  0, 16,  0, 16,  0,
    0,  0,  0,  0, 16,  0, 16,  0,  0,  0,  0,  0, 16,  0, 16,  0,
    0,  0,  0,  0, 16,  0, 16,  0,  0,  1,254,  0, 16,  0, 16,  0,
    0,  2,  1,255,144,  0, 16,  0,  0,  2,  0,  0,112,  0,  8,  0,
    0,  2,  0,  0, 24,  0,  8,  0,  0,  2,  0,  0, 24,  0,  8,  0,
    0,  2,  0,  0, 20,  0,  8,  0,  0,  2,  0,  0, 34,  0,  8,  0,
    0,  2,  0,  0, 34,  0,  8,  0,  0,  2,  0,  0,194,  0,  8,  0,
    0,  1,  0,  1,  1,  0,  8,  0,  0,  1,  0, 15,  0,128,  8,  0,
    0,  1,128, 48,  0,128,  8,  0,  0,  0,255,192,  0,128,  8,  0,
    0,  0,  0,  0,  0,128,  8,  0,  0,  0,  0,  0,  0,128,  8,  0,
    0,  0,  0,  0,  0,128,  8,  0,  0,  0,  0,  0,  0,128,  8,  0,
    0,  0,  0,  0,  0,128,  8,  0,  0,  0,  0,  0,  0,128,  8,  0,
    0,  0, 15,255,255,128,  8,  0,  0,  0, 16,  0,  1,192,  8,  0,
    0,  0, 16,  0,  1, 64,  8,  0,  0,  0, 16,  0,  2, 64,  8,  0,
    0,  0, 16,  0,  2, 96,  8,  0,  0,  0, 24,  0,  4, 32,  8,  0,
    0,  0, 12,  0, 56, 32,  8,  0,  0,  0,  3,255,224, 32,  8,  0,
    0,  0,  0,  0,  0, 32,  8,  0,  0,  0, 12,  0,  0, 96,  8,  0,
    0,  0, 12,  0,  0,128,  8,  0,  0,  0,  3,192,  7,  0,  8,  0,
    0,  0,  0, 63,248,  0,  8,  0,  0,  0,  0,  0,  0,  0,  8,  0,
    0,  0,  0,  0,  0,  0,  8,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0
]

test = [
   12, 12,
    0,  0, 56,  0, 40,  0, 40,  0, 46,  0, 34,  0, 34,  0, 34,  0,
   35,224, 48, 32, 63,224,  0,  0
]

class lcd(object):
    #initializes objects and lcd
    def __init__(self, brightness, port=1):
        self.addr = I2C_ADDRESS
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

        self.lcd_write_cmd(LCD_TEXT_CMD, LCD_SET_FONT, font)

    def lcd_set_point_size(self, n1, n2):
        if n1 < 1 or n1 > 15:
            print("wrong n1 value[0 - 15]")
            return

        if n2 < 1 or n2 > 15:
            print("wrong n2 value[0 - 15]")
            return

        self.lcd_write_cmd(LCD_DRAW_CMD, LCD_POINT_SIZE, n1, n2)

    # put string function
    def lcd_display_string(self, str, x, y, align):
        n = 0

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

    # clear lcd
    # If the graphics screen is deleted with ‘ESC DL’, 
    # for example, that does not affect the contents of the terminal window
    def lcd_clear(self):
        self.lcd_write_cmd(LCD_DISPLAY_CMD, LCD_DELETE_DISPLAY)

    def lcd_draw_point(self, x, y):
        self.lcd_write_cmd(LCD_DRAW_CMD, LCD_DRAW_POINT, x, y)

    def lcd_draw_line(self, x1, y1, x2, y2):
        self.lcd_write_cmd(LCD_DRAW_CMD, LCD_DRAW_STRAIGHT_LINE, x1, y1, x2, y2)

    def lcd_draw_rectangle(self, x1, y1, x2, y2):
        self.lcd_write_cmd(LCD_DRAW_CMD, LCD_DRAW_RECTANGLE, x1, y1, x2, y2)

    def lcd_delete_area(self, x1, y1, x2, y2):
        self.lcd_write_cmd(LCD_DRAW_RECTANGLE, LCD_DELETE_AREA, x1, y1, x2, y2)

    def lcd_invert_area(self, x1, y1, x2, y2):
        self.lcd_write_cmd(LCD_DRAW_RECTANGLE, LCD_INVERT_AREA, x1, y1, x2, y2)

    def lcd_fill_area(self, x1, y1, x2, y2):
        self.lcd_write_cmd(LCD_DRAW_RECTANGLE, LCD_FILL_AREA, x1, y1, x2, y2)

    def lcd_fill_area_pattern(self, x1, y1, x2, y2, pattern):
        if pattern > 15:
            print("wrong pattern value[0 - 15]")
            return        

        self.lcd_write_cmd(LCD_DRAW_RECTANGLE, LCD_AREA_WITH_FILL_PATTERN, x1, y1, x2, y2, pattern)

    def lcd_draw_box(self, x1, y1, x2, y2, pattern):
        if pattern > 15:
            print("wrong pattern value[0 - 15]")
            return      

        self.lcd_write_cmd(LCD_DRAW_RECTANGLE, LCD_DRAW_BOX, x1, y1, x2, y2, pattern)

    def lcd_draw_frame(self, x1, y1, x2, y2, pattern):
        if pattern > 15:
            print("wrong pattern value[0 - 15]")
            return      

        self.lcd_write_cmd(LCD_DRAW_RECTANGLE, LCD_DRAW_FRAME, x1, y1, x2, y2, pattern)

    def lcd_draw_frame_box(self, x1, y1, x2, y2, pattern):
        if pattern > 15:
            print("wrong pattern value[0 - 15]")
            return      

        self.lcd_write_cmd(LCD_DRAW_RECTANGLE, LCD_DRAW_FRAME_BOX, x1, y1, x2, y2, pattern)

    def lcd_draw_bargraph_r(self, n1, x1, y1, x2, y2, aw, ew, tp, pat):
        if n1 < 1 or n1 > 32:
            print("wrong n1 value[1 - 32]")
            return      

        self.lcd_write_cmd(LCD_BARGRAPH_CMD, LCD_BARGRAPH_R, n1, x1, y1, x2, y2, aw, ew, tp, pat)

    def lcd_update_bargraph(self, old_val, new_val):
        self.lcd_write_cmd(LCD_BARGRAPH_CMD, LCD_UPDATE_BARGRAPH, old_val, new_val)

    def lcd_set_orientation(self, orientation):
        if orientation == 0:
            ori = 0
        elif orientation == 90:
            ori = 1
        elif orientation == 180:
            ori = 2
        elif orientation == 270:
            ori = 3
        else:
            print("wrong value of orientation[0, 90, 180, 270]")
            return

        self.lcd_write_cmd(LCD_DISPLAY_CMD, LCD_SET_DISPLAY_ORIENTATION, ori)

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

    def lcd_load_interal_image(self, x, y, n):
        if n < 0 or n > 255:
            print("internal image is not existed [0 - 255]")
        self.lcd_write_cmd(LCD_BITMAP_CMD, LCD_LOAD_INTERNAL_IMAGE, n)

    def lcd_load_image(self, x, y, blh):
        n = 0

        dat = [ESC, ord(LCD_BITMAP_CMD), ord(LCD_LOAD_IMAGE)]
        
        dat.append(x)
        dat.append(y)
        dat.extend(blh)
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

    def demo_screen(self):
        self.lcd_write_cmd(LCD_TERMINAL_CMD, LCD_TERMINAL_OFF)
        self.lcd_clear()

        self.lcd_set_font(SWISS30B)
        self.lcd_display_string('Demo', 60, 0, CENTER)
        self.lcd_set_point_size(2, 2)
        self.lcd_draw_line(0, 30, XMAX, 30)

        self.lcd_set_font(CHICAGO14)
        self.lcd_display_string('Brightness', 5, 35, CENTER)

        self.lcd_draw_bargraph_r(1, 0, 50, XMAX, 50+10, 5, 100, 1, 1)
        self.lcd_update_bargraph(1, 80)        

    def clock(self):
        self.lcd_write_cmd(LCD_TERMINAL_CMD, LCD_TERMINAL_OFF)
        self.lcd_clear()

        self.lcd_set_font(SWISS30B)
        self.lcd_display_string('CLOCK', 60, 0, CENTER)
        self.lcd_set_point_size(2, 2)
        self.lcd_draw_line(0, 30, XMAX, 30)
        self.lcd_set_font(CHICAGO14)
        
        while True:
            self.lcd_delete_area(0, 35, XMAX, YMAX)
            localtime = time.localtime(time.time())
            self.lcd_display_string(str(localtime.tm_year) + '-' + str(localtime.tm_mon) + '-' + str(localtime.tm_mday) + ' ' + str(localtime.tm_hour) + ':' + str(localtime.tm_min) + ':' + str(localtime.tm_sec), 0, 40, CENTER)
            sleep(0.5)

    def draw_picture(self):
        for row in range(0, YPIXEL):
            for col in range (0, XPIXEL):
                self.lcd_draw_point(col, row)

if __name__ == '__main__':
    print("this is RPI I2C driver for EAeDIP128-6")

    l = lcd(2, 1)#设置背光开关，port=1

    # l.demo_screen()
    # l.clock()

    l.lcd_clear()
    l.lcd_load_image(0, 0, test)
