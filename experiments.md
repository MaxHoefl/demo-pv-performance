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

- Writing 40Mb to Azure datalake PV: 2s
- Reading 40Mb from Azure datalake PV: 356ms

Writing 1000 4Mb cubes to Azure blobfuse PV: ~3m
Reading 1 cube of 4Mb from Azure blobfuse PV (when cached): 150ms (50ms)
Reading 1000 cubes of 4Mb from Azure blobfuse PV: ~2m 7s
Reading 10 cubes of 4Mb from Azure blobfuse PV (when cached): 2s (600ms)
Reading 100 cubes of 4Mb from Azure blobfuse PV (when cached): 13s (1s)

Writing 100 9Mb cubes to Azure blobfuse PV: 35s
Reading 1 9Mb cube (when cached): 150ms (55ms)
Reading 10 9Mb cubes (when cached): 1900ms (265ms)

## Mounting Azure blob fuse to pod (with sliced cube)


## Mounting Azure disk to pod

