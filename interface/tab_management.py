import customtkinter as ctk
from tkinter import filedialog, Listbox, MULTIPLE, SINGLE, ttk, font
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from config.settings import *
from config.icons import *
from modules.utils import *
from modules.data_loader import *
import os

class TabManagement:
    def __init__(self, app):
        self.app = app
        self.frame_main = ctk.CTkFrame(app.root, fg_color=MAIN_COLOR, corner_radius=20)
        self.frame_main.grid(row=0, column=1, sticky="nsew")

        self.data_loader = DataLoader(self)  # Cria uma instância do DataLoader, passando o TabManagement como referência

        # Armazena o estado dos arquivos carregados
        self.loaded_eeg_files = []
        self.loaded_emg_files = []
        self.loaded_aux_files = []


        # Dicionários para armazenar as listas de canais e gráficos por aba
        self.channel_listboxes = {}
        self.figures = {}
        self.axs = {}
        self.canvases = {}

        self.show_home()

    def limpar_frame_main(self):
        """Remove todos os widgets do frame principal."""
        for widget in self.frame_main.winfo_children():
            widget.destroy()

    def show_home(self):
        """Mostra a interface inicial no frame principal."""
        self.limpar_frame_main()
        logo_label = ctk.CTkLabel(self.frame_main, image=logo_image, text="")
        logo_label.image = logo_image  # Manter uma referência da imagem para evitar que seja coletada pelo garbage collector
        logo_label.pack(side="top", pady=100)

    def show_upload(self):
        """Configura as abas e botões de upload."""
        self.limpar_frame_main()
        self.tabview = self.create_tabview()

        # Criar textboxes e botões para cada aba
        self.treeview_eeg = self.create_treeview(self.tabview, "EEG")
        self.treeview_emg = self.create_treeview(self.tabview, "EMG")
        self.treeview_aux = self.create_treeview(self.tabview, "AUX")

        self.update_treeview(self.treeview_eeg, self.loaded_eeg_files)
        self.update_treeview(self.treeview_emg, self.loaded_emg_files)
        self.update_treeview(self.treeview_aux, self.loaded_aux_files)

        self.create_button_frame(self.tabview.tab("EEG"), self.data_loader.load_eeg_data, self.delete_selected_eeg)
        self.create_button_frame(self.tabview.tab("EMG"), self.data_loader.load_emg_data, self.delete_selected_emg)
        self.create_button_frame(self.tabview.tab("AUX"), self.data_loader.load_aux_data, self.delete_selected_aux)

        self.create_graph_area(self.tabview.tab("EEG"), "EEG")
        self.create_graph_area(self.tabview.tab("EMG"), "EMG")
        self.create_graph_area(self.tabview.tab("AUX"), "AUX")

    def update_treeview(self, treeview, items):
        """Atualiza o treeview com os itens fornecidos."""
        for item in treeview.get_children():
            treeview.delete(item)
        for emg_data in items:
            treeview.insert("", "end", values=(emg_data.file_path, str(emg_data.sampling_rate) + " Hz", str(emg_data.duration) + " seg", emg_data.active_channels, emg_data.aux_channels))

    def create_treeview(self, tabview, tab_name):
        """Cria um treeview para exibir arquivos carregados."""
        columns = ("file_name", "sampling_rate", "duration", "active_channels", "aux_channels")
        treeview = ttk.Treeview(tabview.tab(tab_name), columns=columns, show="headings", height=8)
        treeview.heading("file_name", text="File Name")
        treeview.heading("sampling_rate", text="Sampling Rate")
        treeview.heading("duration", text="Duration")
        treeview.heading("active_channels", text="Active Channels")
        treeview.heading("aux_channels", text="Aux Channels")

        # Centralizar os valores nas colunas
        for col in columns:
            treeview.column(col, anchor="center", width=100)

        # Definir a fonte e o tamanho da letra
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Helvetica", 14, "bold"), foreground="#797E82", selectbackground=BUTTON_TEXT_COLOR_UPLOAD)
        style.configure("Treeview", font=("Helvetica", 12), foreground="#797E82", selectbackground=BUTTON_TEXT_COLOR_UPLOAD)

        treeview.pack(side="top", padx=5, pady=5, fill="both")
        treeview.bind("<<TreeviewSelect>>", self.on_file_select)

        return treeview
    
    def create_button_frame(self, parent, upload_command, delete_command):
        """Cria um frame para conter os botões de upload e delete."""
        button_frame = ctk.CTkFrame(parent, fg_color=MAIN_COLOR)
        button_frame.pack(side="bottom", fill="x", padx=0, pady=0)

        self.create_upload_button(button_frame, "Upload File", upload_command)
        self.create_delete_button(button_frame, "Delete Selected", delete_command)

    def create_upload_button(self, parent, text, command):
        """Cria um botão para upload de arquivos."""
        button = ctk.CTkButton(parent, text=text, command=command, font=BUTTON_FONT_UPLOAD, text_color=BUTTON_TEXT_COLOR_UPLOAD)
        button.pack(side="right", padx=10, pady=5, ipadx=5, ipady=5)

    def create_delete_button(self, parent, text, command):
        """Cria um botão para deletar arquivos selecionados."""
        button = ctk.CTkButton(parent, text=text, command=command, font=BUTTON_FONT_UPLOAD, text_color=BUTTON_TEXT_COLOR_UPLOAD)
        button.pack(side="right",  fill="both", padx=10, pady=5, ipadx=5, ipady=5)

    def create_tabview(self):
        """Cria um TabView para gerenciar diferentes abas de dados."""
        tabview = ctk.CTkTabview(self.frame_main, corner_radius=15, fg_color=MAIN_COLOR)
        tabview.pack(expand=True, fill="both", pady=20)
        tabview.add("EMG")
        tabview.add("EEG")
        tabview.add("AUX")
        return tabview

    def create_graph_area(self, parent, tab_name):
        """Cria a área de gráfico e a lista de canais para uma aba específica."""
        frame_graph = ctk.CTkFrame(parent, fg_color=MAIN_COLOR)
        frame_graph.pack(side="top", fill="both", expand=True, padx=0, pady=0)

        # Criação da figura e gráfico
        figure = Figure(figsize=(9, 2), dpi=100)
        figure.patch.set_facecolor('#EBEBEB')
        ax = figure.add_subplot(111)
        ax.set_facecolor('#FFFFFF')

        # Adicionar rótulos nos eixos
        ax.set_xlabel("Tempo (s)", fontsize=10, labelpad=10, color='#797E82')  # Legenda do eixo X
        ax.set_ylabel("Amplitude (mV)", fontsize=10, labelpad=10, color='#797E82')  # Legenda do eixo Y
        
        # Estilizar o grid
        ax.grid(True, linestyle='--', linewidth=0.7, color='#d3d3d3')  # Adiciona grid com linhas pontilhadas

        # Estilizar os ticks (marcadores nos eixos)
        ax.tick_params(axis='x', colors='#797E82', labelsize=10)  # Cor e tamanho da fonte dos rótulos do eixo X
        ax.tick_params(axis='y', colors='#797E82', labelsize=10)  # Cor e tamanho da fonte dos rótulos do eixo Y

        # Adicionar título ao gráfico (opcional)
        ax.set_title("Sinal " + str(tab_name), fontsize=14, color='#797E82', pad=15, fontweight='bold')

        canvas = FigureCanvasTkAgg(figure, master=frame_graph)
        canvas.draw()
        canvas.get_tk_widget().pack(side="left", fill="both", expand= True, anchor='w')

        # Armazenar a figura, ax e canvas para referência futura
        self.figures[tab_name] = figure
        self.axs[tab_name] = ax
        self.canvases[tab_name] = canvas

        # Criação da Listbox de canais
        listbox = Listbox(master=frame_graph, selectmode=SINGLE, height= 5, width= 25,foreground="#797E82", selectbackground=BUTTON_SELECTED_TEXT_COLOR, selectforeground="white")
        listbox.pack(side="right", fill="both", padx=10, pady=80)
        listbox.bind("<<ListboxSelect>>", self.on_channel_select)

        custom_font = ("Helvetica", 14, "bold")
        listbox.config(font=custom_font)


        # Armazenar a Listbox para referência futura
        self.channel_listboxes[tab_name] = listbox

    def on_file_select(self, event):
        selected_item = event.widget.selection()[0]
        file_name = event.widget.item(selected_item, "values")[0]

        # Determina qual aba está ativa (EEG, EMG ou AUX)
        tab_name = self.get_active_tab_name()
        emg_data = next((data for data in self.loaded_emg_files if os.path.basename(data.file_path) == file_name), None)

        if emg_data:
            listbox = self.channel_listboxes[tab_name]
            listbox.delete(0, 'end')  # Limpa a Listbox

            # Adiciona os canais ao Listbox da aba ativa
            for channel_name in emg_data.data.columns:
                listbox.insert('end', channel_name)
                print(channel_name)
        else:
            print(f"Nenhum dado encontrado para o arquivo: {file_name}")

    def on_channel_select(self, event):
        """Plota os dados dos canais selecionados no gráfico da aba ativa."""
        print("*************** Channel selected ***************************")

        tab_name = self.get_active_tab_name()
        listbox = self.channel_listboxes[tab_name]
        selected_indices = listbox.curselection()
        selected_channels = [listbox.get(i) for i in selected_indices]

        emg_data = next((data for data in self.loaded_emg_files if os.path.basename(data.file_path) == self.treeview_emg.item(self.treeview_emg.selection()[0], "values")[0]), None)

        if emg_data:
            ax = self.axs[tab_name]
            ax.clear()  # Limpa o gráfico

            # Reaplica as configurações de estilo do gráfico após limpar
            ax.set_facecolor('#FFFFFF')
            ax.set_xlabel("Tempo (s)", fontsize=10 , labelpad=10, color='#797E82')
            ax.set_ylabel("Amplitude (mV)", fontsize=10, labelpad=10, color='#797E82')
            ax.grid(True, linestyle='--', linewidth=0.7, color='#d3d3d3')
            ax.tick_params(axis='x', colors='#797E82', labelsize=10)
            ax.tick_params(axis='y', colors='#797E82', labelsize=10)
            ax.set_title("Sinal " + str(tab_name), fontsize=14, color='#797E82', pad=15, fontweight='bold')

            # Plota os canais selecionados
            for channel in selected_channels:
                if channel in emg_data.data.columns:
                    ax.plot(emg_data.time, emg_data.data[channel], label=channel)
            
            # Adiciona a legenda apenas se houver algum canal plotado
            if selected_channels:
                ax.legend()

            # Redesenha o canvas para refletir as alterações
            self.canvases[tab_name].draw()

    def get_active_tab_name(self):
        """Retorna o nome da aba ativa no TabView."""
        # Acesse o TabView e obtenha a aba ativa.
        # Aqui assumimos que 'self.tabview' é a instância do seu TabView.
        return self.tabview.get()

    def add_loaded_eeg_file(self, file_path):
        """Adiciona um arquivo EEG carregado à lista e atualiza a textbox."""
        self.loaded_eeg_files.append(file_path)

        self.update_treeview(self.treeview_eeg, self.loaded_eeg_files)

    def add_loaded_emg_file(self, file_path):
        """Adiciona um arquivo EMG carregado à lista e atualiza a textbox."""

        self.loaded_emg_files.extend(file_path)

        print(self.loaded_emg_files)

        for emg_data in self.loaded_emg_files:
            print(f"File Path: {emg_data.file_path}")
            print(f"Sampling Rate: {emg_data.sampling_rate}")
            print(f"Duration: {emg_data.duration}")
            print(f"Active Channels: {emg_data.active_channels}")
            print(f"Aux Channels: {emg_data.aux_channels}")
            print(f"Metadata: {emg_data.metadata}")
            print(f"Data: {emg_data.data[:5]}")  # Exemplo: imprime as primeiras 5 linhas de dados
        
        self.update_treeview(self.treeview_emg, self.loaded_emg_files)

    def add_loaded_aux_file(self, file_path):
        """Adiciona um arquivo AUX carregado à lista e atualiza a textbox."""
        self.loaded_aux_files.append(file_path)
        self.update_treeview(self.treeview_aux, self.loaded_aux_files)

    def delete_selected_eeg(self):
        """Deleta os arquivos EEG selecionados."""
        selected_indices = self.treeview_eeg.curselection()
        for index in reversed(selected_indices):
            del self.loaded_eeg_files[index]
        self.update_treeview(self.treeview_eeg, self.loaded_eeg_files)

    def delete_selected_emg(self):
        """Deleta os arquivos EMG selecionados."""
        selected_items = self.treeview_emg.selection()  # Use selection() para obter os itens selecionados
        selected_file_names = [self.treeview_emg.item(item, 'values')[0] for item in selected_items]

        # Remover os itens selecionados da lista loaded_emg_files
        self.loaded_emg_files = [emg_data for emg_data in self.loaded_emg_files if os.path.basename(emg_data.file_path) not in selected_file_names]

        # Deletar os itens selecionados do Treeview
        for item in selected_items:
            self.treeview_emg.delete(item)

        # Atualizar o Treeview
        self.update_treeview(self.treeview_emg, self.loaded_emg_files)

    def delete_selected_aux(self):
        """Deleta os arquivos AUX selecionados."""
        selected_indices = self.treeview_aux.curselection()
        for index in reversed(selected_indices):
            del self.loaded_aux_files[index]
        self.update_treeview(self.treeview_aux, self.loaded_aux_files)

    def show_sync(self):
        """Mostra a interface da Opção 3 no frame principal."""
        self.limpar_frame_main()
        label = ctk.CTkLabel(self.frame_main, text="Pagina de Syncronização dos dados", text_color="black")
        label.pack(pady=20)

    def show_processing(self):
        """Mostra a interface da Opção 3 no frame principal."""
        self.limpar_frame_main()
        label = ctk.CTkLabel(self.frame_main, text="Pagina de Processamento dos dados", text_color="black")
        label.pack(pady=20)

    def show_resize(self):
        """Mostra a interface da Opção 3 no frame principal."""
        self.limpar_frame_main()
        label = ctk.CTkLabel(self.frame_main, text="Pagina de Reamostragem dos dados", text_color="black")
        label.pack(pady=20)
        
    def show_windowing(self):
        """Mostra a interface da Opção 3 no frame principal."""
        self.limpar_frame_main()
        label = ctk.CTkLabel(self.frame_main, text="Pagina de Janelamento dos dados", text_color="black")
        label.pack(pady=20)

    def show_charact(self):
        """Mostra a interface da Opção 3 no frame principal."""
        self.limpar_frame_main()
        label = ctk.CTkLabel(self.frame_main, text="Pagina de extração de caracteristicas", text_color="black")
        label.pack(pady=20)

    def show_save(self):
        """Mostra a interface da Opção 3 no frame principal."""
        self.limpar_frame_main()
        label = ctk.CTkLabel(self.frame_main, text="Pagina de Organização e Salvamento dos dados", text_color="black")
        label.pack(pady=20)