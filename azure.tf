terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "3.35.0"
    }
  }

  required_version = ">= 1.1.0"
}

provider "azurerm" {
  features {}
}

# Define input variables
variable "aks_sp_client_id" {
  description = "Client ID of the Azure service principal for AKS"
}

variable "aks_sp_client_secret" {
  description = "Client Secret of the Azure service principal for AKS"
}


# Create a resource group
resource "azurerm_resource_group" "demo_rg" {
  name     = "demo-rg"
  location = "West Europe"
}

# Create a storage account
resource "azurerm_storage_account" "demost" {
  name                     = "demost41235"
  resource_group_name      = azurerm_resource_group.demo_rg.name
  location                 = azurerm_resource_group.demo_rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  tags = {
    environment = "demo"
  }

  account_kind = "StorageV2"
  is_hns_enabled = true
}

## Enable hierarchical namespace for the storage account (required for Data Lake Gen2)
#resource "azurerm_storage_account_blob_properties" "demost_blob_properties" {
#  storage_account_name = azurerm_storage_account.demost.name
#  resource_group_name  = azurerm_resource_group.demo_rg.name
#
#  default_service_version = "2019-07-07"
#}

# Create container registry
resource "azurerm_container_registry" "demo_acr" {
  name                = "demoacr41235"
  resource_group_name = azurerm_resource_group.demo_rg.name
  location            = azurerm_resource_group.demo_rg.location
  sku                 = "Basic"
  admin_enabled       = true
}

# Create AKS cluster
resource "azurerm_kubernetes_cluster" "demo_aks" {
  name                = "demo-aks"
  location            = azurerm_resource_group.demo_rg.location
  resource_group_name = azurerm_resource_group.demo_rg.name
  dns_prefix          = "demo-aks"

  default_node_pool {
    name       = "default"
    node_count = 1
    vm_size    = "Standard_DS2_v2"
  }

  tags = {
    environment = "demo"
  }

  service_principal {
    client_id     = var.aks_sp_client_id
    client_secret = var.aks_sp_client_secret
  }

  storage_profile {
    blob_driver_enabled = true
  }
}

