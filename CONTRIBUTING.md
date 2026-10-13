# Contributing to Mistral Agents Library

Thank you for your interest in contributing! This document outlines how to contribute to the Mistral Agents Library effectively.

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Create a feature branch** for your changes

## How to Contribute

### Reporting Bugs

Use the [Bug Report template](https://github.com/robintel/mistral-agents-library/issues/new?assignees=&labels=bug&template=bug_report.md) and include:
- Steps to reproduce
- Expected vs. actual behavior
- Agent name and version
- Environment details (OS, Mistral Vibe version, library version)

### Requesting Features

Use the [Feature Request template](https://github.com/robintel/mistral-agents-library/issues/new?assignees=&labels=enhancement&template=feature_request.md) and include:
- The use case or problem you're solving
- Proposed solution
- Acceptance criteria

### Adding a New Agent

1. **Create the agent file** in the appropriate domain folder (e.g., `sdlc/app-dev/`, `data/`, `security/`, or create a new domain folder)
   - Use the existing frontmatter schema: `name`, `domain`, `tier`, `escalate`, `accepts`
   - Follow the structure in [shared/standards.md](shared/standards.md)

2. **Register the agent** in `manifest.yaml`:
   - Add the agent to the `agents` section
   - Add routing rules under `routing`

3. **Test the agent**:
   - Run `./install.py` to compose and install
   - Verify with `vibe --agent <your-agent-name>`
   - Ensure it follows the elegance bar standards

4. **Document the agent**:
   - Add description in the agent file's frontmatter
   - Update README if the agent is user-facing

### Modifying Existing Agents

1. **Follow existing patterns** - match the style, structure, and verbosity of surrounding code
2. **Maintain backward compatibility** where possible
3. **Update tests** if applicable
4. **Document breaking changes** clearly

### Agent Standards

All agents must conform to the [shared/standards.md](shared/standards.md) elegance bar:
- Communication contract compliance
- Artifact quality standards
- Verbosity level adherence
- Cost-tiered routing awareness

## Development Workflow

### Local Development

```bash
# Clone your fork
git clone https://github.com/your-username/mistral-agents-library.git
cd mistral-agents-library

# Make changes
# Test with local install
./install.py --dest /tmp/test-install

# Verify the install
vibe --agent orchestrator
```

### Testing Your Changes

1. **Unit tests**: Add tests in the appropriate directory
2. **Manual testing**: Verify with real prompts and scenarios
3. **Smoke test**: Run `./smoke/smoke.sh` if available
4. **Coverage**: Ensure new code meets the coverage floor (80% default)

## Pull Request Guidelines

1. **Title**: Clear and descriptive (use prefix like `[Agent]` or `[Docs]`)
2. **Description**: Reference the issue, explain the change, note any breaking changes
3. **Commits**: Atomic, well-described commits following [Conventional Commits](https://www.conventionalcommits.org/)
4. **Tests**: All existing tests must pass
5. **Documentation**: Update relevant documentation
6. **Review**: Be responsive to feedback

## Code Review Process

- All PRs require at least one approval
- Maintainers may request changes before merging
- PRs are merged using squash or rebase at maintainer discretion
- Protected branches require passing status checks

## Releasing

Only maintainers can release. The process:
1. Bump version in `manifest.yaml` or relevant files
2. Update CHANGELOG (if maintained)
3. Create a GitHub release with release notes
4. Publish to any package registries (if applicable)

## License

By contributing, you agree to license your contributions under the [MIT License](LICENSE).
