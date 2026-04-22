# Contributing to WinFormPy

Thank you for your interest in contributing to WinFormPy! This guide will help you get started.

## Getting Started

1. **Fork** the repository on GitHub
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/<your-username>/WinFormPy.git
   cd WinFormPy
   ```
3. **Install** dependencies:
   ```bash
   uv sync
   ```
4. **Create a branch** for your change:
   ```bash
   git checkout -b feature/my-feature
   ```

## Development Setup

- **Python >= 3.10** is required
- **uv** is the recommended package manager
- **Tkinter** must be available (built-in with most Python installs)

### Running Tests

```bash
uv run pytest tests/ -v
```

### Linting

```bash
uvx ruff check winformpy/
uvx ruff format winformpy/
```

## Code Conventions

- **PascalCase** for all public API: classes, properties, methods, events
- **snake_case** for local variables and private helpers
- **_underscore prefix** for private/internal members
- All event handlers accept `(sender, e)` where `e` is `EventArgs`
- Optional dependencies use lazy import with `try/except ImportError`

See [`.github/copilot-instructions.md`](.github/copilot-instructions.md) for the full style guide.

## Branch Naming

- `feature/*` — New features
- `bugfix/*` — Bug fixes
- `hotfix/*` — Urgent fixes
- `docs/*` — Documentation only

## Commit Messages

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add DatePickerBox control
fix: correct Dock layout order for Fill panels
docs: update README with new examples
refactor: extract shared install utility
```

## Pull Request Process

1. Ensure all tests pass (`uv run pytest tests/ -v`)
2. Ensure linting passes (`uvx ruff check winformpy/`)
3. Update documentation if you changed public API
4. Update `CHANGELOG.md` with your changes under `[Unreleased]`
5. Submit a pull request against the `main` branch

## What to Contribute

- Bug fixes
- New controls (following the existing facade pattern)
- New examples in `examples/`
- Documentation improvements
- Test coverage improvements
- Performance improvements (with measurable evidence)

## What NOT to Do

- Do not hardcode credentials, API keys, or connection strings
- Do not use `eval()` or `exec()` on user input
- Do not break existing public API without discussion
- Do not add dependencies without discussion

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md).
