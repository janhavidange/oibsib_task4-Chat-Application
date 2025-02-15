import customtkinter
from customtkinter import CTk, CTkSwitch, CTkLabel, StringVar
import sqlite3
from tkinter import messagebox
import os
from PIL import Image
import hashlib
import home


# Password hashing function
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

class AuthApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Chat App")
        self.geometry("500x400")
        self.setup_database()
        customtkinter.set_appearance_mode("system")  # Default to system Mode
        self.mode_switch_var = StringVar(value="system")
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "./assets/images")
        self.exit_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "exit.png")),
                                        dark_image=Image.open(os.path.join(image_path, "exit.png")), size=(20, 20))
        self.show_login()


    # Database Setup
    def setup_database(self):
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT UNIQUE NOT NULL,
                            password TEXT NOT NULL,
                            security_question TEXT NOT NULL,
                            security_answer TEXT NOT NULL
                        )
                    ''')
        conn.commit()
        conn.close()


    def show_login(self):
        self.clear_widgets()
        self.login_frame = customtkinter.CTkFrame(self)
        self.login_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Theme Toggle
        self.mode_switch = customtkinter.CTkSwitch(self.login_frame, text="Dark/Light Mode",
                                    command=self.toggle_mode,
                                    variable=self.mode_switch_var,
                                    onvalue="light", offvalue="dark")
        self.mode_switch.pack(pady=5)
        

        self.exit_button = customtkinter.CTkButton(self.login_frame, corner_radius=0, height=40, border_spacing=10, text="Exit",
                                                    fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                    image=self.exit_image, anchor="w", command=self.destroy)
        self.exit_button.place(x=375, y=5)
        
        
        customtkinter.CTkLabel(self.login_frame, text="Login", font=("Arial", 20)).pack(pady=10)
        
        customtkinter.CTkLabel(self.login_frame, text="Username:").place(x=75, y=85)
        self.login_user_entry = customtkinter.CTkEntry(self.login_frame, placeholder_text="Username")
        self.login_user_entry.pack(pady=5)

        customtkinter.CTkLabel(self.login_frame, text="Password:").place(x=75, y=125)
        self.login_pass_entry = customtkinter.CTkEntry(self.login_frame, placeholder_text="Password", show="*")
        self.login_pass_entry.pack(pady=5)
        
        self.login_btn = customtkinter.CTkButton(self.login_frame, text="Login", command=self.login)
        self.login_btn.pack(pady=5)
        
        self.forgot_pass_btn = customtkinter.CTkButton(self.login_frame, text="Forgot Password?", command=self.show_reset)
        self.forgot_pass_btn.pack(pady=5)
        
        self.signup_btn = customtkinter.CTkButton(self.login_frame, text="Sign Up", command=self.show_signup)
        self.signup_btn.pack(pady=5)
        
    
    def show_signup(self):
        self.clear_widgets()
        self.signup_frame = customtkinter.CTkFrame(self)
        self.signup_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        
        # Theme Toggle
        self.mode_switch = customtkinter.CTkSwitch(self.signup_frame, text="Dark/Light Mode",
                                    command=self.toggle_mode,
                                    variable=self.mode_switch_var,
                                    onvalue="light", offvalue="dark")
        self.mode_switch.pack(pady=5)
        
        self.exit_button = customtkinter.CTkButton(self.signup_frame, corner_radius=0, height=40, border_spacing=10, text="Exit",
                                                    fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                    image=self.exit_image, anchor="w", command=self.destroy)
        self.exit_button.place(x=375, y=5)
        
        customtkinter.CTkLabel(self.signup_frame, text="Sign Up", font=("Arial", 20)).pack(pady=10)
        
        customtkinter.CTkLabel(self.signup_frame, text="Username:").place(x=75, y=85)
        self.signup_user_entry = customtkinter.CTkEntry(self.signup_frame, placeholder_text="Username")
        self.signup_user_entry.pack(pady=5)
        
        customtkinter.CTkLabel(self.signup_frame, text="Password:").place(x=75, y=125)
        self.signup_pass_entry = customtkinter.CTkEntry(self.signup_frame, placeholder_text="Password", show="*")
        self.signup_pass_entry.pack(pady=5)
        
        customtkinter.CTkLabel(self.signup_frame, text="Security Question:").place(x=50, y=165)
        self.security_questions = ["Your nickname?", "Your school name?", "Your mother’s name?"]
        self.security_question_var = customtkinter.StringVar(value=self.security_questions[0])
        self.security_question_dropdown = customtkinter.CTkComboBox(self.signup_frame, values=self.security_questions, variable=self.security_question_var)
        self.security_question_dropdown.pack(pady=5)
        
        customtkinter.CTkLabel(self.signup_frame, text="Security Answer:").place(x=50, y=205)
        self.signup_sec_answer = customtkinter.CTkEntry(self.signup_frame, placeholder_text="Security Answer")
        self.signup_sec_answer.pack(pady=5)
        
        self.signup_btn = customtkinter.CTkButton(self.signup_frame, text="Sign Up", command=self.signup)
        self.signup_btn.pack(pady=5)
        
        self.back_btn = customtkinter.CTkButton(self.signup_frame, text="Back", command=self.show_login)
        self.back_btn.pack(pady=5)
    
    def show_reset(self):
        self.clear_widgets()
        self.reset_frame = customtkinter.CTkFrame(self)
        self.reset_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        
        # Theme Toggle
        self.mode_switch = customtkinter.CTkSwitch(self.reset_frame, text="Dark/Light Mode",
                                    command=self.toggle_mode,
                                    variable=self.mode_switch_var,
                                    onvalue="light", offvalue="dark")
        self.mode_switch.pack(pady=5)
        
        self.exit_button = customtkinter.CTkButton(self.reset_frame, corner_radius=0, height=40, border_spacing=10, text="Exit",
                                                    fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                    image=self.exit_image, anchor="w", command=self.destroy)
        self.exit_button.place(x=375, y=5)
        
        customtkinter.CTkLabel(self.reset_frame, text="Reset Password", font=("Arial", 20)).pack(pady=10)
        
        customtkinter.CTkLabel(self.reset_frame, text="Username:").place(x=75, y=85)
        self.reset_user_entry = customtkinter.CTkEntry(self.reset_frame, placeholder_text="Username")
        self.reset_user_entry.pack(pady=5)
        
        customtkinter.CTkLabel(self.reset_frame, text="Security Question:").place(x=50, y=125)
        self.security_questions = ["Your nickname?", "Your school name?", "Your mother’s name?"]
        self.security_question_var = customtkinter.StringVar(value=self.security_questions[0])
        self.security_question_dropdown = customtkinter.CTkComboBox(self.reset_frame, values=self.security_questions, variable=self.security_question_var)
        self.security_question_dropdown.pack(pady=5)
        
        customtkinter.CTkLabel(self.reset_frame, text="Security Answer:").place(x=50, y=165)
        self.reset_sec_entry = customtkinter.CTkEntry(self.reset_frame, placeholder_text="Answer")
        self.reset_sec_entry.pack(pady=5)
        
        customtkinter.CTkLabel(self.reset_frame, text="New Password:").place(x=50, y=205)
        self.reset_newpass_entry = customtkinter.CTkEntry(self.reset_frame, placeholder_text="New Password", show="*")
        self.reset_newpass_entry.pack(pady=5)
        
        self.reset_btn = customtkinter.CTkButton(self.reset_frame, text="Reset Password", command=self.reset_password)
        self.reset_btn.pack(pady=5)
        
        self.back_btn = customtkinter.CTkButton(self.reset_frame, text="Back", command=self.show_login)
        self.back_btn.pack(pady=5)

            
    def login(self):
        username = self.login_user_entry.get().strip()
        password = self.login_pass_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Username and Password cannot be empty!")
            return

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username=?", (username,))
        result = cursor.fetchone()
        conn.close()
        
        if result and result[0] == hash_password(password):
            messagebox.showinfo("Success", "Login Successful!")
            #self.after(100, self.destroy())
            try:
                self.destroy()
                dashboard = home.App(username=username)
                dashboard.mainloop()
            except:
                pass
        else:
            messagebox.showerror("Error", "Invalid Username or Password")
    
    def signup(self):
        username = self.signup_user_entry.get().strip()
        password = self.signup_pass_entry.get().strip()
        sec_question = self.security_question_var.get().strip()
        sec_answer = self.signup_sec_answer.get().strip()

        if not username or not password or not sec_question or not sec_answer:
            messagebox.showerror("Error", "All fields are required!")
            return

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        try:
            hashed_password = hash_password(password)
            cursor.execute("INSERT INTO users (username, password, security_question, security_answer) VALUES (?, ?, ?, ?)", 
                            (username, hashed_password, sec_question, sec_answer))
            conn.commit()
            messagebox.showinfo("Success", "Account Created Successfully!")
            self.show_login()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists!")
        finally:
            conn.close()
    
    def reset_password(self):
        username = self.reset_user_entry.get().strip()
        sec_question = self.security_question_var.get().strip()
        sec_answer = self.reset_sec_entry.get().strip()
        new_password = self.reset_newpass_entry.get().strip()
        
        if not username or not sec_question or not sec_answer or not new_password:
            messagebox.showerror("Error", "All fields are required!")
            return

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        #cursor.execute("SELECT * FROM users WHERE username=? AND security_question=? AND security_answer=?", (username,sec_question, sec_answer))
        cursor.execute("SELECT security_answer FROM users WHERE username=?", (username,))
        result = cursor.fetchone()
        
        if result and result[0] == sec_answer:
            hashed_password = hash_password(new_password)
            cursor.execute("UPDATE users SET password=? WHERE username=?", (hashed_password, username))
            conn.commit()
            messagebox.showinfo("Success", "Password Reset Successfully!")
            self.create_login_screen()
        else:
            messagebox.showerror("Error", "Incorrect Security Answer!")
        
        conn.close()
    
    def toggle_mode(self):
        mode = self.mode_switch_var.get()
        if mode == "light":
            customtkinter.set_appearance_mode("light")  # Light mode background color
        else:
            customtkinter.set_appearance_mode("dark")
    
    def clear_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()



if __name__ == "__main__":
    app = AuthApp()
    app.mainloop()
