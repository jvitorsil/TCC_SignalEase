import customtkinter as ctk
from config.settings import *
from config.icons import *
import os

class Sidebar:
    def __init__(self, app):
        self.app = app
        self.frame_sidebar = ctk.CTkFrame(app.root, fg_color=SIDEBAR_COLOR, corner_radius=10)
        self.frame_sidebar.grid(row=0, column=0, sticky="ns")
        self.frame_sidebar.grid_propagate(False)
        self.frame_sidebar.configure(width=SIDEBAR_WIDTH_EXPANDED, height=SIDEBAR_HEIGHT)
        
        self.footer_label = ctk.CTkLabel(self.frame_sidebar, image=footer_image, text="")
        self.footer_label.pack(side="bottom", pady=10)

        self.toggle_button = ctk.CTkButton(self.frame_sidebar, command=self.toggle_sidebar, text="", fg_color="transparent", width=TOGGLE_BUTTON_WIDTH, height=TOGGLE_BUTTON_HEIGHT, image=icon_toggle_open, hover_color=HOVER_COLOR)
        self.toggle_button.pack(pady=10, padx=10, side="top", anchor="e")

        self.dados_eeg = None
        self.dados_emg = None
        self.dados_aux = None
        self.sidebar_expanded = True
        # self.selected_button = None


        self.create_sidebar_buttons()

    def create_sidebar_buttons(self):
        """Adiciona os botões da barra lateral."""
        self.btn_home = self.create_sidebar_button("Home", icon_home, icon_home_selected, self.app.tab_management.show_home)
        self.btn_upload = self.create_sidebar_button("Upload files", icon_upload_file, icon_upload_file_selected, self.app.tab_management.show_upload)
        self.btn_sync = self.create_sidebar_button("Synchronization", icon_sync, icon_sync_selected, self.app.tab_management.show_sync)
        self.btn_processing = self.create_sidebar_button("Processing", icon_processing, icon_processing_selected, self.app.tab_management.show_processing)
        self.btn_resize = self.create_sidebar_button("Data Resize", icon_resize, icon_resize_selected, self.app.tab_management.show_resize)
        self.btn_windowing = self.create_sidebar_button("Windowing", icon_windowing, icon_windowing_selected, self.app.tab_management.show_windowing)
        self.btn_charact = self.create_sidebar_button("Characteristic", icon_charact, icon_charact_selected, self.app.tab_management.show_charact)
        self.btn_save = self.create_sidebar_button("Save", icon_save, icon_save_selected, self.app.tab_management.show_save)

    def create_sidebar_button(self, text, icon, icon_selected, command):
        """Helper para criar um botão da barra lateral."""
        button = ctk.CTkButton(
            self.frame_sidebar, text=text, image=icon, command=lambda: self.select_button(button, command, icon_selected, icon),
            fg_color="transparent", hover_color=HOVER_COLOR, font=BUTTON_FONT,
            text_color=BUTTON_TEXT_COLOR, compound="left", anchor="w"
        )
        button.pack(pady=10, padx=10, fill="x")
        return button

    def select_button(self, button, command, icon_selected, icon_unselected):
        """Seleciona um botão e executa o comando associado."""
        if hasattr(self, 'selected_button'):
            self.selected_button.configure(text_color=BUTTON_TEXT_COLOR, image=self.selected_button_unselected_icon)
        button.configure(text_color=BUTTON_SELECTED_TEXT_COLOR, image=icon_selected)
        self.selected_button = button
        self.selected_button_unselected_icon = icon_unselected
        command()

    def toggle_sidebar(self):
        """Alterna o estado da barra lateral entre expandida e encolhida."""
        if  self.sidebar_expanded:
            self.frame_sidebar.configure(width=SIDEBAR_WIDTH_COLLAPSED)
            self.toggle_button.configure(image=icon_toggle_closed)
            self.btn_home.configure(text="", width=SIDEBAR_WIDTH_COLLAPSED)
            self.btn_upload.configure(text="", width=SIDEBAR_WIDTH_COLLAPSED)
            self.btn_sync.configure(text="", width=SIDEBAR_WIDTH_COLLAPSED)
            self.btn_processing.configure(text="", width=SIDEBAR_WIDTH_COLLAPSED)
            self.btn_resize.configure(text="", width=SIDEBAR_WIDTH_COLLAPSED)
            self.btn_windowing.configure(text="", width=SIDEBAR_WIDTH_COLLAPSED)
            self.btn_charact.configure(text="", width=SIDEBAR_WIDTH_COLLAPSED)
            self.btn_save.configure(text="", width=SIDEBAR_WIDTH_COLLAPSED)
            self.footer_label.configure(image="")
        else:
            self.frame_sidebar.configure(width=SIDEBAR_WIDTH_EXPANDED)
            self.toggle_button.configure(image=icon_toggle_open)
            self.btn_home.configure(text="Home", width=SIDEBAR_WIDTH_EXPANDED)
            self.btn_upload.configure(text="Upload files", width=SIDEBAR_WIDTH_EXPANDED)
            self.btn_sync.configure(text="Synchronization", width=SIDEBAR_WIDTH_EXPANDED)
            self.btn_processing.configure(text="Processing", width=SIDEBAR_WIDTH_EXPANDED)
            self.btn_resize.configure(text="Data Resize", width=SIDEBAR_WIDTH_EXPANDED)
            self.btn_windowing.configure(text="Windowing", width=SIDEBAR_WIDTH_EXPANDED)
            self.btn_charact.configure(text="Characteristic", width=SIDEBAR_WIDTH_EXPANDED)
            self.btn_save.configure(text="Save", width=SIDEBAR_WIDTH_EXPANDED)
            self.footer_label.configure(image=footer_image)

        self.frame_sidebar.update_idletasks()
        self.sidebar_expanded = not getattr(self, 'sidebar_expanded', True)