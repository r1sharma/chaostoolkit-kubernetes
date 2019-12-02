# chaos-toolkit-poc
my experiments with chaos toolkit poc

## Creating a deployment:

```kubectl create -f deployment.yml```

## Creating a service:

Expose the deployment in order to create a service:

```kubectl expose deployment sample-app-deployment --type=NodePort```

## Access app URL:
```minikube service sample-app-deployment --url```


