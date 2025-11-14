#!/usr/bin/env python3
"""
增强版PUML文件标签处理脚本
为所有.puml文件添加详尽的20+维度元数据标签
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

class PumlEnhancer:
    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)
        self.processed_count = 0
        self.error_files = []

    def extract_metadata(self, content: str) -> Tuple[Dict[str, str], str, str]:
        """提取现有元数据和图表内容"""
        # 提取@startuml标题
        startuml_match = re.search(r'@startuml\s+(.+)?', content)
        title = startuml_match.group(1).strip() if startuml_match and startuml_match.group(1) else "System Architecture"

        # 提取现有简单元数据
        existing_metadata = {}
        metadata_pattern = r"'\s*@(\w+(?:-\w+)*):\s*(.+)"
        for match in re.finditer(metadata_pattern, content):
            key = match.group(1)
            value = match.group(2).strip()
            existing_metadata[key] = value

        # 提取图表内容（去除元数据部分）
        # 找到元数据块的结束位置
        if "==================================================\n" in content:
            parts = content.split("==================================================\n", 1)
            diagram_content = parts[1] if len(parts) > 1 else content
        else:
            # 如果没有标准分隔符，保留原内容
            diagram_content = content

        return existing_metadata, title, diagram_content

    def analyze_file_content(self, filepath: Path, existing_metadata: Dict[str, str], diagram_content: str) -> Dict[str, str]:
        """基于文件内容智能分析并生成增强标签"""
        filename = filepath.name.lower()
        content_lower = diagram_content.lower()

        # 默认值
        enhanced_tags = {}

        # === 基础分类 ===
        category = existing_metadata.get('category', 'distributed-systems')
        subcategory = existing_metadata.get('subcategory', 'architecture')
        tags = existing_metadata.get('tags', '#distributed-systems, #architecture')
        description = existing_metadata.get('description', filepath.stem.replace('_', ' ').title())

        # 智能分类
        if 'kafka' in filename or 'kafka' in content_lower:
            category = 'distributed-systems'
            subcategory = 'message-queue'
            tags = '#kafka, #message-queue, #event-streaming, #distributed-systems'
        elif 'api_gateway' in filename or 'api gateway' in content_lower:
            category = 'microservices'
            subcategory = 'api-gateway'
            tags = '#api-gateway, #microservices, #routing, #authentication'
        elif 'database' in filename or 'db' in filename:
            category = 'data-storage'
            subcategory = 'database'
            tags = '#database, #storage, #data-management'
        elif 'load_balanc' in filename or 'load balanc' in content_lower:
            category = 'infrastructure'
            subcategory = 'load-balancing'
            tags = '#load-balancer, #high-availability, #traffic-distribution'
        elif 'cache' in filename or 'redis' in content_lower:
            category = 'data-storage'
            subcategory = 'caching'
            tags = '#cache, #redis, #performance, #distributed-cache'
        elif 'kubernetes' in filename or 'k8s' in content_lower:
            category = 'infrastructure'
            subcategory = 'container-orchestration'
            tags = '#kubernetes, #containers, #orchestration, #cloud-native'
        elif 'microservice' in filename or 'microservice' in content_lower:
            category = 'microservices'
            subcategory = 'service-architecture'
            tags = '#microservices, #service-oriented, #distributed-architecture'
        elif 'payment' in filename or 'payment' in content_lower:
            category = 'business-systems'
            subcategory = 'payment-processing'
            tags = '#payment, #fintech, #transactions, #financial-services'
        elif 'chat' in filename or 'messaging' in filename:
            category = 'communication'
            subcategory = 'real-time-messaging'
            tags = '#chat, #real-time, #websocket, #messaging'
        elif 'cdn' in filename or 'content delivery' in content_lower:
            category = 'infrastructure'
            subcategory = 'content-delivery'
            tags = '#cdn, #content-delivery, #edge-computing, #caching'

        enhanced_tags['category'] = category
        enhanced_tags['subcategory'] = subcategory
        enhanced_tags['tags'] = tags
        enhanced_tags['description'] = description

        # === 应用场景 ===
        enhanced_tags['application'] = existing_metadata.get('application', 'General')

        # 智能识别行业
        industries = []
        if any(x in content_lower for x in ['ecommerce', 'e-commerce', 'shopping', 'cart']):
            industries.append('E-commerce')
        if any(x in content_lower for x in ['payment', 'financial', 'banking', 'transaction']):
            industries.append('Financial Services')
        if any(x in content_lower for x in ['social', 'chat', 'messaging', 'feed']):
            industries.append('Social Media')
        if any(x in content_lower for x in ['iot', 'sensor', 'device']):
            industries.append('IoT')
        if any(x in content_lower for x in ['game', 'gaming', 'avatar']):
            industries.append('Gaming')
        if any(x in content_lower for x in ['video', 'audio', 'streaming', 'media']):
            industries.append('Media & Entertainment')
        if any(x in content_lower for x in ['healthcare', 'medical', 'patient']):
            industries.append('Healthcare')
        if any(x in content_lower for x in ['education', 'learning', 'course']):
            industries.append('Education')

        enhanced_tags['industry'] = ', '.join(industries) if industries else 'General, Enterprise'

        # 使用场景
        use_cases = []
        if 'real-time' in content_lower or 'realtime' in content_lower:
            use_cases.append('Real-time Processing')
        if 'analytics' in content_lower or 'analysis' in content_lower:
            use_cases.append('Data Analytics')
        if 'monitoring' in content_lower:
            use_cases.append('System Monitoring')
        if 'search' in content_lower:
            use_cases.append('Search & Discovery')
        if 'recommendation' in content_lower:
            use_cases.append('Recommendation Engine')
        if 'log' in content_lower:
            use_cases.append('Log Aggregation')

        enhanced_tags['use-cases'] = ', '.join(use_cases) if use_cases else 'System Architecture, Scalability, High Availability'
        enhanced_tags['business-value'] = 'Improved scalability, High availability, Better performance, Cost efficiency'

        # === 技术栈 ===
        tech_stack = existing_metadata.get('tech-stack', 'General')

        # 智能识别技术栈
        techs = []
        if 'kafka' in content_lower:
            techs.extend(['Kafka', 'ZooKeeper'])
        if 'redis' in content_lower:
            techs.append('Redis')
        if 'elasticsearch' in content_lower:
            techs.append('Elasticsearch')
        if 'mongodb' in content_lower or 'mongo' in content_lower:
            techs.append('MongoDB')
        if 'mysql' in content_lower or 'postgresql' in content_lower:
            techs.append('MySQL/PostgreSQL')
        if 'kubernetes' in content_lower or 'k8s' in content_lower:
            techs.append('Kubernetes')
        if 'docker' in content_lower:
            techs.append('Docker')
        if 'prometheus' in content_lower:
            techs.extend(['Prometheus', 'Grafana'])
        if 'nginx' in content_lower:
            techs.append('Nginx')
        if 'grpc' in content_lower:
            techs.append('gRPC')
        if 'graphql' in content_lower:
            techs.append('GraphQL')
        if 'spark' in content_lower:
            techs.append('Apache Spark')
        if 'hadoop' in content_lower:
            techs.append('Hadoop')
        if 'dynamodb' in content_lower:
            techs.append('DynamoDB')
        if 'cassandra' in content_lower:
            techs.append('Cassandra')

        enhanced_tags['tech-stack'] = ', '.join(techs) if techs else tech_stack

        # 编程语言
        langs = []
        if 'java' in content_lower:
            langs.append('Java')
        if 'python' in content_lower:
            langs.append('Python')
        if 'go' in content_lower or 'golang' in content_lower:
            langs.append('Go')
        if 'javascript' in content_lower or 'node' in content_lower:
            langs.append('JavaScript/Node.js')
        if 'scala' in content_lower:
            langs.append('Scala')
        if 'rust' in content_lower:
            langs.append('Rust')

        enhanced_tags['programming-languages'] = ', '.join(langs) if langs else 'Language-agnostic'

        # 框架
        frameworks = []
        if 'spring' in content_lower:
            frameworks.append('Spring Boot')
        if 'express' in content_lower:
            frameworks.append('Express.js')
        if 'django' in content_lower:
            frameworks.append('Django')
        if 'react' in content_lower:
            frameworks.append('React')
        if 'kafka streams' in content_lower:
            frameworks.append('Kafka Streams')

        enhanced_tags['frameworks'] = ', '.join(frameworks) if frameworks else 'Framework-agnostic'

        # 协议
        protocols = []
        if 'http' in content_lower or 'rest' in content_lower:
            protocols.append('HTTP/REST')
        if 'grpc' in content_lower:
            protocols.append('gRPC')
        if 'websocket' in content_lower:
            protocols.append('WebSocket')
        if 'tcp' in content_lower:
            protocols.append('TCP')
        if 'mqtt' in content_lower:
            protocols.append('MQTT')
        if 'amqp' in content_lower:
            protocols.append('AMQP')

        enhanced_tags['protocols'] = ', '.join(protocols) if protocols else 'HTTP/REST, TCP'

        # API类型
        enhanced_tags['apis'] = 'REST API, WebSocket, gRPC' if 'grpc' in content_lower else 'REST API'

        # === 架构模式 ===
        patterns = []
        if 'microservice' in content_lower:
            patterns.append('Microservices')
        if 'event' in content_lower:
            patterns.append('Event-Driven Architecture')
        if 'cqrs' in content_lower:
            patterns.append('CQRS')
        if 'saga' in content_lower:
            patterns.append('Saga Pattern')
        if 'circuit' in content_lower:
            patterns.append('Circuit Breaker')
        if 'gateway' in content_lower:
            patterns.append('API Gateway')
        if 'service mesh' in content_lower:
            patterns.append('Service Mesh')

        enhanced_tags['pattern'] = ', '.join(patterns) if patterns else 'Layered Architecture, Client-Server'
        enhanced_tags['design-pattern'] = 'Observer, Producer-Consumer, Repository, Factory'

        # 数据流向
        if 'producer' in content_lower and 'consumer' in content_lower:
            enhanced_tags['data-flow'] = 'Producer → Broker → Consumer'
        elif 'client' in content_lower and 'server' in content_lower:
            enhanced_tags['data-flow'] = 'Client → Gateway → Service → Database'
        else:
            enhanced_tags['data-flow'] = 'Bidirectional, Request-Response'

        # 通信方式
        comm_styles = []
        if 'async' in content_lower or 'queue' in content_lower or 'message' in content_lower:
            comm_styles.append('Asynchronous')
        if 'sync' in content_lower or 'rest' in content_lower:
            comm_styles.append('Synchronous')
        if 'event' in content_lower:
            comm_styles.append('Event-driven')

        enhanced_tags['communication-style'] = ', '.join(comm_styles) if comm_styles else 'Synchronous, Request-Response'

        # === 分布式特性 ===
        # CAP倾向
        if 'kafka' in content_lower or 'cassandra' in content_lower:
            enhanced_tags['cap-focus'] = 'AP (Availability + Partition Tolerance)'
        elif 'zookeeper' in content_lower or 'etcd' in content_lower:
            enhanced_tags['cap-focus'] = 'CP (Consistency + Partition Tolerance)'
        else:
            enhanced_tags['cap-focus'] = 'AP (configurable)'

        # 一致性模型
        if 'strong consistency' in content_lower:
            enhanced_tags['consistency-model'] = 'Strong Consistency'
        elif 'eventual' in content_lower:
            enhanced_tags['consistency-model'] = 'Eventual Consistency'
        else:
            enhanced_tags['consistency-model'] = 'Eventual Consistency (configurable)'

        # 共识算法
        consensus = []
        if 'raft' in content_lower:
            consensus.append('Raft')
        if 'paxos' in content_lower:
            consensus.append('Paxos')
        if 'zab' in content_lower or 'zookeeper' in content_lower:
            consensus.append('ZAB')

        enhanced_tags['consensus-algorithm'] = ', '.join(consensus) if consensus else 'Raft, Leader Election'

        # 分区策略
        if 'hash' in content_lower:
            enhanced_tags['partition-strategy'] = 'Hash-based partitioning, Consistent hashing'
        elif 'range' in content_lower:
            enhanced_tags['partition-strategy'] = 'Range-based partitioning'
        else:
            enhanced_tags['partition-strategy'] = 'Hash-based, Key-based, Custom partitioning'

        # === 性能与扩展 ===
        # 系统规模
        if 'internet scale' in content_lower or 'billion' in content_lower:
            scale = 'Internet Scale (billions of users, millions of QPS)'
        elif 'large' in content_lower or 'million' in content_lower:
            scale = 'Large to Very Large (100K-10M users, 1K-100K QPS)'
        elif 'high traffic' in content_lower or 'high volume' in content_lower:
            scale = 'Large (100K+ users, 1K+ QPS)'
        else:
            scale = 'Medium to Large (1K-100K users, 100-10K QPS)'

        enhanced_tags['scale'] = scale
        enhanced_tags['scalability'] = 'Horizontal scaling, Auto-scaling, Load balancing'

        # 性能指标
        if 'kafka' in content_lower or 'high throughput' in content_lower:
            enhanced_tags['performance-metrics'] = 'Throughput: 1M+ msg/s, Latency: <10ms p99'
            enhanced_tags['throughput'] = 'Very High (1M+ messages/second)'
            enhanced_tags['latency'] = 'Low (<10ms p99)'
        elif 'real-time' in content_lower:
            enhanced_tags['performance-metrics'] = 'Latency: <100ms p99, High throughput'
            enhanced_tags['throughput'] = 'High (100K+ requests/second)'
            enhanced_tags['latency'] = 'Low (<100ms p99)'
        else:
            enhanced_tags['performance-metrics'] = 'Response time: <200ms p95, 10K+ QPS'
            enhanced_tags['throughput'] = 'Medium to High (10K-100K requests/second)'
            enhanced_tags['latency'] = 'Medium (<200ms p95)'

        # 优化技术
        optimizations = []
        if 'cache' in content_lower or 'caching' in content_lower:
            optimizations.append('Caching')
        if 'batch' in content_lower:
            optimizations.append('Batch processing')
        if 'compress' in content_lower:
            optimizations.append('Compression')
        if 'index' in content_lower:
            optimizations.append('Indexing')
        if 'shard' in content_lower or 'partition' in content_lower:
            optimizations.append('Sharding/Partitioning')
        if 'cdn' in content_lower:
            optimizations.append('CDN')

        enhanced_tags['optimization-techniques'] = ', '.join(optimizations) if optimizations else 'Caching, Indexing, Connection pooling, Batch processing'

        # === 可靠性 ===
        enhanced_tags['reliability'] = 'Replication, Redundancy, Health checks, Automatic recovery'

        # 容错机制
        fault_tolerance = []
        if 'replica' in content_lower:
            fault_tolerance.append('Replication')
        if 'failover' in content_lower:
            fault_tolerance.append('Automatic failover')
        if 'circuit' in content_lower:
            fault_tolerance.append('Circuit breaker')
        if 'retry' in content_lower:
            fault_tolerance.append('Retry mechanism')
        if 'backup' in content_lower:
            fault_tolerance.append('Backup and restore')

        enhanced_tags['fault-tolerance'] = ', '.join(fault_tolerance) if fault_tolerance else 'Replication, Failover, Health monitoring, Graceful degradation'

        enhanced_tags['disaster-recovery'] = 'Multi-datacenter replication, Backup strategies, RPO/RTO management'

        # 可用性
        if 'high availability' in content_lower or 'ha' in content_lower:
            enhanced_tags['availability'] = '99.99% (4 nines)'
        elif 'ultra' in content_lower:
            enhanced_tags['availability'] = '99.999% (5 nines)'
        else:
            enhanced_tags['availability'] = '99.9% (3 nines)'

        enhanced_tags['data-durability'] = '99.999999999% (11 nines) with proper replication'

        # === 安全性 ===
        security_features = []
        if 'authentication' in content_lower or 'auth' in content_lower:
            security_features.append('Authentication')
        if 'authorization' in content_lower:
            security_features.append('Authorization')
        if 'encryption' in content_lower or 'ssl' in content_lower or 'tls' in content_lower:
            security_features.append('Encryption')
        if 'firewall' in content_lower:
            security_features.append('Firewall')
        if 'ddos' in content_lower:
            security_features.append('DDoS protection')

        enhanced_tags['security-features'] = ', '.join(security_features) if security_features else 'Authentication, Authorization, Encryption, Audit logging'

        # 认证机制
        auth_methods = []
        if 'oauth' in content_lower:
            auth_methods.append('OAuth 2.0')
        if 'jwt' in content_lower:
            auth_methods.append('JWT')
        if 'sasl' in content_lower:
            auth_methods.append('SASL')
        if 'kerberos' in content_lower:
            auth_methods.append('Kerberos')

        enhanced_tags['authentication'] = ', '.join(auth_methods) if auth_methods else 'OAuth 2.0, JWT, API Keys, SASL'
        enhanced_tags['authorization'] = 'RBAC (Role-Based Access Control), ACLs, Policy-based'

        # 加密
        if 'ssl' in content_lower or 'tls' in content_lower:
            enhanced_tags['encryption'] = 'TLS 1.3 (in-transit), AES-256 (at-rest)'
        else:
            enhanced_tags['encryption'] = 'TLS (in-transit), Optional encryption at rest'

        enhanced_tags['compliance'] = 'GDPR-ready, SOC2, HIPAA-compatible, PCI-DSS'

        # === 存储 ===
        # 存储类型
        storage_types = []
        if 'block' in content_lower:
            storage_types.append('Block Storage')
        if 'object' in content_lower or 's3' in content_lower:
            storage_types.append('Object Storage')
        if 'file' in content_lower:
            storage_types.append('File Storage')
        if 'log' in content_lower:
            storage_types.append('Log Storage')

        enhanced_tags['storage-type'] = ', '.join(storage_types) if storage_types else 'Distributed Storage, Replicated Storage'

        # 数据库类型
        db_types = []
        if 'sql' in content_lower or 'mysql' in content_lower or 'postgres' in content_lower:
            db_types.append('SQL/Relational')
        if 'nosql' in content_lower or 'mongodb' in content_lower or 'cassandra' in content_lower:
            db_types.append('NoSQL')
        if 'redis' in content_lower:
            db_types.append('In-Memory')
        if 'elasticsearch' in content_lower:
            db_types.append('Search Engine')
        if 'graph' in content_lower:
            db_types.append('Graph Database')

        enhanced_tags['database-type'] = ', '.join(db_types) if db_types else 'Polyglot (SQL + NoSQL)'

        # 缓存策略
        cache_strategies = []
        if 'write-through' in content_lower:
            cache_strategies.append('Write-through')
        if 'write-back' in content_lower or 'write-behind' in content_lower:
            cache_strategies.append('Write-back')
        if 'cache-aside' in content_lower or 'lazy loading' in content_lower:
            cache_strategies.append('Cache-aside')

        enhanced_tags['caching-strategy'] = ', '.join(cache_strategies) if cache_strategies else 'Cache-aside, Write-through, TTL-based expiration'
        enhanced_tags['data-persistence'] = 'Disk-based with WAL, Configurable durability, Snapshot backups'

        # === 监控运维 ===
        monitoring = []
        if 'prometheus' in content_lower:
            monitoring.append('Prometheus')
        if 'grafana' in content_lower:
            monitoring.append('Grafana')
        if 'datadog' in content_lower:
            monitoring.append('Datadog')
        if 'elk' in content_lower or 'elasticsearch' in content_lower:
            monitoring.append('ELK Stack')
        if 'newrelic' in content_lower:
            monitoring.append('New Relic')

        enhanced_tags['monitoring'] = ', '.join(monitoring) if monitoring else 'Prometheus, Grafana, Custom metrics, Health checks'
        enhanced_tags['logging'] = 'Centralized logging (ELK/Splunk), Structured logs, Log aggregation'
        enhanced_tags['alerting'] = 'Prometheus Alertmanager, PagerDuty, Custom alerts, SLA monitoring'
        enhanced_tags['observability'] = 'Metrics (RED/USE), Logs, Distributed tracing (Jaeger/Zipkin)'

        # === 部署 ===
        deployment = []
        if 'kubernetes' in content_lower or 'k8s' in content_lower:
            deployment.append('Kubernetes')
        if 'docker' in content_lower:
            deployment.append('Docker')
        if 'cloud' in content_lower:
            deployment.append('Cloud-native')

        enhanced_tags['deployment'] = ', '.join(deployment) if deployment else 'Kubernetes, Docker, Cloud-native, Blue-Green deployment'
        enhanced_tags['infrastructure'] = 'Cloud, On-premise, Hybrid, Multi-cloud'

        # 云服务商
        cloud_providers = []
        if 'aws' in content_lower:
            cloud_providers.append('AWS')
        if 'azure' in content_lower:
            cloud_providers.append('Azure')
        if 'gcp' in content_lower or 'google cloud' in content_lower:
            cloud_providers.append('GCP')
        if 'alibaba' in content_lower:
            cloud_providers.append('Alibaba Cloud')

        enhanced_tags['cloud-provider'] = ', '.join(cloud_providers) if cloud_providers else 'AWS, Azure, GCP, Cloud-agnostic'

        # 容器化
        if 'kubernetes' in content_lower:
            enhanced_tags['containerization'] = 'Docker, Kubernetes (StatefulSets, Deployments), Helm charts'
        elif 'docker' in content_lower:
            enhanced_tags['containerization'] = 'Docker, Docker Compose'
        else:
            enhanced_tags['containerization'] = 'Docker-ready, Container-friendly'

        # === 成本 ===
        enhanced_tags['cost-factors'] = 'Compute instances, Storage costs, Network bandwidth, Licensing'
        enhanced_tags['cost-optimization'] = 'Reserved instances, Auto-scaling, Storage tiering, Compression, Resource right-sizing'
        enhanced_tags['resource-usage'] = 'CPU: Medium-High, Memory: Medium-High, Disk I/O: High, Network: Medium'

        # === 复杂度 ===
        # 根据文件名和内容判断复杂度
        if any(x in filename for x in ['distributed', 'consensus', 'blockchain', 'saga']):
            enhanced_tags['complexity'] = 'Very High'
            enhanced_tags['implementation-difficulty'] = 'High to Very High'
            enhanced_tags['maintenance-complexity'] = 'High'
        elif any(x in filename for x in ['microservice', 'cluster', 'replication', 'sharding']):
            enhanced_tags['complexity'] = 'High'
            enhanced_tags['implementation-difficulty'] = 'Medium to High'
            enhanced_tags['maintenance-complexity'] = 'Medium to High'
        elif any(x in filename for x in ['cache', 'load_balanc', 'gateway']):
            enhanced_tags['complexity'] = 'Medium'
            enhanced_tags['implementation-difficulty'] = 'Medium'
            enhanced_tags['maintenance-complexity'] = 'Medium'
        else:
            enhanced_tags['complexity'] = 'Medium'
            enhanced_tags['implementation-difficulty'] = 'Medium'
            enhanced_tags['maintenance-complexity'] = 'Medium'

        # === 学习 ===
        if enhanced_tags['complexity'] == 'Very High':
            enhanced_tags['difficulty-level'] = 'Expert'
            enhanced_tags['learning-value'] = 'Very High (advanced distributed systems concepts)'
        elif enhanced_tags['complexity'] == 'High':
            enhanced_tags['difficulty-level'] = 'Advanced'
            enhanced_tags['learning-value'] = 'High (important architectural patterns)'
        elif enhanced_tags['complexity'] == 'Medium':
            enhanced_tags['difficulty-level'] = 'Intermediate'
            enhanced_tags['learning-value'] = 'Medium to High (practical system design)'
        else:
            enhanced_tags['difficulty-level'] = 'Beginner to Intermediate'
            enhanced_tags['learning-value'] = 'Medium (fundamental concepts)'

        # 前置知识
        prerequisites = []
        if 'distributed' in content_lower:
            prerequisites.append('Distributed systems basics')
        if 'microservice' in content_lower:
            prerequisites.append('Microservices architecture')
        if 'kafka' in content_lower or 'message' in content_lower:
            prerequisites.append('Message queues, Pub-Sub pattern')
        if 'database' in content_lower:
            prerequisites.append('Database fundamentals, SQL/NoSQL')
        if 'kubernetes' in content_lower:
            prerequisites.append('Containerization, Orchestration')

        enhanced_tags['prerequisites'] = ', '.join(prerequisites) if prerequisites else 'Basic system design, Networking, Data structures'

        # 相关概念
        related = []
        if 'consistency' in content_lower or 'cap' in content_lower:
            related.append('CAP theorem')
        if 'replica' in content_lower:
            related.append('Replication strategies')
        if 'partition' in content_lower or 'shard' in content_lower:
            related.append('Data partitioning')
        if 'event' in content_lower:
            related.append('Event sourcing, CQRS')
        if 'cache' in content_lower:
            related.append('Caching strategies, Cache invalidation')

        enhanced_tags['related-concepts'] = ', '.join(related) if related else 'Scalability, High availability, Fault tolerance, Load balancing'

        # === 数据特征 ===
        if 'big data' in content_lower or 'petabyte' in content_lower:
            enhanced_tags['data-volume'] = 'Very Large (PBs)'
        elif 'terabyte' in content_lower or 'large' in content_lower:
            enhanced_tags['data-volume'] = 'Large (TBs)'
        else:
            enhanced_tags['data-volume'] = 'Medium to Large (GBs to TBs)'

        # 数据速度
        if 'real-time' in content_lower or 'streaming' in content_lower:
            enhanced_tags['data-velocity'] = 'Real-time, High-speed streaming'
        elif 'batch' in content_lower:
            enhanced_tags['data-velocity'] = 'Batch processing, Scheduled'
        else:
            enhanced_tags['data-velocity'] = 'Near real-time, Mixed batch and streaming'

        # 数据多样性
        data_variety = []
        if 'json' in content_lower:
            data_variety.append('JSON')
        if 'avro' in content_lower:
            data_variety.append('Avro')
        if 'protobuf' in content_lower:
            data_variety.append('Protobuf')
        if 'xml' in content_lower:
            data_variety.append('XML')

        enhanced_tags['data-variety'] = ', '.join(data_variety) if data_variety else 'Structured, Semi-structured (JSON, Avro)'
        enhanced_tags['data-model'] = 'Document, Key-Value, Relational, Time-series'

        # === 集成 ===
        enhanced_tags['integration-points'] = 'REST APIs, Message queues, Database connectors, Webhooks'

        # 第三方服务
        third_party = []
        if 's3' in content_lower:
            third_party.append('AWS S3')
        if 'cloudflare' in content_lower:
            third_party.append('Cloudflare')
        if 'stripe' in content_lower or 'payment' in content_lower:
            third_party.append('Payment gateways (Stripe, PayPal)')
        if 'twilio' in content_lower:
            third_party.append('Twilio')

        enhanced_tags['third-party-services'] = ', '.join(third_party) if third_party else 'Cloud storage, CDN, Payment processors, Analytics services'

        # 外部依赖
        dependencies = []
        if 'zookeeper' in content_lower:
            dependencies.append('ZooKeeper')
        if 'etcd' in content_lower:
            dependencies.append('etcd')
        if 'consul' in content_lower:
            dependencies.append('Consul')

        enhanced_tags['external-dependencies'] = ', '.join(dependencies) if dependencies else 'Minimal external dependencies'

        # === 测试 ===
        enhanced_tags['testing-strategy'] = 'Unit tests, Integration tests, Load tests, Chaos engineering'
        enhanced_tags['quality-assurance'] = 'CI/CD pipelines, Code review, Static analysis, Performance testing'

        # === 版本 ===
        enhanced_tags['version'] = '1.0 (current design)'
        enhanced_tags['maturity'] = 'Production-ready, Battle-tested'
        enhanced_tags['evolution-stage'] = 'Active development, Continuous improvement'

        # === 关联 ===
        enhanced_tags['related-files'] = 'See other architecture diagrams in the same directory'
        enhanced_tags['alternatives'] = 'Multiple implementation approaches available'
        enhanced_tags['comparison-with'] = 'Traditional monolithic vs distributed approaches'

        # === 实战 ===
        # 真实案例
        real_world = []
        if 'kafka' in content_lower:
            real_world.append('LinkedIn, Netflix, Uber, Airbnb')
        elif 'microservice' in content_lower:
            real_world.append('Netflix, Amazon, Uber, Spotify')
        elif 'kubernetes' in content_lower:
            real_world.append('Google, Spotify, Pinterest')
        elif 'payment' in content_lower:
            real_world.append('Stripe, PayPal, Square')
        elif 'ecommerce' in content_lower or 'e-commerce' in content_lower:
            real_world.append('Amazon, Alibaba, eBay')

        enhanced_tags['real-world-examples'] = ', '.join(real_world) if real_world else 'Fortune 500 companies, Tech unicorns, Large-scale enterprises'
        enhanced_tags['companies-using'] = ', '.join(real_world) if real_world else 'Many Fortune 500 companies, Tech giants, Startups'
        enhanced_tags['production-readiness'] = 'Production-ready, Battle-tested at scale, Enterprise-grade'

        return enhanced_tags

    def generate_enhanced_metadata(self, tags: Dict[str, str]) -> str:
        """生成增强版元数据字符串"""
        metadata = "' ==================== Enhanced Metadata ====================\n"

        # === 基础分类 ===
        metadata += "' === 基础分类 ===\n"
        metadata += f"' @category: {tags['category']}\n"
        metadata += f"' @subcategory: {tags['subcategory']}\n"
        metadata += f"' @tags: {tags['tags']}\n"
        metadata += f"' @description: {tags['description']}\n"
        metadata += "'\n"

        # === 应用场景 ===
        metadata += "' === 应用场景 ===\n"
        metadata += f"' @application: {tags['application']}\n"
        metadata += f"' @industry: {tags['industry']}\n"
        metadata += f"' @use-cases: {tags['use-cases']}\n"
        metadata += f"' @business-value: {tags['business-value']}\n"
        metadata += "'\n"

        # === 技术栈 ===
        metadata += "' === 技术栈 ===\n"
        metadata += f"' @tech-stack: {tags['tech-stack']}\n"
        metadata += f"' @programming-languages: {tags['programming-languages']}\n"
        metadata += f"' @frameworks: {tags['frameworks']}\n"
        metadata += f"' @protocols: {tags['protocols']}\n"
        metadata += f"' @apis: {tags['apis']}\n"
        metadata += "'\n"

        # === 架构模式 ===
        metadata += "' === 架构模式 ===\n"
        metadata += f"' @pattern: {tags['pattern']}\n"
        metadata += f"' @design-pattern: {tags['design-pattern']}\n"
        metadata += f"' @data-flow: {tags['data-flow']}\n"
        metadata += f"' @communication-style: {tags['communication-style']}\n"
        metadata += "'\n"

        # === 分布式特性 ===
        metadata += "' === 分布式特性 ===\n"
        metadata += f"' @cap-focus: {tags['cap-focus']}\n"
        metadata += f"' @consistency-model: {tags['consistency-model']}\n"
        metadata += f"' @consensus-algorithm: {tags['consensus-algorithm']}\n"
        metadata += f"' @partition-strategy: {tags['partition-strategy']}\n"
        metadata += "'\n"

        # === 性能与扩展 ===
        metadata += "' === 性能与扩展 ===\n"
        metadata += f"' @scale: {tags['scale']}\n"
        metadata += f"' @scalability: {tags['scalability']}\n"
        metadata += f"' @performance-metrics: {tags['performance-metrics']}\n"
        metadata += f"' @optimization-techniques: {tags['optimization-techniques']}\n"
        metadata += f"' @throughput: {tags['throughput']}\n"
        metadata += f"' @latency: {tags['latency']}\n"
        metadata += "'\n"

        # === 可靠性 ===
        metadata += "' === 可靠性 ===\n"
        metadata += f"' @reliability: {tags['reliability']}\n"
        metadata += f"' @fault-tolerance: {tags['fault-tolerance']}\n"
        metadata += f"' @disaster-recovery: {tags['disaster-recovery']}\n"
        metadata += f"' @availability: {tags['availability']}\n"
        metadata += f"' @data-durability: {tags['data-durability']}\n"
        metadata += "'\n"

        # === 安全性 ===
        metadata += "' === 安全性 ===\n"
        metadata += f"' @security-features: {tags['security-features']}\n"
        metadata += f"' @authentication: {tags['authentication']}\n"
        metadata += f"' @authorization: {tags['authorization']}\n"
        metadata += f"' @encryption: {tags['encryption']}\n"
        metadata += f"' @compliance: {tags['compliance']}\n"
        metadata += "'\n"

        # === 存储 ===
        metadata += "' === 存储 ===\n"
        metadata += f"' @storage-type: {tags['storage-type']}\n"
        metadata += f"' @database-type: {tags['database-type']}\n"
        metadata += f"' @caching-strategy: {tags['caching-strategy']}\n"
        metadata += f"' @data-persistence: {tags['data-persistence']}\n"
        metadata += "'\n"

        # === 监控运维 ===
        metadata += "' === 监控运维 ===\n"
        metadata += f"' @monitoring: {tags['monitoring']}\n"
        metadata += f"' @logging: {tags['logging']}\n"
        metadata += f"' @alerting: {tags['alerting']}\n"
        metadata += f"' @observability: {tags['observability']}\n"
        metadata += "'\n"

        # === 部署 ===
        metadata += "' === 部署 ===\n"
        metadata += f"' @deployment: {tags['deployment']}\n"
        metadata += f"' @infrastructure: {tags['infrastructure']}\n"
        metadata += f"' @cloud-provider: {tags['cloud-provider']}\n"
        metadata += f"' @containerization: {tags['containerization']}\n"
        metadata += "'\n"

        # === 成本 ===
        metadata += "' === 成本 ===\n"
        metadata += f"' @cost-factors: {tags['cost-factors']}\n"
        metadata += f"' @cost-optimization: {tags['cost-optimization']}\n"
        metadata += f"' @resource-usage: {tags['resource-usage']}\n"
        metadata += "'\n"

        # === 复杂度 ===
        metadata += "' === 复杂度 ===\n"
        metadata += f"' @complexity: {tags['complexity']}\n"
        metadata += f"' @implementation-difficulty: {tags['implementation-difficulty']}\n"
        metadata += f"' @maintenance-complexity: {tags['maintenance-complexity']}\n"
        metadata += "'\n"

        # === 学习 ===
        metadata += "' === 学习 ===\n"
        metadata += f"' @difficulty-level: {tags['difficulty-level']}\n"
        metadata += f"' @learning-value: {tags['learning-value']}\n"
        metadata += f"' @prerequisites: {tags['prerequisites']}\n"
        metadata += f"' @related-concepts: {tags['related-concepts']}\n"
        metadata += "'\n"

        # === 数据特征 ===
        metadata += "' === 数据特征 ===\n"
        metadata += f"' @data-volume: {tags['data-volume']}\n"
        metadata += f"' @data-velocity: {tags['data-velocity']}\n"
        metadata += f"' @data-variety: {tags['data-variety']}\n"
        metadata += f"' @data-model: {tags['data-model']}\n"
        metadata += "'\n"

        # === 集成 ===
        metadata += "' === 集成 ===\n"
        metadata += f"' @integration-points: {tags['integration-points']}\n"
        metadata += f"' @third-party-services: {tags['third-party-services']}\n"
        metadata += f"' @external-dependencies: {tags['external-dependencies']}\n"
        metadata += "'\n"

        # === 测试 ===
        metadata += "' === 测试 ===\n"
        metadata += f"' @testing-strategy: {tags['testing-strategy']}\n"
        metadata += f"' @quality-assurance: {tags['quality-assurance']}\n"
        metadata += "'\n"

        # === 版本 ===
        metadata += "' === 版本 ===\n"
        metadata += f"' @version: {tags['version']}\n"
        metadata += f"' @maturity: {tags['maturity']}\n"
        metadata += f"' @evolution-stage: {tags['evolution-stage']}\n"
        metadata += "'\n"

        # === 关联 ===
        metadata += "' === 关联 ===\n"
        metadata += f"' @related-files: {tags['related-files']}\n"
        metadata += f"' @alternatives: {tags['alternatives']}\n"
        metadata += f"' @comparison-with: {tags['comparison-with']}\n"
        metadata += "'\n"

        # === 实战 ===
        metadata += "' === 实战 ===\n"
        metadata += f"' @real-world-examples: {tags['real-world-examples']}\n"
        metadata += f"' @companies-using: {tags['companies-using']}\n"
        metadata += f"' @production-readiness: {tags['production-readiness']}\n"
        metadata += "' ==================================================\n"

        return metadata

    def process_file(self, filepath: Path) -> bool:
        """处理单个PUML文件"""
        try:
            # 读取文件
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # 提取现有元数据和图表内容
            existing_metadata, title, diagram_content = self.extract_metadata(content)

            # 分析并生成增强标签
            enhanced_tags = self.analyze_file_content(filepath, existing_metadata, diagram_content)

            # 生成增强元数据
            new_metadata = self.generate_enhanced_metadata(enhanced_tags)

            # 构建新文件内容
            new_content = f"@startuml {title}\n{new_metadata}\n{diagram_content}"

            # 写回文件
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)

            self.processed_count += 1
            print(f"✓ 已处理: {filepath.name}")
            return True

        except Exception as e:
            print(f"✗ 错误处理 {filepath}: {str(e)}")
            self.error_files.append((str(filepath), str(e)))
            return False

    def process_all_files(self):
        """处理所有PUML文件"""
        puml_files = list(self.base_dir.rglob("*.puml"))
        total_files = len(puml_files)

        print(f"\n开始处理 {total_files} 个PUML文件...\n")

        for filepath in puml_files:
            # 跳过common_style.puml（工具文件）
            if filepath.name == 'common_style.puml':
                print(f"⊘ 跳过工具文件: {filepath.name}")
                continue

            self.process_file(filepath)

        # 打印总结
        print(f"\n{'='*60}")
        print(f"处理完成！")
        print(f"总文件数: {total_files}")
        print(f"成功处理: {self.processed_count}")
        print(f"失败/跳过: {len(self.error_files)}")

        if self.error_files:
            print(f"\n失败的文件:")
            for filepath, error in self.error_files:
                print(f"  - {filepath}: {error}")

def main():
    base_dir = "/Users/huangyingw/Dropbox/myproject/git/system_design/worktrees/puml-categorize-deduplicate"
    enhancer = PumlEnhancer(base_dir)
    enhancer.process_all_files()

if __name__ == "__main__":
    main()
