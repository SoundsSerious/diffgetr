# PyPI Setup Instructions

This guide will help you set up PyPI publishing for the diffgetr library using GitHub Actions with trusted publishing.

## 1. Create PyPI Account

1. Go to [PyPI.org](https://pypi.org) and create an account
2. Verify your email address
3. (Optional) Go to [TestPyPI.org](https://test.pypi.org) and create an account for testing

## 2. Set Up Trusted Publishing on PyPI

### For Production PyPI:

1. Log into [PyPI.org](https://pypi.org)
2. Go to your account settings
3. Navigate to "Publishing" tab
4. Click "Add a new pending publisher"
5. Fill in the details:
   - **PyPI Project Name**: `diffgetr`
   - **Owner**: Your GitHub username/organization
   - **Repository name**: `diffgetr` (or whatever your repo is named)
   - **Workflow name**: `main.yml`
   - **Environment name**: `release`

### For Test PyPI (Optional):

1. Log into [TestPyPI.org](https://test.pypi.org)
2. Follow the same steps as above

## 3. Configure GitHub Repository

### Set Up Environment:

1. Go to your GitHub repository
2. Navigate to Settings → Environments
3. Create a new environment named `release`
4. (Optional) Add protection rules like:
   - Required reviewers
   - Restrict to main branch only
   - Wait timer before deployment

### Repository Secrets (if not using trusted publishing):

If you prefer API tokens instead of trusted publishing:

1. Go to PyPI → Account Settings → API Tokens
2. Create a new token with scope limited to your project
3. In GitHub: Settings → Secrets and Variables → Actions
4. Add secret: `PYPI_API_TOKEN` with your token value

## 4. Update pyproject.toml

Make sure your `pyproject.toml` has the correct metadata:

```toml
[project]
name = "diffgetr"
version = "0.1.0"  # Update this for new releases
description = "A Python library for comparing nested data structures with detailed diff reporting and interactive navigation."
authors = [
    { name = "Your Actual Name", email = "your.actual.email@example.com" }
]
readme = "README.md"
license = "MIT"
requires-python = ">=3.7"

[project.urls]
Homepage = "https://github.com/yourusername/diffgetr"
Repository = "https://github.com/yourusername/diffgetr"
Issues = "https://github.com/yourusername/diffgetr/issues"
```

## 5. Workflow Overview

The CI/CD pipeline works as follows:

### On Pull Requests:
1. ✅ **Version Check**: Ensures the version in `pyproject.toml` doesn't already exist as a GitHub release
2. ✅ **Build & Test**: Builds the package and runs unit tests
3. ✅ **Code Formatting**: Runs `black` and auto-commits formatting changes

### On Main Branch Push:
1. ✅ **Build & Test**: Same as PR checks but must pass to continue
2. ✅ **Publish to PyPI**: Uses trusted publishing to upload package
3. ✅ **GitHub Release**: Creates a GitHub release with changelog and artifacts

## 6. Release Process

To create a new release:

1. **Update Version**: Edit `pyproject.toml` and bump the version number
2. **Create PR**: Make your changes and create a pull request
3. **Review**: The PR workflow will check version availability and run tests
4. **Merge**: When merged to main, the package will automatically:
   - Be published to PyPI
   - Create a GitHub release
   - Include built artifacts

## 7. Testing Your Setup

### Test Locally:
```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Test build
python -m build

# Test installation
pip install dist/*.whl
```

### Test with TestPyPI:
Modify the GitHub workflow to publish to TestPyPI first:

```yaml
- name: Publish to TestPyPI
  uses: pypa/gh-action-pypi-publish@release/v1
  with:
    repository-url: https://test.pypi.org/legacy/
```

## 8. Troubleshooting

### Common Issues:

1. **"Project name already exists"**: The package name might be taken. Consider a different name.

2. **"Invalid authentication"**: Check your trusted publishing setup matches exactly.

3. **"Version already exists"**: You need to bump the version in `pyproject.toml`.

4. **"Workflow failed"**: Check the GitHub Actions logs for specific error messages.

### Trusted Publishing Not Working?

Fall back to API tokens:

1. Create PyPI API token
2. Add to GitHub secrets as `PYPI_API_TOKEN`
3. Modify workflow to use:
   ```yaml
   - name: Publish to PyPI
     uses: pypa/gh-action-pypi-publish@release/v1
     with:
       password: ${{ secrets.PYPI_API_TOKEN }}
   ```

## 9. Security Considerations

- ✅ **Trusted Publishing**: More secure than API tokens
- ✅ **Environment Protection**: Requires approval for releases
- ✅ **Branch Protection**: Only allow releases from main branch
- ✅ **Version Control**: Automatic version checking prevents duplicates

## 10. Next Steps

1. Update the repository URL in `pyproject.toml`
2. Update author information
3. Set up the PyPI trusted publisher
4. Create your first release by bumping the version!

Your package will be available at: `https://pypi.org/project/diffgetr/`