from django.apps import AppConfig
from doc_classification import loading_cnn_model

cnn_model = None

max_file_size = 1024 * 1024 * 10


class AnalysisConfig(AppConfig):
    name = 'analysis'

    def ready(self):
        global cnn_model
        cnn_model = loading_cnn_model()
