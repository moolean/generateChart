#!/bin/bash
set -e

# PARTITION=ac2e5ca0-6a9e-4a5a-8129-bc5b9ceb12a5 # VQA_H800_high
# PARTITION=f8eb8140-553a-4bc6-9919-a42fdaecf9bd # VQA
PARTITION=cc4cdf6c-944a-4c46-a9de-3d508a06c4dd # AMP
# PARTITION=b7c081ea-ab5a-4278-ab4a-c51bc222de13 # H100_SHARE

WORKSPACE=a58d023b-de76-475f-89c2-7e50f7aa3c7a
CONTAINTER=registry.ms-sc-01.maoshanwangtech.com/studio-aicl/ubuntu20.04-py3.10-cuda11.8-cudnn8-transformer4.28.0:master-20230626-172512-32302
MOUNT=ce3b1174-f6eb-11ee-a372-82d352e10aed:/mnt/afs,1f29056c-c3f2-11ee-967e-2aea81fd34ba:/mnt/afs2,047443d2-c3f2-11ee-a5f9-9e29792dec2f:/mnt/afs1

# ** 更改版本名需要与跑的代码的名字一致（不加.py） **
version=$1

# ** 确认工作目录一定要是自己的目录，以防覆盖他人结果 **
# work_dir=/mnt/afs/user/yaotiankuo/generateChart

######################⬆需要更改⬆######################

JOBNAME="ytk_gendata_${version}"
echo 任务名为$JOBNAME

GPU_PER_NODE=8
NNODES=1
echo 使用的节点数量为$NNODES
echo 使用显卡数为$GPU_PER_NODE

sco acp jobs create \
--workspace-name  $WORKSPACE --aec2-name $PARTITION \
--container-image-url $CONTAINTER \
--storage-mount $MOUNT \
--worker-spec "N6lS.Iu.I80.${GPU_PER_NODE}" \
-f pytorch -N "${NNODES}" \
-j $JOBNAME \
--command="bash $(pwd)/mst/generate.sh ${version} $(pwd) > $(pwd)/log/${version}.log"