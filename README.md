# DicomToPng
convert dicom images to png, and then dump into sequence directory

## Background

[好大夫][1] supports uploading compressed DICOM electronic films, but on the [健康160][2] platform, only mobile phone photos are possible, posing clarity issues. Moreover, the [健康160][2] platform only allows uploading 8 images. Previously, attempts to consult a certain chief physician online at [好大夫][1] were unsuccessful, despite observations that this physician typically accepts consultations on the [健康160][2] platform. Therefore, the plan is to convert DICOM files to PNG in batches, concatenate them into sets of 8 arranged in grids, and upload them to 160 for remote consultations. Currently, there hasn't been success finding a batch conversion tool that meets these requirements; spent half the night yesterday implementing batch PNG conversion using Python, with plans to support concatenation next.

## Usage
```bash
pip install -r requirements.txt
python DicomToPng.py
```

output as below:

<div style="text-align: center;">

![output](output.jpg)

</div>

## TODO
- [ ] Support concatenating and saving images as multiple individual images in a 6-grid arrangement.

[1]: https://www.haodf.com/	"好大夫"
[2]: https://www.96110.com/ "健康160"