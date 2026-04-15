# Logs

For logs, deploy Loki + Promtail using the Grafana Helm charts:

- `grafana/loki`
- `grafana/promtail`

Promtail scrapes pod stdout/stderr logs from Kubernetes nodes and ships them to Loki.
Grafana is used to visualize both Prometheus metrics and Loki logs.
