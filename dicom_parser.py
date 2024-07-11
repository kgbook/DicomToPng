import SimpleITK as sitk
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from dicom_info import DicomInfo
from config import Font
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
def dump_pngs(output_directory: str, dicom_directory: str, title: Font, text: Font):
    # 读取DICOM序列
    reader = sitk.ImageSeriesReader()
    series_ids = reader.GetGDCMSeriesIDs(dicom_directory)
    if not series_ids:
        print("No DICOM series found in the directory.")
        return
    print(f"Found {len(series_ids)} DICOM series in the directory.")

    for series_id in series_ids:
        # 获取当前序列ID的所有文件名
        series_file_names = reader.GetGDCMSeriesFileNames(dicom_directory, series_id)
        reader.SetFileNames(series_file_names)
        image_array = reader.Execute()
        series_array = sitk.GetArrayFromImage(image_array)

        # 读取序列中的第一个文件来获取窗宽窗位
        first_image = sitk.ReadImage(series_file_names[0])
        series_info = DicomInfo(first_image)
        print(f"{series_info.__dict__}")
        for i in range(series_array.shape[0]):
            # print(f"Processing file {i} of {len(series_file_names)}, {series_file_names[i]}")
            slice = series_array[i, :, :]
            windowed_slice = apply_window_level(slice, series_info.window_width,
                                                series_info.window_center)
            out_basename = os.path.basename(os.path.splitext(series_file_names[i])[0]) + ".png"
            out_dirname = f"{output_directory}/{series_info.series_name}"
            if not os.path.exists(out_dirname):
                os.makedirs(out_dirname)
            output_file_path = f"{out_dirname}/{out_basename}"
            Image.fromarray(windowed_slice).save(output_file_path)
            add_text_to_image(out_img=output_file_path, in_img=output_file_path,conf=title,ctx=series_info.patient_name, position=(10, 10))
            add_text_to_image(out_img=output_file_path, in_img=output_file_path,conf=text,ctx=series_info.patient_id, position=(10, 30))
            add_text_to_image(out_img=output_file_path, in_img=output_file_path, conf=text,ctx=f'{series_info.patient_birthday}, {series_info.patient_sex}, {series_info.patient_age}', position=(10, 45))
            add_text_to_image(out_img=output_file_path, in_img=output_file_path, conf=text,ctx=f'{series_info.study_date}{series_info.study_time}',position=(10, 70))