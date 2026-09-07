# Project 7 – Production CI/CD Application

A containerized Python Flask application used to demonstrate a production-style CI/CD and GitOps deployment workflow on AWS.

This repository is the **application repository** for Project 7. It contains the application source code, automated tests, Dockerfile, version information, and GitHub Actions workflows.

---

## Architecture

```text
Developer
    │
    ▼
GitHub Application Repository
    │
    ▼
GitHub Actions CI Pipeline
    │
    ├── Run Python Tests
    ├── Build Docker Image
    ├── Push Immutable SHA Image to Amazon ECR
    │
    ▼
Update GitOps Repository
    │
    ▼
Argo CD
    │
    ├── Development Environment
    │
    └── Production Environment
```

---

## Application

The application is built using:

- Python
- Flask
- Docker
- Pytest

It exposes the following endpoints:

| Endpoint | Description |
|---|---|
| `/` | Application information and version |
| `/health` | Health check endpoint |
| `/version` | Application version information |

Example response:

```json
{
  "application": "project-7-cicd-app",
  "version": "0.3.0",
  "message": "Project 7 CI/CD application v0.3.0 is running"
}
```

---

## Containerization

The application is packaged as a Docker container.

The container:

- Uses Python 3.12
- Installs application dependencies
- Runs the Flask application on port `8080`
- Is designed for deployment to Kubernetes

Build the image locally:

```bash
docker build -t project-7-cicd-app:local .
```

Run the container locally:

```bash
docker run -p 8080:8080 project-7-cicd-app:local
```

Test the application:

```bash
curl http://localhost:8080/
curl http://localhost:8080/health
curl http://localhost:8080/version
```

---

## Testing

The project uses Pytest for automated testing.

Run the tests:

```bash
pip install -r requirements.txt
pytest -v
```

Current tests cover:

- Application home endpoint
- Health check endpoint
- Version endpoint

Example test result:

```text
3 passed
```

---

# CI/CD Pipeline

The GitHub Actions CI pipeline automatically runs when changes are pushed to the `main` branch.

The pipeline performs the following steps:

1. Checkout the application repository.
2. Set up Python.
3. Install application dependencies.
4. Run automated tests.
5. Build the Docker image.
6. Authenticate to AWS using GitHub OIDC.
7. Push the container image to Amazon ECR.
8. Tag the image using the immutable Git commit SHA.
9. Update the Development GitOps manifest.
10. Commit and push the updated GitOps configuration.

---

## Immutable Image Tags

Container images are tagged using the Git commit SHA.

Example:

```text
project-7-cicd-app:74fc6c612567ecac91e7c307d7a079a482085451
```

Using immutable SHA-based image tags provides:

- Immutable deployments
- Source-to-deployment traceability
- Reproducible releases
- Reliable rollbacks
- Clear artifact identification

Each deployed container image can be traced back to a specific Git commit.

---

## AWS Authentication with GitHub OIDC

The CI/CD pipeline uses GitHub OpenID Connect (OIDC) to authenticate with AWS.

The workflow assumes an AWS IAM role using:

```text
GitHub Actions
      │
      ▼
GitHub OIDC Token
      │
      ▼
AWS IAM Role
      │
      ▼
Temporary AWS Credentials
```

This avoids storing long-lived AWS access keys in GitHub Secrets.

---

## GitOps Workflow

Application deployment manifests are maintained in a separate GitOps repository.

```text
project-7-gitops
```

The CI pipeline does not directly deploy workloads to Kubernetes.

Instead, the workflow follows this model:

```text
GitHub Actions CI
        │
        ▼
Update GitOps Repository
        │
        ▼
Git Commit
        │
        ▼
Argo CD detects change
        │
        ▼
Kubernetes reconciliation
        │
        ▼
Application deployment
```

This separates:

- Application source code
- Infrastructure configuration
- Deployment configuration

---

# Development Deployment

When code is pushed to the `main` branch:

```text
Developer Push
      │
      ▼
GitHub Actions
      │
      ├── Run Tests
      │
      ├── Build Docker Image
      │
      ├── Push SHA Image to Amazon ECR
      │
      ▼
Update Development GitOps Manifest
      │
      ▼
Git Commit
      │
      ▼
Argo CD
      │
      ▼
Amazon EKS
```

The Development environment automatically receives the newly built immutable container image.

---

# Production Promotion

Production deployment is intentionally separated from the Development pipeline.

Production promotion is performed through a manually triggered GitHub Actions workflow.

The workflow requires an immutable image SHA.

Example:

```text
74fc6c612567ecac91e7c307d7a079a482085451
```

The production promotion workflow performs the following steps:

1. Receive the immutable image SHA.
2. Require the GitHub `production` environment.
3. Verify that the image exists in Amazon ECR.
4. Checkout the GitOps repository.
5. Update the Production image tag.
6. Commit the GitOps change.
7. Push the promotion commit.
8. Argo CD reconciles the Production environment.

This ensures that Production deployments use a previously built artifact rather than rebuilding the application.

---

## GitHub Environment Approval

The Production workflow uses a dedicated GitHub environment:

```text
production
```

This allows Production deployments to be controlled independently from Development deployments.

The workflow architecture is:

```text
Manual Promotion
      │
      ▼
GitHub Production Environment
      │
      ▼
Approval
      │
      ▼
Verify Immutable Image
      │
      ▼
Update Production GitOps Manifest
      │
      ▼
Argo CD
      │
      ▼
Production Deployment
```

This provides an additional control point before Production changes are deployed.

---

# Rollback Strategy

The project uses GitOps and immutable container images to support controlled rollbacks.

Because deployments reference immutable Git commit SHA image tags, a previous version can be restored by reverting the GitOps repository.

Rollback flow:

```text
Production Issue
      │
      ▼
Identify Previous Working Image SHA
      │
      ▼
Revert GitOps Manifest
      │
      ▼
Git Commit
      │
      ▼
Argo CD detects change
      │
      ▼
Kubernetes deploys previous image
```

Example:

```bash
git log --oneline
```

Revert a deployment commit:

```bash
git revert <commit-id>
```

After the GitOps change is pushed, Argo CD reconciles the cluster to the previous desired state.

---

# Security

The project implements several CI/CD security practices.

### GitHub OIDC

GitHub Actions uses OIDC to obtain temporary AWS credentials.

No long-lived AWS access keys are stored in GitHub Secrets.

### IAM Roles

AWS access is controlled through IAM roles and permissions.

### GitHub App Authentication

A GitHub App token is used to authenticate updates to the GitOps repository.

### Immutable Container Images

Container images use Git commit SHA tags instead of mutable tags such as:

```text
latest
```

### Separate Repositories

The project separates:

- Application source code
- Infrastructure as Code
- Kubernetes deployment configuration

---

# Repository Structure

```text
.
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── promote-prod.yml
│
├── app/
│   ├── __init__.py
│   └── main.py
│
├── tests/
│   └── test_main.py
│
├── Dockerfile
├── requirements.txt
├── pytest.ini
├── VERSION
└── README.md
```

---

# Related Repositories

This project is divided into three repositories.

### Application Repository

```text
project-7-cicd-app
```

Contains:

- Flask application
- Automated tests
- Dockerfile
- GitHub Actions CI/CD workflows

### Infrastructure Repository

```text
project-7-infrastructure
```

Contains:

- Terraform configuration
- AWS networking
- Amazon EKS
- Amazon ECR
- IAM configuration

### GitOps Repository

```text
project-7-gitops
```

Contains:

- Kubernetes manifests
- Kustomize configuration
- Development overlays
- Production overlays
- Argo CD applications

---

# Technologies Used

- AWS
- Amazon ECR
- Amazon EKS
- Terraform
- Docker
- Kubernetes
- Kustomize
- Argo CD
- GitHub Actions
- GitHub OIDC
- GitHub App
- Python
- Flask
- Pytest

---

# Project Highlights

- Automated CI testing
- Containerized Flask application
- Docker-based application packaging
- Immutable SHA-based container images
- Amazon ECR integration
- GitHub OIDC authentication
- Temporary AWS credentials
- GitHub App authentication
- Separate GitOps repository
- Automated Development deployments
- Controlled Production promotion
- GitHub Environment approval
- Argo CD reconciliation
- Kubernetes deployment management
- Git-based rollback strategy
- Immutable deployment artifacts

---

# Project Status

The AWS infrastructure used for the project was provisioned using Terraform and has been cleaned up after project completion.

The repositories retain the complete Infrastructure as Code, application source code, CI/CD workflows, and GitOps configuration for demonstration and portfolio purposes.

