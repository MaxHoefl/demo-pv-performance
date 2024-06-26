terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.94.0"
    }
  }

  required_version = ">= 1.1.0"
}

provider "azurerm" {
  features {}
}

# Create a resource group
resource "azurerm_resource_group" "demo_rg" {
  name     = "demo-rg"
  location = "North Europe"
}

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

  identity {
    type = "SystemAssigned"
  }

  storage_profile {
    blob_driver_enabled = true
  }

  tags = {
    environment = "development"
  }
}

resource "azurerm_role_assignment" "aks_acr_role" {
  principal_id                     = azurerm_kubernetes_cluster.demo_aks.kubelet_identity[0].object_id
  role_definition_name             = "AcrPull"
  scope                            = azurerm_container_registry.demo_acr.id
  skip_service_principal_aad_check = true
}

resource "azurerm_storage_account" "demo_sa_datalake" {
  name                     = "demosa41235"
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

# Define the storage account
resource "azurerm_storage_account" "demo_sa" {
  name                     = "demosa91776"
  resource_group_name      = azurerm_resource_group.demo_rg.name
  location                 = azurerm_resource_group.demo_rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

# Define the file share within the storage account
resource "azurerm_storage_share" "demo_fs" {
  name                 = "demofs91776"
  storage_account_name = azurerm_storage_account.demo_sa.name
  quota                = 50
}