from adl.core.registries import Plugin


class PluginNamePlugin(Plugin):
    type = "adl_bouy_sc_ftp_decoder"
    label = "ADL Bouy SC FTP Decoder"
    
    def get_urls(self):
        return []
    
    def get_station_data(self, station_link, start_date=None, end_date=None):
        return []
