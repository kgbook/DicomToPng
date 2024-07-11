#!/usr/bin/env python3
import configparser

class Font:
    def __init__(self, font: str, fontsize: int, color: str):
        self.font = font
        self.size = fontsize
        self.color = color

class Config:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.in_dir = self.config['dcom']['dir']
        self.out_dir = self.config['png']['dir']
        font = self.config['font']['font']
        fontcolor = self.config['font']['color']
        fontsize = int(self.config['font']['title_fontsize'])
        self.title = Font(font, fontsize, fontcolor)
        fontsize = int(self.config['font']['text_fontsize'])
        self.text = Font(font, fontsize, fontcolor)