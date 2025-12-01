import pandas as pd
import os


# datas = []
# folder_path = r"C:\Users\kimsohee\Desktop\sohee\VSCode Projects\TOSEL\bank\example"
# for filename in os.listdir(folder_path):
#     datas.append(filename.split("_example")[0])

# print(datas)

# excel_path = r"C:\Users\kimsohee\Desktop\sohee\VSCode Projects\TOSEL\image_info.xlsx"
# df = pd.read_excel(excel_path)

# # 3. alias 컬럼이 datas 리스트에 포함된 행만 필터링
# filtered_df = df[df["alias"].isin(datas)]

# # 4. 새로운 엑셀로 저장
# save_path = r"C:\Users\kimsohee\Desktop\sohee\VSCode Projects\TOSEL\image_info_new.xlsx"
# filtered_df.to_excel(save_path, index=False)

# print("새 파일 저장 완료:", save_path)


import pandas as pd
from pprint import pformat
import os

# 엑셀 파일 경로
excel_path = r"C:\Users\kimsohee\Desktop\sohee\VSCode Projects\TOSEL\image_info.xlsx"

# 엑셀 읽기
df = pd.read_excel(excel_path)

# 딕셔너리 형태로 변환
IMAGE_RULES = {
    row["alias"]: {
        "option_img": int(row["option_img"]),
        "material_img": int(row["material_img"]),
        "practical_img": int(row["practical_img"]),
        "type": row["type"],
    }
    for _, row in df.iterrows()
}

save_path = r"C:\Users\kimsohee\Desktop\sohee\VSCode Projects\TOSEL\src\utils\img_generate_config.py"

# 5. .py 파일로 저장
with open(save_path, "w", encoding="utf-8") as f:
    f.write("# 자동 생성된 이미지 설정 파일\n")
    f.write("# 엑셀: image_info.xlsx 기준\n\n")
    f.write("IMAGE_RULES = ")
    f.write(pformat(IMAGE_RULES, indent=4, width=120))
    f.write("\n")

print("생성 완료:", save_path)
