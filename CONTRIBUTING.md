# Contributing to n8n HR Automation System

Thank you for your interest in contributing to this project! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to:
- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on constructive criticism
- Accept feedback gracefully

## How to Contribute

### Reporting Issues

1. **Check existing issues** first to avoid duplicates
2. **Use issue templates** when available
3. **Provide detailed information**:
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - System information
   - Error messages/logs

### Suggesting Enhancements

1. **Open a discussion** first for major changes
2. **Describe the problem** you're solving
3. **Explain your solution** clearly
4. **Consider backward compatibility**

### Pull Requests

#### Before Starting

1. **Fork the repository**
2. **Create a feature branch** from `main`
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Keep your fork updated**
   ```bash
   git remote add upstream https://github.com/xliberty2008x/n8n_hr_viragames_automation.git
   git fetch upstream
   git merge upstream/main
   ```

#### Making Changes

1. **Follow the project structure**:
   - Documentation in `/docs` for GitHub Pages
   - API examples in `/config/api-examples`
   - Workflow templates in `/config/n8n-workflows`
   - Technical docs in `/documentation`

2. **Code Style**:
   - Use clear, descriptive names
   - Comment complex logic
   - Keep functions focused and small
   - Follow existing patterns

3. **Documentation**:
   - Update relevant documentation
   - Add comments for complex code
   - Include examples where helpful
   - Update README if needed

4. **Testing**:
   - Test your changes thoroughly
   - Verify workflows still function
   - Check API integrations
   - Ensure documentation builds

#### Submitting PR

1. **Write clear commit messages**:
   ```
   feat: Add department sync error handling
   
   - Implement retry logic for API failures
   - Add detailed error logging
   - Send Slack notifications on critical errors
   ```

2. **PR Description Template**:
   ```markdown
   ## Description
   Brief description of changes
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Documentation update
   - [ ] Performance improvement
   
   ## Testing
   - [ ] Tested locally
   - [ ] Updated documentation
   - [ ] All workflows function correctly
   
   ## Related Issues
   Closes #123
   ```

3. **Keep PRs focused** - one feature/fix per PR

4. **Be responsive** to review feedback

## Development Setup

### Prerequisites

- Node.js 18+
- n8n installed locally
- Git
- API access to test accounts (optional)

### Local Development

1. **Clone your fork**:
   ```bash
   git clone https://github.com/yourusername/n8n_hr_viragames_automation.git
   cd n8n_hr_viragames_automation
   ```

2. **Set up n8n locally**:
   ```bash
   npm install -g n8n
   n8n start
   ```

3. **Test workflows**:
   - Import workflows from `/config/n8n-workflows`
   - Use test API credentials
   - Verify functionality

### Documentation Development

1. **GitHub Pages** (in `/docs`):
   - Edit HTML files directly
   - Test locally with any web server
   - Maintain responsive design
   - Check all links work

2. **Technical Docs** (in `/documentation`):
   - Write in Markdown
   - Use clear headings
   - Include code examples
   - Add diagrams where helpful

## Workflow Contributions

### Creating New Workflows

1. **Export from n8n** as JSON
2. **Remove sensitive data**:
   - API keys
   - URLs (replace with placeholders)
   - Personal information
3. **Document the workflow**:
   - Purpose and use case
   - Required credentials
   - Configuration steps
   - Expected outcomes

### Improving Existing Workflows

1. **Maintain backward compatibility**
2. **Document breaking changes**
3. **Test thoroughly**
4. **Update related documentation**

## API Integration Guidelines

### Adding New Integrations

1. **Create example configuration** in `/config/api-examples`
2. **Document authentication** requirements
3. **Include rate limit** information
4. **Provide field mappings**
5. **Add error handling** examples

### Updating Existing Integrations

1. **Check API version** compatibility
2. **Test with real data**
3. **Update documentation**
4. **Consider migration path** for users

## Documentation Standards

### Writing Style

- **Be concise** but complete
- **Use active voice**
- **Include examples**
- **Explain the "why"** not just "how"
- **Keep beginner-friendly**

### Formatting

- Use **Markdown** for technical docs
- Include **code blocks** with syntax highlighting
- Add **screenshots** for UI elements
- Create **diagrams** for complex flows
- Use **tables** for structured data

## Review Process

1. **Automated checks** run on all PRs
2. **Maintainer review** for approval
3. **Discussion** for clarification
4. **Merge** when approved

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Thanked in project documentation

## Getting Help

- **Documentation**: [GitHub Pages](https://xliberty2008x.github.io/n8n_hr_viragames_automation/)
- **Issues**: [GitHub Issues](https://github.com/xliberty2008x/n8n_hr_viragames_automation/issues)
- **Discussions**: Use GitHub Discussions
- **Claude AI**: Mention @claude in issues/PRs

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Thank You!

Your contributions make this project better for everyone. We appreciate your time and effort!