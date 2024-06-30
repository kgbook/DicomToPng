#!/usr/bin/env python3
import configparser

class Config:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.in_dir = self.config['dcom']['dir']
        self.out_dir = self.config['png']['dir']