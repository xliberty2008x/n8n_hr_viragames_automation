# n8n HR Automation System - Vira Games

**AI-powered HR process automation integrating TeamTailor, BambooHR, Notion, and Slack**

[![GitHub Pages](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://xliberty2008x.github.io/n8n_hr_viragames_automation/)
[![Claude AI](https://img.shields.io/badge/AI-Claude%20Agent-purple)](https://claude.ai)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## 🎯 Project Overview

This repository contains the documentation and configuration for an advanced HR automation system that:
- **Saves 85% of HR manager's time** on routine operations
- **Reduces errors by 80%** through automated data entry
- **Integrates 4 major platforms** seamlessly
- **Processes requests in 3 minutes** instead of 45-60 minutes

## 🚀 Quick Links

- 📖 **[Documentation Site](https://xliberty2008x.github.io/n8n_hr_viragames_automation/)** - Complete setup and usage guides
- 🎥 **[Video Demo](https://www.loom.com/share/efa273c5ea30401ea4063c91b92a1d67)** - See the system in action
- 🛠️ **[Setup Guide](https://xliberty2008x.github.io/n8n_hr_viragames_automation/setup.html)** - Get started quickly
- 🐛 **[Troubleshooting](https://xliberty2008x.github.io/n8n_hr_viragames_automation/troubleshooting.html)** - Common issues and solutions

## 📁 Repository Structure

```
n8n_hr_viragames_automation/
│
├── 📄 docs/                    # GitHub Pages documentation site
│   ├── index.html             # Landing page with system overview
│   ├── setup.html             # Installation and configuration guide
│   ├── docs.html              # Technical documentation
│   ├── troubleshooting.html   # Problem-solving guide
│   └── assets/                # Static resources
│       ├── css/               # Stylesheets
│       ├── js/                # JavaScript files
│       └── img/               # Icons and images
│
├── 🤖 .github/                 # GitHub configuration
│   └── workflows/             # Automation workflows
│       └── claude-agent.yml   # Claude AI assistant integration
│
├── 📝 config/                  # Configuration templates
│   ├── n8n-workflows/         # n8n workflow JSON files
│   └── api-examples/          # API configuration examples
│
├── 📚 documentation/           # Additional documentation
│   ├── api-reference/         # API documentation
│   ├── integration-guides/    # Step-by-step integration guides
│   └── architecture/          # System architecture diagrams
│
├── CLAUDE.md                  # Claude agent instructions
├── README.md                  # This file
└── LICENSE                    # Project license
```

## 🔧 Core Features

### 1️⃣ **Department Synchronization**
- Automatic sync between Notion and TeamTailor
- Weekly scheduled runs
- Processing time: 1-2 minutes

### 2️⃣ **Job Requisition Creation**
- Creates requisitions in TeamTailor from Notion data
- Triggered on demand
- Processing time: 30 seconds

### 3️⃣ **Employee Onboarding**
- Automatic BambooHR profile creation
- Webhook-triggered process
- Processing time: 2-3 minutes

## 🤝 Integration Partners

| Platform | Purpose | Integration Type |
|----------|---------|------------------|
| **TeamTailor** | Applicant Tracking System | REST API |
| **BambooHR** | HR Information System | REST API |
| **Notion** | HR Database & Planning | API v2 |
| **Slack** | Team Notifications | Webhooks |
| **n8n** | Workflow Automation | Self-hosted |

## 🚀 Getting Started

### Prerequisites
- n8n instance (cloud or self-hosted)
- API access to TeamTailor, BambooHR, and Notion
- Slack workspace (optional)

### Quick Start
1. **Clone this repository**
   ```bash
   git clone https://github.com/xliberty2008x/n8n_hr_viragames_automation.git
   ```

2. **Review the documentation**
   - Visit our [GitHub Pages site](https://xliberty2008x.github.io/n8n_hr_viragames_automation/)

3. **Configure your integrations**
   - Follow the [Setup Guide](https://xliberty2008x.github.io/n8n_hr_viragames_automation/setup.html)

4. **Import n8n workflows**
   - Use templates from `config/n8n-workflows/`

## 🤖 Claude AI Assistant

This repository includes Claude AI integration for:
- Automated code review and suggestions
- Issue resolution assistance
- Documentation improvements

**How to use:** Simply mention `@claude` in any issue or pull request comment.

## 📊 Performance Metrics

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Process Time | 45-60 min | 5-7 min | **85% faster** |
| Error Rate | 20% | 4% | **80% reduction** |
| Data Entry | Manual | Automated | **100% automated** |
| Systems Updated | 1 | 4 | **4x coverage** |

## 🛡️ Security & Compliance

- All API credentials stored securely in n8n
- GDPR-compliant data handling
- Audit logs for all operations
- Role-based access control

## 📝 Contributing

We welcome contributions! Please:
1. Fork this repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## 👥 Team

**Developed by:** AI Automation Department, Vira Games  
**Author:** Kyrylo Dubovyk  
**Contact:** [GitHub Issues](https://github.com/xliberty2008x/n8n_hr_viragames_automation/issues)

## 🙏 Acknowledgments

- Vira Games HR Team for requirements and testing
- n8n community for workflow automation platform
- Integration partners for their excellent APIs

---

<div align="center">
  <strong>⚡ Powered by AI Automation Department | Vira Games</strong>
</div>