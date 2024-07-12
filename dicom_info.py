import SimpleITK as sitk

class DicomInfo:
    def __init__(self, image: sitk.Image):
        self.patient_name: str = self.get_patient_name(image)  # 姓名
        self.patient_id: str = str(self.get_patient_id(image))  # 患者ID
        self.patient_age: int = self.get_patient_age(image)  # 年龄
        self.patient_sex: str = self.get_patient_sex(image)  # 性别
        self.patient_birthday: str = self.get_patient_birthday(image)  # 出生日期
        self.study_id: str = self.get_study_id(image)  # 病历ID
        self.study_date: str = self.get_study_date(image)  # 病历日期
        self.study_time: str = self.get_study_time(image)  # 病历时间
        self.study_description: str = self.get_study_description(image)  # 病历描述
        self.series_modality: str = self.get_series_modality(image)  # 序列类型
        self.series_number: int = self.get_series_number(image)  # 序列号
        self.series_name: str = self.get_series_name(image)  # 序列名称

        self.window_center = self.get_window_center(image)  # 窗口宽度
        self.window_width = self.get_window_width(image)  # 窗口中心
        self.image_width: int = self.get_image_width(image)  # 图像宽度
        self.image_height: int = self.get_image_height(image)  # 图像高度

        self.TR: float = self.get_repetition_time(image)  # 重复时间
        self.TE: float = self.get_echo_time(image)  # 回波时间
        self.TA: float = self.get_acquisition_time(image)  # 采集时间
        self.BW: float = self.get_pixel_bandwidth(image)  # 像素带宽
        self.TP: float = self.get_flip_angle(image)  # 翻转角度
        self.SP: float = self.get_spacing_between_slices(image)  # 切片间距
        self.SL: float = self.get_slice_thickness(image)  # 切片厚度
        self.FoV: str = self.get_pixel_spacing(image)  # 像素间距

        self.dicom_path: str = ''  # DICOM文件路径
        self.png_path: str = ''  # PNG文件路径
        self.hospital: str = self.get_hospital(image)  # 医院名称

    def get_dicom_metadata(self, image: sitk.Image, tag: str, name: str):
        try:
            return image.GetMetaData(tag)
        except RuntimeError:  # 如果指定的标签不存在，则捕获异常
            return f"N/A"

    def get_patient_name(self, image: sitk.Image):
        return self.get_dicom_metadata(image, '0010|0010', 'Patient Name')

    def get_patient_id(self, image: sitk.Image):
        return self.get_dicom_metadata(image, '0010|0020', "Patient ID")

    def get_patient_sex(self, image: sitk.Image):
        return self.get_dicom_metadata(image, '0010|0040', "Patient Sex")

    def get_patient_birthday(self, image: sitk.Image):
        date = self.get_dicom_metadata(image, '0010|0030', "Patient Birthday")
        formatted_date = date[:4] + '-' + date[4:6] + '-' + date[6:]
        return formatted_date

    def get_patient_age(self, image: sitk.Image):
        return self.get_dicom_metadata(image, '0010|1010', 'Patient Age')

    def get_hospital(self, image: sitk.Image):
        return self.get_dicom_metadata(image, '0008|0080', 'Hospital Name')

    def get_study_id(self, image: sitk.Image):
        return self.get_dicom_metadata(image, '0020|0010', "Study ID")

    def get_study_date(self, image: sitk.Image):
        date = self.get_dicom_metadata(image, '0008|0020', 'Study Date')
        formatted_date = date[:4] + '-' + date[4:6] + '-' + date[6:]
        return formatted_date

    def get_study_time(self, image: sitk.Image):
        study_time = self.get_dicom_metadata(image, '0008|0030', 'Study Time').split('.')[0]
        formatted_time = study_time[:2] + ':' + study_time[2:4] + ':' + study_time[4:]
        return formatted_time

    def get_study_description(self, image: sitk.Image):
        return self.get_dicom_metadata(image, '0008|1030', "Study Description")

    def get_series_id(self, image: sitk.Image):
        return self.get_dicom_metadata(image, '0020|000E', "Series Instance UID")

    def get_series_description(self, image: sitk.Image):
        return self.get_dicom_metadata(image, '0008|103E', "Series Description")

    def get_series_modality(self, image: sitk.Image):
        return self.get_dicom_metadata(image, '0008|0060', "Series Modality")
    def get_series_number(self, image: sitk.Image):
        return self.get_dicom_metadata(image, '0020|0011', "Series Number")

    def get_series_name(self, image: sitk.Image):
        return self.get_dicom_metadata(image, '0008|103e', 'Series Name')

    def get_window_center(self, image: sitk.Image):
        # 获取窗宽窗位
        window_center = self.get_dicom_metadata(image, '0028|1050', 'Window Center')
        return float(window_center)

    def get_window_width(self, image: sitk.Image):
        # 获取窗宽窗位
        width = self.get_dicom_metadata(image, '0028|1051', 'Window Width')
        return float(width)

    def get_image_width(self, image: sitk.Image):
        return image.GetWidth()

    def get_image_height(self, image: sitk.Image):
        return image.GetHeight()

    def get_repetition_time(self, image: sitk.Image):
        return float(self.get_dicom_metadata(image, '0018|0080', 'Repetition Time (TR)'))

    def get_echo_time(self, image: sitk.Image):
        return float(self.get_dicom_metadata(image, '0018|0081', 'Echo Time (TE)'))

    def get_acquisition_time(self, image: sitk.Image):
        return float(self.get_dicom_metadata(image, '0008|0032', 'Acquisition Time (TA)'))

    def get_pixel_bandwidth(self, image: sitk.Image):
        return float(self.get_dicom_metadata(image, '0018|0095', 'Pixel Bandwidth (BW)'))

    def get_flip_angle(self, image: sitk.Image):
        return float(self.get_dicom_metadata(image, '0018|1314', 'Flip Angle (TP)'))

    def get_spacing_between_slices(self, image: sitk.Image):
        return float(self.get_dicom_metadata(image, '0018|0088', 'Spacing Between Slices (SP)'))

    def get_slice_thickness(self, image: sitk.Image):
        return float(self.get_dicom_metadata(image, '0018|0050', 'Slice Thickness (SL)'))

    def get_pixel_spacing(self, image: sitk.Image):
        return self.get_dicom_metadata(image, '0028|0030', 'Pixel Spacing (FoV)')