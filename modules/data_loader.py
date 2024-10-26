# modules/data_loader.py
import pandas as pd
from tkinter import filedialog
from modules.emg_data import EMGData
import scipy.io as sio
import numpy as np

class DataLoader:
    def __init__(self, tab_manager):
        self.tab_manager = tab_manager
        self.data_sets = {}  # Dicionário para armazenar todos os conjuntos de dados carregados

    def load_file(self, file_path):
        """Carrega um arquivo de dados e retorna um objeto EMGData."""
        file_extension = file_path.split('.')[-1].lower()
        metadata = {}
        data = None 

        try:
            if file_extension == 'csv':
                data = pd.read_csv(file_path)
                metadata['tipo'] = 'csv'

            elif file_extension == 'txt':
                with open(file_path, 'r', encoding='latin1') as file:
                    lines = file.readlines()
                metadata = self.extract_metadata_txt(lines)

                # Cabeçalho das colunas com nomes dos canais ativos e auxiliares
                column_names = [f'EMG_{channel}' for channel in metadata['active_channels']] + \
                            [f'AUX_{channel}' for channel in metadata['aux_channels']]
                
                data = pd.DataFrame(self.extract_data_txt(lines, metadata))
                data.columns = column_names

            elif file_extension == 'mat':
                mat_data = sio.loadmat(file_path)
                data = pd.DataFrame(mat_data['variavel_de_interesse'])  # Ajuste a chave conforme necessário
                metadata['tipo'] = 'mat'

            else:
                print("Formato de arquivo não suportado.")
                return None
        except Exception as e:
            print(f"Erro ao carregar o arquivo {file_path}: {e}")
            return None

        sampling_rate = metadata.get('sampling_rate', 2000)
        duration = metadata.get('duration', len(data) / sampling_rate)
        active_channels = metadata.get('active_channels', [])
        aux_channels = metadata.get('aux_channels', [])
        n_samples = metadata.get('nSamples', 1)
        time = np.linspace(0, duration, n_samples)

        # Criar um objeto EMGData e armazená-lo
        data_set = EMGData(file_path, data, time, sampling_rate, duration, active_channels, aux_channels, metadata)
        self.data_sets[file_path] = data_set

        print(f"Arquivo {file_path} carregado com sucesso!")

        return data_set

    def extract_metadata_txt(self, lines):
        """Extrai metadados de arquivos .txt."""
        metadata = {
            'nSamples': 0,
            'num_active_channels': 0,
            'sampling_rate': 0,
            'duration': 0,
            'active_channels': [],
            'aux_channels': []
        }

        for line in lines:
            if '[Número de amostras por canal]' in line:
                metadata['nSamples'] = int(float(line.split(' = ')[1].strip()))
            if '[Taxa de amostragem por canal]' in line:
                metadata['sampling_rate'] = int(line.split(' = ')[1].strip().replace(' Hz', ''))
            if '[Duração]' in line:
                metadata['duration'] = float(line.split(' = ')[1].strip().replace(' seg', ''))
            if '[Número de canais]' in line:
                metadata['num_active_channels'] = int(line.split(' = ')[1].strip())
            if '[Canais utilizados]' in line:
                channels_str = line.split(' = ')[1].strip()
                for channel in channels_str.split():
                    channel_int = int(channel)
                    if channel_int <= 8:
                        metadata['active_channels'].append(channel_int)
                    elif channel_int > 8:
                        metadata['aux_channels'].append(channel_int)
        
        print(f"Metadados extraídos: {metadata}")
        return metadata


    def extract_data_txt(self, lines, metadata):
        """Extrai dados de arquivos .txt a partir das linhas e metadados fornecidos."""
        data_section = False
        data = []

        for line in lines:
            if data_section and line.strip() != '':
                data.append([float(value) for value in line.strip().split('\t')])
            if '[Dados]' in line:
                data_section = True

        return data


    def load_eeg_data(self):
        """Carrega e exibe dados EEG."""
        file_path = filedialog.askopenfilename(filetypes=[("Arquivos CSV", "*.csv")])
        if file_path:
            data_set = self.load_file(file_path)
            if data_set:
                self.tab_manager.add_loaded_eeg_file(file_path)  # Atualiza a lista e a textbox de EEG


    def load_emg_data(self):
        """Carrega e exibe dados EMG."""
        file_paths = filedialog.askopenfilenames(filetypes=[("Todos os arquivos", "*.csv *.txt *.mat")])
        if file_paths:
            data_sets = [self.load_file(path) for path in file_paths if self.load_file(path)]
            self.tab_manager.add_loaded_emg_file(data_sets)  # Atualiza a lista e a textbox de EMG


    def load_aux_data(self):
        """Carrega e exibe dados AUX."""
        file_path = filedialog.askopenfilename(filetypes=[("Todos os arquivos", "*.csv *.txt *.mat")])
        if file_path:
            data_set = self.load_file(file_path)
            if data_set:
                self.tab_manager.add_loaded_aux_file(file_path)  # Atualiza a lista e a textbox de AUX
