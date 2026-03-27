# {Project Name}

> {One-line description of what this project does and who it's for.}

![Status](https://img.shields.io/badge/status-{status}-{color})
![Version](https://img.shields.io/badge/version-{version}-blue)
![License](https://img.shields.io/badge/license-{license}-green)

---

## 📋 Documentation

| Document | Description | Status |
|----------|-------------|--------|
| [PRD](docs/PRD-{slug}.md) | Product Requirements | {status} |
| [SDD](docs/design/SDD-{slug}.md) | Software Design | {status} |
| [Design System](docs/design/DESIGN-SYSTEM.md) | Design tokens & components | {status} |
| [Doc Index](docs/INDEX.md) | Full document registry | — |

---

## 🚀 Quick Start

```bash
# 1. Clone and install
git clone {repo-url}
cd {project-name}
{install-command}   # npm install / pip install -r requirements.txt / etc.

# 2. Configure environment
cp .env.example .env
# Edit .env with your values

# 3. Run development server
{dev-command}   # npm run dev / uvicorn main:app --reload / etc.
```

> **Requirements:** {Node 18+ / Python 3.11+ / etc.}

---

## 🏗️ Project Structure

```
{project-name}/
├── src/                  # Application source code
├── tests/                # Test suites
│   ├── unit/
│   └── integration/
├── docs/                 # Project documentation
│   ├── INDEX.md          # Document registry
│   ├── PRD-{slug}.md
│   └── design/
├── .env.example          # Environment variable template
├── SECURITY.md           # Security policy
└── CHANGELOG.md          # Version history
```

---

## 🧪 Testing

```bash
# Run all tests
{test-command}

# Run with coverage
{coverage-command}
```

**Coverage target:** ≥ 80%

---

## 🚢 Deployment

| Environment | URL | Trigger |
|-------------|-----|---------|
| Development | localhost | manual |
| Staging | {staging-url} | push to `staging` |
| Production | {prod-url} | manual approval |

See [SDD §4.1 Environment Strategy](docs/design/SDD-{slug}.md) for details.

---

## 🔒 Security

See [SECURITY.md](SECURITY.md) for our security policy and vulnerability disclosure process.

---

## 📝 Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

---

## 👥 Team

| Role | Name |
|------|------|
| Product Owner | [Name] |
| Tech Lead | [Name] |
