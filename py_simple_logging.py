import time
from datetime import datetime
import colorama
import os

class LogLevel():    
    class LogColor:
        def __init__(self, name, code, html, rgb):
            self.name = name
            self.code = code
            self.html = html
            self.rgb = rgb
        
    def __init__(self, level, name, description, code, html, rgb):
        self.color = self.LogColor(name, code, html, rgb)
        self.level = level
        self.name = name
        
class LogWidgetMeta:
    log_levels = {  'a': LogLevel(0, 'all', 'white', "\033[37m", "<font color=\"White\">", (255,255,255)),  
                    'd': LogLevel(1, 'debug', 'blue', "\033[94m", "<font color=\"Blue\">", (0,0,255)),
                    'i': LogLevel(2, 'info', 'white', "\033[37m", "<font color=\"White\">", (255,255,255)),
                    's': LogLevel(2, 'success', 'green', "\033[92m", "<font color=\"Green\">", (0,255,0)),
                    'w': LogLevel(3, 'warning', 'orange', "\033[93m", "<font color=\"Orange\">", (255,155,0)),
                    'e': LogLevel(4, 'exception', 'red', "\033[91m", "<font color=\"Red\">", (255,0,0)),
                }
        
    def __init__(self, min_log_level='a'):
        self.tag = "LogWidgetMeta"
        self.min_log_level = 'a'
        self.log_level = self.min_log_level
        self.color_reset = LogLevel.LogColor('reset', "\033[0;0m", "</>", (255,255,255))
        self.enabled = True
        self.text_lines = []
    
    def set_min_log_level(self, level):
        self.i("LOGGER", f"{self.tag} Logging Level Changed: {self.min_log_level} - {str(self.log_levels[self.min_log_level])}")
        self.min_log_level = level

    def get_min_log_level_index(self):
        return list(self.log_levels.keys()).index(self.min_log_level)

    def setEnabled(self, enabled):
        self.i("LOGGER", f"Logging has been {self.status_string(enabled)}") 
        self.enabled = enabled
        
    def status_string(self, status):
        return "ENABLED" if status else "DISABLED"
    
    def append(self, tag, text, log_level, **kwargs):    
        if self.log_levels[log_level].level < self.log_levels[self.min_log_level].level:
            return None
        dateTimeObj = datetime.now()
        timestampStr = dateTimeObj.strftime("%d-%b-%Y %H:%M:%S") + " - "
        log_text = f"{timestampStr} {self.log_level}[{tag}]: {text}"
        return log_text
    
    def flush_lines(self):
        pass    
    
    def destroy(self):
        pass
    
    def check_log_status(self, text):
        pass
    
    def on_logging_level_changed(self, new_logging_level):
        pass
    
class FileLogWidget(LogWidgetMeta):
    def __init__(self, min_log_level='a', filename=None, dir_path="logs"):
        super(FileLogWidget, self).__init__(min_log_level)
        self.tag = "FileLogWidget"
        filename = f"log_{datetime.now().strftime('%d_%b_%Y-%H_%M_%S')}.txt" if filename is None else filename   
        self.log_file_path = f"{dir_path}/{filename}.txt" 
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        self.file = open(self.log_file_path, "w+")
        
    def append(self, tag, text, log_level, flush=True, **kwargs):  
        text = super().append(tag, text, log_level, **kwargs)
        self.text_lines.append(text)
        if flush:
            self.flush_lines()
        return None
            
    def flush_lines(self):
        while len(self.text_lines) > 0:
            line = self.text_lines.pop()
            self.file.write(f"{line}\n")  
        return None   
            
    def destroy(self):
        self.file.close()
        
        
class ConsoleLogWidget(LogWidgetMeta):
    def __init__(self, min_log_level='a'):
        super(ConsoleLogWidget, self).__init__(min_log_level)
        self.tag = "ConsoleLogWidget"
    
    def append(self, tag, text, log_level, flush=True, color=None, **kwargs):  
        text = super().append(tag, text, log_level, **kwargs)
        color = LogWidgetMeta.log_levels[log_level].color.code
        self.text_lines.append(f"{color}{text}{self.color_reset.code}")
        if flush:
            self.flush_lines()
        return None
            
    def flush_lines(self):        
        while len(self.text_lines) > 0:
            line = self.text_lines.pop()
            print(line)   
        return None

# class QtLogWidget(LogWidgetMeta, QWidget):
#     def __init__(self, logger):
#         import PySide2.QtWidgets as pyQtWidgets
#         import PySide2.QtGui as pyQtGui
#         super(LogWidget, self).__init__()
#         self.tag = "QtLogWidget"
#         self.main_layout = pyQtWidgets.QVBoxLayout()
#         self.extra_layout = pyQtWidgets.QHBoxLayout()
#         self.logger = logger
#         self.text_area = pyQtWidgets.QTextEdit()
#         self.text_area.setReadOnly(True)
#         self.text_area.setFont(QFont("Courier New", 9))

#         self.title = pyQtWidgets.QLabel("LOG")
#         self.filter_label = pyQtWidgets.QLabel("Filter level:")
#         self.filter_combobox = pyQtWidgets.QComboBox()
#         for key in self.logger.log_levels.keys():
#             self.filter_combobox.addItem(str(self.logger.log_levels[key]) + " - " + key, key)
#         self.filter_combobox.currentIndexChanged.connect(self.on_logging_level_changed)
#         self.enable_checkbox = pyQtWidgets.QCheckBox("Enable")
#         self.enable_checkbox.stateChanged.connect(self.enable_checkbox_changed)
#         self.console_checkbox = pyQtWidgets.QCheckBox("Console")
#         self.console_checkbox.stateChanged.connect(self.console_checkbox_changed)
#         self.widget_checkbox = pyQtWidgets.QCheckBox("Widget")
#         self.widget_checkbox.stateChanged.connect(self.widget_checkbox_changed)
#         self.file_checkbox = pyQtWidgets.QCheckBox("File")
#         self.file_checkbox.stateChanged.connect(self.file_checkbox_changed)

#         self.extra_layout.addWidget(self.title)
#         self.extra_layout.addWidget(self.filter_label)
#         self.extra_layout.addWidget(self.filter_combobox)
#         self.extra_layout.addWidget(self.enable_checkbox)
#         self.extra_layout.addWidget(self.console_checkbox)
#         self.extra_layout.addWidget(self.widget_checkbox)
#         self.extra_layout.addWidget(self.file_checkbox)
#         self.extra_layout.addStretch(1)

#         self.main_layout.addLayout(self.extra_layout)
#         self.main_layout.addWidget(self.text_area)
#         self.check_log_status()

#         self.setLayout(self.main_layout)
        
#     def init(self):
#         self.logWidget = LogWidget(self)

#     def append(self, text):
#         text = super().append(text)
#         self.text_area.append(text)
#         # self.text_area.moveCursor(QTextCursor.End)
#         self.text_area.verticalScrollBar().setValue(self.text_area.verticalScrollBar().maximum())
        
#     def on_logging_level_changed(self, new_logging_level):
#         self.logger.set_min_log_level(self.filter_combobox.itemData(new_logging_level))        

#     def enable_checkbox_changed(self, value):
#         self.logger.setEnabled(value)
#         self.check_log_status()

#     def console_checkbox_changed(self, value):
#         self.logger.setConsoleEnabled(value)
#         self.check_log_status()

#     def widget_checkbox_changed(self, value):
#         self.logger.setWidgetEnabled(value)
#         self.check_log_status()

#     def file_checkbox_changed(self, value):
#         self.logger.setFileEnabled(value)
#         self.check_log_status()

#     def check_log_status(self):
#         self.filter_combobox.setCurrentIndex(self.logger.get_min_log_level_index())

#         self.enable_checkbox.setChecked(self.logger.enabled)
#         self.console_checkbox.setChecked(self.logger.enable_console)
#         self.widget_checkbox.setChecked(self.logger.enable_widget)
#         self.file_checkbox.setChecked(self.logger.save_to_file)

#         self.console_checkbox.setEnabled(self.logger.enabled)
#         self.widget_checkbox.setEnabled(self.logger.enabled)
#         self.file_checkbox.setEnabled(self.logger.enabled)

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
    
    def __init__(self, min_log_level='a', drawer=None, draw_type=None, canvas=None):
        super(VisualLogWidget, self).__init__(min_log_level)
        self.tag = "VisualLogWidget"
        self.drawer = drawer
        self.draw_type = self.Type.NONE if draw_type is None else draw_type
        self.canvas = canvas
        self.font = None
        self.font_size = 20
        self.line_height = 20
    
    def set_canvas(self, canvas):
        self.canvas = canvas
    
    def draw_text_line(self, start, end, color, thickness):
        pass
    
    def draw_line(self, start, end, color, thickness):
        pass
    
    def draw_circle(self, center, color, radius, thickness):
        pass
    
    def append(self, tag, text, log_level, flush=False, color=None, pos=None, font=None, font_size=1, line_height=None, **kwargs):
        if pos is None:
            pos = VisualLogWidget.Point(10, 10)
        text = super().append(tag, text, log_level, **kwargs)
        font = self.font if font is None else font
        font_size == self.font_size if font_size is None else font_size
        line_height = self.line_height if line_height is None else line_height
        color = LogWidgetMeta.log_levels[log_level].color.rgb if color is None else color
        self.text_lines.append(self.DebugTextLine(text, color, self.Point(pos.x, pos.y), font, font_size))
        pos.y += line_height
        return pos
    
    def flush_lines(self, draw=True, canvas=None, debug=False):
        if debug:
            print(f"[{self.tag}] Flushing {len(self.text_lines)} lines")
        return 
    
    
class CvLogWidget(VisualLogWidget):
    def __init__(self, min_log_level='a', cv=None):
        super(CvLogWidget, self).__init__(cv, VisualLogWidget.OPENCV)
        self.tag = "CVLogWidget"
        
    def append(self, tag, text, log_level, flush=False, color=None, pos=None, font=None, font_size=1, line_height=None, **kwargs):
        return super().append(tag, text, log_level, flush, color, pos, font, font_size, line_height, **kwargs)
    
    def flush_lines(self, draw=True, canvas=None, debug=False):
        super().flush_lines(draw, canvas, debug)
        while len(self.text_lines) > 0:
            line = self.text_lines.pop()
            if draw:
                try:
                    self.draw_text_line(line, canvas)
                except Exception as e:
                    print(f"[{self.tag}] Error printing line '{line.text}': {e}")
        if debug:
            print(f"[{self.tag}] Remaining {len(self.text_lines)} lines")
        
    def draw_text_line(self, line, canvas=None):
        canvas = self.canvas if canvas is None else canvas
        self.drawer.putText(canvas, line.text, (int(line.pos.x), int(line.pos.y)), 0, line.font_size, line.color, 2)
    
    def draw_line(self, start, end, color, thickness):
        self.drawer.line(self.canvas, (int(start.x), int(start.y)), (int(end.x), int(end.y)), color, thickness)
        
    def draw_circle(self, center, color, radius, thickness):
        self.drawer.circle(self.canvas, (int(center.x), int(center.y)), radius, color, thickness)
        
        
class PyGameLogWidget(VisualLogWidget):
    def __init__(self, min_log_level='a', pygame=None, font=None, font_size=16, canvas=None):
        super(PyGameLogWidget, self).__init__(min_log_level, drawer=pygame, draw_type=VisualLogWidget.Type.PYGAME, canvas=canvas)
        self.tag = "PyGameLogWidget"
        self.font = pygame.font.SysFont('Arial', 16) if font is None else font
        self.font_size = font_size
        self.line_height = self.font_size*0.8
        
    def append(self, tag, text, log_level, flush=False, color=None, pos=None, font=None, font_size=1, line_height=None, **kwargs):
        return super().append(tag, text, log_level, flush, color, pos, font, font_size, line_height, **kwargs)
    
    def flush_lines(self, draw=True, canvas=None, debug=False):
        super().flush_lines(draw, canvas, debug)
        while len(self.text_lines) > 0:
            line = self.text_lines.pop()
            if draw:
                try:
                    self.draw_text_line(line, canvas)
                except Exception as e:
                    print(f"[{self.tag}] Error printing line '{line.text}': {e}")
        if debug:
            print(f"[{self.tag}] Remaining {len(self.text_lines)} lines")
    def draw_text_line(self, line, canvas=None):
        canvas = self.canvas if canvas is None else canvas
        canvas.blit(line.font.render(line.text, True, line.color), (int(line.pos.x), int(line.pos.y)))
    
    def draw_line(self, start, end, color, thickness):
        self.drawer.draw.line(self.canvas, color=color, start_pos=(int(start.x), int(start.y)), end_pos=(int(end.x), int(end.y)), width=thickness)
        
    def draw_circle(self, center, color, radius, thickness):
        self.drawer.draw.circle(self.canvas, color=color, center=(int(center.x), int(center.y)), radius=radius, width=thickness)


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

@Singleton
class Log(object):
    def __init__(self):
        self.widgets = []
        
    def add_widget(self, widget):
        self.widgets.append(widget)
        
    def w(self, tag, text, **kwargs):
        return self.append(tag, text, 'w', **kwargs)

    def d(self, tag, text, **kwargs):
        return self.append(tag, text, 'd', **kwargs)

    def e(self, tag, text, **kwargs):
        return self.append(tag, text, 'e', **kwargs)

    def s(self, tag, text, **kwargs):
        return self.append(tag, text, 's', **kwargs)

    def i(self, tag, text, **kwargs):
        return self.append(tag, text, 'i', **kwargs)

    def append(self, tag, text, log_level='a', **kwargs):
        for widget in self.widgets:
            res = widget.append(tag, text, log_level, **kwargs)    
            if res is not None:
                pos = res      
        return pos
        # if self.enabled:
        #     color = self.colors[color_name]
        #     color_reset = self.colors['reset']
        #     if self.log_levels[log_level] >= self.log_levels[self.min_log_level]:
        #         if self.enable_widget and log_to_widget and self.logWidget is not None:
        #             try:
        #                 final_text = timestampStr + color.color_html + " " + log_text + color_reset.color_html
        #                 self.logWidget.append(final_text + "\n")
        #             except Exception as e:
        #                 print("Exception writing to LOG Widget:" + str(e))
        #                 pass
        #         if self.enable_console:
        #             final_text = timestampStr + color.color_code + " " + log_text + color_reset.color_code
        #             print(final_text)
        #         if self.save_to_file:
        #             try:
        #                 self.file.write(timestampStr + log_text + "\n")
        #             except Exception as e:
        #                 print("Exception writing to LOG File:" +str(e))
        #                 pass
        
    def flush(self):
        for widget in self.widgets:
            widget.flush_lines()
            
    def init(self):
        for widget in self.widgets:
            widget.init()
            
    def destroy(self):
        for widget in self.widgets:
            widget.destroy()

log = Log.Instance()
