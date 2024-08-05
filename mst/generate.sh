set -x
echo 开始生成
!/usr/bin/env bash

export PATH=/mnt/afs/user/yaotiankuo/.conda/bin:$PATH
export TORCH_EXTENSIONS_DIR=/mnt/afs/user/yaotiankuo/.cache/torch_extensions

work_dir=$2
cd $work_dir

# 更改环境（不必须）
source activate
conda activate /mnt/afs/user/yaotiankuo/.conda/envs/chart

export PYTHONPATH=$(pwd):$PYTHONPATH
echo "$work_dir/${1}.py" 
python ${1}.py --num 100000 --workers 112