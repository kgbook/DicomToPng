#!/usr/bin/env python3

from config import Config
from series_info import SeriesInfo
import dicom_parser

if __name__ == "__main__":
    conf = Config()
    series_dict = dicom_parser.dump_pngs(dicom_directory=conf.in_dir,
                           output_directory=conf.out_dir,
                           title=conf.title,
                           text=conf.text)
    print('\n')
    if isinstance(series_dict, dict):
        for key, value in series_dict.items():
            print(f"{key}:")
            if isinstance(value, SeriesInfo):
                print(f"{value.series_meta.__dict__}")
                for png_file in value.png_files:
                    print(f"PNG File: {png_file}")
            print("---")