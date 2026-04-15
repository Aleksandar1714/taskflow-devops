{{- define "taskflow.name" -}}
{{- .Chart.Name -}}
{{- end -}}

{{- define "taskflow.fullname" -}}
{{- printf "%s-%s" .Release.Name .Chart.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
