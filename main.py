from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform
from kivy.clock import Clock
from applayout import AppLayout
from android_permissions import AndroidPermissions
import paho.mqtt.client as mqtt

if platform == 'android':
    from jnius import autoclass
    from android.runnable import run_on_ui_thread
    from android import mActivity
    View = autoclass('android.view.View')

    TessBaseAPI = autoclass('com.googlecode.tesseract.android.TessBaseAPI')
    tessApi = TessBaseAPI()
    print("TessAPI version:", tessApi.getVersion())

    @run_on_ui_thread
    def hide_landscape_status_bar(instance, width, height):
        # width,height gives false layout events, on pinch/spread 
        # so use Window.width and Window.height
        if Window.width > Window.height: 
            # Hide status bar
            option = View.SYSTEM_UI_FLAG_FULLSCREEN
        else:
            # Show status bar 
            option = View.SYSTEM_UI_FLAG_VISIBLE
        mActivity.getWindow().getDecorView().setSystemUiVisibility(option)
elif platform != 'ios':
    # Dispose of that nasty red dot, required for gestures4kivy.
    from kivy.config import Config 
    Config.set('input', 'mouse', 'mouse, disable_multitouch')

class MyApp(App):
    
    def build(self):
        self.layout = AppLayout()
        if platform == 'android':
            Window.bind(on_resize=hide_landscape_status_bar)
        return self.layout

    def on_start(self):
        self.dont_gc = AndroidPermissions(self.start_app)

    def start_app(self):
        self.dont_gc = None
        # Can't connect camera till after on_start()
        Clock.schedule_once(self.connect_camera)

    def connect_camera(self,dt):
        self.client = mqtt.Client()
        self.client.connect('nas.local')
        self.client.loop_start()

        self.layout.edge_detect.callback = self.callback
        self.layout.edge_detect.connect_camera(analyze_pixels_resolution = 720,
                                               enable_analyze_pixels = True)
        Clock.schedule_once(self.torch_start, 3) #allow some time for camera to warm up

    def callback(self, dt):
        print('torch off', self.layout.edge_detect.image_size)
        self.layout.edge_detect.torch('off')
        self.client.publish("flowy/raw", self.layout.edge_detect.pixels)

    def torch_start(self, dt):
        print('torch on')
        self.layout.edge_detect.torch('on')
        Clock.schedule_once(self.torch_stop, 10)

    def torch_stop(self, dt):
        self.layout.edge_detect.capture.set()
        Clock.schedule_once(self.torch_start, 30)
        #Clock.schedule_once(self.disconnect, 2) #allow some time for capture
        #Clock.schedule_once(self.connect_camera, 30)

    def disconnect(self, dt):
        self.layout.edge_detect.disconnect_camera()

    def on_stop(self):
        self.layout.edge_detect.disconnect_camera()

MyApp().run()

