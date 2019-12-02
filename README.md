# chaos-toolkit-poc
my experiments with chaos toolkit poc

## Build project

```mvn clean install```

## Build Docker image

```docker build -t sample:1.2 .```

## Creating a deployment:

```kubectl create -f deployment.yml```

## Creating a service:

Expose the deployment in order to create a service:

```kubectl expose deployment sample-app-deployment --type=NodePort```

## Access app URL:
```minikube service sample-app-deployment --url```

## Run chaos test

``` chaos run experiment.json```
