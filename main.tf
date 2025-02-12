terraform {
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = ">= 2.0.0"
    }
  }
}

# Configure the Kubernetes provider. This example uses your local kubeconfig.
provider "kubernetes" {
  config_path = "~/.kube/config"
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
        container {
          name  = "hsa-ct"
          image = "hsa:latest"  # Replace with your desired Docker image
          image_pull_policy = "Never"
          # Optionally, expose a port from the container.
          port {
            container_port = 80
          }
        }
      }
    }
  }
}
