from typing import List
import SimpleITK as sitk
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from dicom_info import DicomInfo
from config import Font
from series_info import SeriesInfo
import os.path

def apply_window_level(image_array, window_width, window_center):
    """
    应用窗宽窗位调整图像亮度和对比度。
    """
    img_min = window_center - window_width / 2
    img_max = window_center + window_width / 2
    windowed_img = np.clip(image_array, img_min, img_max)
    windowed_img = (windowed_img - img_min) / (img_max - img_min) * 255.0
    return windowed_img.astype(np.uint8)
def add_text_to_image(out_img: str, in_img: str, ctx: str, position: tuple[int, int], conf: Font):
    image = Image.open(in_img)
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype(conf.font, conf.size)
    except IOError:
        font = ImageFont.load_default()
    draw.text(position, ctx, font=font, fill=conf.color)
    image.save(out_img)

def dump_pngs(output_directory: str, dicom_directory: str, title: Font, text: Font) -> dict[str, SeriesInfo] :
    # 读取DICOM序列
    reader = sitk.ImageSeriesReader()
    series_ids = reader.GetGDCMSeriesIDs(dicom_directory)
    if not series_ids:
        print("No DICOM series found in the directory.")
        return
    print(f"Found {len(series_ids)} DICOM series in the directory.")

    series_info_dict : dict[str, SeriesInfo] = {}
    for series_id in series_ids:
        series_file_names = reader.GetGDCMSeriesFileNames(dicom_directory, series_id)
        reader.SetFileNames(series_file_names)
        image_array = reader.Execute()
        series_array = sitk.GetArrayFromImage(image_array)

        first_image = sitk.ReadImage(series_file_names[0])
        first_dcm_info = DicomInfo(first_image)
        png_files : List[str] = []
        for i in range(series_array.shape[0]):
            slice = series_array[i, :, :]
            windowed_slice = apply_window_level(slice, first_dcm_info.window_width,
                                                first_dcm_info.window_center)
            out_basename = os.path.basename(os.path.splitext(series_file_names[i])[0]) + ".png"
            out_dirname = f"{output_directory}/{first_dcm_info.series_name}".replace(' ', '')
            if not os.path.exists(out_dirname):
                os.makedirs(out_dirname)
            output_file_path = f"{out_dirname}/{out_basename}"
            Image.fromarray(windowed_slice).save(output_file_path)
            png_files.append(output_file_path)

            if 'T2_Images' in first_dcm_info.series_name:
                continue
            add_text_to_image(out_img=output_file_path, in_img=output_file_path,conf=title,ctx=first_dcm_info.patient_name, position=(5, 10))
            add_text_to_image(out_img=output_file_path, in_img=output_file_path,conf=text,ctx=first_dcm_info.patient_id, position=(5, 30))
            add_text_to_image(out_img=output_file_path, in_img=output_file_path, conf=text,ctx=f'{first_dcm_info.patient_birthday}, {first_dcm_info.patient_sex}, {first_dcm_info.patient_age}', position=(5, 45))
            add_text_to_image(out_img=output_file_path, in_img=output_file_path, conf=text,ctx=f'{first_dcm_info.study_date} {first_dcm_info.study_time}',position=(5, 70))
            add_text_to_image(out_img=output_file_path, in_img=output_file_path, conf=text,ctx=f'图像: {i}/{len(series_file_names)}', position=(5, 85))
            add_text_to_image(out_img=output_file_path, in_img=output_file_path, conf=text, ctx=f'序列: {first_dcm_info.series_number}', position=(5, 100))
            add_text_to_image(out_img=output_file_path, in_img=output_file_path, conf=text, ctx=first_dcm_info.series_name, position=(5, first_dcm_info.image_height - 75))
            add_text_to_image(out_img=output_file_path, in_img=output_file_path, conf=text, ctx=f'TR:{first_dcm_info.TR}', position=(5, first_dcm_info.image_height - 60))
            add_text_to_image(out_img=output_file_path, in_img=output_file_path, conf=text, ctx=f'TE:{first_dcm_info.TE}',position=(5, first_dcm_info.image_height - 45))
            add_text_to_image(out_img=output_file_path, in_img=output_file_path, conf=text, ctx=f'TP:{first_dcm_info.TP}', position=(5, first_dcm_info.image_height - 30))
            add_text_to_image(out_img=output_file_path, in_img=output_file_path, conf=text, ctx=f'SP:{first_dcm_info.SP}', position=(5, first_dcm_info.image_height - 15))
        series_info_dict[first_dcm_info.series_name] = SeriesInfo(series_meta=first_dcm_info, png_files=png_files)
    return series_info_dict