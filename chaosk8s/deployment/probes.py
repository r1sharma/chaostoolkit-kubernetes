# -*- coding: utf-8 -*-
import time
from typing import List, Tuple

from chaoslib.exceptions import ActivityFailed
from chaoslib.types import Configuration, Secrets
from kubernetes import client
from logzero import logger

from chaosk8s import create_k8s_api_client

__all__ = ["collect_deployment_status"]


def collect_deployment_status(deployment_name: str, ns: str = "default",
                              duration: int = 60, every: int = 1,
                              configuration: Configuration = None,
                              secrets: Secrets = None) \
                                  -> List[Tuple[str, str, str]]:
    """
    Read deployment's status for a while.
    """
    api = create_k8s_api_client(secrets)
    v1beta = client.AppsV1beta1Api(api)

    conditions = []
    end = time.time() + duration
    while True:
        if time.time() >= end:
            break

        time.sleep(every)

        deployment = v1beta.read_namespaced_deployment_status(
            namespace=ns, name=deployment_name)

        status = deployment.status
        conditions.append([
            (c.type, c.status, c.reason) for c in status.conditions
        ])

    return conditions
