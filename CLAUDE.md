# CLAUDE.md - AI Assistant Guide for Cropify-AI

**Last Updated**: 2026-01-22
**Project**: Cropify-AI
**Repository**: Paups02/K-RED90-Cropify-AI

## Project Overview

Cropify-AI is an AI-powered agricultural application focused on crop management, analysis, and optimization. This document serves as a comprehensive guide for AI assistants working on this codebase.

## Current Repository State

**Status**: New repository - initial setup phase
**Main Branch**: TBD (to be established)
**Active Branch**: `claude/claude-md-mkp9014afitdnlm9-eWGM9`

## Codebase Structure

### Expected Directory Layout

As the project develops, follow this recommended structure:

```
K-RED90-Cropify-AI/
├── src/                    # Source code
│   ├── components/         # Reusable UI components
│   ├── services/           # Business logic and API services
│   ├── models/             # Data models and types
│   ├── utils/              # Utility functions
│   ├── config/             # Configuration files
│   └── tests/              # Test files
├── public/                 # Static assets
├── docs/                   # Documentation
├── scripts/                # Build and deployment scripts
├── .github/                # GitHub workflows and templates
├── package.json            # Dependencies (if Node.js/npm)
├── requirements.txt        # Dependencies (if Python)
├── README.md               # Project documentation
└── CLAUDE.md              # This file

```

### Technology Stack

**To Be Determined** - Update this section once the tech stack is chosen. Considerations for Cropify-AI:

- **Frontend**: React, Vue.js, or Angular for web interface
- **Backend**: Node.js, Python (Django/Flask), or Go
- **AI/ML**: TensorFlow, PyTorch, or scikit-learn for crop analysis
- **Database**: PostgreSQL, MongoDB, or Firebase
- **Cloud**: AWS, GCP, or Azure for deployment
- **Computer Vision**: OpenCV for image processing (if needed)

## Development Workflows

### Branch Strategy

1. **Feature Branches**: All development happens on feature branches
   - Format: `claude/claude-md-<session-id>` for AI assistant work
   - Format: `feature/<feature-name>` for human developers

2. **Main Branch**: Protected branch containing stable code
   - All changes must go through pull requests
   - Requires review before merging

3. **Branch Lifecycle**:
   ```bash
   # Create new feature branch
   git checkout -b feature/crop-analysis

   # Make changes and commit
   git add .
   git commit -m "Add crop disease detection model"

   # Push to remote
   git push -u origin feature/crop-analysis

   # Create PR when ready
   gh pr create --title "Add crop disease detection" --body "..."
   ```

### Commit Message Conventions

Follow conventional commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `perf`: Performance improvements

**Examples**:
```
feat(crop-detection): add image preprocessing pipeline

Implement preprocessing pipeline for crop images including:
- Noise reduction
- Color normalization
- Region of interest extraction

Closes #123
```

### Pull Request Process

1. **Create PR** with descriptive title and comprehensive description
2. **Include**:
   - Summary of changes (2-3 bullet points)
   - Test plan or checklist
   - Screenshots/demos if applicable
   - Related issue numbers
3. **Review**: Wait for code review and address feedback
4. **Merge**: Squash and merge when approved

### Testing Standards

#### Test Coverage Requirements
- **Minimum**: 80% code coverage for new features
- **Critical paths**: 100% coverage for business logic

#### Test Types
1. **Unit Tests**: Test individual functions/components
2. **Integration Tests**: Test component interactions
3. **E2E Tests**: Test complete user workflows
4. **Visual Tests**: Test UI components (if applicable)

#### Running Tests
```bash
# Run all tests
npm test  # or pytest, depending on stack

# Run with coverage
npm run test:coverage

# Run specific test file
npm test path/to/test.spec.js
```

## Key Conventions for AI Assistants

### Code Quality Standards

1. **Always Read Before Modifying**
   - NEVER propose changes to code you haven't read
   - Read entire files to understand context
   - Check related files for dependencies

2. **Follow Existing Patterns**
   - Match existing code style and conventions
   - Use the same naming conventions
   - Follow established architectural patterns

3. **Security First**
   - Validate all user inputs
   - Sanitize data before database queries
   - Use parameterized queries (no SQL injection)
   - Implement proper authentication/authorization
   - Never commit secrets or API keys
   - Check for OWASP Top 10 vulnerabilities

4. **Performance Considerations**
   - Optimize database queries
   - Implement caching where appropriate
   - Use lazy loading for large datasets
   - Consider memory usage for image processing

5. **Error Handling**
   - Always handle errors gracefully
   - Provide meaningful error messages
   - Log errors appropriately
   - Don't expose sensitive info in errors

### Domain-Specific Guidelines

#### Agriculture/Crop Management

1. **Data Accuracy**: Crop health and yield predictions must be highly accurate
2. **Image Processing**: Follow best practices for agricultural image analysis
3. **Units**: Use consistent units (metric preferred) for measurements
4. **Terminology**: Use correct agricultural/botanical terminology
5. **Seasonal Considerations**: Account for growing seasons and regional differences

#### AI/ML Best Practices

1. **Model Versioning**: Track model versions and performance metrics
2. **Data Validation**: Validate training data quality
3. **Bias Detection**: Monitor for and mitigate model bias
4. **Explainability**: Provide explanations for AI predictions
5. **Fallbacks**: Implement graceful degradation if AI services fail

### Code Organization

1. **Single Responsibility**: Each function/class should do one thing well
2. **DRY Principle**: Don't repeat yourself - extract common logic
3. **Clear Naming**: Use descriptive, self-documenting names
4. **Comments**: Only comment "why", not "what" (code should be self-explanatory)
5. **File Size**: Keep files under 500 lines; split if larger

### Documentation Requirements

1. **Function Documentation**: Document all public functions/methods
2. **API Documentation**: Document all endpoints with examples
3. **README Updates**: Update README when adding major features
4. **Architecture Docs**: Document major architectural decisions
5. **Change Log**: Maintain CHANGELOG.md for releases

## Task Management

### Using TodoWrite Tool

AI assistants should use the TodoWrite tool for:
- Multi-step tasks (3+ steps)
- Complex features requiring planning
- Tasks explicitly requested by users
- Tracking implementation progress

**Example Todo Structure**:
```
1. Research existing crop detection libraries
2. Design image preprocessing pipeline
3. Implement core detection algorithm
4. Add unit tests for detection logic
5. Integrate with frontend API
6. Update documentation
```

### Task Breakdown Principles

- Break large tasks into small, actionable items
- Mark ONE task as in_progress at a time
- Complete tasks immediately when finished
- Remove obsolete tasks from the list

## Environment Setup

### Prerequisites

**To Be Determined** - Update when stack is chosen:

```bash
# Example for Node.js project
node --version  # >= 18.x
npm --version   # >= 9.x

# Example for Python project
python --version  # >= 3.9
pip --version
```

### Installation

```bash
# Clone repository
git clone https://github.com/Paups02/K-RED90-Cropify-AI.git
cd K-RED90-Cropify-AI

# Install dependencies (example)
npm install  # or pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run development server
npm run dev  # or python manage.py runserver
```

### Environment Variables

Document required environment variables:

```env
# API Keys
OPENAI_API_KEY=your_key_here
WEATHER_API_KEY=your_key_here

# Database
DATABASE_URL=postgresql://localhost/cropify_db

# AWS (if used)
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_S3_BUCKET=cropify-images

# Application
NODE_ENV=development
PORT=3000
```

## Common Tasks

### Adding a New Feature

1. Create feature branch: `git checkout -b feature/your-feature`
2. Use TodoWrite to plan implementation steps
3. Implement feature following conventions above
4. Write tests achieving 80%+ coverage
5. Update documentation (README, API docs)
6. Create pull request with detailed description

### Fixing a Bug

1. Reproduce the bug and write a failing test
2. Identify root cause (read related code)
3. Implement fix following existing patterns
4. Verify test now passes
5. Check for similar issues elsewhere
6. Commit with descriptive message
7. Create PR or push to feature branch

### Refactoring Code

1. Ensure tests exist for code being refactored
2. Make small, incremental changes
3. Run tests after each change
4. Don't add features while refactoring
5. Document any API changes
6. Get review for large refactorings

## Troubleshooting

### Common Issues

**Issue**: Tests failing after changes
**Solution**: Run tests locally, check dependencies, review error messages

**Issue**: Merge conflicts
**Solution**: `git fetch origin`, `git rebase origin/main`, resolve conflicts

**Issue**: Performance degradation
**Solution**: Profile code, check database queries, review caching

**Issue**: AI model not loading
**Solution**: Check model file paths, verify dependencies, review memory usage

## Resources

### Documentation Links

- Project README: `README.md`
- API Documentation: `docs/api.md` (when created)
- Architecture: `docs/architecture.md` (when created)
- Contributing Guide: `CONTRIBUTING.md` (when created)

### External Resources

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Clean Code Principles](https://github.com/ryanmcdermott/clean-code-javascript)

## Project-Specific Notes

### Agricultural Domain Knowledge

When working with crop-related features:
- Understand crop growth stages: germination, vegetative, reproductive, maturation
- Common crop diseases: blight, rust, mildew, mosaic virus
- Environmental factors: soil pH, moisture, temperature, sunlight
- Pest identification and management
- Yield estimation methodologies

### AI Model Considerations

- **Input**: Likely crop images (RGB or multispectral)
- **Output**: Classifications, predictions, recommendations
- **Training Data**: Ensure diverse dataset across seasons/regions
- **Validation**: Use k-fold cross-validation
- **Metrics**: Accuracy, precision, recall, F1-score
- **Deployment**: Consider edge deployment for offline use

## Version History

- **2026-01-22**: Initial CLAUDE.md creation (empty repository setup)

## Next Steps

As the project develops, update this document with:

1. ✅ Confirmed technology stack
2. ✅ Actual codebase structure
3. ✅ Specific coding standards and linters
4. ✅ CI/CD pipeline details
5. ✅ Deployment procedures
6. ✅ Production environment details
7. ✅ Team communication channels
8. ✅ Issue tracking workflow

---

**Note for AI Assistants**: This document should be treated as the source of truth for development practices. When in doubt, consult this file before making decisions. Update this document as the project evolves to reflect current practices and conventions.
