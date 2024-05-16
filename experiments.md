# Experiments

## Mounting Azure file share to pod

We mount an Azure file share to pod via PV that uses the `file.csi.azure.com` storage driver.

- Writing 3Gb to Azure file PV: 30s
- Reading 3Gb from Azure file PV: 1m
- Writing 305Mb to Azure file PV: 3.95s
- Reading 305Mb from Azure file PV: 5.35s
- Writing 305Kb to Azure file PV: 516ms
- Reading 305Kb from Azure file PV: 193ms

## Mounting Azure blob fuse to pod (without sliced cube)

We mount an Azure datalake (gen2 HNS) to pod via PV that uses `blob.csi.azure.com` storage driver.


## Mounting Azure blob fuse to pod (with sliced cube)


## Mounting Azure disk to pod

