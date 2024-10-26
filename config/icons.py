from config.settings import *
from modules.utils import create_icon
import os

# Caminho base para as imagens
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

footer_image = create_icon(os.path.join(base_path, "images", "SignalEase.png"), (49, 160, 250), (75, 75))
logo_image = create_icon(os.path.join(base_path, "images", "SignalEase.png"), (200, 200, 200), (300, 300))

icon_toggle_closed = create_icon(os.path.join(base_path, "images", "menu.png"), (100, 113, 124), (30, 30))
icon_toggle_open = create_icon(os.path.join(base_path, "images", "menu_open.png"), (100, 113, 124), (30, 30))

icon_home = create_icon(os.path.join(base_path, "images", "home.png"), (100, 113, 124), (30, 30))
icon_upload_file = create_icon(os.path.join(base_path, "images", "upload_file.png"), (100, 113, 124), (30, 30))
icon_sync = create_icon(os.path.join(base_path, "images", "sync.png"), (100, 113, 124), (30, 30))
icon_processing = create_icon(os.path.join(base_path, "images", "timeline.png"), (100, 113, 124), (30, 30))
icon_resize = create_icon(os.path.join(base_path, "images", "resize.png"), (100, 113, 124), (30, 30))
icon_windowing = create_icon(os.path.join(base_path, "images", "windowing.png"), (100, 113, 124), (30, 30))
icon_charact = create_icon(os.path.join(base_path, "images", "characteristics.png"), (100, 113, 124), (30, 30))
icon_save = create_icon(os.path.join(base_path, "images", "save.png"), (100, 113, 124), (30, 30))

icon_home_selected = create_icon(os.path.join(base_path, "images", "home.png"), (49, 160, 250), (30, 30))
icon_upload_file_selected = create_icon(os.path.join(base_path, "images", "upload_file.png"), (49, 160, 250), (30, 30))
icon_sync_selected = create_icon(os.path.join(base_path, "images", "sync.png"), (49, 160, 250), (30, 30))
icon_processing_selected = create_icon(os.path.join(base_path, "images", "timeline.png"), (49, 160, 250), (30, 30))
icon_resize_selected = create_icon(os.path.join(base_path, "images", "resize.png"), (49, 160, 250), (30, 30))
icon_windowing_selected = create_icon(os.path.join(base_path, "images", "windowing.png"), (49, 160, 250), (30, 30))
icon_charact_selected = create_icon(os.path.join(base_path, "images", "characteristics.png"), (49, 160, 250), (30, 30))
icon_save_selected = create_icon(os.path.join(base_path, "images", "save.png"), (49, 160, 250), (30, 30))