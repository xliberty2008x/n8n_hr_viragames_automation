# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains the **n8n HR Automation System** for Vira Games, integrating TeamTailor, BambooHR, Notion, and Slack through the n8n workflow automation platform. The system automates HR processes, saving 85% of manual work time.

## Repository Structure

```
n8n_hr_viragames_automation/
├── docs/                       # GitHub Pages documentation site
│   ├── index.html             # Landing page
│   ├── setup.html             # Setup guide
│   ├── docs.html              # Technical documentation
│   ├── troubleshooting.html   # Troubleshooting guide
│   └── assets/                # CSS, JS, images
├── .github/                   # GitHub configuration
│   └── workflows/             # GitHub Actions
│       └── claude-agent.yml   # Claude AI integration
├── config/                    # Configuration files
│   ├── n8n-workflows/         # n8n workflow templates
│   └── api-examples/          # API configuration examples
├── documentation/             # Additional documentation
│   ├── api-reference/         # API documentation
│   ├── integration-guides/    # Step-by-step guides
│   └── architecture/          # System design docs
├── CLAUDE.md                  # This file
├── README.md                  # Project overview
├── LICENSE                    # MIT License
└── CONTRIBUTING.md           # Contribution guidelines
```

## Key Technologies

- **n8n**: Workflow automation platform
- **TeamTailor**: Applicant Tracking System (ATS)
- **BambooHR**: HR Information System (HRIS)
- **Notion**: HR database and planning
- **Slack**: Team notifications
- **GitHub Pages**: Documentation hosting

## Development Guidelines

### When Working with Documentation (docs/)
1. Maintain responsive design for all HTML pages
2. Keep JavaScript minimal and performant
3. Ensure all links work correctly
4. Test on multiple browsers
5. Optimize images for web

### When Working with Workflows (config/n8n-workflows/)
1. Export workflows without credentials
2. Use placeholders for sensitive data
3. Document each workflow's purpose
4. Include setup instructions
5. Test thoroughly before committing

### When Working with API Examples (config/api-examples/)
1. Never commit real API keys or tokens
2. Use clear placeholder values
3. Include all required endpoints
4. Document rate limits
5. Provide field mappings

### When Working with GitHub Actions (.github/workflows/)
1. Test workflows in a fork first
2. Use secrets for sensitive data
3. Include error handling
4. Document trigger conditions
5. Keep workflows efficient

## Claude Agent Capabilities

When mentioned with `@claude`, you can help with:
- Code reviews and improvements
- Documentation updates
- Workflow optimization
- API integration assistance
- Troubleshooting and debugging
- Architecture recommendations

## Important Context

### Business Goals
- Reduce manual HR work by 85%
- Eliminate data duplication
- Ensure data consistency across systems
- Provide real-time synchronization
- Minimize human error in data entry

### Technical Constraints
- API rate limits must be respected
- Workflows should complete within 5 minutes
- Error handling must be comprehensive
- All integrations must be secure
- Documentation must be user-friendly

### Common Tasks
1. **Department Sync**: Weekly synchronization between Notion and TeamTailor
2. **Job Requisition**: Creating job postings from Notion data
3. **Employee Onboarding**: Automated profile creation in BambooHR when hired

## Security Considerations

- Never expose API credentials in code or documentation
- Use environment variables for sensitive configuration
- Implement proper error handling to avoid data leaks
- Follow GDPR compliance for employee data
- Use webhook signatures for verification

## Testing Guidelines

1. Test all workflows with sample data first
2. Verify API integrations individually
3. Check error handling scenarios
4. Validate data transformations
5. Ensure notifications work correctly

## Support Resources

- **Documentation**: https://xliberty2008x.github.io/n8n_hr_viragames_automation/
- **Video Demo**: https://www.loom.com/share/efa273c5ea30401ea4063c91b92a1d67
- **Issues**: GitHub Issues for bug reports and features
- **n8n Docs**: https://docs.n8n.io/

## Maintenance Notes

- Review API usage monthly to stay within limits
- Update credentials quarterly or on compromise
- Check for API version updates regularly
- Monitor workflow execution times
- Keep documentation synchronized with changes