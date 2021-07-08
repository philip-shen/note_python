from diagrams import Diagram, Cluster

# onprem
from diagrams.onprem.analytics import Beam, Databricks, Dbt, Flink, Hadoop, Hive, Metabase, Norikra, Singer, Spark, Storm, Tableau
from diagrams.onprem.cd import Spinnaker, TektonCli, Tekton
from diagrams.onprem.ci import Circleci, Concourseci, Droneci, Gitlabci, Jenkins, Teamcity, Travisci, Zuulci
from diagrams.onprem.client import Client, User, Users
from diagrams.onprem.compute import Nomad, Server
from diagrams.onprem.container import Rkt, Docker
from diagrams.onprem.database import Scylla, Postgresql, Oracle, Neo4J, Mysql, Mssql, Mongodb, Mariadb, Janusgraph, Influxdb, Hbase, Druid, Dgraph, Couchdb, Couchbase, Cockroachdb, Clickhouse, Cassandra
from diagrams.onprem.etl import Embulk
from diagrams.onprem.gitops import Flux, Flagger, Argocd
from diagrams.onprem.iac import Terraform, Awx, Atlantis, Ansible
from diagrams.onprem.inmemory import Redis, Memcached, Hazelcast, Aerospike
from diagrams.onprem.logging import SyslogNg, Rsyslog, Loki, Graylog, Fluentd, Fluentbit
from diagrams.onprem.mlops import Polyaxon
from diagrams.onprem.monitoring import Thanos, Splunk, Sentry, Prometheus, PrometheusOperator, Grafana, Datadog
from diagrams.onprem.network import Zookeeper, Vyos, Traefik, Tomcat, Pomerium, Pfsense, Nginx, Linkerd, Kong, Istio, Internet, Haproxy, Etcd, Envoy, Consul, Caddy, Apache
from diagrams.onprem.queue import Zeromq, Rabbitmq, Kafka, Celery, Activemq
from diagrams.onprem.search import Solr
from diagrams.onprem.security import Vault, Trivy
from diagrams.onprem.vcs import Gitlab, Github, Git
from diagrams.onprem.workflow import Nifi, Kubeflow, Digdag, Airflow

# aws
from diagrams.aws.analytics import Analytics, Athena, Cloudsearch, CloudsearchSearchDocuments, DataPipeline, EMR, EMRCluster, EMRHdfsCluster, ElasticsearchService, Glue, GlueCrawlers, GlueDataCatalog, Kinesis, KinesisDataAnalytics, KinesisDataFirehose, KinesisDataStreams, KinesisVideoStreams, LakeFormation, ManagedStreamingForKafka, Quicksight, RedshiftDenseComputeNode, RedshiftDenseStorageNode, Redshift
from diagrams.aws.ar import Sumerian
from diagrams.aws.blockchain import QuantumLedgerDatabaseQldb, ManagedBlockchain
from diagrams.aws.business import Workmail, Chime, AlexaForBusiness
from diagrams.aws.compute import VmwareCloudOnAWS, ThinkboxXmesh, ThinkboxStoke, ThinkboxSequoia, ThinkboxKrakatoa, ThinkboxFrost, ThinkboxDraft, ThinkboxDeadline, ServerlessApplicationRepository, Outposts, Lightsail, Lambda, Fargate, ElasticKubernetesService, ElasticContainerService, ElasticBeanstalk, EC2, EC2ContainerRegistry, Compute, Batch, ApplicationAutoScaling
from diagrams.aws.cost import SavingsPlans, ReservedInstanceReporting, CostExplorer, CostAndUsageReport, Budgets
from diagrams.aws.database import Timestream, Redshift, RDS, RDSOnVmware, QuantumLedgerDatabaseQldb, Neptune, Elasticache, Dynamodb, DynamodbTable, DynamodbGlobalSecondaryIndex, DynamodbDax, DocumentdbMongodbCompatibility, Database, DatabaseMigrationService, Aurora
from diagrams.aws.devtools import XRay, ToolsAndSdks, DeveloperTools, CommandLineInterface, Codestar, Codepipeline, Codedeploy, Codecommit, Codebuild, Cloud9, CloudDevelopmentKit
from diagrams.aws.enablement import Support, ProfessionalServices, ManagedServices, Iq
from diagrams.aws.enduser import Workspaces, Worklink, Workdocs, Appstream20
from diagrams.aws.engagement import SimpleEmailServiceSes, Pinpoint, Connect
from diagrams.aws.game import Gamelift
from diagrams.aws.general import Users, User, TradicionalServer, Marketplace, GenericSDK, GenericSamlToken, GenericOfficeBuilding, GenericFirewall, GenericDatabase, General, Disk
from diagrams.aws.integration import StepFunctions, SimpleQueueServiceSqs, SimpleNotificationServiceSns, MQ, Eventbridge, ConsoleMobileApplication, Appsync, ApplicationIntegration
from diagrams.aws.iot import IotTopic, IotThingsGraph, IotSitewise, IotShadow, IotRule, IotPolicy, IotPolicyEmergency, IotMqtt, IotLambda, IotJobs, IotHttp2, IotHttp, IotHardwareBoard, IotGreengrass, IotGreengrassConnector, IotEvents, IotDeviceManagement, IotDeviceDefender, IotCore, IotCertificate, IotCamera, IotButton, IotAnalytics, IotAlexaSkill, IotAlexaEcho, IotAction, Iot1Click, InternetOfThings, Freertos
from diagrams.aws.management import WellArchitectedTool, TrustedAdvisor, SystemsManager, SystemsManagerParameterStore, ServiceCatalog, Organizations, Opsworks, ManagementConsole, ManagedServices, LicenseManager, ControlTower, Config, CommandLineInterface, Codeguru, Cloudwatch, Cloudtrail, Cloudformation, AutoScaling
from diagrams.aws.media import ElementalServer, ElementalMediatailor, ElementalMediastore, ElementalMediapackage, ElementalMedialive, ElementalMediaconvert, ElementalMediaconnect, ElementalLive, ElementalDelta, ElementalConductor, ElasticTranscoder
from diagrams.aws.migration import TransferForSftp, Snowmobile, Snowball, SnowballEdge, ServerMigrationService, MigrationHub, MigrationAndTransfer, Datasync, DatabaseMigrationService, CloudendureMigration, ApplicationDiscoveryService
from diagrams.aws.ml import Translate, Transcribe, Textract, TensorflowOnAWS, Sagemaker, SagemakerTrainingJob, SagemakerNotebook, SagemakerModel, SagemakerGroundTruth, Rekognition, Polly, Personalize, MachineLearning, Lex, Forecast, ElasticInference, Deepracer, Deeplens, DeepLearningContainers, DeepLearningAmis, Comprehend, ApacheMxnetOnAWS
from diagrams.aws.mobile import Pinpoint, DeviceFarm, Appsync, APIGateway, APIGatewayEndpoint, Amplify
from diagrams.aws.network import VPC, VPCRouter, VPCPeering, TransitGateway, SiteToSiteVpn, RouteTable, Route53, PublicSubnet, Privatelink, PrivateSubnet, NetworkingAndContentDelivery, NATGateway, Nacl, InternetGateway, GlobalAccelerator, Endpoint, ElasticLoadBalancing, DirectConnect, CloudFront, CloudMap, ClientVpn, AppMesh, APIGateway
from diagrams.aws.quantum import Braket
from diagrams.aws.robotics import Robotics, Robomaker, RobomakerSimulator
from diagrams.aws.satellite import GroundStation
from diagrams.aws.security import WAF, SingleSignOn, Shield, SecurityIdentityAndCompliance, SecurityHub, SecretsManager, ResourceAccessManager, Macie, KeyManagementService, Inspector, IdentityAndAccessManagementIam, IdentityAndAccessManagementIamRole, IdentityAndAccessManagementIamPermissions, IdentityAndAccessManagementIamAWSSts, IdentityAndAccessManagementIamAccessAnalyzer, Guardduty, FirewallManager, DirectoryService, Detective, Cognito, Cloudhsm, CloudDirectory, CertificateManager, Artifact
from diagrams.aws.storage import Storage, StorageGateway, Snowmobile, Snowball, SnowballEdge, SimpleStorageServiceS3, S3Glacier, Fsx, FsxForWindowsFileServer, FsxForLustre, ElasticFileSystemEFS, ElasticBlockStoreEBS, EFSStandardPrimaryBg, EFSInfrequentaccessPrimaryBg, CloudendureDisasterRecovery, Backup

# azure
from diagrams.azure.analytics import StreamAnalyticsJobs, LogAnalyticsWorkspaces, Hdinsightclusters, EventHubs, EventHubClusters, Databricks, DataLakeStoreGen1, DataLakeAnalytics, DataFactories, DataExplorerClusters, AnalysisServices
from diagrams.azure.compute import VM, VMWindows, VMLinux, VMImages, VMClassic, ServiceFabricClusters, SAPHANAOnAzure, MeshApplications, KubernetesServices, FunctionApps, Disks, DiskSnapshots, ContainerRegistries, ContainerInstances, CloudsimpleVirtualMachines, CloudServices, CloudServicesClassic, CitrixVirtualDesktopsEssentials, BatchAccounts, AvailabilitySets
from diagrams.azure.database import VirtualDatacenter, VirtualClusters, SQLServers, SQLServerStretchDatabases, SQLManagedInstances, SQLDatawarehouse, SQLDatabases, ManagedDatabases, ElasticJobAgents, ElasticDatabasePools, DatabaseForPostgresqlServers, DatabaseForMysqlServers, DatabaseForMariadbServers, DataLake, CosmosDb, CacheForRedis, BlobStorage
from diagrams.azure.devops import TestPlans, Repos, Pipelines, DevtestLabs, Devops, Boards, Artifacts, ApplicationInsights
from diagrams.azure.general import Whatsnew, Userresource, Userprivacy, Usericon, Userhealthicon, Twousericon, Templates, Tags, Tag, Supportrequests, Support, Subscriptions, Shareddashboard, Servicehealth, Resourcegroups, Resource, Reservations, Recent, Quickstartcenter, Marketplace, Managementgroups, Information, Helpsupport, Developertools, Azurehome, Allresources
from diagrams.azure.identity import ManagedIdentities, InformationProtection, IdentityGovernance, EnterpriseApplications, ConditionalAccess, AppRegistrations, ADPrivilegedIdentityManagement, ADIdentityProtection, ADDomainServices, ADB2C, ActiveDirectory, ActiveDirectoryConnectHealth, AccessReview
from diagrams.azure.integration import StorsimpleDeviceManagers, SoftwareAsAService, ServiceCatalogManagedApplicationDefinitions, ServiceBus, ServiceBusRelays, SendgridAccounts, LogicApps, LogicAppsCustomConnector, IntegrationServiceEnvironments, IntegrationAccounts, EventGridTopics, EventGridSubscriptions, EventGridDomains, DataCatalog, AppConfiguration, APIManagement, APIForFhir
from diagrams.azure.iot import Windows10IotCoreServices, TimeSeriesInsightsEventsSources, TimeSeriesInsightsEnvironments, Sphere, Maps, IotHub, IotHubSecurity, IotCentralApplications, DigitalTwins, DeviceProvisioningServices
from diagrams.azure.migration import RecoveryServicesVaults, MigrationProjects, DatabaseMigrationServices
from diagrams.azure.ml import MachineLearningStudioWorkspaces, MachineLearningStudioWebServices, MachineLearningStudioWebServicePlans, MachineLearningServiceWorkspaces, GenomicsAccounts, CognitiveServices, BotServices, BatchAI
from diagrams.azure.mobile import NotificationHubs, MobileEngagement, AppServiceMobile
from diagrams.azure.network import VirtualWans, VirtualNetworks, VirtualNetworkGateways, VirtualNetworkClassic, TrafficManagerProfiles, ServiceEndpointPolicies, RouteTables, RouteFilters, ReservedIpAddressesClassic, PublicIpAddresses, OnPremisesDataGateways, NetworkWatcher, NetworkSecurityGroupsClassic, NetworkInterfaces, LocalNetworkGateways, LoadBalancers, FrontDoors, Firewall, ExpressrouteCircuits, DNSZones, DNSPrivateZones, DDOSProtectionPlans, Connections, CDNProfiles, ApplicationSecurityGroups, ApplicationGateway
from diagrams.azure.security import Sentinel, SecurityCenter, KeyVaults
from diagrams.azure.storage import TableStorage, StorsimpleDeviceManagers, StorsimpleDataManagers, StorageSyncServices, StorageExplorer, StorageAccounts, StorageAccountsClassic, QueuesStorage, NetappFiles, GeneralStorage, DataLakeStorage, DataBox, DataBoxEdgeDataBoxGateway, BlobStorage, Azurefxtedgefiler, ArchiveStorage
from diagrams.azure.web import Signalr, Search, NotificationHubNamespaces, MediaServices, AppServices, AppServicePlans, AppServiceEnvironments, AppServiceDomains, AppServiceCertificates, APIConnections

# Programming
from diagrams.programming.framework import Vue, Spring, React, Rails, Laravel, Flutter, Flask, Ember, Django, Backbone, Angular
from diagrams.programming.language import Typescript, Swift, Rust, Ruby, R, Python, Php, Nodejs, Matlab, Kotlin, Javascript, Java, Go, Dart, Csharp, Cpp, C, Bash

# Saas
from diagrams.saas.alerting import Pushover, Opsgenie
from diagrams.saas.analytics import Stitch, Snowflake
from diagrams.saas.cdn import Cloudflare
from diagrams.saas.chat import Telegram, Slack
from diagrams.saas.identity import Okta, Auth0
from diagrams.saas.logging import Papertrail, Datadog
from diagrams.saas.media import Cloudinary
from diagrams.saas.recommendation import Recombee
from diagrams.saas.social import Twitter, Facebook

# Generic
from diagrams.generic.database import SQL
from diagrams.generic.device import Tablet, Mobile
from diagrams.generic.network import VPN, Switch, Router, Firewall
from diagrams.generic.os import Windows, Ubuntu, Suse, LinuxGeneral, IOS, Centos, Android
from diagrams.generic.place import Datacenter
from diagrams.generic.storage import Storage
from diagrams.generic.virtualization import XEN, Vmware, Virtualbox

# Elastic
from diagrams.elastic.elasticsearch import Sql, SecuritySettings, Monitoring, Maps, MachineLearning, Logstash, Kibana, Elasticsearch, Beats, Alerting
from diagrams.elastic.enterprisesearch import WorkplaceSearch, SiteSearch, EnterpriseSearch, AppSearch
from diagrams.elastic.observability import Uptime, Observability, Metrics, Logs, APM
from diagrams.elastic.orchestration import ECK, ECE
from diagrams.elastic.saas import Elastic, Cloud
from diagrams.elastic.security import SIEM, Security, Endpoint

# # Outscale
# from diagrams.outscale.compute import DirectConnect, Compute
# from diagrams.outscale.network import SiteToSiteVpng, Net, NatService, LoadBalancer, InternetService, ClientVpn
# from diagrams.outscale.security import IdentityAndAccessManagement, Firewall
# from diagrams.outscale.storage import Storage, SimpleStorageService

# Firebase
from diagrams.firebase.base import Firebase
from diagrams.firebase.develop import Storage, RealtimeDatabase, MLKit, Hosting, Functions, Firestore, Authentication
from diagrams.firebase.extentions import Extensions
from diagrams.firebase.grow import RemoteConfig, Predictions, Messaging, Invites, InAppMessaging, DynamicLinks, AppIndexing, ABTesting
from diagrams.firebase.quality import TestLab, PerformanceMonitoring, Crashlytics, CrashReporting, AppDistribution

# OpenStack
from diagrams.openstack.apiproxies import EC2API
from diagrams.openstack.applicationlifecycle import Solum, Murano, Masakari, Freezer
from diagrams.openstack.baremetal import Ironic, Cyborg
from diagrams.openstack.billing import Cloudkitty
from diagrams.openstack.compute import Zun, Qinling, Nova
from diagrams.openstack.containerservices import Kuryr
from diagrams.openstack.deployment import Tripleo, Kolla, Helm, Chef, Charms, Ansible
from diagrams.openstack.frontend import Horizon
from diagrams.openstack.monitoring import Telemetry, Monasca
from diagrams.openstack.multiregion import Tricircle
from diagrams.openstack.networking import Octavia, Neutron, Designate
from diagrams.openstack.nfv import Tacker
from diagrams.openstack.optimization import Watcher, Vitrage, Rally, Congress
from diagrams.openstack.orchestration import Zaqar, Senlin, Mistral, Heat, Blazar
from diagrams.openstack.packaging import RPM, Puppet, LOCI
from diagrams.openstack.sharedservices import Searchlight, Keystone, Karbor, Glance, Barbican
from diagrams.openstack.storage import Swift, Manila, Cinder
from diagrams.openstack.user import Openstackclient
from diagrams.openstack.workloadprovisioning import Trove, Sahara, Magnum

# OCI
from diagrams.oci.compute import VM, VMWhite, OKE, OKEWhite, OCIR, OCIRWhite, InstancePools, InstancePoolsWhite, Functions, FunctionsWhite, Container, ContainerWhite, BM, BMWhite, Autoscale, AutoscaleWhite
from diagrams.oci.connectivity import VPN, VPNWhite, NATGateway, NATGatewayWhite, FastConnect, FastConnectWhite, DNS, DNSWhite, DisconnectedRegions, DisconnectedRegionsWhite, CustomerPremise, CustomerPremiseWhite, CustomerDatacntrWhite, CustomerDatacenter, CDN, CDNWhite, Backbone, BackboneWhite
# from diagrams.oci.database import Stream, StreamWhite, Science, ScienceWhite, DMS, DMSWhite, Dis, DisWhite, Dcat, DcatWhite, DataflowApache, DataflowApacheWhite, DatabaseService, DatabaseServiceWhite, BigdataService, BigdataServiceWhite, Autonomous, AutonomousWhite
from diagrams.oci.devops import ResourceMgmt, ResourceMgmtWhite, APIService, APIServiceWhite, APIGateway, APIGatewayWhite
from diagrams.oci.governance import Tagging, TaggingWhite, Policies, PoliciesWhite, OCID, OCIDWhite, Logging, LoggingWhite, Groups, GroupsWhite, Compartments, CompartmentsWhite, Audit, AuditWhite
from diagrams.oci.monitoring import Workflow, WorkflowWhite, Telemetry, TelemetryWhite, Search, SearchWhite, Queue, QueueWhite, Notifications, NotificationsWhite, HealthCheck, HealthCheckWhite, Events, EventsWhite, Email, EmailWhite, Alarm, AlarmWhite
from diagrams.oci.network import Vcn, VcnWhite, ServiceGateway, ServiceGatewayWhite, SecurityLists, SecurityListsWhite, RouteTable, RouteTableWhite, LoadBalancer, LoadBalancerWhite, InternetGateway, InternetGatewayWhite, Firewall, FirewallWhite, Drg, DrgWhite
from diagrams.oci.security import WAF, WAFWhite, Vault, VaultWhite, MaxSecurityZone, MaxSecurityZoneWhite, KeyManagement, KeyManagementWhite, IDAccess, IDAccessWhite, Encryption, EncryptionWhite, DDOS, DDOSWhite, CloudGuard, CloudGuardWhite
from diagrams.oci.storage import StorageGateway, StorageGatewayWhite, ObjectStorage, ObjectStorageWhite, FileStorage, FileStorageWhite, ElasticPerformance, ElasticPerformanceWhite, DataTransfer, DataTransferWhite, Buckets, BucketsWhite, BlockStorage, BlockStorageWhite, BlockStorageClone, BlockStorageCloneWhite, BackupRestore, BackupRestoreWhite

# AlibabaCloud
from diagrams.alibabacloud.analytics import OpenSearch, ElaticMapReduce, DataLakeAnalytics, ClickHouse, AnalyticDb
from diagrams.alibabacloud.application import Yida, SmartConversationAnalysis, RdCloud, PerformanceTestingService, OpenSearch, NodeJsPerformancePlatform, MessageNotificationService, LogService, DirectMail, CodePipeline, CloudCallCenter, BlockchainAsAService, BeeBot, ApiGateway
from diagrams.alibabacloud.communication import MobilePush, DirectMail
from diagrams.alibabacloud.compute import WebAppService, SimpleApplicationServer, ServerlessAppEngine, ServerLoadBalancer, ResourceOrchestrationService, OperationOrchestrationService, FunctionCompute, ElasticSearch, ElasticHighPerformanceComputing, ElasticContainerInstance, ElasticComputeService, ContainerService, ContainerRegistry, BatchCompute, AutoScaling
from diagrams.alibabacloud.database import RelationalDatabaseService, HybriddbForMysql, GraphDatabaseService, DisributeRelationalDatabaseService, DatabaseBackupService, DataTransmissionService, DataManagementService, ApsaradbSqlserver, ApsaradbRedis, ApsaradbPpas, ApsaradbPostgresql, ApsaradbPolardb, ApsaradbOceanbase, ApsaradbMongodb, ApsaradbMemcache, ApsaradbHbase, ApsaradbCassandra
from diagrams.alibabacloud.iot import IotPlatform, IotMobileConnectionPackage, IotLinkWan, IotInternetDeviceId
from diagrams.alibabacloud.network import VpnGateway, VirtualPrivateCloud, SmartAccessGateway, ServerLoadBalancer, NatGateway, ExpressConnect, ElasticIpAddress, CloudEnterpriseNetwork, Cdn
from diagrams.alibabacloud.security import WebApplicationFirewall, SslCertificates, ServerGuard, SecurityCenter, ManagedSecurityService, IdVerification, GameShield, DbAudit, DataEncryptionService, CrowdsourcedSecurityTesting, ContentModeration, CloudSecurityScanner, CloudFirewall, BastionHost, AntifraudService, AntiDdosPro, AntiDdosBasic, AntiBotService
from diagrams.alibabacloud.storage import ObjectTableStore, ObjectStorageService, Imm, HybridCloudDisasterRecovery, HybridBackupRecovery, FileStorageNas, FileStorageHdfs, CloudStorageGateway
from diagrams.alibabacloud.web import Domain, Dns

# K8S
from diagrams.k8s.clusterconfig import Quota, Limits, HPA
from diagrams.k8s.compute import STS, RS, Pod, Job, DS, Deploy, Cronjob
from diagrams.k8s.controlplane import Sched, Kubelet, KProxy, CM, CCM, API
from diagrams.k8s.ecosystem import Kustomize, Krew, Helm
from diagrams.k8s.group import NS
from diagrams.k8s.infra import Node, Master, ETCD
from diagrams.k8s.network import SVC, Netpol, Ing, Ep
from diagrams.k8s.others import PSP, CRD
from diagrams.k8s.podconfig import Secret, CM
from diagrams.k8s.rbac import User, SA, Role, RB, Group, CRB, CRole
from diagrams.k8s.storage import Vol, SC, PVC, PV

# GCP
from diagrams.gcp.analytics import Pubsub, Genomics, Dataproc, Dataprep, Datalab, Dataflow, DataFusion, DataCatalog, Composer, Bigquery
from diagrams.gcp.compute import Run, KubernetesEngine, GPU, GKEOnPrem, Functions, ContainerOptimizedOS, ComputeEngine, AppEngine
from diagrams.gcp.database import SQL, Spanner, Memorystore, Firestore, Datastore, Bigtable
from diagrams.gcp.devtools import ToolsForVisualStudio, ToolsForPowershell, ToolsForEclipse, TestLab, Tasks, SourceRepositories, SDK, Scheduler, MavenAppEnginePlugin, IdePlugins, GradleAppEnginePlugin, ContainerRegistry, Code, CodeForIntellij, Build
from diagrams.gcp.iot import IotCore
from diagrams.gcp.migration import TransferAppliance
from diagrams.gcp.ml import VisionAPI, VideoIntelligenceAPI, TranslationAPI, TPU, TextToSpeech, SpeechToText, RecommendationsAI, NaturalLanguageAPI, JobsAPI, InferenceAPI, DialogFlowEnterpriseEdition, Automl, AutomlVision, AutomlVideoIntelligence, AutomlTranslation, AutomlTables, AutomlNaturalLanguage, AIPlatform, AIPlatformDataLabelingService, AIHub, AdvancedSolutionsLab
from diagrams.gcp.network import VPN, VirtualPrivateCloud, TrafficDirector, StandardNetworkTier, Routes, Router, PremiumNetworkTier, PartnerInterconnect, Network, NAT, LoadBalancing, FirewallRules, ExternalIpAddresses, DNS, DedicatedInterconnect, CDN, Armor
from diagrams.gcp.security import SecurityScanner, SecurityCommandCenter, ResourceManager, KeyManagementService, IAP, Iam
from diagrams.gcp.storage import Storage, PersistentDisk, Filestore

node_list_all = {
    'OnPrem': {
        'analytics': ['Beam', 'Databricks', 'Dbt', 'Flink', 'Hadoop', 'Hive', 'Metabase', 'Norikra', 'Singer', 'Spark', 'Storm', 'Tableau'],
        'cd': ['Spinnaker', 'TektonCli', 'Tekton'],
        'ci': ['Circleci', 'Concourseci', 'Droneci', 'Gitlabci', 'Jenkins', 'Teamcity', 'Travisci', 'Zuulci'],
        'client': ['Client', 'User', 'Users'],
        'compute': ['Nomad', 'Server'],
        'container': ['Rkt', 'Docker', ],
        'database': ['Scylla', 'Postgresql', 'Oracle', 'Neo4J', 'Mysql', 'Mssql', 'Mongodb', 'Mariadb', 'Janusgraph', 'Influxdb', 'Hbase', 'Druid', 'Dgraph', 'Couchdb', 'Couchbase', 'Cockroachdb', 'Clickhouse', 'Cassandra', ],
        'etl': ['Embulk', ],
        'gitops': ['Flux', 'Flagger', 'Argocd', ],
        'iac': ['Terraform', 'Awx', 'Atlantis', 'Ansible', ],
        'inmemory': ['Redis', 'Memcached', 'Hazelcast', 'Aerospike', ],
        'logging': ['SyslogNg', 'Rsyslog', 'Loki', 'Graylog', 'Fluentd', 'Fluentbit', ],
        'mlops': ['Polyaxon', ],
        'monitoring': ['Thanos', 'Splunk', 'Sentry', 'Prometheus', 'PrometheusOperator', 'Grafana', 'Datadog', ],
        'network': ['Zookeeper', 'Vyos', 'Traefik', 'Tomcat', 'Pomerium', 'Pfsense', 'Nginx', 'Linkerd', 'Kong', 'Istio', 'Internet', 'Haproxy', 'Etcd', 'Envoy', 'Consul', 'Caddy', 'Apache', ],
        'queue': ['Zeromq', 'Rabbitmq', 'Kafka', 'Celery', 'Activemq', ],
        'search': ['Solr'],
        'security': ['Vault', 'Trivy', ],
        'vcs': ['Gitlab', 'Github', 'Git', ],
        'workflow': ['Nifi', 'Kubeflow', 'Digdag', 'Airflow', ]
    },
    'AWS': {
        'analytics': ['Analytics', 'Athena', 'Cloudsearch', 'CloudsearchSearchDocuments', 'DataPipeline', 'EMR', 'EMRCluster', 'EMRHdfsCluster', 'ElasticsearchService', 'Glue', 'GlueCrawlers', 'GlueDataCatalog', 'Kinesis', 'KinesisDataAnalytics', 'KinesisDataFirehose', 'KinesisDataStreams', 'KinesisVideoStreams', 'LakeFormation', 'ManagedStreamingForKafka', 'Quicksight', 'RedshiftDenseComputeNode', 'RedshiftDenseStorageNode', 'Redshift'],
        'ar': ['Sumerian', ],
        'blockchain': ['QuantumLedgerDatabaseQldb', 'ManagedBlockchain', ],
        'business': ['Workmail', 'Chime', 'AlexaForBusiness', ],
        'compute': ['VmwareCloudOnAWS', 'ThinkboxXmesh', 'ThinkboxStoke', 'ThinkboxSequoia', 'ThinkboxKrakatoa', 'ThinkboxFrost', 'ThinkboxDraft', 'ThinkboxDeadline', 'ServerlessApplicationRepository', 'Outposts', 'Lightsail', 'Lambda', 'Fargate', 'ElasticKubernetesService', 'ElasticContainerService', 'ElasticBeanstalk', 'EC2', 'EC2ContainerRegistry', 'Compute', 'Batch', 'ApplicationAutoScaling', ],
        'cost': ['SavingsPlans', 'ReservedInstanceReporting', 'CostExplorer', 'CostAndUsageReport', 'Budgets', ],
        'database': ['Timestream', 'Redshift', 'RDS', 'RDSOnVmware', 'QuantumLedgerDatabaseQldb', 'Neptune', 'Elasticache', 'Dynamodb', 'DynamodbTable', 'DynamodbGlobalSecondaryIndex', 'DynamodbDax', 'DocumentdbMongodbCompatibility', 'Database', 'DatabaseMigrationService', 'Aurora', ],
        'devtools': ['XRay', 'ToolsAndSdks', 'DeveloperTools', 'CommandLineInterface', 'Codestar', 'Codepipeline', 'Codedeploy', 'Codecommit', 'Codebuild', 'Cloud9', 'CloudDevelopmentKit', ],
        'enablement': ['Support', 'ProfessionalServices', 'ManagedServices', 'Iq', ],
        'enduser': ['Workspaces', 'Worklink', 'Workdocs', 'Appstream20', ],
        'engagement': ['SimpleEmailServiceSes', 'Pinpoint', 'Connect', ],
        'game': ['Gamelift', ],
        'general': ['Users', 'User', 'TradicionalServer', 'Marketplace', 'GenericSDK', 'GenericSamlToken', 'GenericOfficeBuilding', 'GenericFirewall', 'GenericDatabase', 'General', 'Disk', ],
        'integration': ['StepFunctions', 'SimpleQueueServiceSqs', 'SimpleNotificationServiceSns', 'MQ', 'Eventbridge', 'ConsoleMobileApplication', 'Appsync', 'ApplicationIntegration', ],
        'iot': ['IotTopic', 'IotThingsGraph', 'IotSitewise', 'IotShadow', 'IotRule', 'IotPolicy', 'IotPolicyEmergency', 'IotMqtt', 'IotLambda', 'IotJobs', 'IotHttp2', 'IotHttp', 'IotHardwareBoard', 'IotGreengrass', 'IotGreengrassConnector', 'IotEvents', 'IotDeviceManagement', 'IotDeviceDefender', 'IotCore', 'IotCertificate', 'IotCamera', 'IotButton', 'IotAnalytics', 'IotAlexaSkill', 'IotAlexaEcho', 'IotAction', 'Iot1Click', 'InternetOfThings', 'Freertos', ],
        'management': ['WellArchitectedTool', 'TrustedAdvisor', 'SystemsManager', 'SystemsManagerParameterStore', 'ServiceCatalog', 'Organizations', 'Opsworks', 'ManagementConsole', 'ManagedServices', 'LicenseManager', 'ControlTower', 'Config', 'CommandLineInterface', 'Codeguru', 'Cloudwatch', 'Cloudtrail', 'Cloudformation', 'AutoScaling', ],
        'media': ['ElementalServer', 'ElementalMediatailor', 'ElementalMediastore', 'ElementalMediapackage', 'ElementalMedialive', 'ElementalMediaconvert', 'ElementalMediaconnect', 'ElementalLive', 'ElementalDelta', 'ElementalConductor', 'ElasticTranscoder', ],
        'migration': ['TransferForSftp', 'Snowmobile', 'Snowball', 'SnowballEdge', 'ServerMigrationService', 'MigrationHub', 'MigrationAndTransfer', 'Datasync', 'DatabaseMigrationService', 'CloudendureMigration', 'ApplicationDiscoveryService', ],
        'ml': ['Translate', 'Transcribe', 'Textract', 'TensorflowOnAWS', 'Sagemaker', 'SagemakerTrainingJob', 'SagemakerNotebook', 'SagemakerModel', 'SagemakerGroundTruth', 'Rekognition', 'Polly', 'Personalize', 'MachineLearning', 'Lex', 'Forecast', 'ElasticInference', 'Deepracer', 'Deeplens', 'DeepLearningContainers', 'DeepLearningAmis', 'Comprehend', 'ApacheMxnetOnAWS', ],
        'mobile': ['Pinpoint', 'DeviceFarm', 'Appsync', 'APIGateway', 'APIGatewayEndpoint', 'Amplify', ],
        'network': ['VPC', 'VPCRouter', 'VPCPeering', 'TransitGateway', 'SiteToSiteVpn', 'RouteTable', 'Route53', 'PublicSubnet', 'Privatelink', 'PrivateSubnet', 'NetworkingAndContentDelivery', 'NATGateway', 'Nacl', 'InternetGateway', 'GlobalAccelerator', 'Endpoint', 'ElasticLoadBalancing', 'DirectConnect', 'CloudFront', 'CloudMap', 'ClientVpn', 'AppMesh', 'APIGateway', ],
        'quantum': ['Braket', ],
        'robotics': ['Robotics', 'Robomaker', 'RobomakerSimulator', ],
        'satellite': ['GroundStation', ],
        'security': ['WAF', 'SingleSignOn', 'Shield', 'SecurityIdentityAndCompliance', 'SecurityHub', 'SecretsManager', 'ResourceAccessManager', 'Macie', 'KeyManagementService', 'Inspector', 'IdentityAndAccessManagementIam', 'IdentityAndAccessManagementIamRole', 'IdentityAndAccessManagementIamPermissions', 'IdentityAndAccessManagementIamAWSSts', 'IdentityAndAccessManagementIamAccessAnalyzer', 'Guardduty', 'FirewallManager', 'DirectoryService', 'Detective', 'Cognito', 'Cloudhsm', 'CloudDirectory', 'CertificateManager', 'Artifact', ],
        'storage': ['Storage', 'StorageGateway', 'Snowmobile', 'Snowball', 'SnowballEdge', 'SimpleStorageServiceS3', 'S3Glacier', 'Fsx', 'FsxForWindowsFileServer', 'FsxForLustre', 'ElasticFileSystemEFS', 'ElasticBlockStoreEBS', 'EFSStandardPrimaryBg', 'EFSInfrequentaccessPrimaryBg', 'CloudendureDisasterRecovery', 'Backup', ],
    },
    'Azure': {
        'analytics': ['StreamAnalyticsJobs', 'LogAnalyticsWorkspaces', 'Hdinsightclusters', 'EventHubs', 'EventHubClusters', 'Databricks', 'DataLakeStoreGen1', 'DataLakeAnalytics', 'DataFactories', 'DataExplorerClusters', 'AnalysisServices', ],
        'compute': ['VM', 'VMWindows', 'VMLinux', 'VMImages', 'VMClassic', 'ServiceFabricClusters', 'SAPHANAOnAzure', 'MeshApplications', 'KubernetesServices', 'FunctionApps', 'Disks', 'DiskSnapshots', 'ContainerRegistries', 'ContainerInstances', 'CloudsimpleVirtualMachines', 'CloudServices', 'CloudServicesClassic', 'CitrixVirtualDesktopsEssentials', 'BatchAccounts', 'AvailabilitySets', ],
        'database': ['VirtualDatacenter', 'VirtualClusters', 'SQLServers', 'SQLServerStretchDatabases', 'SQLManagedInstances', 'SQLDatawarehouse', 'SQLDatabases', 'ManagedDatabases', 'ElasticJobAgents', 'ElasticDatabasePools', 'DatabaseForPostgresqlServers', 'DatabaseForMysqlServers', 'DatabaseForMariadbServers', 'DataLake', 'CosmosDb', 'CacheForRedis', 'BlobStorage', ],
        'devops': ['TestPlans', 'Repos', 'Pipelines', 'DevtestLabs', 'Devops', 'Boards', 'Artifacts', 'ApplicationInsights', ],
        'general': ['Whatsnew', 'Userresource', 'Userprivacy', 'Usericon', 'Userhealthicon', 'Twousericon', 'Templates', 'Tags', 'Tag', 'Supportrequests', 'Support', 'Subscriptions', 'Shareddashboard', 'Servicehealth', 'Resourcegroups', 'Resource', 'Reservations', 'Recent', 'Quickstartcenter', 'Marketplace', 'Managementgroups', 'Information', 'Helpsupport', 'Developertools', 'Azurehome', 'Allresources', ],
        'identity': ['ManagedIdentities', 'InformationProtection', 'IdentityGovernance', 'EnterpriseApplications', 'ConditionalAccess', 'AppRegistrations', 'ADPrivilegedIdentityManagement', 'ADIdentityProtection', 'ADDomainServices', 'ADB2C', 'ActiveDirectory', 'ActiveDirectoryConnectHealth', 'AccessReview', ],
        'integration': ['StorsimpleDeviceManagers', 'SoftwareAsAService', 'ServiceCatalogManagedApplicationDefinitions', 'ServiceBus', 'ServiceBusRelays', 'SendgridAccounts', 'LogicApps', 'LogicAppsCustomConnector', 'IntegrationServiceEnvironments', 'IntegrationAccounts', 'EventGridTopics', 'EventGridSubscriptions', 'EventGridDomains', 'DataCatalog', 'AppConfiguration', 'APIManagement', 'APIForFhir', ],
        'iot': ['Windows10IotCoreServices', 'TimeSeriesInsightsEventsSources', 'TimeSeriesInsightsEnvironments', 'Sphere', 'Maps', 'IotHub', 'IotHubSecurity', 'IotCentralApplications', 'DigitalTwins', 'DeviceProvisioningServices', ],
        'migration': ['RecoveryServicesVaults', 'MigrationProjects', 'DatabaseMigrationServices', ],
        'ml': ['MachineLearningStudioWorkspaces', 'MachineLearningStudioWebServices', 'MachineLearningStudioWebServicePlans', 'MachineLearningServiceWorkspaces', 'GenomicsAccounts', 'CognitiveServices', 'BotServices', 'BatchAI', ],
        'mobile': ['NotificationHubs', 'MobileEngagement', 'AppServiceMobile', ],
        'network': ['VirtualWans', 'VirtualNetworks', 'VirtualNetworkGateways', 'VirtualNetworkClassic', 'TrafficManagerProfiles', 'ServiceEndpointPolicies', 'RouteTables', 'RouteFilters', 'ReservedIpAddressesClassic', 'PublicIpAddresses', 'OnPremisesDataGateways', 'NetworkWatcher', 'NetworkSecurityGroupsClassic', 'NetworkInterfaces', 'LocalNetworkGateways', 'LoadBalancers', 'FrontDoors', 'Firewall', 'ExpressrouteCircuits', 'DNSZones', 'DNSPrivateZones', 'DDOSProtectionPlans', 'Connections', 'CDNProfiles', 'ApplicationSecurityGroups', 'ApplicationGateway', ],
        'security': ['Sentinel', 'SecurityCenter', 'KeyVaults', ],
        'storage': ['TableStorage', 'StorsimpleDeviceManagers', 'StorsimpleDataManagers', 'StorageSyncServices', 'StorageExplorer', 'StorageAccounts', 'StorageAccountsClassic', 'QueuesStorage', 'NetappFiles', 'GeneralStorage', 'DataLakeStorage', 'DataBox', 'DataBoxEdgeDataBoxGateway', 'BlobStorage', 'Azurefxtedgefiler', 'ArchiveStorage', ],
        'web': ['Signalr', 'Search', 'NotificationHubNamespaces', 'MediaServices', 'AppServices', 'AppServicePlans', 'AppServiceEnvironments', 'AppServiceDomains', 'AppServiceCertificates', 'APIConnections', ]
    },
    'Saas': {
        'alerting': ['Pushover', 'Opsgenie', ],
        'analytics': ['Stitch', 'Snowflake', ],
        'cdn': ['Cloudflare', ],
        'chat': ['Telegram', 'Slack', ],
        'identity': ['Okta', 'Auth0', ],
        'logging': ['Papertrail', 'Datadog', ],
        'media': ['Cloudinary', ],
        'recommendation': ['Recombee', ],
        'social': ['Twitter', 'Facebook', ]
    },
    'Programming': {
        'framework': ['Vue', 'Spring', 'React', 'Rails', 'Laravel', 'Flutter', 'Flask', 'Ember', 'Django', 'Backbone', 'Angular', ],
        'language': ['Typescript', 'Swift', 'Rust', 'Ruby', 'R', 'Python', 'Php', 'Nodejs', 'Matlab', 'Kotlin', 'Javascript', 'Java', 'Go', 'Dart', 'Csharp', 'Cpp', 'C', 'Bash', ]
    },
    'Generic': {
        # 'blank': ['Blank', ],
        # 'compute': ['Rack', ],
        'database': ['SQL', ],
        'device': ['Tablet', 'Mobile', ],
        'network': ['VPN', 'Switch', 'Router', 'Firewall', ],
        'os': ['Windows', 'Ubuntu', 'Suse', 'LinuxGeneral', 'IOS', 'Centos', 'Android', ],
        'place': ['Datacenter', ],
        'storage': ['Storage', ],
        'virtualization': ['XEN', 'Vmware', 'Virtualbox', ],
    },
    'Elastic': {
        'elasticsearch': ['Sql', 'SecuritySettings', 'Monitoring', 'Maps', 'MachineLearning', 'Logstash', 'Kibana', 'Elasticsearch', 'Beats', 'Alerting', ],
        'enterprisesearch': ['WorkplaceSearch', 'SiteSearch', 'EnterpriseSearch', 'AppSearch', ],
        'observability': ['Uptime', 'Observability', 'Metrics', 'Logs', 'APM', ],
        'orchestration': ['ECK', 'ECE', ],
        'saas': ['Elastic', 'Cloud', ],
        'security': ['SIEM', 'Security', 'Endpoint', ],
    },
    'GCP': {
        'analytics': ['Pubsub', 'Genomics', 'Dataproc', 'Dataprep', 'Datalab', 'Dataflow', 'DataFusion', 'DataCatalog', 'Composer', 'Bigquery', ],
        'compute': ['Run', 'KubernetesEngine', 'GPU', 'GKEOnPrem', 'Functions', 'ContainerOptimizedOS', 'ComputeEngine', 'AppEngine', ],
        'database': ['SQL', 'Spanner', 'Memorystore', 'Firestore', 'Datastore', 'Bigtable', ],
        'devtools': ['ToolsForVisualStudio', 'ToolsForPowershell', 'ToolsForEclipse', 'TestLab', 'Tasks', 'SourceRepositories', 'SDK', 'Scheduler', 'MavenAppEnginePlugin', 'IdePlugins', 'GradleAppEnginePlugin', 'ContainerRegistry', 'Code', 'CodeForIntellij', 'Build', ],
        'iot': ['IotCore', ],
        'migration': ['TransferAppliance', ],
        'ml': ['VisionAPI', 'VideoIntelligenceAPI', 'TranslationAPI', 'TPU', 'TextToSpeech', 'SpeechToText', 'RecommendationsAI', 'NaturalLanguageAPI', 'JobsAPI', 'InferenceAPI', 'DialogFlowEnterpriseEdition', 'Automl', 'AutomlVision', 'AutomlVideoIntelligence', 'AutomlTranslation', 'AutomlTables', 'AutomlNaturalLanguage', 'AIPlatform', 'AIPlatformDataLabelingService', 'AIHub', 'AdvancedSolutionsLab', ],
        'network': ['VPN', 'VirtualPrivateCloud', 'TrafficDirector', 'StandardNetworkTier', 'Routes', 'Router', 'PremiumNetworkTier', 'PartnerInterconnect', 'Network', 'NAT', 'LoadBalancing', 'FirewallRules', 'ExternalIpAddresses', 'DNS', 'DedicatedInterconnect', 'CDN', 'Armor', ],
        'security': ['SecurityScanner', 'SecurityCommandCenter', 'ResourceManager', 'KeyManagementService', 'IAP', 'Iam', ],
        'storage': ['Storage', 'PersistentDisk', 'Filestore', ],
    },
    'K8S': {
        'clusterconfig': ['Quota', 'Limits', 'HPA', ],
        'compute': ['STS', 'RS', 'Pod', 'Job', 'DS', 'Deploy', 'Cronjob', ],
        'controlplane': ['Sched', 'Kubelet', 'KProxy', 'CM', 'CCM', 'API', ],
        'ecosystem': ['Kustomize', 'Krew', 'Helm', ],
        'group': ['NS', ],
        'infra': ['Node', 'Master', 'ETCD', ],
        'network': ['SVC', 'Netpol', 'Ing', 'Ep', ],
        'others': ['PSP', 'CRD', ],
        'podconfig': ['Secret', 'CM', ],
        'rbac': ['User', 'SA', 'Role', 'RB', 'Group', 'CRB', 'CRole', ],
        'storage': ['Vol', 'SC', 'PVC', 'PV', ],
    },
    'AlibabaCloud': {
        'analytics': ['OpenSearch', 'ElaticMapReduce', 'DataLakeAnalytics', 'ClickHouse', 'AnalyticDb', ],
        'application': ['Yida', 'SmartConversationAnalysis', 'RdCloud', 'PerformanceTestingService', 'OpenSearch', 'NodeJsPerformancePlatform', 'MessageNotificationService', 'LogService', 'DirectMail', 'CodePipeline', 'CloudCallCenter', 'BlockchainAsAService', 'BeeBot', 'ApiGateway', ],
        'communication': ['MobilePush', 'DirectMail', ],
        'compute': ['WebAppService', 'SimpleApplicationServer', 'ServerlessAppEngine', 'ServerLoadBalancer', 'ResourceOrchestrationService', 'OperationOrchestrationService', 'FunctionCompute', 'ElasticSearch', 'ElasticHighPerformanceComputing', 'ElasticContainerInstance', 'ElasticComputeService', 'ContainerService', 'ContainerRegistry', 'BatchCompute', 'AutoScaling', ],
        'database': ['RelationalDatabaseService', 'HybriddbForMysql', 'GraphDatabaseService', 'DisributeRelationalDatabaseService', 'DatabaseBackupService', 'DataTransmissionService', 'DataManagementService', 'ApsaradbSqlserver', 'ApsaradbRedis', 'ApsaradbPpas', 'ApsaradbPostgresql', 'ApsaradbPolardb', 'ApsaradbOceanbase', 'ApsaradbMongodb', 'ApsaradbMemcache', 'ApsaradbHbase', 'ApsaradbCassandra', ],
        'iot': ['IotPlatform', 'IotMobileConnectionPackage', 'IotLinkWan', 'IotInternetDeviceId', ],
        'network': ['VpnGateway', 'VirtualPrivateCloud', 'SmartAccessGateway', 'ServerLoadBalancer', 'NatGateway', 'ExpressConnect', 'ElasticIpAddress', 'CloudEnterpriseNetwork', 'Cdn', ],
        'security': ['WebApplicationFirewall', 'SslCertificates', 'ServerGuard', 'SecurityCenter', 'ManagedSecurityService', 'IdVerification', 'GameShield', 'DbAudit', 'DataEncryptionService', 'CrowdsourcedSecurityTesting', 'ContentModeration', 'CloudSecurityScanner', 'CloudFirewall', 'BastionHost', 'AntifraudService', 'AntiDdosPro', 'AntiDdosBasic', 'AntiBotService', ],
        'storage': ['ObjectTableStore', 'ObjectStorageService', 'Imm', 'HybridCloudDisasterRecovery', 'HybridBackupRecovery', 'FileStorageNas', 'FileStorageHdfs', 'CloudStorageGateway', ],
        'web': ['Domain', 'Dns', ],
    },
    'OCI': {
        'compute': ['VM', 'VMWhite', 'OKE', 'OKEWhite', 'OCIR', 'OCIRWhite', 'InstancePools', 'InstancePoolsWhite', 'Functions', 'FunctionsWhite', 'Container', 'ContainerWhite', 'BM', 'BMWhite', 'Autoscale', 'AutoscaleWhite', ],
        'connectivity': ['VPN', 'VPNWhite', 'NATGateway', 'NATGatewayWhite', 'FastConnect', 'FastConnectWhite', 'DNS', 'DNSWhite', 'DisconnectedRegions', 'DisconnectedRegionsWhite', 'CustomerPremise', 'CustomerPremiseWhite', 'CustomerDatacntrWhite', 'CustomerDatacenter', 'CDN', 'CDNWhite', 'Backbone', 'BackboneWhite', ],
        # 'database': ['Stream', 'StreamWhite', 'Science', 'ScienceWhite', 'DMS', 'DMSWhite', 'Dis', 'DisWhite', 'Dcat', 'DcatWhite', 'DataflowApache', 'DataflowApacheWhite', 'DatabaseService', 'DatabaseServiceWhite', 'BigdataService', 'BigdataServiceWhite', 'Autonomous', 'AutonomousWhite', ],
        'devops': ['ResourceMgmt', 'ResourceMgmtWhite', 'APIService', 'APIServiceWhite', 'APIGateway', 'APIGatewayWhite', ],
        'governance': ['Tagging', 'TaggingWhite', 'Policies', 'PoliciesWhite', 'OCID', 'OCIDWhite', 'Logging', 'LoggingWhite', 'Groups', 'GroupsWhite', 'Compartments', 'CompartmentsWhite', 'Audit', 'AuditWhite', ],
        'monitoring': ['Workflow', 'WorkflowWhite', 'Telemetry', 'TelemetryWhite', 'Search', 'SearchWhite', 'Queue', 'QueueWhite', 'Notifications', 'NotificationsWhite', 'HealthCheck', 'HealthCheckWhite', 'Events', 'EventsWhite', 'Email', 'EmailWhite', 'Alarm', 'AlarmWhite', ],
        'network': ['Vcn', 'VcnWhite', 'ServiceGateway', 'ServiceGatewayWhite', 'SecurityLists', 'SecurityListsWhite', 'RouteTable', 'RouteTableWhite', 'LoadBalancer', 'LoadBalancerWhite', 'InternetGateway', 'InternetGatewayWhite', 'Firewall', 'FirewallWhite', 'Drg', 'DrgWhite', ],
        'security': ['WAF', 'WAFWhite', 'Vault', 'VaultWhite', 'MaxSecurityZone', 'MaxSecurityZoneWhite', 'KeyManagement', 'KeyManagementWhite', 'IDAccess', 'IDAccessWhite', 'Encryption', 'EncryptionWhite', 'DDOS', 'DDOSWhite', 'CloudGuard', 'CloudGuardWhite', ],
        'storage': ['StorageGateway', 'StorageGatewayWhite', 'ObjectStorage', 'ObjectStorageWhite', 'FileStorage', 'FileStorageWhite', 'ElasticPerformance', 'ElasticPerformanceWhite', 'DataTransfer', 'DataTransferWhite', 'Buckets', 'BucketsWhite', 'BlockStorage', 'BlockStorageWhite', 'BlockStorageClone', 'BlockStorageCloneWhite', 'BackupRestore', 'BackupRestoreWhite', ],
    },
    'OpenStack': {
        'apiproxies': ['EC2API', ],
        'applicationlifecycle': ['Solum', 'Murano', 'Masakari', 'Freezer', ],
        'baremetal': ['Ironic', 'Cyborg', ],
        'billing': ['Cloudkitty', ],
        'compute': ['Zun', 'Qinling', 'Nova', ],
        'containerservices': ['Kuryr', ],
        'deployment': ['Tripleo', 'Kolla', 'Helm', 'Chef', 'Charms', 'Ansible', ],
        'frontend': ['Horizon', ],
        'monitoring': ['Telemetry', 'Monasca', ],
        'multiregion': ['Tricircle', ],
        'networking': ['Octavia', 'Neutron', 'Designate', ],
        'nfv': ['Tacker', ],
        'optimization': ['Watcher', 'Vitrage', 'Rally', 'Congress', ],
        'orchestration': ['Zaqar', 'Senlin', 'Mistral', 'Heat', 'Blazar', ],
        'packaging': ['RPM', 'Puppet', 'LOCI', ],
        'sharedservices': ['Searchlight', 'Keystone', 'Karbor', 'Glance', 'Barbican', ],
        'storage': ['Swift', 'Manila', 'Cinder', ],
        'user': ['Openstackclient', ],
        'workloadprovisioning': ['Trove', 'Sahara', 'Magnum', ],
    },
    'Firebase': {
        'base': ['Firebase', ],
        'develop': ['Storage', 'RealtimeDatabase', 'MLKit', 'Hosting', 'Functions', 'Firestore', 'Authentication', ],
        'extentions': ['Extensions', ],
        'grow': ['RemoteConfig', 'Predictions', 'Messaging', 'Invites', 'InAppMessaging', 'DynamicLinks', 'AppIndexing', 'ABTesting', ],
        'quality': ['TestLab', 'PerformanceMonitoring', 'Crashlytics', 'CrashReporting', 'AppDistribution', ],
    },
    # 'Outscale': {
    #     'compute':['Compute','DirectConnect'],
    #     'network': ['SiteToSiteVpng', 'Net', 'NatService', 'LoadBalancer', 'InternetService', 'ClientVpn', ],
    #     'security': ['IdentityAndAccessManagement', 'Firewall', ],
    #     'storage': ['Storage', 'SimpleStorageService', ],
    # }
}

graph_attr_node_resource = {
    "fontsize": "45"
}

graph_attr_node_class = {
    "fontsize": "30"
}

with Diagram('Nodes list', direction="LR"):

    for node_resource, node_resourcs_list in node_list_all.items():
        with Cluster(node_resource, graph_attr=graph_attr_node_resource):
            for node_class, node_class_list in node_resourcs_list.items():
                with Cluster(node_resource + '.' + node_class, graph_attr=graph_attr_node_class):
                    node_list = node_class_list
                    for n in range(len(node_list)):
                        node_name = node_list[n]
                        exec("{} = {}".format(
                            node_class + "_" + node_name, node_name + "('" + node_name + "')"))

                    for n in range(len(node_list)):
                        node_left = node_class + "_" + node_list[n]
                        if n != len(node_list)-1:
                            node_right = node_class + "_" + node_list[n+1]
                            exec("{} >> {}".format(node_left, node_right))