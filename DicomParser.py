import SimpleITK as sitk
import numpy as np
from PIL import Image
import DicomMetaData
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

def dump_pngs(dicom_directory, output_directory):
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
        image = reader.Execute()
        series_array = sitk.GetArrayFromImage(image)

        # 读取序列中的第一个文件来获取窗宽窗位
        first_image = sitk.ReadImage(series_file_names[0])
        window_center = DicomMetaData.get_window_center(first_image)
        window_width = DicomMetaData.get_window_width(first_image)
        sequence_name = DicomMetaData.get_sequence_name(first_image)
        print(f"sequence_name:{sequence_name}, Window Center: {window_center}, Window Width: {window_width}"
              f"Series ID: {series_id}, Number of Images: {len(series_file_names)}")
        for i in range(series_array.shape[0]):
            # print(f"Processing file {i} of {len(series_file_names)}, {series_file_names[i]}")
            slice = series_array[i, :, :]
            windowed_slice = apply_window_level(slice, window_width, window_center)
            out_basename = os.path.basename(os.path.splitext(series_file_names[i])[0]) + ".png"
            out_dirname = f"{output_directory}/{sequence_name}"
            if not os.path.exists(out_dirname):
                os.makedirs(out_dirname)
            output_file_path = f"{out_dirname}/{out_basename}"
            Image.fromarray(windowed_slice).save(output_file_path)