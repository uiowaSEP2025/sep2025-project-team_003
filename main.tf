terraform {
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


variable "SSHURL" {
  description = "User+URL of SSH provider (e.g, bob@10.1.1.1)"
  type        = string
  sensitive   = true
}


variable "SSHPASS" {
  description = "Password of SSH provider"
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

resource "null_resource" "always_run" {
  triggers = {
    always_run = timestamp()
    # this is to force TF to run everytime.
    # It is too complex to keep track of checksums of directory,
    # and main branch expects to run very little.
  }

  provisioner "local-exec" {
    command = "./docker-build-stage.sh pass"
    environment = {
      SSHURL = var.SSHURL
      SSHPASS = var.SSHPASS
    }
  }


}

# Define a Kubernetes Deployment that runs a single container from a Docker image.
resource "kubernetes_deployment" "hsa-dp" {
  metadata {
    name = "hsa-dp"
    labels = {
      app = "hsa"
    }
  }

  lifecycle {
    replace_triggered_by = [
      null_resource.always_run
    ]
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
          image_pull_policy = "Never"
          image = "docker.io/library/hsa-app:latest"

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

  depends_on = [null_resource.always_run]
}


resource "kubernetes_service" "hsa-service" {
  metadata {
    name = "hsa-service"
  }

  lifecycle {
    replace_triggered_by = [
      null_resource.always_run
    ]
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
  depends_on = [null_resource.always_run]
}
