import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from ibm_analyzer import sent_analysis


class ChatPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        #chat page 2x2
        self.cols = 2
        self.rows = 2

        #upper left side: chat history
        self.history = ScrollableLabel(height=Window.size[1]*0.7, width=Window.size[0]*0.6, size_hint_y=None)
        self.add_widget(self.history)

        #upper right side: list of users shown
        self.inside = GridLayout(cols=1, rows=6, size_hint_x=None)
        self.inside.name = Label(text="users online")
        self.inside.user1 = Label(text= "user1")
        self.inside.user2 = Label(text= "user2")
        self.inside.user3 = Label(text= "user3")
        self.inside.user4 = Label(text= "user4")
        self.inside.user5 = Label(text= "user5")

        self.inside.add_widget(self.inside.name)
        self.inside.add_widget(self.inside.user1)
        self.inside.add_widget(self.inside.user2)
        self.inside.add_widget(self.inside.user3)
        self.inside.add_widget(self.inside.user4)
        self.inside.add_widget(self.inside.user5)

        self.add_widget(self.inside)

        #lower left side: new message
        self.new_message = TextInput(multiline=True)
        self.add_widget(self.new_message)

        #lower right side: send button
        self.send = Button(text="Send", size_hint_x=None)
        self.send.bind(on_press=self.send_message)
        self.add_widget(self.send)

        #gets called when the button is pressed
        Window.bind(on_key_down=self.on_key_down)

    def on_key_down(self, instance, keyboard, keycode, text, modifiers):

        # enter key equals the send button
        if keycode == 40:
            self.send_message(None)

    def send_message(self, _):

        message = self.new_message.text
        self.new_message.text = ''

        if message:
            self.history.update_chat_history(f'YOU > {sent_analysis(message)}')

    def receive_message(self, message):
        self.history.update_chat_history(f'USER > {sent_analysis(message)}')


#for inside the upper left grid
class ScrollableLabel(ScrollView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = GridLayout(cols=1, size_hint_y=None)
        self.add_widget(self.layout)

        self.chat_history = Label(size_hint_y=None)
        self.scroll_to_point = Label()

        self.layout.add_widget(self.chat_history)
        self.layout.add_widget(self.scroll_to_point)

    def update_chat_history(self, message):

        self.chat_history.text += '\n\n' + message

        #adjust the size of the grid
        self.layout.height = self.chat_history.texture_size[1]
        self.chat_history.height = self.chat_history.texture_size[1] + 20
        self.chat_history.text_size = (self.chat_history.width * 0.98, None)

        self.scroll_to(self.scroll_to_point) #automatically scroll down when message goes over the grid


#main app
class TheApp(App):
    def build(self):
        return ChatPage()


if __name__ == "__main__":
    chat_app = TheApp()
    chat_app.run()
