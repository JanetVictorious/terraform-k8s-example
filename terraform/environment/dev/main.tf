provider "kubernetes" {
  config_path    = "~/.kube/config"
  config_context = "minikube"
}

module "kubernetes_modules" {
  # depends_on = [module.azure_modules]
  source = "../../modules/kubernetes"

  env       = var.env
  namespace = var.namespace
}
