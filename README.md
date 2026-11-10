# Oficina Execution Service — FIAP Tech Challenge Fase 4

Microsserviço independente responsável pela execução de ordens de serviço, com persistência NoSQL própria.

## Responsabilidades e arquitetura

- Enfileirar uma OS para execução.
- Consultar o item de trabalho.
- Iniciar, concluir com descrição de diagnóstico e cancelar itens elegíveis.
- Persistir dados em **DynamoDB Local** no ambiente de demonstração, com PVC próprio.

O runtime é FastAPI `app.persistent_api:app`, com repositório `DynamoExecutionRepository`. O worker da Saga, hospedado separadamente no repositório da Oficina API, usa chamadas REST; não há acesso cruzado aos bancos.

## Endpoints

`GET /health`, `GET /openapi.json`, `POST /work-items`, `GET /work-items/{order_id}`, `POST /work-items/{order_id}/start`, `POST /work-items/{order_id}/complete`, `POST /work-items/{order_id}/cancel`. Swagger UI: `/docs` quando exposto.

## Testes e qualidade

Validação **local em 09/11/2026**: **21 testes aprovados, cobertura 95,59%, Ruff aprovado e YAML Kubernetes válido**. O workflow [Execution Phase 4 - quality](https://github.com/YasminLuna/oficina-execution-service/actions/workflows/phase4-quality.yml) configura Ruff, pytest com cobertura mínima de 80%, validação YAML e build Docker. **O status remoto mais recente não foi confirmado**.

## Demonstração

Cluster local: `kind-fiap-fase4`; namespace: `fiap-fase4`. O fluxo E2E demonstrou criação, execução concluída e cenário de compensação sem criação de item após falha HTTP simulada.

Repositórios: [API](https://github.com/YasminLuna/oficina-api) · [Billing](https://github.com/YasminLuna/oficina-billing-service).

## Pendências de entrega

Confirmar GitHub Actions remoto, proteção da branch principal, deploy Kubernetes **automatizado** e evidências de observabilidade. O workflow atual **não realiza deploy**. Não provisionar recursos AWS pagos sem autorização.
