provider "azurerm" {
  features {}
  subscription_id = "3fc6e493-e905-48c1-ab12-784d6b0f6e29"
}

resource "azurerm_resource_group" "translator" {
  name     = "azure-translation-group"
  location = "East US"
}

data "azurerm_key_vault" "translatorkv" {
  name                = "translatorkeyvault8j53d" # Replace with your Key Vault name
  resource_group_name = azurerm_resource_group.translator.name
}

# Retrieve the Admin Password Secret
data "azurerm_key_vault_secret" "postgres_admin_password" {
  name         = "PostgresAdminPassword" # Replace with your secret name
  key_vault_id = data.azurerm_key_vault.translatorkv.id
}


resource "azurerm_postgresql_server" "translator" {
  name                = "postgresql-tranlation-1"
  location            = azurerm_resource_group.translator.location
  resource_group_name = azurerm_resource_group.translator.name

  sku_name = "B_Gen5_2"

  storage_mb                   = 5120
  backup_retention_days        = 7
  geo_redundant_backup_enabled = false
  auto_grow_enabled            = true

  administrator_login          = "psqladmin"
  administrator_login_password = data.azurerm_key_vault_secret.postgres_admin_password.value # Using the secret from Key Vault "X3f%t#sz1#d*j"
  version                      = "9.5"
  ssl_enforcement_enabled      = true
}

resource "azurerm_postgresql_database" "translator" {
  name                = "translationsdb"
  resource_group_name = azurerm_resource_group.translator.name
  server_name         = azurerm_postgresql_server.translator.name
  charset             = "UTF8"
  collation           = "English_United States.1252"

  # prevent the possibility of accidental data loss
  lifecycle {
    prevent_destroy = true
  }
}

# Translator Service
resource "random_string" "azurerm_cognitive_account_name" {
  length  = 13
  lower   = true
  numeric = false
  special = false
  upper   = false
}

resource "azurerm_cognitive_account" "cognitive_service" {
  name                = "CognitiveService-${random_string.azurerm_cognitive_account_name.result}"
  location            = azurerm_resource_group.translator.location
  resource_group_name = azurerm_resource_group.translator.name
  sku_name            = "S0"
  kind                = "CognitiveServices"
}



# Create an App Service Plan
resource "azurerm_service_plan" "translator" {
  name                = "translator"
  resource_group_name = azurerm_resource_group.translator.name
  location            = azurerm_resource_group.translator.location
  os_type             = "Linux"
  sku_name            = "F1"
}

#creating python web app
resource "azurerm_linux_web_app" "translator" {
  name                = "translatorapp"
  resource_group_name = azurerm_resource_group.translator.name
  location            = azurerm_service_plan.translator.location
  service_plan_id     = azurerm_service_plan.translator.id

  site_config {
    always_on = false
    application_stack {
      python_version = "3.11"
    }
  }
}


data "azurerm_key_vault" "translator" {
  name                = "translator-key-vault"
  resource_group_name = azurerm_resource_group.translator.name
}

