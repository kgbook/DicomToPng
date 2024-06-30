def get_dicom_metadata(image, tag, name):
    try:
        return image.GetMetaData(tag)
    except RuntimeError:  # 如果指定的标签不存在，则捕获异常
        return f"{name} Not Available"

def get_patients_name(image):
    # 获取病人姓名
    patient_name = get_dicom_metadata(image, '0010|0010', 'Patient Name')
    return patient_name

def get_study_date(image):
    # 获取研究日期
    study_date = get_dicom_metadata(image, '0008|0020', 'Study Date')
    return study_date

def get_patient_age(image):
    # 获取病人年龄
    patient_age = get_dicom_metadata(image, '0010|1010', 'Patient Age')
    return patient_age

def get_hospital(image):
    # 获取医院名称
    hospital = get_dicom_metadata(image, '0008|0080', 'Hospital Name')
    return hospital

def get_sequence_name(image):
    # 获取序列名称
    sequence = get_dicom_metadata(image, '0008|103e', 'Sequence Name')
    return sequence

def get_window_center(image):
    # 获取窗宽窗位
    window_center = get_dicom_metadata(image, '0028|1050', 'Window Center')
    return float(window_center)

def get_window_width(image):
    # 获取窗宽窗位
    width = get_dicom_metadata(image, '0028|1051', 'Window Width')
    return float(width)

def get_width(image):
    return image.GetWidth()

def get_height(image):
    return image.GetHeight()