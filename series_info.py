from dataclasses import dataclass, field
from typing import List
from dicom_info import DicomInfo

@dataclass
class SeriesInfo:
    series_meta: DicomInfo
    png_files: List[str] = field(default_factory=list)