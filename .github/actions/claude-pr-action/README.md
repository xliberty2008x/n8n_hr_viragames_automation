# Claude PR Action

A composite GitHub Action that integrates Claude (via Amazon Bedrock) to automatically respond to mentions in GitHub issues and pull request comments.

## Features

- Responds to `@claude` mentions in:
  - Issue comments
  - Pull request comments
  - Pull request review comments
  - New issues
- Uses Amazon Bedrock to invoke Claude models
- Secure authentication via GitHub App tokens
- AWS credentials via OIDC (no long-lived secrets)

## Usage

This action is used internally by the workflow in `.github/workflows/claude-pr.yml`.

### Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `trigger_phrase` | The phrase that triggers Claude (e.g., "@claude") | Yes | - |
| `timeout_minutes` | Maximum time for the action to run | No | 60 |
| `github_token` | GitHub token with permissions to post comments | Yes | - |
| `use_bedrock` | Whether to use AWS Bedrock | Yes | - |
| `model` | The Claude model ID to use | Yes | - |

### AWS Configuration

The action expects AWS credentials to be configured via the workflow that calls it. It uses:
- AWS Bedrock Runtime API
- The specified Claude model from the `model` input

### Permissions Required

The GitHub token must have:
- `issues: write` - to post comments on issues
- `pull-requests: write` - to post comments on PRs
- `contents: read` - to read repository content

## Example

See `.github/workflows/claude-pr.yml` for a complete example of how this action is used.

## Troubleshooting

### No response from Claude
- Check AWS credentials are properly configured
- Verify the model ID is correct and available in your region
- Check CloudWatch logs for Bedrock invocation errors

### Comments not posting
- Verify GitHub App has correct permissions
- Check the GitHub token has write access to issues/PRs
- Review action logs for API errors

## License

MIT
