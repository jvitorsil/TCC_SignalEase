import customtkinter as ctk
from config.settings import *
from interface.sidebar import Sidebar
from interface.tab_management import TabManagement

class InterfaceApp:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.tab_management = TabManagement(self)  # Inicialize tab_management primeiro
        self.sidebar = Sidebar(self)  # Depois inicialize sidebar
    
    def setup_window(self):
        """Configurações iniciais da janela principal."""
        self.root.title("SignalEase")
        self.root.geometry("1024x720")

        self.root.wm_minsize(1024, 720)  # Ajuste os valores conforme necessário

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

def iniciar_interface():
    root = ctk.CTk()
    app = InterfaceApp(root)
    root.mainloop()