# Demo PV Performance

The purpose of this repository is to measure performance differences between PVs on AKS:
- PV mounted from Azure data lake Gen2 (data resides remote to the node)
- PV local to the node (data resides on the node)


## How to conduct the experiment

- Setup Azure infrastructure
    - AKS cluster
    - Storage account #1 (Azure datalake gen2)
    - Storage account #2 (Azure files)
    - Storage account #3 (Azure blob store)

- Deploy four instances of a web API with GET endpoint to retrieve data from the four different storage solutions
- Use k6 to measure performance differences between the four instances



