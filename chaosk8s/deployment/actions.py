# -*- coding: utf-8 -*-
from chaoslib.exceptions import ActivityFailed
from chaoslib.types import Configuration, Secrets
from kubernetes import client
from logzero import logger

from chaosk8s import create_k8s_api_client

__all__ = ["rollback_deployment", "set_deployment_image"]


def rollback_deployment(deployment_name: str, to_revision: int = None,
                        ns: str = "default",
                        configuration: Configuration = None,
                        secrets: Secrets = None):
    """
    Undo a deployment's rollout.
    """
    api = create_k8s_api_client(secrets)
    v1beta = client.AppsV1beta1Api(api)
    rollback = client.AppsV1beta1DeploymentRollback(
        name=deployment_name,
        rollback_to=client.AppsV1beta1RollbackConfig(revision=to_revision)
    )

    try:
        res = v1beta.create_namespaced_deployment_rollback(
            "{}-rollback".format(deployment_name),
            namespace=ns,
            body=rollback
        )
    except ApiException as x:
        raise ActivityFailed(
            "Deployment '{}/{}' rollback failed {}".format(
                ns, deployment_name, x.body))

        return res


def set_deployment_image(deployment_name: str, image: str,
                         container_name: str = None, ns: str = "default",
                         configuration: Configuration = None,
                         secrets: Secrets = None):
    """
    Patch a deploymen's container to set the given image.
    """
    api = create_k8s_api_client(secrets)
    v1beta = client.AppsV1beta1Api(api)

    container = {
        "image": image
    }
    if container_name:
        container["name"] = container_name

    body = {
        "spec": {
            "template": {
                "spec": {
                    "containers": [container]
                }
            }
        }
    }

    try:
        res = v1beta.patch_namespaced_deployment(
            name=deployment_name, namespace=ns, body=body)
    except ApiException as x:
        raise ActivityFailed(
            "Deployment '{}/{}' image of container '{}' "
            "could not be set {}".format(
                ns, deployment_name, container_name, x.body))

        return res
