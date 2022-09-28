# Terraform Kubernetes Example

This is a stab at deploying a model on a k8s cluster using `minikube` specifying and deploying all resources with `Terraform`.

---

## Python training pipeline

Train a simple model to be used for *simulated* online inference.

* Upload data to the [data folder](/training_pipeline/data/).
* Modify parameters in [constants.py](/training_pipeline/constants.py) to fit the `target` and `features` of the dataset.
* Kick-start training by running [run_pipeline.py](/training_pipeline/run_pipeline.py).

> NOTE: This pipeline is deliberately using `numpy` over `pandas`. Many steps could have been simplified with the built-in functionalities of `pandas` but for various reasons `pandas` was excluded.

### Serving with FastAPI

Modify class `Penguin` in [main.py](/training_pipeline/serving/app/main.py) to fit dataset.

Build docker image:

```bash
# Use Python version as tag
# Stand in root folder
docker build -t model-serving:3.10.6 .
```

Check that model is working out of container by running the following:

```bash
docker run --rm -p 80:80 model-serving:3.10.6
```

> This will spin up a service of the API.

In a new terminal window (or under [localhost](https://localhost:80/docs)) make some predictions by running:

```bash
# cd into training_pipeline/serving
curl -X POST http://localhost:80/predict \
    -d @./penguin_examples/0.json \
    -H "Content-Type: application/json"
```

> Once you've verified that the running container can take input data and return predictions you can stop the running API.

#### Debugging FastAPI

In case the API needs debugging, set breakpoint in [main.py](/training_pipeline/serving/app/main.py) and run debugger from your console (VSCode, Pycharm, etc.).

This will start the API session, go to [localhost](https://localhost:80/docs) and send an example `JSON` (or send data via `curl`) to the API. You should hit the breakpoint and you can start debugging.

---

## Terraform resources

All terraform resources reside in the [terraform folder](/terraform/). The main orchestration script is [main.tf](/terraform/environment/dev/main.tf) which will specify to use `minikube` as configuration and which [Kubernetes modules](/terraform/modules/kubernetes/main.tf) to deploy.

Some convetion:

* `main.tf` scripts are describing `Terraform` resources
* `variables.tf` / `terraform.tfvars` describes variables being used
* `versions.tf` describes provider versions used for resources

### Kubernetes manifests

All `YAML` manifests reside in the [manifest folder](/terraform/modules/kubernetes/manifests/).

While there are Kubernetes resources on `Terraform` for deployment, service, etc. the use of traditional `YAML` files are sometimes nice to have. By utilizing the `kubernetes_manifest` (from Kubernetes) or `kubectl_manifest` (from `gavinbunney/kubectl`) you can easily deploy to a cluster by using already existing `YAML` files. One advantage of this is that you can keep your code small while still deploying large complex `YAML` files.

---

## Run cluster on minikube

Before deploying resources we need to start `minikube`:

```bash
minikube start --driver=docker
```
