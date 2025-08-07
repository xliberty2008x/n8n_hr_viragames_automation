# CLAUDE.md

**IMPORTANT: This is a website project. All issues and changes should be related to website content and structure.**

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 📝 Progress Tracking

**ALWAYS track your progress in this file when working on issues.**

### Current Progress
- [x] Initial project exploration completed
- [x] CLAUDE.md updated with comprehensive instructions
- [x] Added BambooHR pay rate change feature to website (Scenario 4)

## 🌐 Project Overview

This is a **GitHub Pages website** that documents the HR Integration System for Vira Games. The website showcases an automation system that integrates TeamTailor, BambooHR, Notion, and Slack through n8n workflows.

**Website URL:** Served from `/docs` directory via GitHub Pages

## 🎯 Purpose

The website serves as:
1. Documentation hub for HR automation workflows
2. Setup guide for the integration system
3. Troubleshooting resource for common issues
4. Showcase of automation capabilities

## 📁 Project Structure

```
n8n_hr_viragames_automation/
├── docs/                        # GitHub Pages website root
│   ├── index.html              # Landing page - system overview
│   ├── setup.html              # Installation and setup guide
│   ├── troubleshooting.html   # Common issues and solutions
│   ├── docs.html               # Detailed technical documentation
│   ├── assets/
│   │   ├── css/               # Stylesheets
│   │   │   ├── style.css      # Main styles
│   │   │   └── docs.css       # Documentation-specific styles
│   │   ├── js/                # JavaScript files
│   │   │   ├── main.js        # Main interactivity
│   │   │   └── docs.js        # Documentation navigation
│   │   └── img/               # Images and icons
│   │       ├── bamboohr-icon.svg
│   │       ├── n8n-icon.svg
│   │       └── teamtailor-icon.svg
│   └── LOOM_VIDEO_INSTRUCTIONS.md
├── .github/workflows/          # GitHub Actions automation
└── CLAUDE.md                   # This file - project instructions
```

## 💻 Technology Stack

- **Frontend:** Pure HTML, CSS, JavaScript (no framework)
- **Styling:** Custom CSS with responsive design
- **Icons:** Font Awesome + custom SVGs
- **Typography:** Google Fonts (Inter)
- **Code Highlighting:** Prism.js
- **Video:** Loom embeds for demonstrations

## 📄 Website Pages

### 1. Landing Page (`index.html`)
- Hero section with key metrics
- Features overview
- Architecture diagram
- Three main automation scenarios
- Video presentation
- Call-to-action sections

### 2. Setup Guide (`setup.html`)
- Prerequisites and requirements
- Step-by-step installation
- Configuration instructions
- Testing procedures

### 3. Documentation (`docs.html`)
- Comprehensive technical details
- API integrations documentation
- Workflow descriptions
- Error handling with AI
- Best practices

### 4. Troubleshooting (`troubleshooting.html`)
- Common issues and solutions
- Debugging guides
- FAQ section

## 🎨 Design System

### Colors
- Primary: Blue (#007bff)
- Success: Green (#28a745)
- Warning: Yellow (#ffc107)
- Danger: Red (#dc3545)
- Dark backgrounds with light text

### Components
- Cards for features and scenarios
- Alert boxes for important information
- Code blocks with syntax highlighting
- Interactive navigation with search
- Responsive mobile menu

## 📝 Content Guidelines

When adding new content:

1. **Language:** Ukrainian (UA) for all user-facing content
2. **Tone:** Professional but approachable
3. **Structure:** Use semantic HTML5 elements
4. **Accessibility:** Include proper ARIA labels and alt text
5. **Performance:** Optimize images and minimize JavaScript

## 🔧 Development Guidelines

### For Website Updates

1. **HTML Structure:**
   - Use semantic HTML5 tags
   - Maintain consistent indentation
   - Include proper meta tags

2. **CSS Styling:**
   - Follow BEM methodology where applicable
   - Use CSS variables for theme consistency
   - Ensure mobile responsiveness

3. **JavaScript:**
   - Keep scripts modular
   - Use vanilla JavaScript (no jQuery)
   - Ensure graceful degradation

4. **Content Updates:**
   - Verify all links work
   - Test on multiple browsers
   - Check mobile responsiveness

### For New Features

1. Identify the appropriate page for the content
2. Follow existing HTML structure patterns
3. Apply consistent styling using existing CSS classes
4. Update navigation if adding new sections
5. Test thoroughly before committing

## 🚀 Current Features

### Implemented Automations

1. **Department Synchronization**
   - Notion ↔ TeamTailor sync
   - Weekly scheduled runs
   - 1-2 minute execution

2. **Job Requisition Creation**
   - Notion → TeamTailor
   - Triggered on demand
   - 30 second execution

3. **Employee Onboarding**
   - TeamTailor → BambooHR
   - Webhook triggered
   - 2-3 minute execution

### In Progress Features

- BambooHR pay rate change notifications to Slack
- Webhook integration pending (support ticket open)

## 🔄 GitHub Actions Integration

The repository includes GitHub workflows that:
- Automate deployment to GitHub Pages
- Integrate with Claude agent for code assistance
- Handle automated testing and validation

## 📋 Important Notes

1. **Every issue is website-related** - All changes should update website content or structure
2. **Track progress here** - Update this file with your progress on issues
3. **Test locally first** - Verify changes before pushing
4. **Maintain consistency** - Follow existing patterns and styles
5. **Document changes** - Update relevant documentation when adding features