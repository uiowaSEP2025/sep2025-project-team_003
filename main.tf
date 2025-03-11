terraform {

  backend "s3" {
    bucket         = "hsa-tf-state"
    key            = "terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    
    skip_credentials_validation = true
    skip_metadata_api_check     = true
    skip_region_validation      = true
    skip_requesting_account_id  = true
    skip_s3_checksum            = true
    use_path_style              = true

  }

  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = ">= 2.0.0"
    }
  }
}

# configure values from environment.
variable "DATABASE_NAME" {
  description = "The application secret key"
  type        = string
  sensitive   = true
}

variable "DATABASE_IP" {
  description = "The application secret key"
  type        = string
  sensitive   = true
}

variable "DATABASE_USERNAME" {
  description = "The application secret key"
  type        = string
  sensitive   = true
}

variable "DATABASE_PASSWORD" {
  description = "Database password"
  type        = string
  sensitive   = true
}

# Configure the Kubernetes provider. This example uses your local kubeconfig.
provider "kubernetes" {
  config_path = "~/.kube/config"
}

resource "kubernetes_secret" "hsa-secrets" {
  metadata {
    name = "db-secrets"
  }

  data = {
    DATABASE_IP  = var.DATABASE_IP
    DATABASE_NAME = var.DATABASE_NAME
    DATABASE_USERNAME = var.DATABASE_USERNAME
    DATABASE_PASSWORD = var.DATABASE_PASSWORD
  }

  type = "Opaque"
}

# Define a Kubernetes Deployment that runs a single container from a Docker image.
resource "kubernetes_deployment" "hsa-dp" {
  metadata {
    name = "hsa-dp"
    labels = {
      app = "hsa"
    }
  }
  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "hsa"
      }
    }

    template {
      metadata {
        labels = {
          app = "hsa"
        }
      }

      spec {
        host_network = true

        container {
          name  = "hsa-ct"
          image = "mzeng1417/hsa-image-store:latest"

          port {
            container_port = 8000
          }

          env_from {
            secret_ref {
              name = kubernetes_secret.hsa-secrets.metadata[0].name
            }
          }
        }
      }
    }
  }
}


resource "kubernetes_service" "hsa-service" {
  metadata {
    name = "hsa-service"
  }

  spec {
    selector = {
      app = "hsa"
    }

    port {
      port        = 8000          # Expose the container's port inside the cluster
      target_port = 8000          # Target the container's internal port
      node_port   = 30000         # Expose the service on the node's IP at this port
    }

    type = "NodePort"  # Expose it as a NodePort
  }
}
