from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.utils import platform
from edgedetect import EdgeDetect

class AppLayout(FloatLayout):
    edge_detect = ObjectProperty()
        
class ButtonsLayout(RelativeLayout):
    normal = StringProperty()
    down = StringProperty()
    state = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if platform == 'android':
            self.normal = 'icons/cellphone-screenshot_white.png'
            self.down   = 'icons/cellphone-screenshot_red.png'
        else:
            self.normal = 'icons/monitor-screenshot_white.png'
            self.down   = 'icons/monitor-screenshot_red.png'
  
    def on_size(self, layout, size):
        if platform == 'android': 
            self.ids.screen.min_state_time = 0.3 
        else:
            self.ids.screen.min_state_time = 1
        if Window.width < Window.height:
            self.pos = (0 , 0)
            self.size_hint = (1 , 0.2)
            self.ids.other.pos_hint  = {'center_x':.3,'center_y':.5}
            self.ids.other.size_hint = (.2, None)
            self.ids.screen.pos_hint  = {'center_x':.7,'center_y':.5}
            self.ids.screen.size_hint = (.2, None)
        else:
            self.pos = (Window.width * 0.8, 0)
            self.size_hint = (0.2 , 1)
            self.ids.other.pos_hint  = {'center_x':.5,'center_y':.7}
            self.ids.other.size_hint = (None, .2)
            self.ids.screen.pos_hint  = {'center_x':.5,'center_y':.3}
            self.ids.screen.size_hint = (None, .2)

    def screenshot(self):
        self.parent.edge_detect.capture_screenshot()

    def torch(self, state):
        if state == 'toggle':
            self.state = not self.state
            torch = 'on' if self.state else 'off'
        else:
            torch = state
        self.parent.edge_detect.torch(torch)

Builder.load_string("""
<AppLayout>:
    edge_detect: self.ids.preview
    EdgeDetect:
        aspect_ratio: '16:9'
        id:preview
    ButtonsLayout:
        id:buttons

<ButtonsLayout>:
    normal:
    down:
    Button:
        id:other
        on_press: root.torch('toggle')
        height: self.width
        width: self.height
        background_normal: 'icons/camera-flip-outline.png'
        background_down:   'icons/camera-flip-outline.png'
    Button:
        id:screen
        on_press: root.screenshot()
        height: self.width
        width: self.height
        background_normal: root.normal
        background_down: root.down
""")

            
