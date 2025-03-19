# Log Aggregation Solution for LMS Production

This document outlines the recommended log aggregation solution for the LMS system in a production environment.

## Overview

The LMS system now has a standardized logging system with structured logging capabilities. For production environments, we recommend implementing a centralized log aggregation solution to facilitate monitoring, analysis, and troubleshooting across all components of the system.

## Recommended Solution: ELK Stack

We recommend using the ELK Stack (Elasticsearch, Logstash, Kibana) for log aggregation, with the following components:

1. **Elasticsearch**: For storing and indexing logs
2. **Logstash**: For collecting, processing, and forwarding logs
3. **Kibana**: For visualizing and searching logs
4. **Filebeat**: For collecting logs from files and forwarding them to Logstash

## Implementation Steps

### 1. Configure JSON Log Output

The LMS backend is already configured to output logs in JSON format when the `LMS_STRUCTURED_LOGGING` environment variable is set to `true`. Ensure this is enabled in production:

```bash
export LMS_STRUCTURED_LOGGING=true
export LMS_STRUCTURED_LOG_FORMAT=json
```

### 2. Install Filebeat on Application Servers

Filebeat will monitor log files and forward them to Logstash:

```bash
# Install Filebeat
curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-8.x-amd64.deb
sudo dpkg -i filebeat-8.x-amd64.deb

# Configure Filebeat
sudo nano /etc/filebeat/filebeat.yml
```

Sample Filebeat configuration:

```yaml
filebeat.inputs:
- type: log
  enabled: true
  paths:
    - /home/ubuntu/lms/logs/*.log
  json.keys_under_root: true
  json.add_error_key: true

output.logstash:
  hosts: ["logstash-server:5044"]
```

### 3. Set Up Logstash for Processing

Install and configure Logstash on a dedicated server or container:

```bash
# Install Logstash
sudo apt-get install logstash

# Configure Logstash
sudo nano /etc/logstash/conf.d/lms.conf
```

Sample Logstash configuration:

```conf
input {
  beats {
    port => 5044
  }
}

filter {
  if [timestamp] {
    date {
      match => [ "timestamp", "ISO8601" ]
      target => "@timestamp"
    }
  }
  
  if [level] {
    mutate {
      rename => { "level" => "log_level" }
    }
  }
  
  # Add environment tag
  mutate {
    add_field => { "environment" => "${ENVIRONMENT:production}" }
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "lms-logs-%{+YYYY.MM.dd}"
  }
}
```

### 4. Install and Configure Elasticsearch

Set up Elasticsearch to store and index the logs:

```bash
# Install Elasticsearch
sudo apt-get install elasticsearch

# Configure Elasticsearch
sudo nano /etc/elasticsearch/elasticsearch.yml
```

Sample Elasticsearch configuration:

```yaml
cluster.name: lms-logging
node.name: lms-node-1
network.host: 0.0.0.0
http.port: 9200
discovery.type: single-node
```

### 5. Set Up Kibana for Visualization

Install and configure Kibana for log visualization:

```bash
# Install Kibana
sudo apt-get install kibana

# Configure Kibana
sudo nano /etc/kibana/kibana.yml
```

Sample Kibana configuration:

```yaml
server.port: 5601
server.host: "0.0.0.0"
elasticsearch.hosts: ["http://elasticsearch:9200"]
```

### 6. Create Index Patterns and Dashboards

Once logs are flowing into Elasticsearch, configure Kibana with:

1. Index patterns for `lms-logs-*`
2. Saved searches for common queries (errors, warnings, etc.)
3. Dashboards for monitoring system health
4. Alerts for critical errors

## Alternative Solutions

If the ELK stack is too complex or resource-intensive, consider these alternatives:

1. **Graylog**: Open-source log management with a user-friendly interface
2. **AWS CloudWatch Logs**: If running on AWS infrastructure
3. **Google Cloud Logging**: If running on GCP infrastructure
4. **Azure Monitor**: If running on Azure infrastructure
5. **Papertrail or Loggly**: Hosted log management services

## Security Considerations

1. **Authentication**: Secure all components with proper authentication
2. **Network Security**: Use TLS for all communications between components
3. **Data Retention**: Implement log rotation and retention policies
4. **PII Management**: Ensure personal information is properly handled according to regulations

## Monitoring and Alerting

Configure alerts for:

1. **Error Rate**: Sudden increase in error messages
2. **Server Errors**: Any 5xx errors in the API
3. **Authentication Failures**: Multiple failed login attempts
4. **Performance Issues**: Slow response times
5. **Disk Space**: Low disk space on logging servers

## Implementation Checklist

- [ ] Enable structured JSON logging in production
- [ ] Install and configure Filebeat on all application servers
- [ ] Set up Logstash server and configure filters
- [ ] Deploy Elasticsearch for log storage
- [ ] Configure Kibana for visualization
- [ ] Create dashboards and alerts
- [ ] Document the setup and monitoring procedures
- [ ] Train the operations team on log analysis 