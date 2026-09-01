import customtkinter as ctk
from login_window import LoginWindow
from dashboard import Dashboard
import customtkinter as ctk
import theme

# ctk.set_appearance_mode("System")
# ctk.set_default_color_theme("custom_theme.json")
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Task Management System")
        self.geometry("1200x800")
        self.minsize(800, 600)
        
        self.show_login()
        
    def show_login(self):
        for widget in self.winfo_children():
            widget.destroy()
            
        self.login_frame = LoginWindow(self, self.on_login_success)
        self.login_frame.pack(fill="both", expand=True)
        
    def on_login_success(self, user):
        self.user = user
        for widget in self.winfo_children():
            widget.destroy()
            
        self.dashboard_frame = Dashboard(self, self.user, self.on_logout)
        self.dashboard_frame.pack(fill="both", expand=True)
        
    def on_logout(self):
        self.user = None
        self.show_login()

if __name__ == "__main__":
    app = App()
    app.mainloop()
