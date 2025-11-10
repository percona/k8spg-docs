# Secrets Resource options

A Kubernetes Secret is an object used to store sensitive data, such as passwords, tokens, or keys in a secure and manageable way. Unlike ConfigMaps, Secrets are specifically designed to hold confidential information and can be mounted as volumes or injected into environment variables within Pods.

## `apiVersion`

Specifies the API version of the Custom Resource.

## `kind`

Defines the type of resource being created: `Secret`.

## `metadata.name`

Contains the metadata about the resource, such as its name.

## `type`

Defines the type of data stored within the Secret resource. `Opaque` type signals to Kubernetes and to the Operator that the content of the secret is custom and unstructured.

## `stringData`

The data that you pass to the Operator within the Secret.

| Value type  | Example    |
| ----------- | ---------- |
| :material-code-string: string     | `PMM_SERVER_TOKEN` |
