# Deployment Considerations

## 1. What approach would you use to version and track different models in production?

To track the versioning of models in production, I rely on what I learned during my studies and previous work experiences.
After training the model, I save it using the format model_v(version)date. This allows me to clearly identify which model was created and when.
It's a very simple approach, but I find it effective and functional.

Of course, in a professional environment, I would use a tool like MLflow instead. It not only allows you to assign a custom name, but also to add tags to register and track the model properly.

---

## 2. What key metrics would you monitor for this API service and the prediction model?

For this project, I would integrate Prometheus and Grafana, or even use the basic Kubernetes metrics (in the case of creating a cluster where every pod is a different application of this project like: App, ml, test), to help track the model's health and performance over time.
Of course, since this is a simple application, it would be enough to monitor things like the number of requests, response latency, and error rate within the API.
As for the model, I would monitor the data distribution to better understand any outliers, and also track the prediction volume that is, how often the model is being used.