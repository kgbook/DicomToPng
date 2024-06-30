#!/usr/bin/env python3

from config import Config
import DicomParser

if __name__ == "__main__":
    conf = Config()
    DicomParser.dump_pngs(conf.in_dir, conf.out_dir)