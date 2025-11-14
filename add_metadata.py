#!/usr/bin/env python3
"""
批量为 .puml 文件添加元数据标签
"""

import os
import re
from pathlib import Path

# 文件到元数据的映射
METADATA_MAP = {
    # Architecture diagrams
    "kubernetes_persistent_storage_lifecycle_with_pv_pvc_and_pod_interaction.puml": {
        "category": "container-orchestration",
        "tags": "#kubernetes, #storage, #persistent-volume",
        "application": "General",
        "tech_stack": "Kubernetes",
        "pattern": "Persistent Storage Management",
        "description": "Kubernetes存储生命周期，展示PV/PVC/Pod交互流程"
    },
    "spark_data_partitioning_and_optimization_framework.puml": {
        "category": "data-processing",
        "tags": "#spark, #data-partitioning, #optimization",
        "application": "General",
        "tech_stack": "Spark",
        "pattern": "Data Partitioning",
        "description": "Spark数据分区和优化框架，包含分区策略和数据倾斜处理"
    },
    "spark_mapreduce_comparison.puml": {
        "category": "data-processing",
        "tags": "#spark, #mapreduce, #comparison",
        "application": "General",
        "tech_stack": "Spark, MapReduce",
        "pattern": "Batch Processing",
        "description": "Spark与MapReduce对比分析，展示两种大数据处理框架的差异"
    },
    "data_storage_options_comparison_and_use_cases.puml": {
        "category": "database",
        "tags": "#database, #elasticsearch, #comparison",
        "application": "General",
        "tech_stack": "Database, Elasticsearch",
        "pattern": "Storage Selection",
        "description": "数据存储方案对比，包含数据库和Elasticsearch的应用场景"
    },
    "kafka_cluster_architecture_overview.puml": {
        "category": "message-queue",
        "tags": "#kafka, #distributed-systems, #zookeeper, #monitoring",
        "application": "General",
        "tech_stack": "Kafka, ZooKeeper, Prometheus, Grafana",
        "pattern": "Distributed Message Queue",
        "description": "Kafka集群架构概览，包含Broker、ZooKeeper、监控和安全层"
    },
    "kafka_security_architecture_with_authentication_authorization_and_encryption.puml": {
        "category": "message-queue",
        "tags": "#kafka, #security, #authentication, #encryption",
        "application": "General",
        "tech_stack": "Kafka, SSL/TLS, SASL",
        "pattern": "Security Architecture",
        "description": "Kafka安全架构，包含认证、授权和加密机制"
    },
    "kafka_cluster_monitoring_and_management_tools_with_prometheus_integration.puml": {
        "category": "monitoring",
        "tags": "#kafka, #monitoring, #prometheus, #grafana",
        "application": "General",
        "tech_stack": "Kafka, Prometheus, Grafana, JMX",
        "pattern": "Monitoring System",
        "description": "Kafka集群监控管理工具，集成Prometheus进行指标收集"
    },
    "kafka_fault_handling_and_recovery.puml": {
        "category": "message-queue",
        "tags": "#kafka, #fault-tolerance, #disaster-recovery",
        "application": "General",
        "tech_stack": "Kafka",
        "pattern": "Fault Tolerance",
        "description": "Kafka故障处理和恢复机制"
    },
    "kafka_producer_consumer_detailed_structure.puml": {
        "category": "message-queue",
        "tags": "#kafka, #producer, #consumer",
        "application": "General",
        "tech_stack": "Kafka",
        "pattern": "Message Queue",
        "description": "Kafka生产者消费者详细结构"
    },
    "kafka_data_flow_detailed_process.puml": {
        "category": "message-queue",
        "tags": "#kafka, #data-flow, #distributed-systems",
        "application": "General",
        "tech_stack": "Kafka",
        "pattern": "Message Flow",
        "description": "Kafka数据流详细处理过程"
    },
    "distributed_message_queue_system_with_producers_consumers_and_brokers.puml": {
        "category": "message-queue",
        "tags": "#message-queue, #distributed-systems, #kafka",
        "application": "General",
        "tech_stack": "Message Queue, Kafka",
        "pattern": "Distributed Message Queue",
        "description": "分布式消息队列系统，包含生产者、消费者和Broker"
    },
    "microservices_with_databases.puml": {
        "category": "microservices",
        "tags": "#microservices, #database, #distributed-systems",
        "application": "General",
        "tech_stack": "Microservices, Database",
        "pattern": "Microservices",
        "description": "微服务架构与数据库设计"
    },
    "rate_limiting_system_for_api_and_ddos_protection_with_token_and_leaky_bucket.puml": {
        "category": "security",
        "tags": "#rate-limiting, #api-gateway, #ddos-protection",
        "application": "General",
        "tech_stack": "Token Bucket, Leaky Bucket",
        "pattern": "Rate Limiting",
        "description": "API限流系统，用于DDoS防护，包含令牌桶和漏桶算法"
    },
    "database_sharding_analysis.puml": {
        "category": "database",
        "tags": "#database, #sharding, #distributed-systems",
        "application": "General",
        "tech_stack": "Database Sharding",
        "pattern": "Sharding",
        "description": "数据库分片分析"
    },
    "cap_theory_diagram_with_database_examples_and_trade_offs.puml": {
        "category": "distributed-systems",
        "tags": "#cap-theory, #distributed-systems, #database",
        "application": "General",
        "tech_stack": "Various Databases",
        "pattern": "CAP Theorem",
        "description": "CAP理论图示，包含数据库示例和权衡分析"
    },
    "spark_kubernetes_architecture.puml": {
        "category": "data-processing",
        "tags": "#spark, #kubernetes, #container-orchestration",
        "application": "General",
        "tech_stack": "Spark, Kubernetes",
        "pattern": "Container Orchestration",
        "description": "Spark在Kubernetes上的架构部署"
    },

    # Twitter
    "twitter_database_schema.puml": {
        "category": "social-media",
        "tags": "#twitter, #database, #sharding, #nosql, #redis",
        "application": "Twitter",
        "tech_stack": "NoSQL, Redis, Sharding",
        "pattern": "Distributed Database, Sharding",
        "description": "Twitter数据库架构设计，包含用户、推文、关注、评论等核心实体及分片策略"
    },
    "twitter_user_auth_service_with_oauth_jwt_2fa_and_rate_limiting.puml": {
        "category": "security",
        "tags": "#twitter, #authentication, #oauth, #jwt, #2fa, #redis",
        "application": "Twitter",
        "tech_stack": "OAuth, JWT, Redis",
        "pattern": "Authentication & Authorization",
        "description": "Twitter用户认证服务，包含OAuth、JWT、2FA和限流机制"
    },
    "twitter_social_interaction_service.puml": {
        "category": "social-media",
        "tags": "#twitter, #social-interaction, #microservices",
        "application": "Twitter",
        "tech_stack": "Microservices",
        "pattern": "Microservices",
        "description": "Twitter社交互动服务，处理点赞、评论、转发等功能"
    },
    "twitter_system_performance_bottlenecks_and_optimizations_for_high_concurrency.puml": {
        "category": "social-media",
        "tags": "#twitter, #high-concurrency, #performance-optimization, #redis, #kafka",
        "application": "Twitter",
        "tech_stack": "Redis, Kafka, CDN",
        "pattern": "High-Concurrency Optimization",
        "description": "Twitter系统性能瓶颈和高并发优化方案"
    },
    "twitter_push_notification_service.puml": {
        "category": "social-media",
        "tags": "#twitter, #push-notification, #real-time",
        "application": "Twitter",
        "tech_stack": "WebSocket, Redis, Message Queue",
        "pattern": "Push Notification",
        "description": "Twitter推送通知服务"
    },
    "timeline_update_service_detailed_architecture.puml": {
        "category": "social-media",
        "tags": "#twitter, #timeline, #redis, #kafka",
        "application": "Twitter",
        "tech_stack": "Redis, Kafka",
        "pattern": "Event-Driven",
        "description": "Twitter时间线更新服务详细架构"
    },
    "twitter_realtime_communication_service.puml": {
        "category": "real-time-communication",
        "tags": "#twitter, #websocket, #real-time, #chat",
        "application": "Twitter",
        "tech_stack": "WebSocket, Redis",
        "pattern": "Real-Time Communication",
        "description": "Twitter实时通信服务"
    },
    "twitter_comment_system_with_moderation_threading_and_real_time_updates.puml": {
        "category": "social-media",
        "tags": "#twitter, #comment-system, #moderation, #real-time",
        "application": "Twitter",
        "tech_stack": "Redis, Kafka, ML",
        "pattern": "Event-Driven, Content Moderation",
        "description": "Twitter评论系统，包含审核、线程化和实时更新"
    },
    "twitter_comment_system_with_ml_moderation_and_real_time_processing.puml": {
        "category": "social-media",
        "tags": "#twitter, #comment-system, #ml, #real-time, #kafka",
        "application": "Twitter",
        "tech_stack": "Kafka, ML, Redis",
        "pattern": "ML-Powered Moderation",
        "description": "Twitter评论系统，集成机器学习审核和实时处理"
    },

    # Telegram
    "Telegram_End_To_End_Encryption.puml": {
        "category": "security",
        "tags": "#telegram, #encryption, #security, #e2e-encryption",
        "application": "Telegram",
        "tech_stack": "Diffie-Hellman, Encryption",
        "pattern": "End-to-End Encryption",
        "description": "Telegram端到端加密架构，展示消息加密和密钥交换流程"
    },
    "Telegram_Disaster_Recovery_And_Backup.puml": {
        "category": "distributed-systems",
        "tags": "#telegram, #disaster-recovery, #backup, #fault-tolerance",
        "application": "Telegram",
        "tech_stack": "Backup Systems",
        "pattern": "Disaster Recovery",
        "description": "Telegram灾难恢复和备份系统"
    },
    "Telegram_Voice_Video_Call_WebRTC_Architecture.puml": {
        "category": "real-time-communication",
        "tags": "#telegram, #webrtc, #video-call, #voice-call",
        "application": "Telegram",
        "tech_stack": "WebRTC",
        "pattern": "Real-Time Communication",
        "description": "Telegram语音视频通话WebRTC架构"
    },
    "Telegram_Complete_Database_Schema.puml": {
        "category": "real-time-communication",
        "tags": "#telegram, #database, #schema",
        "application": "Telegram",
        "tech_stack": "Database",
        "pattern": "Database Design",
        "description": "Telegram完整数据库架构"
    },
    "Telegram_Multi_Device_Sync.puml": {
        "category": "real-time-communication",
        "tags": "#telegram, #multi-device, #sync, #distributed-systems",
        "application": "Telegram",
        "tech_stack": "Sync Protocol",
        "pattern": "Multi-Device Synchronization",
        "description": "Telegram多设备同步机制"
    },
    "Telegram_File_Transfer_And_Storage.puml": {
        "category": "distributed-file-system",
        "tags": "#telegram, #file-transfer, #storage",
        "application": "Telegram",
        "tech_stack": "File Storage",
        "pattern": "File Transfer",
        "description": "Telegram文件传输和存储系统"
    },
    "telegram_enhanced_group_chat_system_architecture.puml": {
        "category": "real-time-communication",
        "tags": "#telegram, #group-chat, #real-time, #websocket",
        "application": "Telegram",
        "tech_stack": "WebSocket, Redis",
        "pattern": "Group Chat",
        "description": "Telegram增强群聊系统架构"
    },
    "telegram_message_prioritization_and_delivery_system_with_load_balancing.puml": {
        "category": "real-time-communication",
        "tags": "#telegram, #message-queue, #load-balancing, #prioritization",
        "application": "Telegram",
        "tech_stack": "Message Queue, Load Balancer",
        "pattern": "Priority Queue",
        "description": "Telegram消息优先级和分发系统，包含负载均衡"
    },

    # IMVU
    "avatar_loading_optimization_process.puml": {
        "category": "performance-optimization",
        "tags": "#imvu, #avatar, #caching, #optimization",
        "application": "IMVU",
        "tech_stack": "Cache, Database",
        "pattern": "Caching Strategy",
        "description": "IMVU头像加载优化流程，包含缓存和元数据分析"
    },
    "imvu_data_storage_overview.puml": {
        "category": "database",
        "tags": "#imvu, #database, #storage",
        "application": "IMVU",
        "tech_stack": "Database",
        "pattern": "Data Storage",
        "description": "IMVU数据存储架构概览"
    },
    "imvu_kafka_spark_real_time_processing_for_user_activity_and_analytics.puml": {
        "category": "data-processing",
        "tags": "#imvu, #kafka, #spark, #real-time, #analytics",
        "application": "IMVU",
        "tech_stack": "Kafka, Spark",
        "pattern": "Real-Time Analytics",
        "description": "IMVU用户活动和分析的Kafka+Spark实时处理系统"
    },
    "imvu_elasticsearch_architecture_diagram.puml": {
        "category": "search-recommendation",
        "tags": "#imvu, #elasticsearch, #search",
        "application": "IMVU",
        "tech_stack": "Elasticsearch",
        "pattern": "Search System",
        "description": "IMVU Elasticsearch搜索架构"
    },

    # Seckill (闪购)
    "high_concurrency_seckill_system_backend_architecture_with_distributed_transactions_and_anti_fraud.puml": {
        "category": "ecommerce",
        "tags": "#seckill, #high-concurrency, #redis, #distributed-transaction, #anti-fraud",
        "application": "Seckill",
        "tech_stack": "Redis, Memcached, Message Queue, MongoDB, Cassandra, Elasticsearch",
        "pattern": "High-Concurrency, Distributed Transaction, CQRS",
        "description": "高并发闪购系统后端架构，包含分布式事务处理和反欺诈机制"
    },
    "database_design_nosql_sharding_caching_for_high_concurrency.puml": {
        "category": "ecommerce",
        "tags": "#seckill, #database, #nosql, #sharding, #redis",
        "application": "Seckill",
        "tech_stack": "NoSQL, Redis, Sharding",
        "pattern": "High-Concurrency Database",
        "description": "闪购系统数据库设计，包含NoSQL、分片和缓存策略"
    },
    "seckill_system_frontend_architecture_with_cdn_and_local_caching.puml": {
        "category": "ecommerce",
        "tags": "#seckill, #cdn, #caching, #frontend",
        "application": "Seckill",
        "tech_stack": "CDN, Local Cache",
        "pattern": "Frontend Optimization",
        "description": "闪购系统前端架构，包含CDN和本地缓存"
    },
    "seckill_system_data_layer_architecture_with_sharding_caching_and_consistency_management.puml": {
        "category": "ecommerce",
        "tags": "#seckill, #database, #sharding, #redis, #consistency",
        "application": "Seckill",
        "tech_stack": "Redis, Database Sharding",
        "pattern": "Data Consistency",
        "description": "闪购系统数据层架构，包含分片、缓存和一致性管理"
    },

    # Calendar
    "high_traffic_calendar_optimized_architecture.puml": {
        "category": "distributed-systems",
        "tags": "#calendar, #high-concurrency, #redis, #mongodb",
        "application": "Calendar",
        "tech_stack": "Redis, MongoDB, Load Balancer",
        "pattern": "High-Traffic System",
        "description": "高流量日历系统优化架构"
    },
    "process_modifying_recurrence_rules.puml": {
        "category": "distributed-systems",
        "tags": "#calendar, #recurrence, #algorithm",
        "application": "Calendar",
        "tech_stack": "MongoDB",
        "pattern": "Recurrence Processing",
        "description": "日历循环规则修改处理流程"
    },
    "high_traffic_calendar_mongodb_design_with_sharding_and_indexing.puml": {
        "category": "database",
        "tags": "#calendar, #mongodb, #sharding, #indexing",
        "application": "Calendar",
        "tech_stack": "MongoDB",
        "pattern": "Sharding Strategy",
        "description": "高流量日历MongoDB设计，包含分片和索引策略"
    },
    "high_traffic_calendar_backend_overview.puml": {
        "category": "distributed-systems",
        "tags": "#calendar, #backend, #microservices",
        "application": "Calendar",
        "tech_stack": "Microservices",
        "pattern": "Microservices",
        "description": "高流量日历系统后端架构概览"
    },
    "high_traffic_calendar_mongodb_architecture.puml": {
        "category": "database",
        "tags": "#calendar, #mongodb, #distributed-systems",
        "application": "Calendar",
        "tech_stack": "MongoDB",
        "pattern": "Database Architecture",
        "description": "高流量日历MongoDB架构"
    },
}


def create_metadata_comment(metadata):
    """创建元数据注释"""
    return f"""' ==================== Metadata ====================
' @category: {metadata['category']}
' @tags: {metadata['tags']}
' @application: {metadata['application']}
' @tech-stack: {metadata['tech_stack']}
' @pattern: {metadata['pattern']}
' @description: {metadata['description']}
' ==================================================
"""


def add_metadata_to_file(file_path, metadata):
    """为单个文件添加元数据"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 检查是否已经有元数据
        if '==================== Metadata ====================' in content:
            print(f"⏭️  跳过 {file_path.name} (已有元数据)")
            return False

        # 找到 @startuml 后的位置
        startuml_match = re.search(r'(@startuml[^\n]*)\n', content)
        if not startuml_match:
            print(f"❌ 错误: {file_path.name} 没有找到 @startuml")
            return False

        # 插入元数据
        startuml_line = startuml_match.group(1)
        metadata_comment = create_metadata_comment(metadata)

        new_content = content.replace(
            startuml_match.group(0),
            f"{startuml_line}\n{metadata_comment}\n"
        )

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"✅ 已处理 {file_path.name}")
        return True

    except Exception as e:
        print(f"❌ 错误处理 {file_path}: {e}")
        return False


def main():
    """主函数"""
    base_dir = Path("/Users/huangyingw/Dropbox/myproject/git/system_design")

    processed = 0
    skipped = 0
    errors = 0

    print(f"开始处理 .puml 文件...")
    print(f"基础目录: {base_dir}")
    print(f"预定义映射: {len(METADATA_MAP)} 个文件\n")

    for filename, metadata in METADATA_MAP.items():
        # 查找文件
        files = list(base_dir.rglob(filename))

        if not files:
            print(f"⚠️  未找到: {filename}")
            errors += 1
            continue

        if len(files) > 1:
            print(f"⚠️  找到多个: {filename}")
            for f in files:
                print(f"    {f}")

        # 处理第一个找到的文件
        if add_metadata_to_file(files[0], metadata):
            processed += 1
        else:
            skipped += 1

    print(f"\n" + "="*60)
    print(f"处理完成!")
    print(f"✅ 已处理: {processed} 个文件")
    print(f"⏭️  已跳过: {skipped} 个文件")
    print(f"❌ 错误: {errors} 个文件")
    print("="*60)


if __name__ == "__main__":
    main()
