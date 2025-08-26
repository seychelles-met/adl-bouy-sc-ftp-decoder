from adl_ftp_plugin.registries import ftp_decoder_registry
from django.apps import AppConfig


class BouySCDecoderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = "adl_bouy_sc_ftp_decoder"
    
    def ready(self):
        from .decoders import BouySCDecoder
        
        ftp_decoder_registry.register(BouySCDecoder())
