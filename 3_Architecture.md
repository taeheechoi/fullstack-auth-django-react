https://medium.com/geekculture/the-best-saas-tech-stack-for-your-startup-application-fad631dcd1a7

Approach
1. Remain Agile
2. Simplify development and maintenance
3. Optimize costs


SaaS technology Stack
```
    Internet

    AWS Cloud

    Cloudfront CDN, S3 React App

    VPC?

    Public subnet, ALB

    Private subnet 

        ECS Cluster

            Postgres SQL RDS Multi Tenant <-> Security Manager, Elastic Cache or Redis <-> Django App, Python Workers <-> DynamoDB
```

Backend language: Python, 

Python framework: Django or Flask

Front language: React

Microservices: Docker

Microservices clusting system(container orchestration tool): Amazon ECS Fargate

Multi-tenant Architecture

Database: Amazon DynamoDB or RDS, Amazon S3

Database Multi-tenancy

Cloud storage: S3  

CDN: Amazon CloudFront CDN, Cloudflare CDN

Caching: Elastic Cache or Redis 
