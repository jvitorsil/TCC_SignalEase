import pandas as pd
import scipy.io as sio

class EMGData:
    def __init__(self, file_path, data, time, sampling_rate, duration, active_channels, aux_channels, metadata):
        self.file_path = file_path.split('/')[-1]  # Caminho do arquivo
        self.data = data  # DataFrame contendo os dados
        self.time = time
        self.sampling_rate = sampling_rate  # Frequência de amostragem
        self.duration = duration  # Duração da coleta
        self.active_channels = active_channels  # Canais ativos (números)
        self.aux_channels = aux_channels  # Canais auxiliares (números)
        self.metadata = metadata  # Outros metadados (ex: informações de cada canal)

    def __str__(self):
        return f"EMGData from {self.file_path} with {len(self.active_channels)} active channels."

# Dicionário para armazenar os conjuntos de dados carregados
data_sets = {}