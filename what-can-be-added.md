## securit context
- runAsNonRoot
- runAsUser
- runAsGroup
- fsGroup
- seccompProfile
  type: RuntimeDefault
- readOnlyRootFilesystem
- allowPrivilegeEscalation
- capability:
    drop:
      - All

## termiantion uses
- terminationGracePeriodSeconds

## servicename:
- name
- ports

## deployments:
- replicas
- selectors
- security context
- strategy: type 
- template

## Pod
- container
- resource
- security context
- image
- readiness probe
- liveness probe
- startup probe
- security context
- port

### opt
- hooks postStart, prestop
- terminationGracePeriodSeconds
- service accout
- wheather to mount service account