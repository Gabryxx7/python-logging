import time
from datetime import datetime
import colorama
import os

class LogWidgetMeta:
     def __init__(self):
        self.logging_levels = {'a':0, 'd':1, 'i':2, 's':2, 'w':3, 'e':4}
        self.tag = "LogWidgetMeta"
        
    def append(self, text):
        pass
    
    def check_log_status(self, text):
        pass
    
    def on_logging_level_changed(self, new_logging_level):
        pass
        

class QtLogWidget(LogWidgetMeta, QWidget):
    def __init__(self, logger):
        import PySide2.QtWidgets as pyQtWidgets
        import PySide2.QtGui as pyQtGui
        super(LogWidget, self).__init__()
        self.tag = "QtLogWidget"
        self.main_layout = pyQtWidgets.QVBoxLayout()
        self.extra_layout = pyQtWidgets.QHBoxLayout()
        self.logger = logger
        self.text_area = pyQtWidgets.QTextEdit()
        self.text_area.setReadOnly(True)
        self.text_area.setFont(QFont("Courier New", 9))

        self.title = pyQtWidgets.QLabel("LOG")
        self.filter_label = pyQtWidgets.QLabel("Filter level:")
        self.filter_combobox = pyQtWidgets.QComboBox()
        for key in self.logger.logging_levels.keys():
            self.filter_combobox.addItem(str(self.logger.logging_levels[key]) + " - " + key, key)
        self.filter_combobox.currentIndexChanged.connect(self.on_logging_level_changed)
        self.enable_checkbox = pyQtWidgets.QCheckBox("Enable")
        self.enable_checkbox.stateChanged.connect(self.enable_checkbox_changed)
        self.console_checkbox = pyQtWidgets.QCheckBox("Console")
        self.console_checkbox.stateChanged.connect(self.console_checkbox_changed)
        self.widget_checkbox = pyQtWidgets.QCheckBox("Widget")
        self.widget_checkbox.stateChanged.connect(self.widget_checkbox_changed)
        self.file_checkbox = pyQtWidgets.QCheckBox("File")
        self.file_checkbox.stateChanged.connect(self.file_checkbox_changed)

        self.extra_layout.addWidget(self.title)
        self.extra_layout.addWidget(self.filter_label)
        self.extra_layout.addWidget(self.filter_combobox)
        self.extra_layout.addWidget(self.enable_checkbox)
        self.extra_layout.addWidget(self.console_checkbox)
        self.extra_layout.addWidget(self.widget_checkbox)
        self.extra_layout.addWidget(self.file_checkbox)
        self.extra_layout.addStretch(1)

        self.main_layout.addLayout(self.extra_layout)
        self.main_layout.addWidget(self.text_area)
        self.check_log_status()

        self.setLayout(self.main_layout)

    def append(self, text):
        self.text_area.append(text)
        # self.text_area.moveCursor(QTextCursor.End)
        self.text_area.verticalScrollBar().setValue(self.text_area.verticalScrollBar().maximum())
        
    def on_logging_level_changed(self, new_logging_level):
        self.logger.set_min_level(self.filter_combobox.itemData(new_logging_level))        

    def enable_checkbox_changed(self, value):
        self.logger.setEnabled(value)
        self.check_log_status()

    def console_checkbox_changed(self, value):
        self.logger.setConsoleEnabled(value)
        self.check_log_status()

    def widget_checkbox_changed(self, value):
        self.logger.setWidgetEnabled(value)
        self.check_log_status()

    def file_checkbox_changed(self, value):
        self.logger.setFileEnabled(value)
        self.check_log_status()

    def check_log_status(self):
        self.filter_combobox.setCurrentIndex(self.logger.get_min_level_index())

        self.enable_checkbox.setChecked(self.logger.enabled)
        self.console_checkbox.setChecked(self.logger.enable_console)
        self.widget_checkbox.setChecked(self.logger.enable_widget)
        self.file_checkbox.setChecked(self.logger.save_to_file)

        self.console_checkbox.setEnabled(self.logger.enabled)
        self.widget_checkbox.setEnabled(self.logger.enabled)
        self.file_checkbox.setEnabled(self.logger.enabled)

class VisualLogWidget(LogWidgetMeta):
    class Type:
        NONE = "None"
        OPENCV = 'cv'
        PYGAME = 'pygame'
    class Point:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            
    class DebugTextLine:
        def __init__(self, text, color, pos, font=None, font_size=0.4, line_height=-1):
            self.text = text
            self.color = color
            self.pos = pos
            self.font = font
            self.font_size = font_size
            self.line_height = line_height
            if line_height < 0:
                self.line_height = self.font_size*0.8
    
    def __init__(self, logger, drawer, draw_type=None):
        self.logger = logger
        self.drawer = None
        self.draw_type = self.NONE if draw_type is None else draw_type
        self.canvas = None
        self.font = None
        self.font_size = 20
        self.line_height = 20
        self.text_lines_buffer = []
    
    def set_canvas(self, canvas):
        self.canvas = canvas
    
    def draw_text_line(self, start, end, color, thickness):
        pass
    
    def draw_line(self, start, end, color, thickness):
        pass
    
    def draw_circle(self, center, color, radius, thickness)):
        pass
    
    def add_text_line(self, text_line, color, pos, font=None, font_size, line_height=None):
        font = self.font if font is None else font
        font_size == self.font_size if font_size is None else font_size
        line_height = self.line_height if line_height is None else line_height
        self.buffer.append(self.DebugTextLine(text_line, color, self.Point(pos.x, pos.y), font_size))
        pos.y += line_height
        return pos
    
    def flush_text_lines(self, draw=True, canvas=None, debug=False):
        if debug:
            print(f"[{self.tag}] Flushing {len(self.buffer)} lines")
        while len(self.text_lines_buffer) > 0:
            line = self.text_lines_buffer.pop()
            if draw:
                try:
                    self.draw_text_line(line canvas)
                except Exception as e:
                    print(f"[{self.tag}] Error printing line '{line.text}'")

    
class CvLogWidget(VisualLogWidget):
    def __init__(self, logger, cv):
        super(CvLogWidget, self).__init__(logger, cv, VisualLogWidget.OPENCV)
        
    def draw_text_line(self, line, canvas=None):
        canvas = self.canvas if canvas is None else canvas
        self.drawer.putText(canvas, line.text, (int(line.pos.x), int(line.pos.y)), 0, line.font_size, line.color, 2)
    
    def draw_line(self, start, end, color, thickness):
        self.drawer.line(self.canvas, (int(start.x), int(start.y)), (int(end.x), int(end.y)), color, thickness)
        
    def draw_circle(self, center, color, radius, thickness):
        self.drawer.circle(self.canvas, (int(center.x), int(center.y)), radius, color, thickness)
        
        
class PyGameLogWidget(VisualLogWidget):
    def __init__(self, logger, pygame, font):
        super(PyGameLogWidget, self).__init__(logger, pygame, VisualLogWidget.PYGAME)
        self.font = font
        self.font_size = self.font.size
        self.line_height = self.font_size*0.8
        
    def draw_text_line(self, line, canvas=None):
        canvas = self.canvas if canvas is None else canvas
        canvas.blit(line.font.render(line.text, True, line.color), (int(line.pos.x), int(line.pos.y)))
    
    def draw_line(self, start, end, color, thickness):
        self.drawer.draw.line(self.canvas, color=color, start_pos=(int(start.x), int(start.y)), end_pos=(int(end.x), int(end.y)), width=thickness)
        
    def draw_circle(self, center, color, radius, thickness):
        self.drawer.draw.circle(self.canvas, color=color, center=(int(center.x), int(center.y)), radius=radius, width=thickness)
    
class FileLogWidget:
    def __init__(self, cls):
        self._cls = cls


class Singleton:
    def __init__(self, cls):
        self._cls = cls

    def Instance(self):
        try:
            return self._instance
        except AttributeError:
            self._instance = self._cls()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `Instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._cls)

class LogColor():
    def __init__(self, name, code, html):
        self.color_name = name
        self.color_code = code
        self.color_html = html

@Singleton
class Log(object):
    def __init__(self):
        self.logging_levels = {'a':0, 'd':1, 'i':2, 's':2, 'w':3, 'e':4}
        self.min_level = 'a'
        self.log_file = "log.txt"
        self.file = open(self.log_file, "w+")
        self.enabled = True
        self.enable_console = True
        self.enable_widget = True
        self.save_to_file = True
        self.logWidget = None

        self.colors = {'red': LogColor('red', "\033[91m", "<font color=\"Red\">"),
                       'green': LogColor('green', "\033[92m", "<font color=\"Green\">"),
                       'white': LogColor('white', "\033[37m", "<font color=\"White\">"),
                       'blue': LogColor('blue', "\033[94m", "<font color=\"Blue\">"),
                       'orange': LogColor('orange', "\033[93m", "<font color=\"Orange\">"),
                       'reset': LogColor('orange', "\033[0;0m", "</>")}

    def set_min_level(self, level):
        self.i("LOGGER", "Logging Level Changed: " + self.min_level + " - " + str(self.logging_levels[self.min_level]))
        self.min_level = level

    def get_min_level_index(self):
        return list(self.logging_levels.keys()).index(self.min_level)

    def setEnabled(self, enabled):
        self.i("LOGGER", "Logging has been " + self.status_string(enabled))
        self.enabled = enabled

    def setConsoleEnabled(self, enabled):
        self.i("LOGGER", "Logging CONSOLE has been " + self.status_string(enabled))
        self.enable_console = enabled

    def setWidgetEnabled(self, enabled):
        self.i("LOGGER", "Logging WIDGET has been " + self.status_string(enabled))
        self.enable_widget = enabled

    def setFileEnabled(self, enabled):
        self.i("LOGGER", "Logging FILE has been " + self.status_string(enabled)+": " + os.path.abspath(self.log_file))
        self.save_to_file = enabled

    def status_string(self, status):
        if status:
            return "ENABLED"
        else:
            return  "DISABLED"

    def w(self, tag, text, log_to_widget=True):
        self.print("orange", tag, text, 'w', log_to_widget)

    def d(self, tag, text, log_to_widget=True):
        self.print("blue", tag, text, 'd', log_to_widget)

    def e(self, tag, text, log_to_widget=True):
        self.print("red", tag, text, 'e', log_to_widget)

    def s(self, tag, text, log_to_widget=True):
        self.print("green", tag, text, 's', log_to_widget)

    def i(self, tag, text, log_to_widget=True):
        self.print("white", tag, text, 'i', log_to_widget)

    def print(self, color_name, tag, text, log_level, log_to_widget=True):
        if self.enabled:
            color = self.colors[color_name]
            color_reset = self.colors['reset']
            if self.logging_levels[log_level] >= self.logging_levels[self.min_level]:
                dateTimeObj = datetime.now()
                timestampStr = dateTimeObj.strftime("%d-%b-%Y %H:%M:%S") + " - "
                log_text = log_level + "["+str(tag)+"]: " +str(text)
                if self.enable_widget and log_to_widget and self.logWidget is not None:
                    try:
                        final_text = timestampStr + color.color_html + " " + log_text + color_reset.color_html
                        self.logWidget.append(final_text + "\n")
                    except Exception as e:
                        print("Exception writing to LOG Widget:" + str(e))
                        pass
                if self.enable_console:
                    final_text = timestampStr + color.color_code + " " + log_text + color_reset.color_code
                    print(final_text)
                if self.save_to_file:
                    try:
                        self.file.write(timestampStr + log_text + "\n")
                    except Exception as e:
                        print("Exception writing to LOG File:" +str(e))
                        pass
    def create_log_widget(self):
        self.logWidget = LogWidget(self)


log = Log.Instance()
