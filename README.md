# Набор миниутилит(python-скриптов) для предварительной подготовки данных к тестированию

Миниутилиты находятся в папке `prepare_data` данного репозитория.

## Описание миниутилит

#### 1. prepare_img.py 

Миниутилита для "кодирования" бинарными штрих-кодами картинок с помощью класса **EncodeIMG** из `encode_img.py`

##### Принимаемые параметры

- `-i` - папка с "входными" изображениями. По умолчанию - `"..\src_imgs"`
- `-o` - папка с "выходными" изображениями. По умолчанию - `"..\src_imgs2"`

Пример - `prepare_img.py -i ..\src_imgs -o ..\src_imgs2`

#### 2. prepare_txt_markup.py

Миниутилита для подготовки истинной разметки по формату txt проекта ГОСНИИАС **SOKOL v3 (Контрольный эксперимент)**.
Переводит json (формат проекта **ThermaManager** в txt с "кодированием" номером (число в первой строке).

##### Принимаемые параметры

- `-j` - папка с "входной" разметкой формата JSON (как в [ThermalManager](http://192.168.33.113/cross/thermalmanager)). По умолчанию - `"..\json_translate"`
- `-t` - папка с "выходной" разметкой формата TXT (как в [SOKOL v3 (Контрольный эксперимент)](http://192.168.33.113/windows_group/sokol_control_experiment)). По умолчанию - `"..\txt_markup2"`
- `-s` - размер изображений для пересчета координат из абсолютных в относительные. По умолчанию - `"640x480"`
- `-m` - режим пересчета координат из абсолютные в относительные (без смещения из угла в центр - `raw`, со смещением - `offset`). По умолчанию - `"raw"`

Пример - `prepare_txt_markup.py -j ..\json_translate -t ..\txt_markup2 -s 640x480 -m raw`

#### 3. view_b_box.py

Миниутилита для просмотра расположения b-box на картинке. Входной формат - не "кодированный" txt (формат KITTY)

##### Принимаемые параметры

- `-i` - папка с "входными" картинками. По умолчанию - `"..\src_imgs"`
- `-m` - папка с "входной" разметкой формата TXT (формат kitti). По умолчанию - `"..\txt_markup"`
- `-n` - номер картинки-разметки для просмотра. По умолчанию - `"1"`

Пример - `view_b_box.py -i ..\src_imgs -t ..\txt_markup -n 1`
