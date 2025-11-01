@description('Deployment location')
param location string = resourceGroup().location

@description('Backend container image tag (e.g. main-<sha>)')
param backendImageTag string

@description('Frontend container image tag (e.g. main-<sha>)')
param frontendImageTag string

@description('Backend container CPU cores as string convertible to decimal (e.g. "0.5")')
param backendCpu string = '0.5'

@description('Backend container memory request (e.g. "1Gi")')
param backendMemory string = '1Gi'

@description('Frontend container CPU cores as string convertible to decimal (e.g. "0.25")')
param frontendCpu string = '0.25'

@description('Frontend container memory request (e.g. "0.5Gi")')
param frontendMemory string = '0.5Gi'

@description('Allowed CORS origins for backend (comma-separated list)')
param corsOrigins string = 'https://localhost:5173'

@description('Secret key (temporary injection). For production prefer Key Vault reference pattern.')
@secure()
param secretKey string

@description('Existing container apps environment name (already provisioned externally)')
param existingContainerAppsEnvironmentName string = 'ideahub-env-weu'

@description('Existing Azure Container Registry name')
param existingAcrName string = 'ideahubappregistry'

@description('User-assigned managed identity name for container apps')
param userAssignedIdentityName string = 'ideahub-containerapps-mi'

// NOTE: This template assumes the resource group already contains:
// - Container Apps Environment: ideahub-env-weu
// - Azure Container Registry: ideahubappregistry
// It deploys or updates backend and frontend container apps to reference new image tags.

var backendAppName = 'aideahub-api' // per user-provided actual name (typo preserved intentionally)
var frontendAppName = 'ideahub-frontend'

resource acr 'Microsoft.ContainerRegistry/registries@2023-01-01-preview' existing = {
  name: existingAcrName
}

resource containerEnv 'Microsoft.App/managedEnvironments@2024-03-01' existing = {
  name: existingContainerAppsEnvironmentName
}

resource containerAppsIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: userAssignedIdentityName
  location: location
}

resource acrPullRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(acr.id, containerAppsIdentity.id, 'acrpull')
  scope: acr
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '7f951dda-4ed3-4680-a7ca-43fe172d538d')
    principalId: containerAppsIdentity.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

resource backendApp 'Microsoft.App/containerApps@2024-03-01' = {
  name: backendAppName
  location: location
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${containerAppsIdentity.id}': {}
    }
  }
  properties: {
    managedEnvironmentId: containerEnv.id
    configuration: {
      ingress: {
        external: true
        targetPort: 8000
        transport: 'auto'
        corsPolicy: {
          allowedOrigins: split(corsOrigins, ',')
          allowedMethods: [ 'GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS' ]
          allowedHeaders: [ '*' ]
          exposeHeaders: []
          maxAge: 3600
          allowCredentials: true
        }
      }
      registries: [
        {
          server: '${existingAcrName}.azurecr.io'
          identity: containerAppsIdentity.id
        }
      ]
      secrets: [
        {
          name: 'secret-key'
          value: secretKey
        }
      ]
    }
    template: {
      containers: [
        {
          name: 'backend'
          image: '${existingAcrName}.azurecr.io/ideahub-backend:${backendImageTag}'
          resources: {
            cpu: json(backendCpu)
            memory: backendMemory
          }
          env: [
            {
              name: 'APP_ENV'
              value: 'prod'
            }
            {
              name: 'SECRET_KEY'
              secretRef: 'secret-key'
            }
          ]
          probes: [
            {
              type: 'liveness'
              httpGet: {
                path: '/health'
                port: 8000
              }
              initialDelaySeconds: 10
              periodSeconds: 15
            }
          ]
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 5
        rules: [
          {
            name: 'http-concurrency'
            http: {
              metadata: {
                concurrentRequests: '50'
              }
            }
          }
        ]
      }
    }
  }
}

resource frontendApp 'Microsoft.App/containerApps@2024-03-01' = {
  name: frontendAppName
  location: location
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${containerAppsIdentity.id}': {}
    }
  }
  properties: {
    managedEnvironmentId: containerEnv.id
    configuration: {
      ingress: {
        external: true
        targetPort: 80
        transport: 'auto'
      }
      registries: [
        {
          server: '${existingAcrName}.azurecr.io'
          identity: containerAppsIdentity.id
        }
      ]
    }
    template: {
      containers: [
        {
          name: 'frontend'
          image: '${existingAcrName}.azurecr.io/ideahub-frontend:${frontendImageTag}'
          resources: {
            cpu: json(frontendCpu)
            memory: frontendMemory
          }
          env: [
            {
              name: 'VITE_API_BASE'
              value: 'https://${backendApp.name}.${location}.azurecontainerapps.io'
            }
          ]
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 3
      }
    }
  }
}

output backendUrl string = backendApp.properties.configuration.ingress.fqdn
output frontendUrl string = frontendApp.properties.configuration.ingress.fqdn
