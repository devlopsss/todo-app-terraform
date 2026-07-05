# Serverless Todo App — AWS Cloud Project

A production-grade serverless SaaS backend with authentication, built on AWS.
Inspired by [Maqtba](https://maqtba.com/) — Cloud Education Platform.

---

## Architecture

Browser (S3 Static Website)
↓
API Gateway (REST API)
├── /signup  ─→ Lambda (todo_signup)  ─→ Cognito
├── /confirm ─→ Lambda (todo_confirm) ─→ Cognito
├── /login   ─→ Lambda (todo_login)   ─→ Cognito + Secrets Manager
│
└── Lambda Authorizer (JWT validation)
↓
├── /create  ─→ Lambda (todo_create)  ─→ DynamoDB
├── /read    ─→ Lambda (todo_read)    ─→ DynamoDB
├── /update  ─→ Lambda (todo_update)  ─→ DynamoDB
└── /delete  ─→ Lambda (todo_delete)  ─→ DynamoDB

---

## Services Used

| Service | Purpose |
|---|---|
| **Amazon Cognito** | User authentication — signup, login, JWT tokens |
| **API Gateway** | REST API — routing, throttling, access logging |
| **AWS Lambda** | Business logic — 8 serverless functions (Python 3.12) |
| **DynamoDB** | NoSQL database — per-user todo storage |
| **Secrets Manager** | Secure storage of Cognito client credentials |
| **S3** | Static frontend hosting |
| **IAM** | Least privilege roles and policies |
| **CloudWatch** | Logs and metrics for all Lambda functions and API Gateway |

---

## Security Design

### Authentication Flow
The browser never communicates with Cognito directly.
All auth calls go through our own API Gateway endpoints,
keeping the Cognito client secret server-side only.


Browser → POST /signup  → Lambda → Cognito
Browser → POST /login   → Lambda → Cognito (returns JWT)
Browser → POST /create  → API Gateway → Lambda Authorizer → Lambda → DynamoDB
↑
validates JWT, extracts userId



### Security Measures
- **Secrets Manager** — Cognito credentials never hardcoded or exposed
- **Lambda Authorizer** — every protected route validates JWT before execution
- **Least privilege IAM** — each policy scoped to specific ARNs and actions only
- **DynamoDB partition key** — userId ensures users can only access their own data
- **API Gateway throttling** — 100 req/s rate limit, 50 burst limit
- **CloudWatch logging** — full audit trail of all API calls
- **X-Ray tracing** — enabled on API Gateway for request tracing
- **DynamoDB encryption** — AES256 encryption at rest
- **DynamoDB PITR** — point-in-time recovery enabled (35 day window)
- **S3 versioning** — frontend file history preserved
- **S3 encryption** — AES256 encryption at rest

---

## API Endpoints

### Public (no auth required)
| Method | Endpoint | Description |
|---|---|---|
| POST | `/signup` | Create a new account |
| POST | `/confirm` | Verify email with code |
| POST | `/login` | Authenticate and receive JWT token |

### Protected (JWT required)
| Method | Endpoint | Description |
|---|---|---|
| POST | `/create` | Create a new todo |
| GET | `/read` | List all todos for current user |
| PUT | `/update/{todoId}` | Update a todo |
| DELETE | `/delete/{todoId}` | Delete a todo |

---

## Data Model

```json
{
  "userId":    "649864c8-f081-707d-47fe-ced12705a9a3",
  "todoId":    "61b75bbc-f8e6-4a18-84d1-95c0e71cecd2",
  "title":     "Learn AWS Lambda",
  "status":    "pending",
  "createdAt": "2026-06-29T20:47:25.929527"
}
```

DynamoDB composite key: `userId` (partition) + `todoId` (sort)
This guarantees per-user data isolation at the database level.

---

## Infrastructure as Code

All resources are managed with **Terraform** using a modular structure:

---

## Data Model

```json
{
  "userId":    "649864c8-f081-707d-47fe-ced12705a9a3",
  "todoId":    "61b75bbc-f8e6-4a18-84d1-95c0e71cecd2",
  "title":     "Learn AWS Lambda",
  "status":    "pending",
  "createdAt": "2026-06-29T20:47:25.929527"
}
```

DynamoDB composite key: `userId` (partition) + `todoId` (sort)
This guarantees per-user data isolation at the database level.

---

## Infrastructure as Code

All resources are managed with **Terraform** using a modular structure:

todo-app-terraform/
├── main.tf                         # root module
├── variables.tf
├── outputs.tf
├── terraform.tfvars
└── modules/
├── cognito/                    # user pool + app client
├── dynamodb/                   # table with encryption + PITR
├── iam/                        # roles + least privilege policies
├── lambda/                     # 8 functions + CloudWatch log groups
├── api_gateway/                # REST API + authorizer + stage + logging
├── secrets_manager/            # Cognito credentials
└── s3/                         # frontend bucket + versioning + encryption

### Deploy from scratch

```bash
# Prerequisites: Terraform >= 1.0, AWS CLI configured

git clone <your-repo>
cd todo-app-terraform
terraform init
terraform plan
terraform apply
```

### Tear down

```bash
terraform destroy
```

---

## Debugging Notes

Key lessons learned during build — saved for future reference:

| Issue | Fix |
|---|---|
| Lambda not invoked by API Gateway | Add `aws_lambda_permission` with `apigateway.amazonaws.com` principal |
| `requestContext` missing in Lambda event | Enable **Lambda Proxy Integration** on API Gateway method |
| Wrong userId path in Lambda Authorizer | Lambda Authorizer uses `event['requestContext']['authorizer']['sub']` not `['claims']['sub']` |
| Body is a string not a dict | Always use `json.loads(event['body'])` even with proxy integration |
| Cognito `SECRET_HASH` error | `SECRET_HASH` goes inside `AuthParameters` for `InitiateAuth`, not at top level |
| CORS errors from browser | Add CORS headers to every Lambda response + enable CORS on API Gateway |

---

## Future Improvements

See [IMPROVEMENTS.md](./IMPROVEMENTS.md) for planned enhancements including:
- CloudFront + ACM for HTTPS on the frontend
- WAF for API Gateway protection
- CloudWatch alarms for error alerting
- VPC for network-level isolation

---

## SAA-C03 Exam Concepts Demonstrated

| Concept | Where |
|---|---|
| Serverless architecture | Lambda + API Gateway + DynamoDB |
| Event-driven design | API Gateway → Lambda Authorizer → Lambda |
| Least privilege IAM | Scoped policies per service |
| Encryption at rest | DynamoDB + S3 AES256 |
| High availability | Serverless = no single point of failure |
| Cost optimization | PAY_PER_REQUEST DynamoDB + Lambda pay-per-invocation |
| Decoupled auth | Cognito + Lambda Authorizer pattern |
| IaC best practices | Modular Terraform with remote state ready |

---

## Cost Estimate (low traffic)

| Service | Free Tier | Estimated cost |
|---|---|---|
| Lambda | 1M requests/month | ~$0 |
| API Gateway | 1M calls/month | ~$0 |
| DynamoDB | 25GB + 200M requests | ~$0 |
| Cognito | 50,000 MAU | ~$0 |
| Secrets Manager | — | ~$0.40/month |
| S3 | 5GB | ~$0 |
| CloudWatch | 5GB logs | ~$0 |
| **Total** | | **~$0.40/month** |

---

## Author

Built as part of AWS Solutions Architect Associate (SAA-C03) learning path.

---

## CI/CD Pipeline

This project uses GitHub Actions for automated deployment.

| Trigger | Jobs |
|---|---|
| Push to `main` | Validate → Deploy |
| Pull Request | Validate → Plan |

### Remote State
Terraform state is stored in S3:
- Bucket: `todo-app-terraform-state-642494479460`
- Versioning: enabled
- Encryption: AES256

### Required GitHub Secrets
| Secret | Description |
|---|---|
| `AWS_ACCESS_KEY_ID` | CI user access key |
| `AWS_SECRET_ACCESS_KEY` | CI user secret key |
| `AWS_ACCOUNT_ID` | AWS account ID |
# test
