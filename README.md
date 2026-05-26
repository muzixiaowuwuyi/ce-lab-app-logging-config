# AWS CloudWatch Application Logging Configuration Lab

An end-to-end cloud observability implementation utilizing a multi-tier logging architecture. This repository demonstrates how to capture, format, and aggregate application-level events into centralized cloud storage using modern structured logging practices and AWS infrastructure.

**Repository URL:** [https://github.com/muzixiaowuwuyi/ce-lab-app-logging-config](https://github.com/muzixiaowuwuyi/ce-lab-app-logging-config)

---

## 🏗️ Architecture Overview

The system streams structured telemetries from a local context into AWS CloudWatch through the following continuous data pipeline:

1. **Application Layer:** A Python Flask application generates decoupled, structured events serialized via `structlog` as single-line JSON.
2. **Buffer Layer:** High-frequency events are persisted sequentially to a local log file (`application.log`).
3. **Transport Layer:** The AWS CloudWatch Agent watches the file buffer, attaches EC2 system metadata, and streams records into an isolated AWS Log Stream.
4. **Analytics Layer:** AWS CloudWatch Logs Insights dynamically parses keys from the JSON payload to allow advanced analytical queries.

---

## 📂 Project Structure

```text
.
├── app/
│   ├── server.py              # Flask API with structlog integration
│   └── requirements.txt       # Python runtime dependencies
├── config/
│   ├── cloudwatch-agent-config.json  # Production-ready CloudWatch Agent scheme
│   ├── log-group-config.txt   # Destination log group mapping
│   └── retention-policy.txt   # Lifecycle/retention configuration (30 days)
├── examples/
│   ├── sample-logs.json       # Production-grade structured log sample
│   └── queries.txt            # Pre-defined CloudWatch Insights queries
└── screenshots/               # Verified architectural phase execution evidence
    ├── 01-log-group.png
    ├── 02-log-streams.png
    ├── 03-logs-insights.png
    └── 04-application-running.png