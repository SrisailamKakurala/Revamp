# GitHub Actions — Comprehensive Study Notes

These notes are based on the structure and concepts in your own [GitHub Actions Comprehensive Guide](https://github.com/SrisailamKakurala/github-actions?utm_source=chatgpt.com). I’m keeping its terminology and topic coverage, while organizing the material into a study-friendly format with explanations and YAML examples.

The guide covers the fundamentals first, then moves into triggers, workflow conditions, expressions, automation, deployment, and advanced workflow design.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://github.com\&sz=32)

SrisailamKakurala/github-actions · GitHub



## 1. Introduction to GitHub Actions

GitHub Actions is GitHub’s automation platform. It lets you automatically execute tasks when events happen in a repository.

For example:

- When you push code → run tests.
- When you create a pull request → check code quality.
- When tests pass on `main` → deploy the application.
- Every night → run scheduled maintenance.

### CI and CD

| Term                        | Meaning                                                        |
| --------------------------- | -------------------------------------------------------------- |
| CI — Continuous Integration | Automatically build and test code when changes are introduced. |
| CD — Continuous Delivery    | Keep code ready for deployment after it passes checks.         |
| CD — Continuous Deployment  | Automatically deploy successful changes to an environment.     |

### Core concepts

| Concept  | Meaning                                  |
| -------- | ---------------------------------------- |
| Workflow | A YAML file defining automated tasks.    |
| Event    | Something that triggers a workflow.      |
| Job      | A group of steps executed on a runner.   |
| Step     | One task inside a job.                   |
| Action   | A reusable unit of automation.           |
| Runner   | The machine/environment executing a job. |

Think of it this way: Event → Workflow → Job → Steps → Actions or commands → Result.

## 2. Workflow files and directory structure

GitHub Actions workflow files are stored in:

```
.github/
└── workflows/
    ├── ci.yml
    ├── test.yml
    └── deploy.yml
```

A workflow file uses YAML syntax and usually contains:

```
name: CI Workflow

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Run tests
        run: npm test
```

### Main workflow components

- `name`: Workflow's display name.
- `on`: Events that trigger the workflow.
- `jobs`: Jobs that need to execute.
- `runs-on`: Runner environment for a job.
- `steps`: Individual tasks inside the job.
- `uses`: Runs a reusable action.
- `run`: Executes a shell command.

## 3. Events and workflow triggers

Events are trigger points that tell GitHub when to execute a workflow.

### Common events

| Event                 | When it triggers                         |
| --------------------- | ---------------------------------------- |
| `push`                | Commits are pushed.                      |
| `pull_request`        | A pull request is opened or updated.     |
| `issues`              | An issue is opened, edited, or closed.   |
| `release`             | A release event occurs.                  |
| `workflow_dispatch`   | Someone manually starts a workflow.      |
| `schedule`            | A scheduled time is reached.             |
| `repository_dispatch` | An external system sends a custom event. |
| `status`              | A commit status changes.                 |

### 3.1 Push event

Runs when commits are pushed.

```
on:
  push:
    branches:
      - main
    paths:
      - '**/*.js'
```

Here:

- `branches` limits execution to pushes on `main`.
- `paths` limits execution to changes involving JavaScript files.

### 3.2 Pull request event

```
on:
  pull_request:
    types: [opened, closed]
```

This workflow runs when a pull request is opened or closed.

### 3.3 Issue event

```
on:
  issues:
    types: [opened, edited, closed]
```

Useful for automating issue management.

### 3.4 Release event

```
on:
  release:
    types: [created, published]
```

Useful for automating release-related tasks.

### 3.5 Manual trigger — `workflow_dispatch`

Allows a user to start a workflow manually from GitHub's Actions interface.

```
on:
  workflow_dispatch:
    inputs:
      deploy_env:
        description: 'Deployment Environment'
        required: true
        default: 'staging'
```

The user can supply an input such as `staging` or `production`.

### 3.6 Scheduled trigger — `schedule`

Runs workflows according to a cron expression.

```
on:
  schedule:
    - cron: '0 0 * * *'
```

This example schedules a workflow at midnight UTC every day.

### 3.7 Other built-in events in your guide

Your README also lists:

- `create` / `delete`: Branch or tag creation/deletion.
- `fork`: Repository forked.
- `deployment`: A deployment is created.
- `deployment_status`: Deployment status changes.
- `pull_request_review`: A pull request review is submitted.
- `pull_request_target`: Pull request workflow using the target repository context and permissions.
- `discussion`: Discussion activity.
- `star`: Repository starred.
- `workflow_run`: Another workflow completes.
- `check_run` / `check_suite`: Check status events.

Important distinction: `workflow_dispatch` is a manual GitHub UI trigger; `repository_dispatch` is designed for an external system to trigger a workflow through the GitHub API.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://github.com\&sz=32)

SrisailamKakurala/github-actions · GitHub



## 4. Custom webhook triggers

Your README goes deeper into two triggers that are especially useful for connecting GitHub Actions with other applications.

### 4.1 `workflow_dispatch` — manual execution

You can manually start a workflow and provide inputs.

```
name: Manual Deployment

on:
  workflow_dispatch:
    inputs:
      environment:
        description: Deployment environment
        required: true
        default: production

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Show environment
        run: echo "Deploying to ${{ inputs.environment }}"
```

Use case: You want to deploy to staging or production only when someone explicitly starts the workflow.

### 4.2 `repository_dispatch` — external execution

This allows an external application or server to trigger a workflow using GitHub's API.

```
name: External Trigger

on:
  repository_dispatch:
    types:
      - sync-data

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - name: Read payload
        run: echo '${{ toJSON(github.event.client_payload) }}'
```

An external system sends a POST request:

```
curl -X POST \
  -H "Authorization: Bearer YOUR_GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/OWNER/REPO/dispatches \
  -d '{"event_type":"sync-data","client_payload":{"key":"value"}}'
```

The `event_type` must match the configured event type. The `client_payload` carries custom data.

| `workflow_dispatch`             | `repository_dispatch`              |
| ------------------------------- | ---------------------------------- |
| Started manually through GitHub | Triggered through the API          |
| User provides workflow inputs   | External system provides a payload |
| Useful for manual deployments   | Useful for external integrations   |

## 5. Conditional execution

Conditionals determine whether a job or step should execute.

The main keyword is:

```
if: <condition>
```

### 5.1 Workflow-level filtering

Your README explains that workflow execution can be restricted using event filters.

```
on:
  push:
    branches:
      - main
```

This limits the trigger to pushes on `main`.

### 5.2 Job-level conditions

```
jobs:
  build:
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    steps:
      - run: echo "Running for a pull request"
```

The job executes only when the triggering event is a pull request.

### 5.3 Step-level conditions

```
steps:
  - name: Build
    run: echo "Building..."

  - name: Deploy
    if: success()
    run: echo "Deploying..."
```

The deploy step executes only if the preceding steps succeeded.

### 5.4 Status-check functions

| Function      | Purpose                                  |
| ------------- | ---------------------------------------- |
| `success()`   | Runs when previous steps/jobs succeeded. |
| `failure()`   | Runs when a previous step/job failed.    |
| `always()`    | Runs regardless of success or failure.   |
| `cancelled()` | Runs when execution was canceled.        |

### 5.5 Event-specific conditions

```
if: github.event_name == 'push'
```

Checks the event type.

```
if: startsWith(github.ref, 'refs/heads/main')
```

Checks whether the Git reference starts with the main branch reference.

```
if: github.actor == 'octocat'
```

Checks who triggered the workflow.

### 5.6 Combining conditions

```
if: github.ref == 'refs/heads/main' && success()
```

Operators:

- `&&` — AND: both conditions must be true.
- `||` — OR: at least one condition must be true.
- `!` — NOT: reverses a condition.

### 5.7 Conditions using manual inputs

```
on:
  workflow_dispatch:
    inputs:
      deploy:
        description: Should deploy?
        required: true
        default: 'false'

jobs:
  deploy:
    runs-on: ubuntu-latest
    if: github.event.inputs.deploy == 'true'
    steps:
      - run: echo "Deploying..."
```

The job runs only if the input is `true`.

## 6. Expressions

Expressions allow workflows to calculate values, access dynamic information, and make decisions.

### 6.1 Syntax

```
if: ${{ github.ref == 'refs/heads/main' }}
```

The `${{ }}` syntax tells GitHub Actions to evaluate an expression.

### 6.2 Operators

\| Category | Operators |\
\|---|---|\
\| Arithmetic | `+`, `-`, `*`, `/`, `%` |\
\| Comparison | `==`, `!=`, `<`, `<=`, `>`, `>=` |\
\| Logical | `&&`, `||`, `!` |

### 6.3 Built-in functions

Status functions

```
success()
failure()
cancelled()
always()
```

String functions

```
startsWith(github.ref, 'refs/heads/')
endsWith(github.ref, '/main')
contains(github.event_name, 'push')
```

Utility functions

```
format('Deploying to {0}', github.ref)
join(github.event.issue.labels.*.name, ', ')
toJSON(github.event)
```

### 6.4 Practical examples

Check the current branch:

```
if: ${{ github.ref == 'refs/heads/main' }}
```

Check the pull request author:

```
if: ${{ github.event.pull_request.user.login == 'octocat' }}
```

Run only after success:

```
if: ${{ success() }}
```

Combine conditions:

```
if: ${{ github.actor == 'octocat' && github.event_name == 'push' }}
```

Remember the difference:

- `if` decides whether something should execute.
- Expressions provide the dynamic values and logic used to make that decision.

## 7. Runners

A runner is the machine that executes your workflow jobs.

Your README describes two main types.

### 7.1 GitHub-hosted runners

GitHub provides and manages the virtual machine.

Common operating systems:

- Ubuntu
- Windows
- macOS

Example:

```
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: echo "Hello World"
```

Advantages:

- No infrastructure setup.
- Preconfigured with common development tools.
- GitHub manages maintenance and updates.
- Suitable for general CI/CD workflows.

Disadvantages:

- Less control over the underlying environment.
- Resource and usage limitations.

### 7.2 Self-hosted runners

You configure and maintain your own machine.

```
jobs:
  build:
    runs-on: self-hosted
    steps:
      - uses: actions/checkout@v2
      - run: echo "Running on my machine"
```

You can also use labels:

```
runs-on: [self-hosted, linux]
```

Advantages:

- Control over installed software and configuration.
- Custom hardware and environments.
- Useful for private network access and specialized workloads.

Disadvantages:

- You maintain the machine.
- You handle updates, scaling, and hardware failures.
- Security and cleanup become your responsibility.

### 7.3 Runner lifecycle

1. A workflow is triggered.
2. GitHub finds an available runner.
3. The runner executes the job's steps.
4. The job completes or fails.
5. GitHub-hosted environments are discarded; self-hosted environments can persist.

### 7.4 Choosing a runner

| Requirement                     | Suitable runner   |
| ------------------------------- | ----------------- |
| Normal Node.js/Python testing   | GitHub-hosted     |
| Windows/macOS testing           | GitHub-hosted     |
| Custom software or hardware     | Self-hosted       |
| Access to a private network     | Often self-hosted |
| Full control over machine setup | Self-hosted       |

## 8. Workflow commands

Workflow commands allow a running script to communicate with the GitHub Actions runner.

They can set environment variables, create log annotations, mask sensitive values, and organize logs.

### 8.1 Set environment variables

Use the `GITHUB_ENV` file:

```
steps:
  - name: Set variable
    run: echo "MY_VAR=Hello World" >> $GITHUB_ENV

  - name: Read variable
    run: echo "$MY_VAR"
```

The variable becomes available to subsequent steps in the same job.

### 8.2 Set outputs

Outputs allow one step to pass a value to another step.

Your README includes the older `set-output` syntax. It is deprecated. The modern approach uses `GITHUB_OUTPUT`:

```
steps:
  - name: Generate output
    id: step1
    run: echo "message=Hello World" >> $GITHUB_OUTPUT

  - name: Read output
    run: echo "${{ steps.step1.outputs.message }}"
```

Notice:

- `id` gives the step an identifier.
- `GITHUB_OUTPUT` stores the output.
- `steps.step1.outputs.message` retrieves it.

### 8.3 Group logs

```
- name: Group logs
  run: |
    echo "::group::Build logs"
    echo "Installing dependencies..."
    echo "Building application..."
    echo "::endgroup::"
```

This groups related log messages in the Actions interface.

### 8.4 Annotations

Annotations display warnings, errors, and notices.

```
echo "::warning::This is a warning"
echo "::error::This is an error"
echo "::notice::This is an informational message"
```

You can also associate an annotation with a file and line:

```
echo "::error file=app.js,line=10,col=15::Something went wrong"
```

### 8.5 Mask sensitive values

```
echo "::add-mask::my-sensitive-value"
```

This tells GitHub Actions to mask that value in logs.

It is not a replacement for securely storing secrets.

### 8.6 Debug messages

```
echo "::debug::Checking application configuration"
```

Useful when troubleshooting workflows.

### 8.7 Upload artifacts

Artifacts are files generated during a workflow that you want to preserve or download later.

```
- name: Upload logs
  uses: actions/upload-artifact@v3
  with:
    name: my-logs
    path: ./logs/
```

Examples of artifacts:

- Test reports.
- Build output.
- Compiled files.
- Debug logs.

### Workflow commands summary

| Command           | Purpose                   |
| ----------------- | ------------------------- |
| `GITHUB_ENV`      | Set environment variables |
| `GITHUB_OUTPUT`   | Set step outputs          |
| `::group::`       | Group logs                |
| `::endgroup::`    | End a log group           |
| `::debug::`       | Add debug information     |
| `::warning::`     | Add warning annotation    |
| `::error::`       | Add error annotation      |
| `::notice::`      | Add notice annotation     |
| `::add-mask::`    | Mask a sensitive value    |
| `upload-artifact` | Save workflow files       |

## 9. Workflow contexts

Contexts are predefined objects that expose information about the workflow, repository, runner, jobs, and other data.

You access them using expressions:

```
${{ context.property }}
```

### 9.1 `github` context

Provides information about the repository and workflow event.

```
${{ github.repository }}
${{ github.event_name }}
${{ github.actor }}
${{ github.ref }}
${{ github.sha }}
${{ github.run_number }}
```

Examples:

- `github.repository`: repository name.
- `github.event_name`: event that triggered the workflow.
- `github.actor`: user who triggered it.
- `github.ref`: branch or tag reference.
- `github.sha`: commit SHA.

### 9.2 `env` context

Access environment variables:

```
${{ env.MY_VAR }}
```

### 9.3 `job` context

Information about the current job:

```
${{ job.id }}
${{ job.status }}
```

### 9.4 `runner` context

Information about the machine running the job:

```
${{ runner.os }}
${{ runner.temp }}
${{ runner.tool_cache }}
```

### 9.5 `secrets` context

Access stored secrets:

```
${{ secrets.MY_SECRET }}
```

Never print secret values in logs.

### 9.6 `steps` context

Access outputs from earlier steps in the same job:

```
${{ steps.step1.outputs.message }}
```

### 9.7 `strategy` / `matrix` context

Access the current matrix configuration:

```
${{ matrix.os }}
${{ matrix.node }}
```

### 9.8 `needs` context

Access outputs from jobs that the current job depends on:

```
${{ needs.build.outputs.version }}
```

### 9.9 `inputs` context

Access values passed into a manually triggered or reusable workflow:

```
${{ inputs.environment }}
```

### Context cheat sheet

| Context   | What it provides                 |
| --------- | -------------------------------- |
| `github`  | Repository and event information |
| `env`     | Environment variables            |
| `job`     | Current job details              |
| `runner`  | Runner details                   |
| `secrets` | Secret values                    |
| `steps`   | Step outputs                     |
| `matrix`  | Current matrix configuration     |
| `needs`   | Dependency job outputs           |
| `inputs`  | Workflow inputs                  |

## 10. Dependent jobs and execution order

By default, jobs without dependencies can execute in parallel.

To make one job wait for another, use `needs`.

### 10.1 Simple dependency

```
jobs:
  job1:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Job 1"

  job2:
    runs-on: ubuntu-latest
    needs: job1
    steps:
      - run: echo "Job 2"
```

Here:

- `job1` starts first.
- `job2` waits for `job1` to complete successfully.

### 10.2 Multiple dependencies

```
jobs:
  job1:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Job 1"

  job2:
    runs-on: ubuntu-latest
    needs: job1
    steps:
      - run: echo "Job 2"

  job3:
    runs-on: ubuntu-latest
    needs: [job1, job2]
    steps:
      - run: echo "Job 3"
```

Execution order:

```
job1 → job2 → job3
```

`job3` waits for both `job1` and `job2`.

### 10.3 Parallel execution

```
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Testing"

  lint:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Linting"
```

Because neither job depends on the other, they can run in parallel.

### 10.4 Passing outputs between jobs

Sometimes a job generates information that another job needs.

```
jobs:
  build:
    runs-on: ubuntu-latest

    outputs:
      version: ${{ steps.get_version.outputs.version }}

    steps:
      - id: get_version
        run: echo "version=1.0.0" >> $GITHUB_OUTPUT

  deploy:
    runs-on: ubuntu-latest
    needs: build

    steps:
      - name: Use build output
        run: echo "Deploying version ${{ needs.build.outputs.version }}"
```

Understand the chain:

1. The first job creates an output.
2. The job exposes it through its `outputs` section.
3. The second job declares `needs: build`.
4. The second job accesses it through `needs.build.outputs.version`.

### 10.5 Conditional dependencies

```
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Testing"

  deploy:
    runs-on: ubuntu-latest
    needs: test
    if: success() && github.event_name == 'push'
    steps:
      - run: echo "Deploying"
```

This combines job dependencies and conditional execution.

### Best practices

- Keep dependency chains short.
- Use `failure()` or `always()` for failure handling and cleanup.
- Document complex job relationships.
- Use parallel jobs when tasks do not depend on one another.

## 11. Encrypted secrets and environment variables

Your README introduces these topics under:

- Encrypted Secrets
- Configuration Secrets
- Default ENV Variables
- Set Custom ENV Variables

The headings are present, but the detailed explanations under these headings are not filled out. The guide does, however, explain `secrets`, `env`, and `GITHUB_TOKEN` elsewhere.

### 11.1 Environment variables

Environment variables store configuration values that workflows can access.

```
name: Environment Demo

on: push

env:
  APP_NAME: my-app

jobs:
  build:
    runs-on: ubuntu-latest
    env:
      NODE_ENV: production

    steps:
      - name: Print variables
        run: |
          echo "$APP_NAME"
          echo "$NODE_ENV"
```

You can define variables at different levels:

| Location             | Availability          |
| -------------------- | --------------------- |
| Workflow-level `env` | All jobs and steps    |
| Job-level `env`      | All steps in that job |
| Step-level `env`     | Only that step        |

### 11.2 Secrets

Secrets store sensitive information, such as:

- API keys.
- Database passwords.
- Deployment credentials.
- Access tokens.

Example:

```
steps:
  - name: Deploy
    run: ./deploy.sh
    env:
      API_KEY: ${{ secrets.API_KEY }}
```

Secrets should be configured through GitHub's repository, organization, or environment settings.

Important: Never hardcode credentials into workflow files or commit them to your repository.

## 12. GITHUB_TOKEN

`GITHUB_TOKEN` is a token automatically generated by GitHub for each workflow run.

It allows a workflow to interact with GitHub securely.

### What can it do?

- Push commits.
- Create issues.
- Comment on pull requests.
- Publish packages.
- Make authenticated GitHub API requests.
- Automate repository operations.

### 12.1 Using GITHUB_TOKEN

```
name: Token Example

on:
  push:
    branches:
      - main

jobs:
  update:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v3

      - name: Make changes
        run: echo "New content" >> file.txt

      - name: Commit and push
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"

          git add .
          git commit -m "Automated update"
          git push
```

### 12.2 Important properties

| Property           | Explanation                                                |
| ------------------ | ---------------------------------------------------------- |
| Automatic creation | Generated for every workflow run                           |
| Authentication     | Used for GitHub API and repository operations              |
| Permissions        | Controlled by repository settings and workflow permissions |
| Lifecycle          | Valid for the duration of the workflow run                 |
| Scope              | Restricted to the repository's permitted access            |

### 12.3 Making API requests

Your README demonstrates creating an issue using the GitHub API.

```
- name: Create GitHub Issue
  env:
    GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  run: |
    curl -X POST \
      -H "Authorization: Bearer $GH_TOKEN" \
      -H "Accept: application/vnd.github+json" \
      "https://api.github.com/repos/${{ github.repository }}/issues" \
      -d '{"title":"Automated Issue","body":"Created by a workflow."}'
```

### 12.4 Restricting token permissions

Use the `permissions` key to limit what the token can do.

```
jobs:
  build:
    runs-on: ubuntu-latest

    permissions:
      contents: read
      issues: write

    steps:
      - run: echo "Using restricted permissions"
```

- `contents: read` allows reading repository contents.
- `issues: write` allows creating or modifying issues.

### Security best practices

1. Never print tokens in workflow logs.
2. Give tokens only the permissions they need.
3. Prefer `GITHUB_TOKEN` over creating personal access tokens when it is sufficient.
4. Use secrets for external credentials.

## 13. Running scripts in workflows

You can execute commands and scripts directly from GitHub Actions.

### 13.1 Inline commands

```
steps:
  - name: Run commands
    run: |
      echo "Hello World"
      pwd
      ls -la
```

The `|` allows multiple shell commands inside one YAML value.

### 13.2 Run an external script

Suppose your repository contains:

```
project/
├── scripts/
│   └── myscript.sh
└── .github/
    └── workflows/
        └── ci.yml
```

Workflow:

```
steps:
  - name: Checkout repository
    uses: actions/checkout@v3

  - name: Run script
    run: ./scripts/myscript.sh
```

Ensure the script has executable permission:

```
chmod +x scripts/myscript.sh
```

### 13.3 Different shells

```
steps:
  - name: Run Bash
    run: echo "Running Bash"
    shell: bash

  - name: Run PowerShell
    run: Write-Output "Running PowerShell"
    shell: pwsh
```

### 13.4 Run Node.js or Python scripts

```
- name: Run Node.js
  run: node scripts/myscript.js

- name: Run Python
  run: python scripts/myscript.py
```

### Script execution best practices

- Configure reusable values through `env`.
- Install dependencies before executing scripts.
- Use appropriate shells.
- Handle errors properly.
- Your README also mentions `set -e`, which makes a shell script stop when a command fails.

## 14. Publishing packages using workflows

GitHub Actions can automate publishing packages and Docker images.

Your README covers two main examples.

### 14.1 Publishing an npm package

Typical sequence:

```
Checkout code
     ↓
Set up Node.js
     ↓
Authenticate with package registry
     ↓
Install dependencies
     ↓
Build package
     ↓
Publish package
```

Example:

```
name: Publish npm Package

on:
  push:
    branches:
      - main

jobs:
  publish:
    runs-on: ubuntu-latest

    permissions:
      contents: read
      packages: write

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: 16
          registry-url: https://npm.pkg.github.com/

      - name: Install dependencies
        run: npm install

      - name: Build
        run: npm run build

      - name: Publish
        run: npm publish
        env:
          NODE_AUTH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

The registry URL and authentication configure npm to publish to GitHub Packages.

### 14.2 Publishing Docker images

Typical sequence:

```
Checkout code
     ↓
Authenticate with GHCR
     ↓
Build Docker image
     ↓
Push Docker image
```

Example:

```
name: Publish Docker Image

on:
  push:
    branches:
      - main

jobs:
  publish:
    runs-on: ubuntu-latest

    permissions:
      contents: read
      packages: write

    steps:
      - name: Checkout
        uses: actions/checkout@v3

      - name: Login to GHCR
        run: |
          echo "${{ secrets.GITHUB_TOKEN }}" |
          docker login ghcr.io \
            -u "$GITHUB_ACTOR" \
            --password-stdin

      - name: Build image
        run: |
          docker build -t ghcr.io/OWNER/IMAGE-NAME:latest .

      - name: Push image
        run: |
          docker push ghcr.io/OWNER/IMAGE-NAME:latest
```

GHCR stands for GitHub Container Registry.

It stores container images, which can later be pulled and run on servers.

## 15. Publishing GitHub releases

A GitHub release represents a particular version of your project.

For example:

```
v1.0.0
v1.1.0
v2.0.0
```

A release can contain:

- Version information.
- Release notes.
- Compiled application files.
- Downloadable assets.

### Automating releases

Your README demonstrates triggering a release when a version tag is pushed.

```
name: Create GitHub Release

on:
  push:
    tags:
      - 'v*.*.*'

jobs:
  release:
    runs-on: ubuntu-latest

    permissions:
      contents: write

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Create release
        uses: softprops/action-gh-release@v1
        with:
          files: './dist/*'
```

### Execution flow

1. Create a version tag, such as `v1.0.0`.
2. Push the tag to GitHub.
3. The workflow detects the matching tag.
4. The release action creates a GitHub release.
5. The specified files are attached.

This is useful when distributing stable versions of an application or library.

## 16. Deploying to the cloud

Your README has a `deploy to cloud` heading, but it does not contain a detailed implementation under that heading.

It does mention that GitHub Actions can deploy applications to providers such as:

- AWS
- Azure
- Google Cloud

The general process is:

```
Code pushed to GitHub
        ↓
Workflow triggered
        ↓
Checkout repository
        ↓
Install dependencies
        ↓
Build application
        ↓
Authenticate with cloud provider
        ↓
Deploy application
```

The actual deployment commands depend on the hosting provider and application architecture.

## 17. Service containers

Service containers are Docker containers that run alongside a workflow job.

They provide services your application needs during testing.

Examples:

- MySQL.
- PostgreSQL.
- Redis.
- Other supporting services.

### Example: MySQL service container

```
jobs:
  test:
    runs-on: ubuntu-latest

    services:
      mysql:
        image: mysql:5.7
        env:
          MYSQL_ROOT_PASSWORD: root
        ports:
          - 3306:3306

    steps:
      - name: Checkout
        uses: actions/checkout@v3

      - name: Run tests
        run: |
          # Wait for MySQL to start
          sleep 20

          # Run application tests
```

### How it works

1. GitHub starts the job runner.
2. It starts the MySQL service container.
3. The service exposes its port.
4. Your test commands connect to the database.
5. Tests run against the temporary database service.

For a Node.js backend, this is useful when integration tests require an actual database instead of mocked database calls.

## 18. Routing workflows to runners

This topic is closely related to the runners section.

The `runs-on` property decides which machine executes a particular job.

GitHub-hosted example:

```
jobs:
  build:
    runs-on: ubuntu-latest
```

Self-hosted example:

```
jobs:
  build:
    runs-on: self-hosted
```

Self-hosted runner with labels:

```
jobs:
  build:
    runs-on: [self-hosted, linux]
```

The purpose is to ensure that the job runs in an environment with the required operating system, tools, hardware, and configuration.

## 19. CodeQL

CodeQL is a code analysis tool that helps identify bugs and security vulnerabilities.

It analyzes source code using queries that look for potentially problematic patterns.

### What it does

- Analyzes application source code.
- Identifies potential security vulnerabilities.
- Detects problematic coding patterns.
- Can run automatically during CI workflows.

### Example workflow from your README

```
name: CodeQL Analysis

on:
  push:
    branches:
      - main

  pull_request:
    branches:
      - main

jobs:
  analyze:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Initialize CodeQL
        uses: github/codeql-action/init@v2

      - name: Analyze
        uses: github/codeql-action/analyze@v2
```

### Execution flow

```
Push / Pull Request
        ↓
Checkout source code
        ↓
Initialize CodeQL
        ↓
Analyze source code
        ↓
Identify potential issues
```

The goal is to detect problems before they reach production.

## 20. Caching dependencies and build outputs

Caching saves time by reusing files from previous workflow runs.

Without caching, a workflow may repeatedly download and install the same dependencies.

### 20.1 Dependency caching

Example from your README:

```
- name: Cache Node.js dependencies
  uses: actions/cache@v3

  with:
    path: ~/.npm

    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}

    restore-keys: |
      ${{ runner.os }}-node-
```

### Understand each property

| Property       | Meaning                                      |
| -------------- | -------------------------------------------- |
| `path`         | Files or directories to cache                |
| `key`          | Unique identifier for the cache              |
| `hashFiles()`  | Calculates a hash based on matching files    |
| `restore-keys` | Fallback prefixes for finding a usable cache |

Why use `package-lock.json`?

Because it describes the npm dependency versions. If the dependency file changes, the hash changes and a different cache key is generated.

### 20.2 Build output caching

```
- name: Cache build outputs
  uses: actions/cache@v3

  with:
    path: build/

    key: ${{ runner.os }}-build-${{ hashFiles('**/*.cpp') }}

    restore-keys: |
      ${{ runner.os }}-build-
```

Here, the build directory is cached.

### Dependency cache vs artifact

| Cache                         | Artifact                             |
| ----------------------------- | ------------------------------------ |
| Primarily improves speed      | Preserves workflow-generated files   |
| Reused by later workflow runs | Downloaded or transferred later      |
| Uses cache keys               | Uses artifact names                  |
| Useful for dependencies       | Useful for reports and build outputs |

## 21. Workflow status badges

A status badge displays the state of a workflow directly in your repository's README.

For example:



Build passing

Build failing



Your README gives this example:

```
![Workflow Status](https://img.shields.io/github/workflow/status/username/repo-name/Workflow-Name)
```

Replace:

- `username` with your GitHub username.
- `repo-name` with your repository.
- `Workflow-Name` with your workflow's name.

The badge helps visitors quickly see whether the project's automated checks are passing.

## 22. Environment protections

Environments allow you to configure deployment targets such as:

- Development.
- Staging.
- Production.

Your README demonstrates:

```
jobs:
  deploy:
    runs-on: ubuntu-latest

    environment: production

    steps:
      - name: Deploy
        run: echo "Deploying to production"
```

You can configure environment protection rules through GitHub repository settings.

These can restrict access and require approval before deployment, depending on the configured rules.

Example: Your development workflow can run automatically, while production deployment requires approval.

## 23. Job matrix configuration

A matrix allows you to execute the same job using multiple configurations.

Instead of writing separate jobs for each Node.js version or operating system, define a matrix.

### Example

```
jobs:
  build:
    runs-on: ${{ matrix.os }}

    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        node: [18, 20]

    steps:
      - name: Checkout
        uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: ${{ matrix.node }}
```

This produces six combinations:

| Operating system | Node.js |
| ---------------- | ------- |
| Ubuntu           | 18      |
| Ubuntu           | 20      |
| macOS            | 18      |
| macOS            | 20      |
| Windows          | 18      |
| Windows          | 20      |

The benefit is that you can test your application across multiple environments without manually creating six separate jobs.

## 24. Action versions

When you use an action, you specify its version using `@`.

Example:

```
- name: Checkout code
  uses: actions/checkout@v3
```

This tells GitHub to use version 3 of the checkout action.

Your README emphasizes specifying action versions to maintain stability and avoid unexpected changes.

## 25. Exit codes

Exit codes tell GitHub Actions whether a script succeeded or failed.

| Exit code | Meaning |
| --------- | ------- |
| `0`       | Success |
| Non-zero  | Failure |

### Successful command

```
exit 0
```

### Failed command

```
exit 1
```

If a workflow step exits with a non-zero code, the step generally fails, and subsequent steps are skipped unless configured otherwise.

Example:

```
steps:
  - name: Validate
    run: |
      if [ -f package.json ]; then
        echo "Package file exists"
        exit 0
      else
        echo "Package file missing"
        exit 1
      fi
```

This is important because shell scripts and application commands communicate their results to GitHub Actions through exit codes.

## 26. Reusable workflows

Reusable workflows allow you to define a workflow once and call it from other workflows.

This avoids repeating the same CI/CD configuration across repositories or workflow files.

### 26.1 Create a reusable workflow

File:

```
.github/workflows/reusable-workflow.yml
```

```
name: Reusable Workflow

on:
  workflow_call:
    inputs:
      exampleInput:
        required: true
        type: string

jobs:
  example-job:
    runs-on: ubuntu-latest

    steps:
      - name: Display input
        run: echo "Input received: ${{ inputs.exampleInput }}"
```

### 26.2 Call the reusable workflow

File:

```
.github/workflows/main.yml
```

```
name: Main Workflow

on:
  push:
    branches:
      - main

jobs:
  call-reusable-workflow:
    uses: ./.github/workflows/reusable-workflow.yml

    with:
      exampleInput: 'Hello'
```

### Understand the flow

1. The main workflow gets triggered.
2. It calls the reusable workflow.
3. It passes an input using `with`.
4. The reusable workflow receives that input through `inputs`.
5. It executes its jobs.

### Important terms

| Keyword         | Purpose                              |
| --------------- | ------------------------------------ |
| `workflow_call` | Makes a workflow reusable            |
| `inputs`        | Defines parameters                   |
| `with`          | Passes values to the called workflow |
| `uses`          | References the reusable workflow     |

## 27. Creating custom GitHub Actions

Reusable workflows and custom actions are related, but they are not the same.

- A reusable workflow reuses a collection of jobs and steps.
- A custom action packages a reusable task that can be used as a step.

Your README demonstrates creating a custom JavaScript action.

### 27.1 Directory structure

```
my-custom-action/
├── action.yml
├── index.js
└── package.json
```

### 27.2 `action.yml`

This file defines the action's metadata, inputs, outputs, and execution configuration.

```
name: My Custom Action

description: A custom action to demonstrate GitHub Actions

inputs:
  myInput:
    description: Input string
    required: true
    default: default

outputs:
  myOutput:
    description: Output string

runs:
  using: node20
  main: index.js
```

### 27.3 `index.js`

```
const core = require('@actions/core');

try {
  const myInput = core.getInput('myInput');

  console.log(`Received input: ${myInput}`);

  core.setOutput(
    'myOutput',
    `Processed: ${myInput}`
  );

} catch (error) {
  core.setFailed(error.message);
}
```

### Understand the important functions

| Function           | Purpose                             |
| ------------------ | ----------------------------------- |
| `core.getInput()`  | Reads an input passed to the action |
| `core.setOutput()` | Creates an output value             |
| `core.setFailed()` | Marks the action as failed          |
| `console.log()`    | Prints information in workflow logs |

### 27.4 `package.json`

Your README includes:

```
{
  "name": "my-custom-action",
  "version": "1.0.0",
  "main": "index.js",
  "dependencies": {
    "@actions/core": "^1.0.0"
  }
}
```

This defines the Node.js package and its dependency.

### 27.5 Calling a custom action

Once the action is available in your repository:

```
steps:
  - name: Run custom action
    uses: ./
    with:
      myInput: Hello
```

The action receives the input, executes its JavaScript logic, and can return an output.

# 28. Complete concept map

This is the overall structure of the concepts in your README.

GitHub Actions

Automation platform

Events

push, PR, schedule, manual

Workflow

YAML configuration

Jobs

Parallel or sequential execution using needs

Runner

GitHub-hosted or self-hosted

Steps

run commands or use actions

Build & Test

Scripts, dependencies, matrix, CodeQL

Security

Secrets, permissions, GITHUB_TOKEN

Optimization

Caching, artifacts, parallel jobs

Deployment

Cloud, packages, Docker, releases

# 29. Important notes about your README

I preserved the concepts and examples from your repository rather than silently replacing them with a different guide. A few details are worth keeping in mind when you actually implement the examples:

1. Older action versions: Many examples use `actions/checkout@v2`, `actions/cache@v2`, `actions/upload-artifact@v3`, and other older versions. Treat these as examples of syntax, not a recommendation to use those versions in a new project.
2. Deprecated outputs: The old `::set-output` syntax is deprecated. Use `$GITHUB_OUTPUT` for step outputs.
3. Environment variables: A value written to `$GITHUB_ENV` is available to subsequent steps, not automatically to the same step that writes it.
4. Job outputs: To pass data between jobs, use `$GITHUB_OUTPUT`, expose the step output under the job's `outputs`, and access it through `needs`.
5. Cloud deployment: Your README names cloud providers but does not provide a complete deployment implementation.
6. Encrypted/configuration secrets: The headings exist, but detailed notes are missing from the source.

These distinctions matter because your README is a learning reference, while the actual workflow you run needs valid, current action versions and correctly configured permissions.

# 30. What you should be able to do after studying this guide

Use this as your revision checklist:

Your GitHub Actions progress

# 0%

0 of 21 concepts completed

Explain CI, CD, workflows, events, jobs, steps, actions, and runners

Create a workflow triggered by push and pull_request

Use workflow_dispatch inputs and repository_dispatch payloads

Configure branch and path filters

Write job-level and step-level conditions

Use expressions, operators, and built-in functions

Choose between GitHub-hosted and self-hosted runners

Set environment variables and step outputs

Use workflow contexts such as github, env, steps, matrix, and needs

Create dependent jobs and pass outputs between jobs

Store secrets and configure GITHUB_TOKEN permissions

Execute shell, Node.js, and Python scripts

Publish npm packages and Docker images

Automate GitHub releases using tags

Run MySQL or other service containers for testing

Configure CodeQL and dependency caching

Use workflow artifacts and status badges

Configure deployment environments and protections

Build matrix workflows across operating systems and language versions

Create and call reusable workflows

Create a custom JavaScript GitHub Action

My recommendation: Don't just memorize YAML. Build one complete CI/CD pipeline for a Node.js application: run tests on pull requests, build on `main`, cache npm dependencies, publish a Docker image, and deploy it. That one project will connect most of the concepts in your README.

Source: [Your GitHub Actions Comprehensive Guide — README.md](https://github.com/SrisailamKakurala/github-actions?utm_source=chatgpt.com).&#x20;

[image](https://www.google.com/s2/favicons?domain=https://github.com\&sz=32)

SrisailamKakurala/github-actions · GitHub+3
