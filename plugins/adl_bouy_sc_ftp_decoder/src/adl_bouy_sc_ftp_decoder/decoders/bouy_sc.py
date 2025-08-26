import logging

import pandas as pd
from adl_ftp_plugin.registries import FTPDecoder
from django.utils import timezone as dj_timezone

logger = logging.getLogger(__name__)

HEADER = {
    "obs_time": "Observation Time",
    "tp": "the peak period (the reciprocal of the peak frequency) [s]",
    "dirp": "the wave direction at the peak frequency [°]",
    "sprp": "the directional spread at the peak frequency [°]",
    "tz": "the zero-upcross period [s]",
    "hs": "the significant wave height [cm]",
    "ti": "the integral period, or Tm(-2,0) [s]",
    "t1": "the mean period, or Tm(0,1) [s]",
    "tc": "the crest period, or Tm(2,4) [s]",
    "tdw2": "wave period Tm(-1,1) [s]",
    "tdw1": "peak period estimator [s]",
    "tpc": "calculated peak period [s]",
    "nu": "Longuet-Higgins bandwidth parameter []",
    "eps": "bandwidth parameter []",
    "qp": "Goda's peakedness parameter []",
    "ss": "significant steepness []",
    "tref": "reference temperature []",
    "tsea": "Sea surface temperature",
    "bat": "battery status",
}


class BouySCDecoder(FTPDecoder):
    type = "bouy_sc"
    compat_type = "bouy_sc"
    display_name = "Bouy Decoder - Seychelles"
    
    def get_matching_files(self, station_link, files):
        # get all the initial matching files
        matching_files = super().get_matching_files(station_link, files)
        
        if station_link.start_date:
            return matching_files
        
        timezone = station_link.timezone
        
        # sample file name Seychelles}2025-08.his. Here 08 is the month of the year
        # we only want the files that contain the date of today in the name
        zero_padded_this_month = [
            f"{dj_timezone.localtime(timezone=timezone).year}-{str(dj_timezone.now().month).zfill(2)}"]
        matching_files = [file for file in matching_files if any(date in file for date in zero_padded_this_month)]
        
        return matching_files
    
    def decode(self, file_path):
        """
        This method decodes the Seychelles Bouy Data.
        
        :param file_path: The path to the file to decode.
        :return: A dictionary containing the decoded data.
        """
        
        # sample file
        # History file
        # 2025-08-01T07:31:59.999Z,15.38,191.3,37.7,7.143,274.0,11.09,8.23,3.86,9.19,11.05,14.94,0.584,0.840,1.59,3.441E-2,25.00,25.80,0
        
        # Use the HEADER keys as the CSV columns
        col_names = list(HEADER.keys())
        
        # Read CSV without a header, assign our colnames
        df = pd.read_csv(file_path, header=None, names=col_names)
        
        # Parse time column as datetime
        df["obs_time"] = pd.to_datetime(df["obs_time"])
        
        records = df.to_dict(orient="records", )
        
        return {
            "values": records
        }
