import cv2
import qrcode
import numpy as np
from kivy.app import App
from barcode import EAN13
from pyzbar.pyzbar import decode
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from barcode.writer import ImageWriter
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout

class CodeScanner(App):
    def build(self):
        self.window=GridLayout()
        self.window.cols=1
        self.window.size_hint=(0.6,0.7)
        self.window.pos_hint={"center_x":0.5, "center_y":0.5}
        #image that is qrcode and barcode after creating
        self.window.add_widget(Image(source="qrcode.png"))
        self.window.add_widget(Image(source="barcode.png"))
        self.l=Label(text="Result",font_size=15,
                      color="#00FFCE")
        self.window.add_widget(self.l)
        #input for qrcode
        self.lb=Label(text='''Enter the information that you want to store in qrcode\n  it may be texts/links/numbers.. How many you want''',
                      font_size=15,
                      color="#00FFCE"
                      )
        self.window.add_widget(self.lb)
        self.user=TextInput(size_hint=(1,0.5))
        self.window.add_widget(self.user)
        #input for barcode
        self.lb1=Label(text="Enter numbers only that you want to store in barcode\n (barcode contains only 12 digits)",
                      font_size=15,
                      color="#00FFCE")
        self.window.add_widget(self.lb1)
        self.user1=TextInput(multiline=False,
                            size_hint=(1,0.5))
        self.window.add_widget(self.user1)
        #button for qrcode
        self.button=Button(text="create qrcode",
                        size_hint=(1,0.5),
                        color="#00FFCE",
                        bold=True,
                        )
        self.button.bind(on_press=self.callback)
        self.window.add_widget(self.button)
        #button for barcode
        self.button=Button(text="create barcode",
                        size_hint=(1,0.5),
                        color="#00FFCE",
                        bold=True,)
        self.button.bind(on_press=self.callback1)
        self.window.add_widget(self.button)
        #button for scanning
        self.button=Button(text="scanning",
                        size_hint=(1,0.5),
                        color="#00FFCE",
                        background_color="#00FFCE",
                        bold=True,)
        self.button.bind(on_press=self.sc)
        self.window.add_widget(self.button)


        return self.window

    def callback(self, instance):
        self.img=qrcode.make(self.user.text)
        self.img.save("qrcode.png")
        self.l.text="QR code succesfully generated"

    def callback1(self, instance):
         self.number=self.user1.text
         self.a=EAN13(self.number,writer=ImageWriter())
         self.a.save("barcode")
         self.l.text="Barcode succesfully generated"
    def sc(self, instance):
        cap=cv2.VideoCapture(0)
        while True:
            s,img=cap.read()
            for i in decode(img):
                data=i.data.decode("utf-8")
                print(data)
                pts=np.array([i.polygon],np.int32)
                pts=pts.reshape((-1,1,2))
                cv2.polylines(img,[pts],True,(255,0,255),5)
                pts2=i.rect
                cv2.putText(img,data,(pts2[0],pts2[1]),cv2.FONT_HERSHEY_SIMPLEX, 0.9,(255,0,255),2)
            cv2.imshow("image",img)
            cv2.waitKey(1)


        
        
CodeScanner().run()