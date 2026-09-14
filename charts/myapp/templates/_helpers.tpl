{{/*
Expand the name of the chart.
*/}}
{{- define "myapp.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end }}

{{/*
Create a fully qualified app name.
*/}}
{{- define "myapp.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else }}
{{- printf "%s-%s" .Release.Name (include "myapp.name" .) | trunc 63 | trimSuffix "-" -}}
{{- end }}
{{- end }}

{{/*
Common lables
*/}}

{{- define "myapp.labels" -}}
helm.sh/chart: {{ include "myapp.name" . }} - {{ .Chart.Version | replace "+" "-" }}
app.kubernetes.io/managed-by: {{ .Release.service }}
app.kubernetes.io/part-of: {{ .Chart.Name }}
{{- end }}