from socket import *
from tkinter import messagebox, ttk
import customtkinter
from customtkinter import CTk, CTkSwitch, CTkLabel, StringVar
import threading
from PIL import Image
import login


customtkinter.set_default_color_theme("green")

client = socket(AF_INET, SOCK_STREAM)
ip = '127.0.0.1'
port = 55555

client.connect((ip, port))

class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("360x130")
        self.title("Chat App")
        self.label = customtkinter.CTkLabel(self, text="Do you want to exit?")
        self.label.pack(padx=20, pady=20)
        self.label.grid(row=0, column=0, columnspan=2, padx=20, pady=10)

        self.yes_button = customtkinter.CTkButton(self, text="Yes", command=self.exit_f)
        self.yes_button.grid(row=1, column=0, padx=20, pady=10)

        self.no_button = customtkinter.CTkButton(self, text="No", command=self.destroy)
        self.no_button.grid(row=1, column=1, padx=20, pady=10)

    def exit_f(self):
        self.destroy()
        exit()

class App(customtkinter.CTk):
    def __init__(self,username):
        super().__init__()

        self.users = None
        self.sent_message = None
        self.received_message = None
        self.name = username
        self.message_counter = 1
        self.chat_counter = 2
        self.mode_switch_var = StringVar(value="system")
        self.resizable(width=True, height=True)
        self.title("Chat App")
        self.geometry(f"{900}x{725}")
        self.app_logo = customtkinter.CTkImage(light_image=Image.open("assets/images/logo.png"), size=(50, 50))
        self.grid_columnconfigure(0, weight=2)

        self.sidebar_frame = customtkinter.CTkFrame(master=self,corner_radius=0,width=900, height=100)
        self.sidebar_frame.grid(row=0, column=0, columnspan=6,rowspan=4, padx=(20, 10), pady=(10, 10), sticky="nsew")
        #self.sidebar_frame.grid_rowconfigure(4, weight=2)
        
        self.logo = customtkinter.CTkLabel(self.sidebar_frame, text="   Chat App",image=self.app_logo,
                                           compound="left", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo.grid(row=0, column=6, padx=(175,175), pady=10)
        
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="GUEST",font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=2, padx=(20,20),pady=5)
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Clear Chat", command=self.clear_chat)
        self.sidebar_button_1.grid(row=1, column=2,padx=(20,20), pady=(10,20))
        
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Logout", command=self.logout)
        self.sidebar_button_2.grid(row=1, column=6,padx=(175,175), pady=(10,20))


        # Theme Toggle
        self.mode_switch = customtkinter.CTkSwitch(self.sidebar_frame, text="Dark/Light Mode", command=self.toggle_mode,
                                                   variable=self.mode_switch_var, onvalue="light", offvalue="dark")
        self.mode_switch.grid(row=0, column=9, padx=(20,20), pady=(10, 10))

        self.exit_button = customtkinter.CTkButton(self.sidebar_frame, text="Exit", hover_color="Red",
                                                   command=self.exit_app)
        self.exit_button.grid(row=1, column=9, padx=(20,20), pady=(10,20))

        self.entry = customtkinter.CTkEntry(self, placeholder_text="Type a message")
        self.entry.grid(row=5, column=0, columnspan=1, padx=(20,10), pady=(20, 20), sticky="nsew")

         # Emoji Picker
        self.emoji_picker = customtkinter.CTkFrame(self, width=300, height=350)
        self.create_emoji_picker()
        self.emoji_picker.place(x=470, y=515)
        self.emoji_picker.lower()
        self.emoji_picker_visible = False

        # Emoji Button
        self.emoji_button = customtkinter.CTkButton(self, text="😊",fg_color="transparent",border_width=1,text_color=("gray10", "#DCE4EE"),width=50, command=self.toggle_emoji_picker)
        self.emoji_button.grid(row=5, column=1, padx=5, pady=(20, 20), sticky="nsew")

        #file Upload
        self.emoji_button = customtkinter.CTkButton(self, text="📁",fg_color="transparent",border_width=1,text_color=("gray10", "#DCE4EE"),width=50,)
        self.emoji_button.grid(row=5, column=2, padx=5, pady=(20, 20), sticky="nsew")
        
        self.main_button_1 = customtkinter.CTkButton(master=self, text="Send", fg_color="transparent", border_width=2,
                                                     text_color=("gray10", "#DCE4EE"), command=self.send_message)
        self.main_button_1.grid(row=5, column=3, padx=(5, 20), pady=(20, 20), sticky="nsew")

        self.tabview = customtkinter.CTkTabview(master=self, width=250, height=490)
        self.tabview.grid(row=4, column=0, columnspan=4, padx=(20, 10), pady=(10, 0), sticky="nsew")

        self.tabview.add("All")  # add tab at the end
        self.tabview.set("All")  # set currently visible tab

        if self.name == "":
            exit()
        self.set_name(name=self.name)

        recv_thread = threading.Thread(target=self.recv_message)
        recv_thread.daemon = True
        recv_thread.start()
        self.toplevel_window = None


    def toggle_emoji_picker(self):
        if self.emoji_picker_visible:
            self.emoji_picker.lower()
        else:
            self.emoji_picker.lift()
        self.emoji_picker_visible = not self.emoji_picker_visible

    def create_emoji_picker(self):
        notebook = ttk.Notebook(self.emoji_picker)
        notebook.pack(expand=True, fill="both", padx=10, pady=10, ipadx=5, ipady=5)
        notebook.enable_traversal()

        emoji_categories = {
            "😀 Faces": ["😀", "😂", "😎", "😢", "😍", "😡", "🤔", "🤩"],
            "👍 Hands": ["👍", "👎", "👌", "✌️", "🙏", "👏", "🤝", "💪"],
            "❤️ Symbols": ["❤️", "💔", "🔥", "✨", "💫", "⭐", "🎉", "⚡"],
            "🍔 Food": ["🍎", "🍌", "🍕", "🍔", "🍩", "🍫", "🍉", "🥑"],
            "🚗 Travel": ["🚗", "🚀", "✈️", "🚢", "🗺️", "🏕️", "🏖️", "🏝️"]
        }

        for category, emojis in emoji_categories.items():
            frame = customtkinter.CTkFrame(notebook)
            notebook.add(frame, text=category)

            # Emoji Buttons
            for i, emoji_char in enumerate(emojis):
                btn = customtkinter.CTkButton(frame, text=emoji_char, width=40,
                                    command=lambda e=emoji_char: self.add_emoji_from_picker(e))
                btn.grid(row=i//4, column=i%4, padx=5, pady=5)


    def add_emoji_from_picker(self, emoji_char):
        current_text = self.entry.get()
        self.entry.delete(0, "end")
        self.entry.insert(0, current_text + emoji_char)
        self.emoji_picker.lower()
        self.emoji_picker_visible = False

    def toggle_mode(self):
        mode = self.mode_switch_var.get()
        if mode == "light":
            customtkinter.set_appearance_mode("light")  # Light mode background color
        else:
            customtkinter.set_appearance_mode("dark")
            
    def logout(self):
        self.destroy()
        screen = login.AuthApp()
        screen.mainloop()
        exit()
      
    def exit_app(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(self)
            self.toplevel_window.focus()
        else:
            self.toplevel_window.focus()

    def set_name(self, name):
        client.send(name.encode('utf8'))
        self.name = name
        self.logo_label.configure(text=f"Hello {name} !")

    def clear_chat(self):
        current_tab = self.tabview.get()
        for widget in self.tabview.tab(current_tab).grid_slaves():
            widget.grid_forget()

    def send_message(self):
        message = self.entry.get()
        if len(message) > 0:
            self.entry.delete(0, "end")
            self.sent_message = customtkinter.CTkLabel(self.tabview.tab(self.tabview.get()), text="You: " + message + "\n",width=840,
                                                       font=customtkinter.CTkFont(size=20), text_color=("gray10", "#DCE4EE"),anchor="w")
            self.sent_message.grid(row=self.message_counter, column=1, padx=(10, 10), sticky="nsew")
            self.message_counter = self.message_counter + 1
            detailed_message = self.tabview.get() + "--" + message
            client.send(detailed_message.encode('utf8'))

    def recv_message(self):
        while True:
            try:
                server_message = client.recv(1024).decode('utf8')
                print(server_message)

                if server_message.startswith("FILE--"):
                    _, sender, recipient, file_name, file_size = server_message.split("--")
                    self.receive_file(sender, recipient, file_name, int(file_size))
                else:
                    message_array = server_message.split("--")
                    if len(message_array) > 2:
                        if message_array[1] == "All":
                            self.received_message = customtkinter.CTkLabel(self.tabview.tab("All"),
                                                                        text=f"{message_array[0]}: {message_array[2]}",width=840,
                                                                        font=customtkinter.CTkFont(size=20),text_color=("gray10", "#DCE4EE"), anchor="w")
                            self.received_message.grid(row=self.message_counter, column=1, columnspan=2, padx=(10, 10),sticky="nsew")
                            self.message_counter += 1
                        elif message_array[1] == self.name:
                            self.received_message = customtkinter.CTkLabel(self.tabview.tab(message_array[0]),
                                                                        text=f"{message_array[0]}: {message_array[2]}",width=840,
                                                                        font=customtkinter.CTkFont(size=20),text_color="white", anchor="w")
                            self.received_message.grid(row=self.message_counter, column=1, columnspan=2, padx=(10, 10),sticky="nsew")
                            self.message_counter += 1

                if server_message.startswith("new_client-"):
                    self.tabview.add(server_message.split("-")[1])
                elif server_message.startswith("exit_client-"):
                    self.tabview.delete(server_message.split("-")[1])
                elif server_message.startswith("Other users:"):
                    self.users = server_message.split(":")[1]
                    for us in self.users.split(","):
                        if us != self.name:
                            self.tabview.add(us)

            except Exception as e:
                print("Error receiving message:", e)
                break  # Exit loop on error


if __name__ == "__main__":
    app = App("GUEST")
    app.mainloop()