resource "kubernetes_namespace" "k8s_namespace" {
  metadata {
    name = var.namespace
  }
}

# resource "kubernetes_manifest" "config_map" {
#   manifest = yamldecode(
#     templatefile(
#       "${path.module}/manifests/configmap.yaml",
#       {
#         namespace = "${kubernetes_namespace.k8s_namespace.metadata.0.name}",
#       }
#     )
#   )

#   depends_on = [
#     kubernetes_namespace.k8s_namespace,
#   ]
# }

# resource "kubernetes_manifest" "deployment" {
#   manifest = yamldecode(
#     templatefile(
#       "${path.module}/manifests/deployment.yaml",
#       {
#         namespace = "${kubernetes_namespace.k8s_namespace.metadata.0.name}",
#         # configmap = "${kubernetes_manifest.config_map.manifest.metadata.0.name}"
#       }
#     )
#   )

#   depends_on = [
#     kubernetes_namespace.k8s_namespace,
#     # kubernetes_manifest.config_map,
#   ]
# }

# resource "kubernetes_manifest" "service" {
#   manifest = yamldecode(
#     templatefile(
#       "${path.module}/manifests/service.yaml",
#       {
#         namespace = "${kubernetes_namespace.k8s_namespace.metadata.0.name}",
#       }
#     )
#   )

#   depends_on = [
#     kubernetes_namespace.k8s_namespace,
#   ]
# }

# resource "kubernetes_manifest" "auto_scaling" {
#   manifest = yamldecode(
#     templatefile(
#       "${path.module}/manifests/service.yaml",
#       {
#         namespace = "${kubernetes_namespace.k8s_namespace.metadata.0.name}",
#         deployment = "${kubernetes_manifest.deployment.metadata.0.name}"
#       }
#     )
#   )

#   depends_on = [
#     kubernetes_namespace.k8s_namespace,
#   ]
# }
