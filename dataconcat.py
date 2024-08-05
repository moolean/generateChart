"""拼接未成功跑完的数据为jsonl
"""

from datetime import datetime
import os
import sensetool

# 填入需要处理的目录
data_root = "/mnt/afs/user/yaotiankuo/generateChart/opt/data_base_bar_md"



usage = data_root.split("/")[-1].split("_")[-1]
chart_type = "_".join(data_root.split("/")[-1].split("_")[1:-1]) 
json_file_names = os.listdir(os.path.join(data_root, "jsons"))
# 自动生成结果文件名
current_date = datetime.now()
formatted_date = current_date.strftime("%Y%m%d")

optJsonlName = os.path.join(data_root, f"{chart_type}_{formatted_date}_{usage}.jsonl")

f = open(optJsonlName, "w")
for json_fn in json_file_names:
    with open(os.path.join(data_root, "jsons", json_fn)) as json_f:
        f.write(json_f.readline() + "\n")
f.close()

fulljson = os.path.join(os.getcwd(), optJsonlName)
fullimage = os.path.join(os.getcwd(), data_root)
sensetool.startView(fulljson, fullimage, data_root)

pathOverView = {"root": fullimage,
                "annotation": fulljson,
                "data_augment": False,
                "repeat_time": 1,
                "length": len(json_file_names)}

checker = sensetool.checker()
checker.checkfiles(pathOverView)