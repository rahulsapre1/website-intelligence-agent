# Contributing to Website Intelligence Agent

Thank you for your interest in contributing to the Website Intelligence Agent! This document provides guidelines for contributing to the project.

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- Git
- GitHub account

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/website-intelligence-agent.git
   cd website-intelligence-agent
   ```

2. **Backend Setup**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Set up environment variables
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   
   # Set up environment variables
   cp .env.example .env.local
   # Edit .env.local with your API URL
   ```

4. **Database Setup**
   - Create a Supabase project
   - Run the SQL setup script: `sql/setup_tables.sql`
   - Update environment variables with Supabase credentials

## 🔧 Development Workflow

### Branch Strategy
- `main`: Production-ready code
- `develop`: Integration branch for features
- `feature/*`: Feature branches
- `bugfix/*`: Bug fix branches
- `hotfix/*`: Critical bug fixes

### Making Changes

1. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b bugfix/your-bug-fix
   ```

2. **Make Changes**
   - Write clean, readable code
   - Follow existing code style
   - Add tests for new functionality
   - Update documentation as needed

3. **Test Your Changes**
   ```bash
   # Backend tests
   python -m pytest tests/
   
   # Frontend tests
   cd frontend
   npm test
   
   # Full application test
   ./run_tests.py
   ```

4. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

5. **Push and Create PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then create a Pull Request on GitHub.

## 📝 Code Standards

### Python (Backend)
- Follow PEP 8 style guide
- Use type hints
- Write docstrings for functions and classes
- Use meaningful variable names
- Keep functions small and focused

### TypeScript/React (Frontend)
- Follow ESLint configuration
- Use TypeScript strict mode
- Write functional components with hooks
- Use meaningful component and variable names
- Follow React best practices

### Git Commit Messages
Use conventional commit format:
```
type(scope): description

feat: add new feature
fix: fix bug
docs: update documentation
style: formatting changes
refactor: code refactoring
test: add or update tests
chore: maintenance tasks
```

## 🧪 Testing

### Backend Testing
- Unit tests for all services
- Integration tests for API endpoints
- Error case testing
- Mock external services

```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/unit/test_scraper.py

# Run with coverage
python -m pytest --cov=app tests/
```

### Frontend Testing
- Component testing
- API integration testing
- User interaction testing

```bash
cd frontend
npm test
npm run test:coverage
```

## 📚 Documentation

### Code Documentation
- Document all public functions and classes
- Include examples in docstrings
- Update README.md for major changes
- Keep API documentation current

### Pull Request Documentation
- Describe what changes were made
- Explain why changes were necessary
- Include screenshots for UI changes
- Link to related issues

## 🐛 Reporting Issues

### Bug Reports
When reporting bugs, include:
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)
- Screenshots if applicable

### Feature Requests
When requesting features, include:
- Clear description of the feature
- Use case and motivation
- Potential implementation approach
- Any relevant examples or references

## 🔍 Code Review Process

### For Contributors
1. Ensure all tests pass
2. Update documentation
3. Write clear commit messages
4. Request review from maintainers
5. Address feedback promptly

### For Reviewers
1. Check code quality and style
2. Verify tests are comprehensive
3. Ensure documentation is updated
4. Test the changes locally
5. Provide constructive feedback

## 🚀 Release Process

### Version Numbering
We follow semantic versioning (SemVer):
- `MAJOR.MINOR.PATCH`
- Major: Breaking changes
- Minor: New features (backward compatible)
- Patch: Bug fixes (backward compatible)

### Release Checklist
- [ ] All tests passing
- [ ] Documentation updated
- [ ] Version bumped
- [ ] Changelog updated
- [ ] Release notes prepared
- [ ] Deployment tested

## 📋 Project Structure

```
website-intelligence-agent/
├── app/                    # Backend application
│   ├── main.py            # FastAPI app
│   ├── config.py          # Configuration
│   ├── models/            # Pydantic models
│   ├── services/          # Business logic
│   └── utils/             # Utilities
├── frontend/              # Next.js frontend
│   ├── src/
│   │   ├── app/          # App router
│   │   ├── components/   # React components
│   │   ├── lib/          # Utilities
│   │   └── types/        # TypeScript types
├── tests/                 # Test suite
├── docs/                  # Documentation
├── scripts/               # Deployment scripts
└── sql/                   # Database setup
```

## 🤝 Community Guidelines

### Code of Conduct
- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Help others learn and grow

### Communication
- Use clear, concise language
- Be patient with questions
- Provide helpful responses
- Stay on topic in discussions

## 📞 Getting Help

### Resources
- GitHub Issues: For bug reports and feature requests
- GitHub Discussions: For questions and general discussion
- Documentation: Check README.md and docs/ folder
- Code Comments: Look at existing code for examples

### Contact
- Create an issue for questions
- Tag maintainers in PRs for reviews
- Use GitHub Discussions for general questions

## 🎯 Areas for Contribution

### High Priority
- Bug fixes and performance improvements
- Test coverage improvements
- Documentation enhancements
- Error handling improvements

### Medium Priority
- New features and enhancements
- UI/UX improvements
- Additional AI model integrations
- Performance optimizations

### Low Priority
- Code refactoring
- Additional deployment options
- Extended configuration options
- Additional output formats

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing to the Website Intelligence Agent! 🚀
