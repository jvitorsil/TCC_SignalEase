from PIL import Image

import customtkinter as ctk

def change_icon_color(image_path, color):
    """Altera a cor de um ícone PNG."""
    image = Image.open(image_path).convert("RGBA")
    data = image.getdata()
    
    new_data = []
    for item in data:
        if item[3] > 0:  # Apenas altera pixels não transparentes
            new_data.append((color[0], color[1], color[2], item[3]))
        else:
            new_data.append(item)
    
    image.putdata(new_data)
    return image


def create_icon(path, color, size):
    """Helper para criar ícones coloridos e redimensionados."""
    return ctk.CTkImage(change_icon_color(path, color).resize(size), size=size)
