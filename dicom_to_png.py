#!/usr/bin/env python3

from config import Config
import dicom_parser

if __name__ == "__main__":
    conf = Config()
    dicom_parser.dump_pngs(dicom_directory=conf.in_dir,
                           output_directory=conf.out_dir,
                           title=conf.title,
                           text=conf.text)