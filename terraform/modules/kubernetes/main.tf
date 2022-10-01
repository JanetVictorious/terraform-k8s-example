resource "kubernetes_namespace" "k8s_namespace" {
  metadata {
    name = "${var.env}-${var.namespace}"
  }
}

resource "kubernetes_manifest" "deployment" {
  manifest = yamldecode(
    templatefile(
      "${path.module}/manifests/deployment.yaml",
      {
        namespace = "${kubernetes_namespace.k8s_namespace.metadata.0.name}",
      }
    )
  )

  depends_on = [kubernetes_namespace.k8s_namespace]
}

resource "kubernetes_manifest" "service" {
  manifest = yamldecode(
    templatefile(
      "${path.module}/manifests/service.yaml",
      {
        namespace = "${kubernetes_namespace.k8s_namespace.metadata.0.name}",
      }
    )
  )

  depends_on = [kubernetes_namespace.k8s_namespace]
}

resource "kubernetes_manifest" "auto_scaling" {
  manifest = yamldecode(
    templatefile(
      "${path.module}/manifests/autoscale.yaml",
      {
        namespace  = "${kubernetes_namespace.k8s_namespace.metadata.0.name}",
        deployment = "${kubernetes_manifest.deployment.manifest.metadata.name}"
      }
    )
  )

  depends_on = [
    kubernetes_namespace.k8s_namespace,
    kubernetes_manifest.deployment,
  ]
}
