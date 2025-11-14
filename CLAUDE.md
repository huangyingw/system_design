# System Design - PlantUML规范

## PlantUML工作流程

### 文件命名

**只创建一个文件**: `{topic}_system.puml`
- 展示所有核心组件和连接关系
- 必须包含性能瓶颈的注释

**❌ 不要创建**:
- `{topic}_schema.puml` - 数据库设计可以在system图中简单标注
- `{topic}_flow.puml` - 时序图过于复杂，面试时用不上
- `{topic}_design.md` - 设计文档过于详细，面试时用不上

### 绘图规则

**核心原则**: 简洁清晰 > 完整详细

1. **字体大小**: 统一 FontSize 25
   ```plantuml
   skinparam rectangle {
       FontSize 25
   }
   skinparam database {
       FontSize 25
   }
   skinparam note {
       FontSize 25
   }
   ```

2. **必须的组件**:
   - Load Balancer
   - API Gateway
   - Core Service
   - Database (Primary/Replica)
   - Cache (Redis)
   - Message Queue

3. **必须的注释**:
   - 性能瓶颈（Database write, Cache miss, Lock contention）
   - 关键设计决策（Why use this, Scale numbers, Failover strategy）

### 增强元数据标签（Enhanced Metadata）

**所有PUML文件必须使用增强元数据格式**:

```plantuml
@startuml System Name
' ==================== Enhanced Metadata ====================
' === 基础分类 ===
' @category: infrastructure
' @subcategory: load-balancing
' @tags: #load-balancer, #high-availability, #traffic-distribution
' @description: 系统简短描述
'
' === 应用场景 ===
' @application: General
' @industry: General, Enterprise
' @use-cases: Real-time Processing
' @business-value: Improved scalability, High availability
'
' === 技术栈 ===
' @tech-stack: Redis, PostgreSQL, Kafka
' @programming-languages: Go, Java
' @frameworks: Spring Boot
' @protocols: HTTP/REST, gRPC
' @apis: REST API
'
' === 架构模式 ===
' @pattern: Microservices, Event-Driven
' @design-pattern: Observer, Factory
' @data-flow: Client → Gateway → Service → Database
' @communication-style: Asynchronous
'
' === 分布式特性 ===
' @cap-focus: CP (Consistency + Partition Tolerance)
' @consistency-model: Strong Consistency
' @consensus-algorithm: Raft
' @partition-strategy: Hash-based partitioning
'
' === 性能与扩展 ===
' @scale: Large (10K-1M users)
' @scalability: Horizontal scaling
' @performance-metrics: Latency: <100ms p99
' @optimization-techniques: Caching, Indexing
' @throughput: High (100K+ requests/second)
' @latency: Low (<100ms p99)
'
' === 可靠性 ===
' @reliability: Replication, Redundancy
' @fault-tolerance: Failover, Health monitoring
' @disaster-recovery: Multi-datacenter replication
' @availability: 99.99% (4 nines)
' @data-durability: 99.999999999% (11 nines)
'
' === 安全性 ===
' @security-features: Encryption, Authentication
' @authentication: OAuth 2.0, JWT
' @authorization: RBAC
' @encryption: TLS 1.3 (in-transit), AES-256 (at-rest)
' @compliance: GDPR-ready, SOC2
'
' === 存储 ===
' @storage-type: Distributed Storage
' @database-type: SQL, NoSQL
' @caching-strategy: Cache-aside, Write-through
' @data-persistence: Disk-based with WAL
'
' === 监控运维 ===
' @monitoring: Prometheus, Grafana
' @logging: Centralized logging (ELK)
' @alerting: Prometheus Alertmanager
' @observability: Metrics, Logs, Tracing
'
' === 部署 ===
' @deployment: Kubernetes, Docker
' @infrastructure: Cloud, On-premise
' @cloud-provider: AWS, GCP, Azure
' @containerization: Docker-ready
'
' === 成本 ===
' @cost-factors: Compute, Storage, Network
' @cost-optimization: Auto-scaling, Reserved instances
' @resource-usage: CPU: Medium, Memory: Medium
'
' === 复杂度 ===
' @complexity: Medium
' @implementation-difficulty: Medium
' @operational-overhead: Medium
'
' === 面试重点 ===
' @interview-focus: HIGH
' @interview-topics: Scalability, Consistency, Fault tolerance
' @trade-offs: Consistency vs Availability
' @common-questions: How to handle failures?, Scaling strategy?
' ==================================================

[图表内容]
@enduml
```

### 元数据填写指南

#### 必填字段（Minimum Required）
- `@category`: 主分类（infrastructure/database/message-queue等）
- `@tags`: 至少5个标签，推荐10-15个
- `@description`: 系统简短描述

#### 推荐字段（Recommended）
- `@application`: 应用场景
- `@tech-stack`: 技术栈
- `@pattern`: 架构模式
- `@scale`: 规模范围
- `@interview-focus`: HIGH/MEDIUM/LOW

#### PayPal相关标签（For PayPal Interview Prep）
在 `@tags` 中添加以下标签之一：
- `#paypal-core`: 核心支付系统（幂等性、余额、退款、对账）
- `#paypal-infrastructure`: 基础设施（Kafka、数据库、缓存、监控）
- `#paypal-relevant`: 相关业务（电商、库存、订单）
- `#paypal-extended`: 扩展功能（实时通信、搜索推荐）

### 常用标签示例

**技术栈标签**:
- `#redis`, `#kafka`, `#postgresql`, `#mongodb`, `#elasticsearch`
- `#kubernetes`, `#docker`, `#prometheus`, `#grafana`

**架构模式标签**:
- `#microservices`, `#event-driven`, `#cqrs`, `#saga`
- `#serverless`, `#service-mesh`, `#api-gateway`

**特性标签**:
- `#high-concurrency`, `#high-availability`, `#idempotency`
- `#sharding`, `#distributed-lock`, `#circuit-breaker`
- `#fault-tolerance`, `#eventual-consistency`, `#strong-consistency`

**领域标签**:
- `#payment`, `#ecommerce`, `#messaging`, `#search`
- `#recommendation`, `#analytics`, `#logging`, `#monitoring`

### 生成后的必要步骤

1. 检查语法: `/Users/huangyingw/loadrc/bashrc/check_puml.sh filename.puml`
2. 预览图表: `plantumlviewer filename.puml` (后台运行)

### 注意事项

- PlantUML内容只能使用英文（@description可用中文）
- plantumlviewer支持多文件同时预览，不要杀掉进程
- 使用后台运行避免超时: `run_in_background: true`
- 元数据字段可按需选择，不必全部填写，但必填字段必须提供

### 检查清单

生成前确认:
- [ ] 包含所有关键组件
- [ ] 字体 FontSize 25
- [ ] 性能瓶颈有注释
- [ ] 关键设计有注释
- [ ] 图表简洁（≤10个主要组件）
- [ ] **使用增强元数据格式**
- [ ] **@tags ≥ 5个标签**
- [ ] **@interview-focus已设置**
- [ ] **PayPal相关系统已添加对应标签**
