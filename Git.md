Bro, let's rebuild your Git and GitHub knowledge from the ground up, but with a proper developer workflow in mind.

Since you've already learned advanced concepts like rebasing, cherry-picking, squashing, and forking, we're not going to stop at basic commands. We'll start with the fundamentals, refresh your memory, and gradually move toward professional team workflows, open-source contributions, and production-grade GitHub practices.

Think of this as your Git + GitHub revision handbook.

# Git & GitHub Master Notes

Beginner → Advanced → Production

What you'll cover

- Git fundamentals and internal concepts
- Daily Git commands and workflows
- Branching, merging, rebasing
- Cherry-picking, squashing, stashing
- Undoing mistakes and recovering commits
- GitHub repositories, forks, PRs, reviews
- Open-source contribution workflows
- GitHub Actions and CI/CD
- Production-grade repository practices
- Hands-on exercises and revision challenges

  Recommended approach: Learn one section, execute its commands, and move on only after you've practiced.

# PART 1 — Understanding Git

## 1. What exactly is Git?

Git is a distributed version control system (VCS).

In simple terms, it tracks changes in your code over time.

Imagine you're building a FastAPI application.

Day 1:

- Created the application.
- Added task creation.

Day 2:

\- Added authentication.

Day 3:

\- Authentication broke the application.

Without Git, you'd have to manually recover your old code.

With Git, you can inspect previous versions, restore files, create branches, and collaborate with other developers.

### Git vs GitHub

These are two different things.

| Git                          | GitHub                               |
| ---------------------------- | ------------------------------------ |
| Version control system       | Cloud-based code hosting platform    |
| Works locally                | Hosts remote repositories            |
| Tracks code changes          | Hosts repositories and collaboration |
| Handles commits and branches | Handles PRs, issues, reviews         |
| Can work without internet    | Usually requires internet            |

Other platforms similar to GitHub:

- GitLab
- Bitbucket
- Gitea

Remember: Git is the technology. GitHub is one platform built around it.

## 2. How Git actually works

Before memorizing commands, understand these four areas.

Working Directory

Your actual project files where you write code

git add

Staging Area / Index

Changes you've selected for the next commit

git commit

Local Repository

Your committed history, stored in .git

git push

Remote Repository

Your GitHub repository

Let's understand each one.

Working Directory

Your actual project folder.

```
task-manager/
├── app.py
├── requirements.txt
└── README.md
```

You modify files here.

Staging Area

You choose which changes should go into the next commit.

```
git add app.py
```

Only `app.py` is staged, not every modified file.

Local Repository

When you commit, Git saves a snapshot of the staged content in its history.

```
git commit -m "Add task creation API"
```

Remote Repository

When you push, your local commits are sent to a remote repository such as GitHub.

```
git push origin main
```

### Important Git terminology

| Term       | Meaning                                   |
| ---------- | ----------------------------------------- |
| Repository | Project tracked by Git                    |
| Commit     | Saved snapshot of changes                 |
| Branch     | Independent line of development           |
| HEAD       | Pointer to your current checkout          |
| Index      | Another name for staging area             |
| Remote     | Reference to another repository           |
| Origin     | Conventional name for your default remote |
| Hash       | Unique identifier of a Git object         |
| Merge      | Combines histories                        |
| Rebase     | Replays commits onto another base         |

## 3. What happens internally when you commit?

Git primarily stores four object types:

1. Blob: File content.
2. Tree: Directory structure and references to blobs or other trees.
3. Commit: References a tree, parent commit(s), author information, and message.
4. Tag: A named reference to a Git object, often used for releases.

Example:

```
Commit A
   |
   v
Commit B
   |
   v
Commit C
```

Each commit references a tree representing that project's snapshot.

You can inspect Git's objects using:

```
git cat-file -p <hash>
git cat-file -t <hash>
```

To see a commit's details:

```
git show <commit-hash>
```

Git uses content-addressed object storage. Object IDs are generally SHA-1 or SHA-256, depending on the repository's object format.

# PART 2 — Initial Git Setup

## 4. Install and configure Git

Install Git from [git-scm.com](https://git-scm.com/downloads?utm_source=chatgpt.com).

Verify installation:

```
git --version
```

Configure your identity:

```
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

Set your preferred default branch:

```
git config --global init.defaultBranch main
```

Set a default editor if needed:

```
git config --global core.editor "code --wait"
```

View configurations:

```
git config --list
```

Check a specific configuration:

```
git config user.name
```

### Configuration levels

Git configuration can exist at three levels:

| Level      | Scope              |
| ---------- | ------------------ |
| `--system` | Entire machine     |
| `--global` | Your user account  |
| `--local`  | Current repository |

Local settings override global settings, which override system settings.

Example:

```
git config --local user.email "work@example.com"
```

This changes your identity only for that repository.

## 5. Initialize a repository

Create a project:

```
mkdir task-manager
cd task-manager
```

Initialize Git:

```
git init
```

Git creates a hidden `.git` directory.

```
task-manager/
├── .git/
└── app.py
```

The `.git` folder contains the repository's history, configuration, references, and objects.

Check status:

```
git status
```

Add your file:

```
git add app.py
```

Commit:

```
git commit -m "Initial commit"
```

Congratulations. You now have a local Git repository.

## 6. Essential daily commands

These are the commands you'll use constantly.

| Command                       | Purpose                                |
| ----------------------------- | -------------------------------------- |
| `git status`                  | Check working tree and staging status  |
| `git add .`                   | Stage changes in the current directory |
| `git add <file>`              | Stage a particular file                |
| `git commit -m "message"`     | Create a commit                        |
| `git log`                     | View commit history                    |
| `git diff`                    | View unstaged changes                  |
| `git diff --staged`           | View staged changes                    |
| `git show`                    | Inspect a commit                       |
| `git rm <file>`               | Remove a tracked file                  |
| `git mv old new`              | Rename/move a tracked file             |
| `git restore <file>`          | Discard unstaged changes               |
| `git restore --staged <file>` | Unstage a file                         |

### Understanding git diff

Suppose you modify `app.py`.

```
git diff
```

Shows changes between your working directory and staging area.

Then:

```
git add app.py
git diff --staged
```

Shows changes between your staging area and the last commit.

This distinction is extremely important.

# PART 3 — Git Branching

## 7. What is a branch?

A branch is a movable pointer to a commit.

Imagine your production application is working correctly. You now want to add authentication.

You shouldn't experiment directly on the production development branch.

Instead, create a separate branch.

```
main
 |
 A
 |
 B
 |
 C

feature/authentication
 |
 D
 |
 E
```

Both branches share the same earlier history, but the feature branch can evolve independently.

### Create and switch branches

```
# List local branches
git branch

# Create a branch
git branch feature/auth

# Switch to it
git switch feature/auth
```

Shortcut:

```
git switch -c feature/auth
```

Older equivalent:

```
git checkout -b feature/auth
```

I recommend learning `git switch` for branch operations and `git restore` for restoring files.

### Delete branches

```
# Delete a merged local branch
git branch -d feature/auth

# Force-delete an unmerged local branch
git branch -D feature/auth
```

### Rename a branch

```
git branch -m old-name new-name
```

### See all branches

```
git branch -a
```

Includes local and remote-tracking branches.

## 8. Branch naming conventions

In professional projects, use descriptive branch names.

```
feature/user-authentication
feature/task-management
bugfix/login-validation
hotfix/payment-crash
refactor/database-layer
docs/api-documentation
chore/update-dependencies
```

A common pattern:

```
<type>/<short-description>
```

## 9. Merging branches

Suppose you've finished your authentication feature.

You want to integrate it into `main`.

```
git switch main
git merge feature/auth
```

Git combines the changes.

### Three possible merge situations

A. Fast-forward merge

If `main` hasn't changed since the feature branch was created, Git can simply move the branch pointer forward.

```
Before:

A---B---C (main)
         \
          D---E (feature)

After:

A---B---C---D---E (main)
```

No merge commit is necessary.

B. Three-way merge

If both branches have new commits, Git uses their common ancestor and combines the changes.

```
        D---E (feature)
       /
A---B---C---F (main)
             \
              M (merge result)
```

The resulting commit has two parents.

C. Merge conflict

If Git cannot automatically combine changes, it asks you to resolve them.

We'll cover that shortly.

### Disable fast-forward

```
git merge --no-ff feature/auth
```

This creates a merge commit even when fast-forward is possible.

Useful when you want to preserve a visible feature-branch merge in project history.

### Squash merge

```
git merge --squash feature/auth
git commit -m "Add authentication"
```

This combines the feature branch's changes into one staged result on the target branch.

It doesn't create a merge commit or mark the feature branch's commits as merged.

# PART 4 — Remote Repositories and GitHub

## 10. What is a remote?

A remote is a named reference to another Git repository.

For example, your local project may be connected to GitHub.

```
git remote -v
```

Add a remote:

```
git remote add origin https://github.com/username/task-manager.git
```

Change its URL:

```
git remote set-url origin <repository-url>
```

Remove it:

```
git remote remove origin
```

`origin` is simply a conventional name. It isn't a special Git keyword.

## 11. Push, pull, and fetch

These three commands are fundamental to collaboration.

### git push

Sends your local commits to a remote.

```
git push origin main
```

For the first push of a new branch:

```
git push -u origin feature/auth
```

`-u` sets the upstream tracking branch, so later you can use:

```
git push
```

### git fetch

Downloads remote changes and updates remote-tracking references without merging them into your current branch.

```
git fetch origin
```

You can inspect the changes before integrating them.

```
git log HEAD..origin/main --oneline
```

### git pull

Fetches remote changes and integrates them into your current branch.

```
git pull origin main
```

By default, Git typically uses merge behavior.

You can configure pull to rebase instead:

```
git pull --rebase origin main
```

Remember:

- `fetch` = Download and inspect.
- `pull` = Fetch + integrate.
- `push` = Upload your local commits.

My recommendation: use `git fetch` regularly so you understand what's changing before integrating it.

## 12. Clone a GitHub repository

To download an existing repository:

```
git clone https://github.com/username/project.git
```

Clone into a custom folder:

```
git clone https://github.com/username/project.git my-project
```

Clone a specific branch:

```
git clone -b development https://github.com/username/project.git
```

Clone without the complete history:

```
git clone --depth 1 https://github.com/username/project.git
```

This is called a shallow clone.

# PART 5 — Undoing Mistakes

This is one of the most important sections. Every developer makes mistakes. Knowing how to recover is part of being a good developer.

## 13. git restore

You modified a file but haven't staged it.

```
git restore app.py
```

This discards unstaged modifications and restores the file from the index.

Unstage a file:

```
git restore --staged app.py
```

This removes it from the staging area but keeps your working changes.

Be careful: `git restore` can permanently discard uncommitted work.

## 14. git reset

`git reset` moves the current branch pointer and can also modify the index and working directory.

Imagine:

```
A---B---C (HEAD)
```

You want to undo commit C.

### Soft reset

```
git reset --soft HEAD~1
```

- Removes C from the current branch history.
- Keeps changes staged.
- Your files remain unchanged.

### Mixed reset

```
git reset --mixed HEAD~1
```

- Removes C from the current branch history.
- Keeps changes in your working directory.
- Unstages those changes.

This is the default reset mode.

### Hard reset

```
git reset --hard HEAD~1
```

- Removes C from the current branch history.
- Resets the staging area.
- Resets tracked files in your working directory.

Destructive operation

Uncommitted changes can be lost.

### Quick comparison

| Command   | Commit removed? | Changes staged?         |
| --------- | --------------- | ----------------------- |
| `--soft`  | Yes             | Yes                     |
| `--mixed` | Yes             | No                      |
| `--hard`  | Yes             | No; working files reset |

## 15. git revert

Suppose a commit was already pushed to GitHub and other developers may have based work on it.

Instead of rewriting shared history, use:

```
git revert <commit-hash>
```

Git creates a new commit that reverses the selected commit's changes.

```
A---B---C---D
         |
         C is problematic

A---B---C---D---E
                 E reverses C
```

Unlike `reset`, it preserves the existing commit history.

Professional rule: Prefer `revert` when undoing published/shared commits.

## 16. git reflog — your recovery tool

This is a command you should never forget.

Imagine you accidentally run:

```
git reset --hard HEAD~3
```

You think three commits are gone forever.

But Git's reference log often lets you recover the previous branch position.

```
git reflog
```

Example:

```
abc123 HEAD@{0}: reset: moving to HEAD~3
def456 HEAD@{1}: commit: Add authentication
ghi789 HEAD@{2}: commit: Add task update
```

Recover the previous position:

```
git reset --hard def456
```

Or create a recovery branch first:

```
git branch recovery def456
```

Reflog entries are local and eventually expire, so don't rely on them as permanent backups.

# PART 6 — Advanced Git Concepts

Now we're getting into the concepts you mentioned learning a year ago.

## 17. Git stash

Suppose you're working on authentication.

Suddenly, your team asks you to fix an urgent production bug.

You don't want to commit unfinished authentication code.

You can temporarily save your changes using stash.

```
git stash
```

Your working directory becomes clean.

Switch branches:

```
git switch main
git switch -c hotfix/login-error
```

Fix the bug, commit it, and return:

```
git switch feature/auth
```

Restore the saved work:

```
git stash pop
```

### Useful stash commands

```
# Save with a description
git stash push -m "Authentication work in progress"

# List stashes
git stash list

# Apply latest stash without deleting it
git stash apply

# Apply a specific stash
git stash apply stash@{1}

# Delete latest stash
git stash drop

# Delete all stashes
git stash clear
```

Include untracked files:

```
git stash -u
```

`pop` applies a stash and removes it if successful. `apply` keeps it.

## 18. Cherry-picking

Imagine you have two branches:

```
main:       A---B---C
                 \
feature:          D---E---F
```

You need only commit E in `main`, not D or F.

That's exactly what cherry-picking does.

```
git switch main
git cherry-pick <commit-hash>
```

Git applies the changes introduced by that commit and creates a new commit on your current branch.

### Cherry-pick multiple commits

```
git cherry-pick <hash1> <hash2>
```

Pick a range:

```
git cherry-pick <start>..<end>
```

This excludes the starting commit and includes the ending commit.

### If a conflict occurs

```
# Resolve conflicting files first
git add .

# Continue cherry-pick
git cherry-pick --continue
```

Abort it:

```
git cherry-pick --abort
```

Real-world example: A critical bug fix is committed to a development branch. You want that exact fix in the production branch without merging all the development work.

Cherry-pick is useful here.

## 19. Git rebase

Rebase is one of the most important advanced Git concepts.

Imagine:

```
        D---E (feature)
       /
A---B---C---F (main)
```

Your feature branch started from B, but main has progressed to F.

You want your feature commits to appear as if they were developed on top of F.

```
git switch feature
git rebase main
```

Result:

```
A---B---C---F---D'---E' (feature)
```

Notice `D'` and `E'`.

They are new commits with new hashes. Rebase replays changes onto a new base; it doesn't simply move the old commits.

### Merge vs rebase

| Merge                      | Rebase                            |
| -------------------------- | --------------------------------- |
| Combines branch histories  | Replays commits onto a new base   |
| Can create a merge commit  | Usually creates a linear history  |
| Preserves original commits | Creates new commit identities     |
| Safe for shared history    | Requires care with shared history |

### Rebase conflicts

```
git rebase main
```

If conflicts happen:

```
# Fix the conflicting files
git add .

# Continue
git rebase --continue
```

To cancel:

```
git rebase --abort
```

### Important production rule

Never casually rebase commits that other developers are already using.

Why?

Because rebase changes commit hashes. Your teammates may still have the old history.

If you've rewritten your own published feature branch and coordinated the change with your team, you may need:

```
git push --force-with-lease
```

Prefer `--force-with-lease` over `--force`. It checks that the remote branch hasn't changed unexpectedly before replacing it.

## 20. Interactive rebase

This is where you can edit your commit history.

```
git rebase -i HEAD~4
```

This opens an editor showing the last four commits.

Example:

```
pick abc123 Add task model
pick def456 Fix task model
pick ghi789 Add task routes
pick jkl012 Update routes
```

You can change the commands.

| Command  | Purpose                                           |
| -------- | ------------------------------------------------- |
| `pick`   | Keep commit                                       |
| `reword` | Change commit message                             |
| `edit`   | Stop and modify commit                            |
| `squash` | Combine with previous commit and edit message     |
| `fixup`  | Combine with previous commit, discard its message |
| `drop`   | Remove commit                                     |

### Example: Squashing commits

You made these commits:

```
Add task model
Fix task model
Fix typo
Fix typo again
```

You don't want four tiny commits in your final feature history.

Run:

```
git rebase -i HEAD~4
```

Change the list:

```
pick abc123 Add task model
squash def456 Fix task model
squash ghi789 Fix typo
squash jkl012 Fix typo again
```

Git combines them into one commit, letting you edit the final message.

Result:

```
Add task model
```

### Squash vs fixup

- `squash`: Combines commits and lets you edit the resulting message.
- `fixup`: Combines commits and discards the fixup commit's message.

### Amend the latest commit

Forgot to include a file?

```
git add missing_file.py
git commit --amend
```

Change only the message:

```
git commit --amend -m "Improve task creation"
```

This replaces the previous commit with a new one. Avoid amending published commits unless you understand the consequences.

## 21. Git tags

Tags mark specific commits, commonly for releases.

For example:

```
v1.0.0
v1.1.0
v2.0.0
```

Create an annotated tag:

```
git tag -a v1.0.0 -m "First production release"
```

List tags:

```
git tag
```

Inspect:

```
git show v1.0.0
```

Push a tag:

```
git push origin v1.0.0
```

Push all tags:

```
git push origin --tags
```

Delete a local tag:

```
git tag -d v1.0.0
```

Delete a remote tag:

```
git push origin --delete v1.0.0
```

# PART 7 — Git Conflict Resolution

## 22. What is a merge conflict?

Imagine two developers edit the same line.

Developer A:

```
message = "Welcome"
```

Developer B:

```
message = "Hello there"
```

Git can't decide which change is correct.

You might see:

```
<<<<<<< HEADmessage = "Welcome"=======message = "Hello there">>>>>>> feature/greeting
```

These markers show the competing changes.

- `<<<<<<< HEAD`: Current branch's version.
- `=======`: Separates the versions.
- `>>>>>>> feature/greeting`: Incoming branch's version.

You manually decide what the final code should be.

For example:

```
message = "Welcome to our application"
```

Then:

```
git add app.py
git commit
```

For a merge conflict, this completes the merge.

For a rebase conflict, use:

```
git rebase --continue
```

### Conflict resolution workflow

1. Run `git status`.
2. Identify conflicting files.
3. Open them and understand both changes.
4. Combine the correct logic.
5. Remove conflict markers.
6. Test your application.
7. Stage resolved files.
8. Complete the merge/rebase/cherry-pick.

Never blindly choose "Accept Current" or "Accept Incoming" without understanding the code.

# PART 8 — GitHub: Professional Collaboration

## 23. Creating a GitHub repository

Visit [GitHub](https://github.com?utm_source=chatgpt.com).

Create a repository.

You'll typically choose:

- Repository name.
- Description.
- Public or private visibility.
- README initialization.
- `.gitignore` template.
- License.

### Public vs private

Public repository

- Anyone can view the code.
- People can fork it.
- Contributions can be made through pull requests.

Private repository

- Access is restricted.
- You control who can view and contribute.

## 24. Connecting local Git to GitHub

Create a local project:

```
git init
git add .
git commit -m "Initial commit"

git branch -M main

git remote add origin https://github.com/username/task-manager.git

git push -u origin main
```

Your local repository is now connected to GitHub.

### HTTPS vs SSH authentication

HTTPS:

```
git clone https://github.com/username/project.git
```

SSH:

```
git clone git@github.com:username/project.git
```

SSH requires you to configure an SSH key and add its public key to GitHub.

GitHub does not accept your account password for normal Git HTTPS authentication. Use an appropriate credential manager or personal access token when prompted.

## 25. Pull Requests (PRs)

A Pull Request is a request to integrate changes from one branch into another.

Imagine you're working on a team.

Your teammate asks you to implement login authentication.

You:

1. Create a feature branch.
2. Write the authentication code.
3. Commit the changes.
4. Push your branch to GitHub.
5. Open a Pull Request.
6. Teammates review the code.
7. Address feedback.
8. Merge the PR.

Example:

```
git switch -c feature/login
```

Make changes and commit:

```
git add .
git commit -m "Add login authentication"
```

Push:

```
git push -u origin feature/login
```

Go to GitHub and create a PR.

### What should a good PR contain?

- Clear title.
- What was changed.
- Why it was changed.
- Screenshots if UI changes are involved.
- Testing performed.
- Related issue number.
- Potential breaking changes.

Example PR description:

```
## Summary
- Added user login endpoint.
- Added password validation.
- Added JWT token generation.

## Testing
- Tested valid login.
- Tested incorrect password.
- Tested missing email.

## Related issue
Closes #12
```

### PR review terminology

| Term                 | Meaning                                |
| -------------------- | -------------------------------------- |
| Approve              | Reviewer approves changes              |
| Comment              | Reviewer leaves feedback               |
| Request changes      | Reviewer wants changes before approval |
| Resolve conversation | Mark a review discussion as addressed  |
| Merge                | Integrate PR changes                   |

### PR merge strategies

GitHub supports three common merge strategies:

Merge commit

Preserves the branch history and creates a merge commit.

Squash and merge

Combines the PR commits into one commit on the target branch.

Rebase and merge

Replays the PR commits onto the target branch without a merge commit.

Your team should agree on a consistent strategy.

# PART 9 — Forking and Open Source

## 26. What is forking?

Suppose you discover a project on GitHub that you like.

You don't have permission to push directly to its repository.

You can create your own copy under your GitHub account.

That's a fork.

Original repository

github.com/owner/project

Fork

Your fork

github.com/yourname/project

Clone + contribute

Pull Request

Your fork → Original repository

### Complete open-source contribution workflow

Step 1: Fork the repository

Click the Fork button on GitHub.

Step 2: Clone your fork

```
git clone https://github.com/yourname/project.git
cd project
```

Step 3: Add the original repository as upstream

```
git remote add upstream https://github.com/original-owner/project.git
```

Check:

```
git remote -v
```

You should see:

```
origin    your fork
upstream  original repository
```

Step 4: Sync your fork

```
git fetch upstream
```

Update your local main branch:

```
git switch main
git merge upstream/main
```

Or, if your team/project uses a linear history:

```
git rebase upstream/main
```

Push your updated fork:

```
git push origin main
```

Step 5: Create your feature branch

```
git switch -c feature/fix-login
```

Step 6: Make changes and commit

```
git add .
git commit -m "Fix login validation"
```

Step 7: Push to your fork

```
git push -u origin feature/fix-login
```

Step 8: Open a PR

On GitHub, select:

```
base repository: original-owner/project
base branch: main

head repository: yourname/project
compare branch: feature/fix-login
```

Now your contribution is submitted for review.

### Important: origin vs upstream

| Remote     | Meaning             |
| ---------- | ------------------- |
| `origin`   | Your fork           |
| `upstream` | Original repository |

This is a very common open-source workflow.

## 27. Finding open-source projects

Useful resources:

- [Good First Issues](https://github.com/topics/good-first-issue?utm_source=chatgpt.com)
- [Good First Issue website](https://goodfirstissue.dev/?utm_source=chatgpt.com)
- [Up For Grabs](https://up-for-grabs.net/?utm_source=chatgpt.com)
- [GitHub Explore](https://github.com/explore?utm_source=chatgpt.com)

### How to contribute properly

Don't immediately pick a massive feature.

Start with:

1. Documentation improvements.
2. Small bug fixes.
3. Tests.
4. Error handling.
5. Small feature enhancements.

Read these files before contributing:

- `README.md`
- `CONTRIBUTING.md`
- `CODE_OF_CONDUCT.md`
- `LICENSE`

Follow the repository's contribution rules.

# PART 10 — Production-Grade Git Practices

This is where we move from knowing Git to using it as a software engineer.

## 28. Git workflow strategies

There are different ways teams organize branches.

### A. GitHub Flow

A simple and popular workflow.

```
main
  |
  ├── feature/login
  ├── feature/dashboard
  └── bugfix/payment
```

Process:

1. Keep `main` deployable.
2. Create feature branches.
3. Commit changes.
4. Push to GitHub.
5. Open PRs.
6. Review and test.
7. Merge.
8. Deploy.

For many modern web applications, this is a great starting point.

### B. Git Flow

A more structured branching model.

Common branches:

| Branch      | Purpose                 |
| ----------- | ----------------------- |
| `main`      | Production-ready code   |
| `develop`   | Integration branch      |
| `feature/*` | New functionality       |
| `release/*` | Preparing releases      |
| `hotfix/*`  | Urgent production fixes |

Typical flow:

```
feature → develop → release → main
                         |
                       hotfix
```

Git Flow can be useful for projects with scheduled releases and separate stabilization periods. It is not mandatory for every team.

## 29. Protect your main branch

In a production repository, you generally don't want developers directly pushing unfinished code to `main`.

GitHub offers branch protection rules and repository rulesets.

Common protections:

- Require a pull request before merging.
- Require approvals.
- Require CI checks to pass.
- Require conversations to be resolved.
- Restrict force pushes.
- Restrict branch deletion.

This makes the main branch safer.

## 30. `.gitignore`

This file tells Git which untracked files and directories to ignore.

Example for a Python project:

```
# Python cache
__pycache__/
*.py[cod]

# Virtual environments
venv/
.venv/

# Environment variables and secrets
.env
.env.*

# Keep example environment files
!.env.example

# IDE files
.vscode/
.idea/

# Testing
.pytest_cache/
.coverage
htmlcov/

# Build files
dist/
build/

# Operating system
.DS_Store
Thumbs.db
```

### Important

`.gitignore` does not automatically stop tracking files already committed.

If `.env` is already tracked:

```
git rm --cached .env
git commit -m "Stop tracking environment file"
```

If you accidentally committed a secret, simply removing the file is not enough. Rotate the exposed credential and follow a repository-history cleanup process if necessary.

## 31. Never commit secrets

Never commit:

```
.env
database passwords
API keys
JWT secrets
private SSH keys
cloud credentials
```

Instead, provide an example:

`.env.example`

```
DATABASE_URL=postgresql://user:password@localhost/db
JWT_SECRET=replace-this-value
```

Use GitHub Actions secrets or an appropriate secret manager for deployment credentials.

## 32. Conventional Commits

A standard commit message structure helps maintain clean history.

```
<type>(optional scope): description
```

Examples:

```
git commit -m "feat(auth): add JWT authentication"

git commit -m "fix(tasks): handle missing task IDs"

git commit -m "docs(readme): update installation guide"

git commit -m "refactor(api): separate route handlers"

git commit -m "test(auth): add login validation tests"

git commit -m "chore(deps): update FastAPI"
```

Common types:

| Type       | Meaning                 |
| ---------- | ----------------------- |
| `feat`     | New feature             |
| `fix`      | Bug fix                 |
| `docs`     | Documentation           |
| `refactor` | Code restructuring      |
| `test`     | Tests                   |
| `chore`    | Maintenance             |
| `perf`     | Performance improvement |
| `ci`       | CI/CD changes           |
| `build`    | Build system changes    |

## 33. Semantic Versioning

Production applications often use semantic versioning.

```
MAJOR.MINOR.PATCH
```

Example:

```
1.4.2
```

- MAJOR: Breaking changes.
- MINOR: New backward-compatible functionality.
- PATCH: Backward-compatible bug fixes.

Examples:

```
1.0.0 → 1.0.1  Bug fix
1.0.1 → 1.1.0  New feature
1.1.0 → 2.0.0  Breaking API change
```

Create a release tag:

```
git tag -a v1.1.0 -m "Release 1.1.0"
git push origin v1.1.0
```

GitHub can then create a Release from that tag.

# PART 11 — GitHub Actions and CI/CD

## 34. What is GitHub Actions?

GitHub Actions is an automation platform integrated with GitHub.

You can automatically run tasks when events happen in your repository.

For example:

- Someone pushes code.
- Someone opens a PR.
- A release is published.
- A scheduled workflow runs.

You can automatically install dependencies, run tests, check code quality, build applications, and deploy.

### What is CI/CD?

CI — Continuous Integration

Automatically integrate and test code changes.

CD — Continuous Delivery/Deployment

Prepare or automatically deploy tested code.

### Basic GitHub Actions workflow

Create:

```
.github/
└── workflows/
    └── python-tests.yml
```

Add:

```

name: Python API Tests

# Run this workflow on pushes and pull requests to main.
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      # Download repository code
      - name: Checkout code
        uses: actions/checkout@v4

      # Install Python
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      # Install dependencies
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install fastapi httpx pytest

      # Run tests
      - name: Run tests
        run: pytest

```

This is a starting example. In a real project, install from your pinned dependency file and add the tests and configuration your project needs.

### Understanding the YAML

| Property  | Meaning                         |
| --------- | ------------------------------- |
| `name`    | Workflow name                   |
| `on`      | Events that trigger it          |
| `jobs`    | Tasks to execute                |
| `runs-on` | Machine environment             |
| `steps`   | Individual actions/commands     |
| `uses`    | Reuse an existing GitHub Action |
| `run`     | Execute shell commands          |
| `with`    | Pass configuration to an action |

### What happens when you create a PR?

```
Developer pushes code
        ↓
GitHub detects push/PR
        ↓
GitHub Actions starts
        ↓
Install dependencies
        ↓
Run tests
        ↓
Tests pass or fail
        ↓
PR status check updates
```

You can configure branch protection so a PR cannot merge until required checks pass.

# PART 12 — Advanced Tools Worth Knowing

## 35. git bisect

Imagine your application worked 20 commits ago, but now it crashes.

You don't know which commit introduced the bug.

Instead of manually checking every commit, use binary search.

```
git bisect start
git bisect bad
git bisect good <known-good-commit>
```

Git checks out a commit halfway through the range.

Test your application.

If it's broken:

```
git bisect bad
```

If it works:

```
git bisect good
```

Git keeps narrowing down the range.

Finish:

```
git bisect reset
```

This is incredibly useful when debugging large codebases.

## 36. git blame

Want to know who last modified a particular line?

```
git blame app.py
```

For a specific line range:

```
git blame -L 10,30 app.py
```

It shows the commit and author associated with each line's latest change.

Use it to understand history, not to blame teammates.

## 37. git log

Useful history commands:

```
# Standard history
git log

# Compact history
git log --oneline

# Graph view
git log --graph --oneline --all

# Last 5 commits
git log -5

# History of a particular file
git log -- app.py

# Show commits by author
git log --author="Your Name"
```

One of the most useful commands:

```
git log --oneline --graph --decorate --all
```

It gives you a visual representation of branch history in the terminal.

## 38. git clean

Removes untracked files.

Preview what would be deleted:

```
git clean -n
```

Remove untracked files:

```
git clean -f
```

Remove untracked files and directories:

```
git clean -fd
```

Destructive operation

It can delete work that Git isn't tracking. Always preview first.

## 39. Git submodules

A submodule lets you include another Git repository inside your repository.

Example:

```
git submodule add https://github.com/example/library.git libs/library
```

Clone a project with its submodules:

```
git clone --recurse-submodules <repo-url>
```

Initialize existing submodules:

```
git submodule update --init --recursive
```

Submodules are useful when you need to track an external repository at a particular commit. They also introduce additional maintenance complexity, so don't use them unnecessarily.

# PART 13 — A Professional GitHub Repository

## 40. What should a production repository look like?

For your Python API project, a reasonable structure could be:

```
task-manager-api/
│
├── .github/
│   ├── workflows/
│   │   └── tests.yml
│   ├── ISSUE_TEMPLATE/
│   └── PULL_REQUEST_TEMPLATE.md
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── routes/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── database/
│
├── tests/
│   ├── test_tasks.py
│   └── test_auth.py
│
├── .env.example
├── .gitignore
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── requirements.txt
└── pyproject.toml
```

A production-quality repository should generally include:

- Clear README with setup instructions.
- `.gitignore`.
- Dependency management.
- Tests.
- CI workflow.
- License.
- Contribution guidelines if open source.
- Environment variable documentation.
- Security policy.
- Issue and PR templates where useful.

### Useful GitHub features

| Feature       | Why it matters                     |
| ------------- | ---------------------------------- |
| Issues        | Track bugs and tasks               |
| Projects      | Manage project boards              |
| Discussions   | Community conversations            |
| Pull Requests | Code review and integration        |
| Actions       | CI/CD automation                   |
| Releases      | Publish versions                   |
| Packages      | Host packages and container images |
| Dependabot    | Dependency update automation       |
| Code Security | Security scanning and alerts       |
| CODEOWNERS    | Automatically request reviewers    |

Useful documentation:

- [GitHub Docs](https://docs.github.com/en?utm_source=chatgpt.com)
- [GitHub Actions Docs](https://docs.github.com/en/actions?utm_source=chatgpt.com)
- [Official Git Documentation](https://git-scm.com/docs?utm_source=chatgpt.com)

# PART 14 — Your Hands-on Revision Roadmap

Don't just read all these notes. The best way to regain your Git knowledge is to deliberately break things and fix them.

Let's use one project throughout: `git-practice-lab`.

## Exercise 1 — Fundamentals

Beginner

- Create a repository using `git init`.
- Add three Python files.
- Stage one file only.
- Commit it.
- Stage the remaining files.
- Create another commit.
- Inspect `git status`.
- Compare `git diff` and `git diff --staged`.
- Inspect your history using `git log`.

## Exercise 2 — Branching

Beginner → Intermediate

- Create `feature/auth`.
- Add a login function.
- Commit your changes.
- Create `feature/tasks`.
- Add a task creation function.
- Merge both features into `main`.
- Try a fast-forward merge.
- Try a three-way merge.
- Create and resolve a merge conflict.

## Exercise 3 — Undo and Recovery

Intermediate

- Modify a file and use `git restore`.
- Stage a file and unstage it.
- Create three commits.
- Experiment with `git reset --soft`.
- Experiment with `git reset --mixed`.
- Understand `git reset --hard` in a disposable repository.
- Revert a commit.
- Recover a previous branch position using `git reflog`.

## Exercise 4 — Advanced Git

Advanced

- Stash unfinished work.
- Apply and pop stashes.
- Cherry-pick a commit.
- Rebase a feature branch.
- Resolve a rebase conflict.
- Interactive rebase.
- Squash four commits into one.
- Use `fixup`.
- Amend the latest commit.
- Create and push a tag.
- Use `git bisect` to find a deliberately introduced bug.

## Exercise 5 — GitHub Collaboration

Professional

- Create a GitHub account/repository.
- Push your local project.
- Clone the repository into another folder.
- Create a feature branch.
- Push that branch.
- Open a PR.
- Add a PR description.
- Review your own PR.
- Merge using squash and merge.
- Delete the feature branch.

## Exercise 6 — Open Source

Advanced

- Find an open-source Python project.
- Fork it.
- Clone your fork.
- Add the original repository as `upstream`.
- Fetch upstream changes.
- Create a feature branch.
- Make a meaningful contribution.
- Write a good commit message.
- Push to your fork.
- Open a PR against the original project.
- Respond to review feedback.
- Update your PR.

## Exercise 7 — Production workflow

Production-grade

- Create a repository with a proper folder structure.
- Add a `.gitignore`.
- Add `.env.example`.
- Configure branch protection.
- Add PR templates.
- Add GitHub Actions.
- Run automated tests on PRs.
- Add a license.
- Add a README.
- Create a versioned release.
- Configure Dependabot.
- Add a security policy.

# PART 15 — Your Git Cheat Sheet

Keep this section handy when coding.

| What you want                   | Command                          |
| ------------------------------- | -------------------------------- |
| Initialize Git                  | `git init`                       |
| Check status                    | `git status`                     |
| Stage files                     | `git add .`                      |
| Commit                          | `git commit -m "message"`        |
| View history                    | `git log --oneline`              |
| Create branch                   | `git switch -c feature/name`     |
| Switch branch                   | `git switch main`                |
| Merge branch                    | `git merge feature/name`         |
| Rebase branch                   | `git rebase main`                |
| Cherry-pick                     | `git cherry-pick HASH`           |
| Squash commits                  | `git rebase -i HEAD~N`           |
| Stash work                      | `git stash`                      |
| Restore stash                   | `git stash pop`                  |
| Undo latest commit, keep staged | `git reset --soft HEAD~1`        |
| Undo published commit           | `git revert HASH`                |
| Recover history                 | `git reflog`                     |
| Download remote changes         | `git fetch`                      |
| Download and integrate          | `git pull`                       |
| Upload commits                  | `git push`                       |
| Add remote                      | `git remote add origin URL`      |
| Clone repository                | `git clone URL`                  |
| Create tag                      | `git tag -a v1.0.0 -m "Release"` |
| Find bug-introducing commit     | `git bisect`                     |
| Inspect line history            | `git blame FILE`                 |

# Final: How I want you to practice

I'd recommend doing this in three stages:

1. Stage 1: Spend a session revising fundamentals, branches, merging, and remote operations.
2. Stage 2: Practice reset, revert, reflog, stash, cherry-pick, interactive rebase, and conflict resolution in a disposable repository.
3. Stage 3: Contribute to an actual open-source project and set up CI/CD for one of your own projects.

One important thing: don't try to memorize 50 commands. Understand what Git is doing to your working tree, staging area, commits, and branches.

Once those concepts click again, the advanced commands become much easier.

Your first assignment: Create `git-practice-lab`, complete Exercises 1 and 2, and then we'll tackle the advanced Git scenarios with deliberately broken repositories. That's how we'll make sure you can actually recover from mistakes instead of just remembering command syntax.Bro, let's rebuild your Git and GitHub knowledge from the ground up, but with a proper developer workflow in mind.

Since you've already learned advanced concepts like rebasing, cherry-picking, squashing, and forking, we're not going to stop at basic commands. We'll start with the fundamentals, refresh your memory, and gradually move toward professional team workflows, open-source contributions, and production-grade GitHub practices.

Think of this as your Git + GitHub revision handbook.

# Git & GitHub Master Notes

Beginner → Advanced → Production

What you'll cover

- Git fundamentals and internal concepts
- Daily Git commands and workflows
- Branching, merging, rebasing
- Cherry-picking, squashing, stashing
- Undoing mistakes and recovering commits
- GitHub repositories, forks, PRs, reviews
- Open-source contribution workflows
- GitHub Actions and CI/CD
- Production-grade repository practices
- Hands-on exercises and revision challenges

  Recommended approach: Learn one section, execute its commands, and move on only after you've practiced.

# PART 1 — Understanding Git

## 1. What exactly is Git?

Git is a distributed version control system (VCS).

In simple terms, it tracks changes in your code over time.

Imagine you're building a FastAPI application.

Day 1:

- Created the application.
- Added task creation.

Day 2:

\- Added authentication.

Day 3:

\- Authentication broke the application.

Without Git, you'd have to manually recover your old code.

With Git, you can inspect previous versions, restore files, create branches, and collaborate with other developers.

### Git vs GitHub

These are two different things.

| Git                          | GitHub                               |
| ---------------------------- | ------------------------------------ |
| Version control system       | Cloud-based code hosting platform    |
| Works locally                | Hosts remote repositories            |
| Tracks code changes          | Hosts repositories and collaboration |
| Handles commits and branches | Handles PRs, issues, reviews         |
| Can work without internet    | Usually requires internet            |

Other platforms similar to GitHub:

- GitLab
- Bitbucket
- Gitea

Remember: Git is the technology. GitHub is one platform built around it.

## 2. How Git actually works

Before memorizing commands, understand these four areas.

Working Directory

Your actual project files where you write code

git add

Staging Area / Index

Changes you've selected for the next commit

git commit

Local Repository

Your committed history, stored in .git

git push

Remote Repository

Your GitHub repository

Let's understand each one.

Working Directory

Your actual project folder.

```
task-manager/
├── app.py
├── requirements.txt
└── README.md
```

You modify files here.

Staging Area

You choose which changes should go into the next commit.

```
git add app.py
```

Only `app.py` is staged, not every modified file.

Local Repository

When you commit, Git saves a snapshot of the staged content in its history.

```
git commit -m "Add task creation API"
```

Remote Repository

When you push, your local commits are sent to a remote repository such as GitHub.

```
git push origin main
```

### Important Git terminology

| Term       | Meaning                                   |
| ---------- | ----------------------------------------- |
| Repository | Project tracked by Git                    |
| Commit     | Saved snapshot of changes                 |
| Branch     | Independent line of development           |
| HEAD       | Pointer to your current checkout          |
| Index      | Another name for staging area             |
| Remote     | Reference to another repository           |
| Origin     | Conventional name for your default remote |
| Hash       | Unique identifier of a Git object         |
| Merge      | Combines histories                        |
| Rebase     | Replays commits onto another base         |

## 3. What happens internally when you commit?

Git primarily stores four object types:

1. Blob: File content.
2. Tree: Directory structure and references to blobs or other trees.
3. Commit: References a tree, parent commit(s), author information, and message.
4. Tag: A named reference to a Git object, often used for releases.

Example:

```
Commit A
   |
   v
Commit B
   |
   v
Commit C
```

Each commit references a tree representing that project's snapshot.

You can inspect Git's objects using:

```
git cat-file -p <hash>
git cat-file -t <hash>
```

To see a commit's details:

```
git show <commit-hash>
```

Git uses content-addressed object storage. Object IDs are generally SHA-1 or SHA-256, depending on the repository's object format.

# PART 2 — Initial Git Setup

## 4. Install and configure Git

Install Git from [git-scm.com](https://git-scm.com/downloads?utm_source=chatgpt.com).

Verify installation:

```
git --version
```

Configure your identity:

```
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

Set your preferred default branch:

```
git config --global init.defaultBranch main
```

Set a default editor if needed:

```
git config --global core.editor "code --wait"
```

View configurations:

```
git config --list
```

Check a specific configuration:

```
git config user.name
```

### Configuration levels

Git configuration can exist at three levels:

| Level      | Scope              |
| ---------- | ------------------ |
| `--system` | Entire machine     |
| `--global` | Your user account  |
| `--local`  | Current repository |

Local settings override global settings, which override system settings.

Example:

```
git config --local user.email "work@example.com"
```

This changes your identity only for that repository.

## 5. Initialize a repository

Create a project:

```
mkdir task-manager
cd task-manager
```

Initialize Git:

```
git init
```

Git creates a hidden `.git` directory.

```
task-manager/
├── .git/
└── app.py
```

The `.git` folder contains the repository's history, configuration, references, and objects.

Check status:

```
git status
```

Add your file:

```
git add app.py
```

Commit:

```
git commit -m "Initial commit"
```

Congratulations. You now have a local Git repository.

## 6. Essential daily commands

These are the commands you'll use constantly.

| Command                       | Purpose                                |
| ----------------------------- | -------------------------------------- |
| `git status`                  | Check working tree and staging status  |
| `git add .`                   | Stage changes in the current directory |
| `git add <file>`              | Stage a particular file                |
| `git commit -m "message"`     | Create a commit                        |
| `git log`                     | View commit history                    |
| `git diff`                    | View unstaged changes                  |
| `git diff --staged`           | View staged changes                    |
| `git show`                    | Inspect a commit                       |
| `git rm <file>`               | Remove a tracked file                  |
| `git mv old new`              | Rename/move a tracked file             |
| `git restore <file>`          | Discard unstaged changes               |
| `git restore --staged <file>` | Unstage a file                         |

### Understanding git diff

Suppose you modify `app.py`.

```
git diff
```

Shows changes between your working directory and staging area.

Then:

```
git add app.py
git diff --staged
```

Shows changes between your staging area and the last commit.

This distinction is extremely important.

# PART 3 — Git Branching

## 7. What is a branch?

A branch is a movable pointer to a commit.

Imagine your production application is working correctly. You now want to add authentication.

You shouldn't experiment directly on the production development branch.

Instead, create a separate branch.

```
main
 |
 A
 |
 B
 |
 C

feature/authentication
 |
 D
 |
 E
```

Both branches share the same earlier history, but the feature branch can evolve independently.

### Create and switch branches

```
# List local branches
git branch

# Create a branch
git branch feature/auth

# Switch to it
git switch feature/auth
```

Shortcut:

```
git switch -c feature/auth
```

Older equivalent:

```
git checkout -b feature/auth
```

I recommend learning `git switch` for branch operations and `git restore` for restoring files.

### Delete branches

```
# Delete a merged local branch
git branch -d feature/auth

# Force-delete an unmerged local branch
git branch -D feature/auth
```

### Rename a branch

```
git branch -m old-name new-name
```

### See all branches

```
git branch -a
```

Includes local and remote-tracking branches.

## 8. Branch naming conventions

In professional projects, use descriptive branch names.

```
feature/user-authentication
feature/task-management
bugfix/login-validation
hotfix/payment-crash
refactor/database-layer
docs/api-documentation
chore/update-dependencies
```

A common pattern:

```
<type>/<short-description>
```

## 9. Merging branches

Suppose you've finished your authentication feature.

You want to integrate it into `main`.

```
git switch main
git merge feature/auth
```

Git combines the changes.

### Three possible merge situations

A. Fast-forward merge

If `main` hasn't changed since the feature branch was created, Git can simply move the branch pointer forward.

```
Before:

A---B---C (main)
         \
          D---E (feature)

After:

A---B---C---D---E (main)
```

No merge commit is necessary.

B. Three-way merge

If both branches have new commits, Git uses their common ancestor and combines the changes.

```
        D---E (feature)
       /
A---B---C---F (main)
             \
              M (merge result)
```

The resulting commit has two parents.

C. Merge conflict

If Git cannot automatically combine changes, it asks you to resolve them.

We'll cover that shortly.

### Disable fast-forward

```
git merge --no-ff feature/auth
```

This creates a merge commit even when fast-forward is possible.

Useful when you want to preserve a visible feature-branch merge in project history.

### Squash merge

```
git merge --squash feature/auth
git commit -m "Add authentication"
```

This combines the feature branch's changes into one staged result on the target branch.

It doesn't create a merge commit or mark the feature branch's commits as merged.

# PART 4 — Remote Repositories and GitHub

## 10. What is a remote?

A remote is a named reference to another Git repository.

For example, your local project may be connected to GitHub.

```
git remote -v
```

Add a remote:

```
git remote add origin https://github.com/username/task-manager.git
```

Change its URL:

```
git remote set-url origin <repository-url>
```

Remove it:

```
git remote remove origin
```

`origin` is simply a conventional name. It isn't a special Git keyword.

## 11. Push, pull, and fetch

These three commands are fundamental to collaboration.

### git push

Sends your local commits to a remote.

```
git push origin main
```

For the first push of a new branch:

```
git push -u origin feature/auth
```

`-u` sets the upstream tracking branch, so later you can use:

```
git push
```

### git fetch

Downloads remote changes and updates remote-tracking references without merging them into your current branch.

```
git fetch origin
```

You can inspect the changes before integrating them.

```
git log HEAD..origin/main --oneline
```

### git pull

Fetches remote changes and integrates them into your current branch.

```
git pull origin main
```

By default, Git typically uses merge behavior.

You can configure pull to rebase instead:

```
git pull --rebase origin main
```

Remember:

- `fetch` = Download and inspect.
- `pull` = Fetch + integrate.
- `push` = Upload your local commits.

My recommendation: use `git fetch` regularly so you understand what's changing before integrating it.

## 12. Clone a GitHub repository

To download an existing repository:

```
git clone https://github.com/username/project.git
```

Clone into a custom folder:

```
git clone https://github.com/username/project.git my-project
```

Clone a specific branch:

```
git clone -b development https://github.com/username/project.git
```

Clone without the complete history:

```
git clone --depth 1 https://github.com/username/project.git
```

This is called a shallow clone.

# PART 5 — Undoing Mistakes

This is one of the most important sections. Every developer makes mistakes. Knowing how to recover is part of being a good developer.

## 13. git restore

You modified a file but haven't staged it.

```
git restore app.py
```

This discards unstaged modifications and restores the file from the index.

Unstage a file:

```
git restore --staged app.py
```

This removes it from the staging area but keeps your working changes.

Be careful: `git restore` can permanently discard uncommitted work.

## 14. git reset

`git reset` moves the current branch pointer and can also modify the index and working directory.

Imagine:

```
A---B---C (HEAD)
```

You want to undo commit C.

### Soft reset

```
git reset --soft HEAD~1
```

- Removes C from the current branch history.
- Keeps changes staged.
- Your files remain unchanged.

### Mixed reset

```
git reset --mixed HEAD~1
```

- Removes C from the current branch history.
- Keeps changes in your working directory.
- Unstages those changes.

This is the default reset mode.

### Hard reset

```
git reset --hard HEAD~1
```

- Removes C from the current branch history.
- Resets the staging area.
- Resets tracked files in your working directory.

Destructive operation

Uncommitted changes can be lost.

### Quick comparison

| Command   | Commit removed? | Changes staged?         |
| --------- | --------------- | ----------------------- |
| `--soft`  | Yes             | Yes                     |
| `--mixed` | Yes             | No                      |
| `--hard`  | Yes             | No; working files reset |

## 15. git revert

Suppose a commit was already pushed to GitHub and other developers may have based work on it.

Instead of rewriting shared history, use:

```
git revert <commit-hash>
```

Git creates a new commit that reverses the selected commit's changes.

```
A---B---C---D
         |
         C is problematic

A---B---C---D---E
                 E reverses C
```

Unlike `reset`, it preserves the existing commit history.

Professional rule: Prefer `revert` when undoing published/shared commits.

## 16. git reflog — your recovery tool

This is a command you should never forget.

Imagine you accidentally run:

```
git reset --hard HEAD~3
```

You think three commits are gone forever.

But Git's reference log often lets you recover the previous branch position.

```
git reflog
```

Example:

```
abc123 HEAD@{0}: reset: moving to HEAD~3
def456 HEAD@{1}: commit: Add authentication
ghi789 HEAD@{2}: commit: Add task update
```

Recover the previous position:

```
git reset --hard def456
```

Or create a recovery branch first:

```
git branch recovery def456
```

Reflog entries are local and eventually expire, so don't rely on them as permanent backups.

# PART 6 — Advanced Git Concepts

Now we're getting into the concepts you mentioned learning a year ago.

## 17. Git stash

Suppose you're working on authentication.

Suddenly, your team asks you to fix an urgent production bug.

You don't want to commit unfinished authentication code.

You can temporarily save your changes using stash.

```
git stash
```

Your working directory becomes clean.

Switch branches:

```
git switch main
git switch -c hotfix/login-error
```

Fix the bug, commit it, and return:

```
git switch feature/auth
```

Restore the saved work:

```
git stash pop
```

### Useful stash commands

```
# Save with a description
git stash push -m "Authentication work in progress"

# List stashes
git stash list

# Apply latest stash without deleting it
git stash apply

# Apply a specific stash
git stash apply stash@{1}

# Delete latest stash
git stash drop

# Delete all stashes
git stash clear
```

Include untracked files:

```
git stash -u
```

`pop` applies a stash and removes it if successful. `apply` keeps it.

## 18. Cherry-picking

Imagine you have two branches:

```
main:       A---B---C
                 \
feature:          D---E---F
```

You need only commit E in `main`, not D or F.

That's exactly what cherry-picking does.

```
git switch main
git cherry-pick <commit-hash>
```

Git applies the changes introduced by that commit and creates a new commit on your current branch.

### Cherry-pick multiple commits

```
git cherry-pick <hash1> <hash2>
```

Pick a range:

```
git cherry-pick <start>..<end>
```

This excludes the starting commit and includes the ending commit.

### If a conflict occurs

```
# Resolve conflicting files first
git add .

# Continue cherry-pick
git cherry-pick --continue
```

Abort it:

```
git cherry-pick --abort
```

Real-world example: A critical bug fix is committed to a development branch. You want that exact fix in the production branch without merging all the development work.

Cherry-pick is useful here.

## 19. Git rebase

Rebase is one of the most important advanced Git concepts.

Imagine:

```
        D---E (feature)
       /
A---B---C---F (main)
```

Your feature branch started from B, but main has progressed to F.

You want your feature commits to appear as if they were developed on top of F.

```
git switch feature
git rebase main
```

Result:

```
A---B---C---F---D'---E' (feature)
```

Notice `D'` and `E'`.

They are new commits with new hashes. Rebase replays changes onto a new base; it doesn't simply move the old commits.

### Merge vs rebase

| Merge                      | Rebase                            |
| -------------------------- | --------------------------------- |
| Combines branch histories  | Replays commits onto a new base   |
| Can create a merge commit  | Usually creates a linear history  |
| Preserves original commits | Creates new commit identities     |
| Safe for shared history    | Requires care with shared history |

### Rebase conflicts

```
git rebase main
```

If conflicts happen:

```
# Fix the conflicting files
git add .

# Continue
git rebase --continue
```

To cancel:

```
git rebase --abort
```

### Important production rule

Never casually rebase commits that other developers are already using.

Why?

Because rebase changes commit hashes. Your teammates may still have the old history.

If you've rewritten your own published feature branch and coordinated the change with your team, you may need:

```
git push --force-with-lease
```

Prefer `--force-with-lease` over `--force`. It checks that the remote branch hasn't changed unexpectedly before replacing it.

## 20. Interactive rebase

This is where you can edit your commit history.

```
git rebase -i HEAD~4
```

This opens an editor showing the last four commits.

Example:

```
pick abc123 Add task model
pick def456 Fix task model
pick ghi789 Add task routes
pick jkl012 Update routes
```

You can change the commands.

| Command  | Purpose                                           |
| -------- | ------------------------------------------------- |
| `pick`   | Keep commit                                       |
| `reword` | Change commit message                             |
| `edit`   | Stop and modify commit                            |
| `squash` | Combine with previous commit and edit message     |
| `fixup`  | Combine with previous commit, discard its message |
| `drop`   | Remove commit                                     |

### Example: Squashing commits

You made these commits:

```
Add task model
Fix task model
Fix typo
Fix typo again
```

You don't want four tiny commits in your final feature history.

Run:

```
git rebase -i HEAD~4
```

Change the list:

```
pick abc123 Add task model
squash def456 Fix task model
squash ghi789 Fix typo
squash jkl012 Fix typo again
```

Git combines them into one commit, letting you edit the final message.

Result:

```
Add task model
```

### Squash vs fixup

- `squash`: Combines commits and lets you edit the resulting message.
- `fixup`: Combines commits and discards the fixup commit's message.

### Amend the latest commit

Forgot to include a file?

```
git add missing_file.py
git commit --amend
```

Change only the message:

```
git commit --amend -m "Improve task creation"
```

This replaces the previous commit with a new one. Avoid amending published commits unless you understand the consequences.

## 21. Git tags

Tags mark specific commits, commonly for releases.

For example:

```
v1.0.0
v1.1.0
v2.0.0
```

Create an annotated tag:

```
git tag -a v1.0.0 -m "First production release"
```

List tags:

```
git tag
```

Inspect:

```
git show v1.0.0
```

Push a tag:

```
git push origin v1.0.0
```

Push all tags:

```
git push origin --tags
```

Delete a local tag:

```
git tag -d v1.0.0
```

Delete a remote tag:

```
git push origin --delete v1.0.0
```

# PART 7 — Git Conflict Resolution

## 22. What is a merge conflict?

Imagine two developers edit the same line.

Developer A:

```
message = "Welcome"
```

Developer B:

```
message = "Hello there"
```

Git can't decide which change is correct.

You might see:

```
<<<<<<< HEADmessage = "Welcome"=======message = "Hello there">>>>>>> feature/greeting
```

These markers show the competing changes.

- `<<<<<<< HEAD`: Current branch's version.
- `=======`: Separates the versions.
- `>>>>>>> feature/greeting`: Incoming branch's version.

You manually decide what the final code should be.

For example:

```
message = "Welcome to our application"
```

Then:

```
git add app.py
git commit
```

For a merge conflict, this completes the merge.

For a rebase conflict, use:

```
git rebase --continue
```

### Conflict resolution workflow

1. Run `git status`.
2. Identify conflicting files.
3. Open them and understand both changes.
4. Combine the correct logic.
5. Remove conflict markers.
6. Test your application.
7. Stage resolved files.
8. Complete the merge/rebase/cherry-pick.

Never blindly choose "Accept Current" or "Accept Incoming" without understanding the code.

# PART 8 — GitHub: Professional Collaboration

## 23. Creating a GitHub repository

Visit [GitHub](https://github.com?utm_source=chatgpt.com).

Create a repository.

You'll typically choose:

- Repository name.
- Description.
- Public or private visibility.
- README initialization.
- `.gitignore` template.
- License.

### Public vs private

Public repository

- Anyone can view the code.
- People can fork it.
- Contributions can be made through pull requests.

Private repository

- Access is restricted.
- You control who can view and contribute.

## 24. Connecting local Git to GitHub

Create a local project:

```
git init
git add .
git commit -m "Initial commit"

git branch -M main

git remote add origin https://github.com/username/task-manager.git

git push -u origin main
```

Your local repository is now connected to GitHub.

### HTTPS vs SSH authentication

HTTPS:

```
git clone https://github.com/username/project.git
```

SSH:

```
git clone git@github.com:username/project.git
```

SSH requires you to configure an SSH key and add its public key to GitHub.

GitHub does not accept your account password for normal Git HTTPS authentication. Use an appropriate credential manager or personal access token when prompted.

## 25. Pull Requests (PRs)

A Pull Request is a request to integrate changes from one branch into another.

Imagine you're working on a team.

Your teammate asks you to implement login authentication.

You:

1. Create a feature branch.
2. Write the authentication code.
3. Commit the changes.
4. Push your branch to GitHub.
5. Open a Pull Request.
6. Teammates review the code.
7. Address feedback.
8. Merge the PR.

Example:

```
git switch -c feature/login
```

Make changes and commit:

```
git add .
git commit -m "Add login authentication"
```

Push:

```
git push -u origin feature/login
```

Go to GitHub and create a PR.

### What should a good PR contain?

- Clear title.
- What was changed.
- Why it was changed.
- Screenshots if UI changes are involved.
- Testing performed.
- Related issue number.
- Potential breaking changes.

Example PR description:

```
## Summary
- Added user login endpoint.
- Added password validation.
- Added JWT token generation.

## Testing
- Tested valid login.
- Tested incorrect password.
- Tested missing email.

## Related issue
Closes #12
```

### PR review terminology

| Term                 | Meaning                                |
| -------------------- | -------------------------------------- |
| Approve              | Reviewer approves changes              |
| Comment              | Reviewer leaves feedback               |
| Request changes      | Reviewer wants changes before approval |
| Resolve conversation | Mark a review discussion as addressed  |
| Merge                | Integrate PR changes                   |

### PR merge strategies

GitHub supports three common merge strategies:

Merge commit

Preserves the branch history and creates a merge commit.

Squash and merge

Combines the PR commits into one commit on the target branch.

Rebase and merge

Replays the PR commits onto the target branch without a merge commit.

Your team should agree on a consistent strategy.

# PART 9 — Forking and Open Source

## 26. What is forking?

Suppose you discover a project on GitHub that you like.

You don't have permission to push directly to its repository.

You can create your own copy under your GitHub account.

That's a fork.

Original repository

github.com/owner/project

Fork

Your fork

github.com/yourname/project

Clone + contribute

Pull Request

Your fork → Original repository

### Complete open-source contribution workflow

Step 1: Fork the repository

Click the Fork button on GitHub.

Step 2: Clone your fork

```
git clone https://github.com/yourname/project.git
cd project
```

Step 3: Add the original repository as upstream

```
git remote add upstream https://github.com/original-owner/project.git
```

Check:

```
git remote -v
```

You should see:

```
origin    your fork
upstream  original repository
```

Step 4: Sync your fork

```
git fetch upstream
```

Update your local main branch:

```
git switch main
git merge upstream/main
```

Or, if your team/project uses a linear history:

```
git rebase upstream/main
```

Push your updated fork:

```
git push origin main
```

Step 5: Create your feature branch

```
git switch -c feature/fix-login
```

Step 6: Make changes and commit

```
git add .
git commit -m "Fix login validation"
```

Step 7: Push to your fork

```
git push -u origin feature/fix-login
```

Step 8: Open a PR

On GitHub, select:

```
base repository: original-owner/project
base branch: main

head repository: yourname/project
compare branch: feature/fix-login
```

Now your contribution is submitted for review.

### Important: origin vs upstream

| Remote     | Meaning             |
| ---------- | ------------------- |
| `origin`   | Your fork           |
| `upstream` | Original repository |

This is a very common open-source workflow.

## 27. Finding open-source projects

Useful resources:

- [Good First Issues](https://github.com/topics/good-first-issue?utm_source=chatgpt.com)
- [Good First Issue website](https://goodfirstissue.dev/?utm_source=chatgpt.com)
- [Up For Grabs](https://up-for-grabs.net/?utm_source=chatgpt.com)
- [GitHub Explore](https://github.com/explore?utm_source=chatgpt.com)

### How to contribute properly

Don't immediately pick a massive feature.

Start with:

1. Documentation improvements.
2. Small bug fixes.
3. Tests.
4. Error handling.
5. Small feature enhancements.

Read these files before contributing:

- `README.md`
- `CONTRIBUTING.md`
- `CODE_OF_CONDUCT.md`
- `LICENSE`

Follow the repository's contribution rules.

# PART 10 — Production-Grade Git Practices

This is where we move from knowing Git to using it as a software engineer.

## 28. Git workflow strategies

There are different ways teams organize branches.

### A. GitHub Flow

A simple and popular workflow.

```
main
  |
  ├── feature/login
  ├── feature/dashboard
  └── bugfix/payment
```

Process:

1. Keep `main` deployable.
2. Create feature branches.
3. Commit changes.
4. Push to GitHub.
5. Open PRs.
6. Review and test.
7. Merge.
8. Deploy.

For many modern web applications, this is a great starting point.

### B. Git Flow

A more structured branching model.

Common branches:

| Branch      | Purpose                 |
| ----------- | ----------------------- |
| `main`      | Production-ready code   |
| `develop`   | Integration branch      |
| `feature/*` | New functionality       |
| `release/*` | Preparing releases      |
| `hotfix/*`  | Urgent production fixes |

Typical flow:

```
feature → develop → release → main
                         |
                       hotfix
```

Git Flow can be useful for projects with scheduled releases and separate stabilization periods. It is not mandatory for every team.

## 29. Protect your main branch

In a production repository, you generally don't want developers directly pushing unfinished code to `main`.

GitHub offers branch protection rules and repository rulesets.

Common protections:

- Require a pull request before merging.
- Require approvals.
- Require CI checks to pass.
- Require conversations to be resolved.
- Restrict force pushes.
- Restrict branch deletion.

This makes the main branch safer.

## 30. `.gitignore`

This file tells Git which untracked files and directories to ignore.

Example for a Python project:

```
# Python cache
__pycache__/
*.py[cod]

# Virtual environments
venv/
.venv/

# Environment variables and secrets
.env
.env.*

# Keep example environment files
!.env.example

# IDE files
.vscode/
.idea/

# Testing
.pytest_cache/
.coverage
htmlcov/

# Build files
dist/
build/

# Operating system
.DS_Store
Thumbs.db
```

### Important

`.gitignore` does not automatically stop tracking files already committed.

If `.env` is already tracked:

```
git rm --cached .env
git commit -m "Stop tracking environment file"
```

If you accidentally committed a secret, simply removing the file is not enough. Rotate the exposed credential and follow a repository-history cleanup process if necessary.

## 31. Never commit secrets

Never commit:

```
.env
database passwords
API keys
JWT secrets
private SSH keys
cloud credentials
```

Instead, provide an example:

`.env.example`

```
DATABASE_URL=postgresql://user:password@localhost/db
JWT_SECRET=replace-this-value
```

Use GitHub Actions secrets or an appropriate secret manager for deployment credentials.

## 32. Conventional Commits

A standard commit message structure helps maintain clean history.

```
<type>(optional scope): description
```

Examples:

```
git commit -m "feat(auth): add JWT authentication"

git commit -m "fix(tasks): handle missing task IDs"

git commit -m "docs(readme): update installation guide"

git commit -m "refactor(api): separate route handlers"

git commit -m "test(auth): add login validation tests"

git commit -m "chore(deps): update FastAPI"
```

Common types:

| Type       | Meaning                 |
| ---------- | ----------------------- |
| `feat`     | New feature             |
| `fix`      | Bug fix                 |
| `docs`     | Documentation           |
| `refactor` | Code restructuring      |
| `test`     | Tests                   |
| `chore`    | Maintenance             |
| `perf`     | Performance improvement |
| `ci`       | CI/CD changes           |
| `build`    | Build system changes    |

## 33. Semantic Versioning

Production applications often use semantic versioning.

```
MAJOR.MINOR.PATCH
```

Example:

```
1.4.2
```

- MAJOR: Breaking changes.
- MINOR: New backward-compatible functionality.
- PATCH: Backward-compatible bug fixes.

Examples:

```
1.0.0 → 1.0.1  Bug fix
1.0.1 → 1.1.0  New feature
1.1.0 → 2.0.0  Breaking API change
```

Create a release tag:

```
git tag -a v1.1.0 -m "Release 1.1.0"
git push origin v1.1.0
```

GitHub can then create a Release from that tag.

# PART 11 — GitHub Actions and CI/CD

## 34. What is GitHub Actions?

GitHub Actions is an automation platform integrated with GitHub.

You can automatically run tasks when events happen in your repository.

For example:

- Someone pushes code.
- Someone opens a PR.
- A release is published.
- A scheduled workflow runs.

You can automatically install dependencies, run tests, check code quality, build applications, and deploy.

### What is CI/CD?

CI — Continuous Integration

Automatically integrate and test code changes.

CD — Continuous Delivery/Deployment

Prepare or automatically deploy tested code.

### Basic GitHub Actions workflow

Create:

```
.github/
└── workflows/
    └── python-tests.yml
```

Add:

```

name: Python API Tests

# Run this workflow on pushes and pull requests to main.
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      # Download repository code
      - name: Checkout code
        uses: actions/checkout@v4

      # Install Python
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      # Install dependencies
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install fastapi httpx pytest

      # Run tests
      - name: Run tests
        run: pytest

```

This is a starting example. In a real project, install from your pinned dependency file and add the tests and configuration your project needs.

### Understanding the YAML

| Property  | Meaning                         |
| --------- | ------------------------------- |
| `name`    | Workflow name                   |
| `on`      | Events that trigger it          |
| `jobs`    | Tasks to execute                |
| `runs-on` | Machine environment             |
| `steps`   | Individual actions/commands     |
| `uses`    | Reuse an existing GitHub Action |
| `run`     | Execute shell commands          |
| `with`    | Pass configuration to an action |

### What happens when you create a PR?

```
Developer pushes code
        ↓
GitHub detects push/PR
        ↓
GitHub Actions starts
        ↓
Install dependencies
        ↓
Run tests
        ↓
Tests pass or fail
        ↓
PR status check updates
```

You can configure branch protection so a PR cannot merge until required checks pass.

# PART 12 — Advanced Tools Worth Knowing

## 35. git bisect

Imagine your application worked 20 commits ago, but now it crashes.

You don't know which commit introduced the bug.

Instead of manually checking every commit, use binary search.

```
git bisect start
git bisect bad
git bisect good <known-good-commit>
```

Git checks out a commit halfway through the range.

Test your application.

If it's broken:

```
git bisect bad
```

If it works:

```
git bisect good
```

Git keeps narrowing down the range.

Finish:

```
git bisect reset
```

This is incredibly useful when debugging large codebases.

## 36. git blame

Want to know who last modified a particular line?

```
git blame app.py
```

For a specific line range:

```
git blame -L 10,30 app.py
```

It shows the commit and author associated with each line's latest change.

Use it to understand history, not to blame teammates.

## 37. git log

Useful history commands:

```
# Standard history
git log

# Compact history
git log --oneline

# Graph view
git log --graph --oneline --all

# Last 5 commits
git log -5

# History of a particular file
git log -- app.py

# Show commits by author
git log --author="Your Name"
```

One of the most useful commands:

```
git log --oneline --graph --decorate --all
```

It gives you a visual representation of branch history in the terminal.

## 38. git clean

Removes untracked files.

Preview what would be deleted:

```
git clean -n
```

Remove untracked files:

```
git clean -f
```

Remove untracked files and directories:

```
git clean -fd
```

Destructive operation

It can delete work that Git isn't tracking. Always preview first.

## 39. Git submodules

A submodule lets you include another Git repository inside your repository.

Example:

```
git submodule add https://github.com/example/library.git libs/library
```

Clone a project with its submodules:

```
git clone --recurse-submodules <repo-url>
```

Initialize existing submodules:

```
git submodule update --init --recursive
```

Submodules are useful when you need to track an external repository at a particular commit. They also introduce additional maintenance complexity, so don't use them unnecessarily.

# PART 13 — A Professional GitHub Repository

## 40. What should a production repository look like?

For your Python API project, a reasonable structure could be:

```
task-manager-api/
│
├── .github/
│   ├── workflows/
│   │   └── tests.yml
│   ├── ISSUE_TEMPLATE/
│   └── PULL_REQUEST_TEMPLATE.md
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── routes/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── database/
│
├── tests/
│   ├── test_tasks.py
│   └── test_auth.py
│
├── .env.example
├── .gitignore
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── requirements.txt
└── pyproject.toml
```

A production-quality repository should generally include:

- Clear README with setup instructions.
- `.gitignore`.
- Dependency management.
- Tests.
- CI workflow.
- License.
- Contribution guidelines if open source.
- Environment variable documentation.
- Security policy.
- Issue and PR templates where useful.

### Useful GitHub features

| Feature       | Why it matters                     |
| ------------- | ---------------------------------- |
| Issues        | Track bugs and tasks               |
| Projects      | Manage project boards              |
| Discussions   | Community conversations            |
| Pull Requests | Code review and integration        |
| Actions       | CI/CD automation                   |
| Releases      | Publish versions                   |
| Packages      | Host packages and container images |
| Dependabot    | Dependency update automation       |
| Code Security | Security scanning and alerts       |
| CODEOWNERS    | Automatically request reviewers    |

Useful documentation:

- [GitHub Docs](https://docs.github.com/en?utm_source=chatgpt.com)
- [GitHub Actions Docs](https://docs.github.com/en/actions?utm_source=chatgpt.com)
- [Official Git Documentation](https://git-scm.com/docs?utm_source=chatgpt.com)

# PART 14 — Your Hands-on Revision Roadmap

Don't just read all these notes. The best way to regain your Git knowledge is to deliberately break things and fix them.

Let's use one project throughout: `git-practice-lab`.

## Exercise 1 — Fundamentals

Beginner

- Create a repository using `git init`.
- Add three Python files.
- Stage one file only.
- Commit it.
- Stage the remaining files.
- Create another commit.
- Inspect `git status`.
- Compare `git diff` and `git diff --staged`.
- Inspect your history using `git log`.

## Exercise 2 — Branching

Beginner → Intermediate

- Create `feature/auth`.
- Add a login function.
- Commit your changes.
- Create `feature/tasks`.
- Add a task creation function.
- Merge both features into `main`.
- Try a fast-forward merge.
- Try a three-way merge.
- Create and resolve a merge conflict.

## Exercise 3 — Undo and Recovery

Intermediate

- Modify a file and use `git restore`.
- Stage a file and unstage it.
- Create three commits.
- Experiment with `git reset --soft`.
- Experiment with `git reset --mixed`.
- Understand `git reset --hard` in a disposable repository.
- Revert a commit.
- Recover a previous branch position using `git reflog`.

## Exercise 4 — Advanced Git

Advanced

- Stash unfinished work.
- Apply and pop stashes.
- Cherry-pick a commit.
- Rebase a feature branch.
- Resolve a rebase conflict.
- Interactive rebase.
- Squash four commits into one.
- Use `fixup`.
- Amend the latest commit.
- Create and push a tag.
- Use `git bisect` to find a deliberately introduced bug.

## Exercise 5 — GitHub Collaboration

Professional

- Create a GitHub account/repository.
- Push your local project.
- Clone the repository into another folder.
- Create a feature branch.
- Push that branch.
- Open a PR.
- Add a PR description.
- Review your own PR.
- Merge using squash and merge.
- Delete the feature branch.

## Exercise 6 — Open Source

Advanced

- Find an open-source Python project.
- Fork it.
- Clone your fork.
- Add the original repository as `upstream`.
- Fetch upstream changes.
- Create a feature branch.
- Make a meaningful contribution.
- Write a good commit message.
- Push to your fork.
- Open a PR against the original project.
- Respond to review feedback.
- Update your PR.

## Exercise 7 — Production workflow

Production-grade

- Create a repository with a proper folder structure.
- Add a `.gitignore`.
- Add `.env.example`.
- Configure branch protection.
- Add PR templates.
- Add GitHub Actions.
- Run automated tests on PRs.
- Add a license.
- Add a README.
- Create a versioned release.
- Configure Dependabot.
- Add a security policy.

# PART 15 — Your Git Cheat Sheet

Keep this section handy when coding.

| What you want                   | Command                          |
| ------------------------------- | -------------------------------- |
| Initialize Git                  | `git init`                       |
| Check status                    | `git status`                     |
| Stage files                     | `git add .`                      |
| Commit                          | `git commit -m "message"`        |
| View history                    | `git log --oneline`              |
| Create branch                   | `git switch -c feature/name`     |
| Switch branch                   | `git switch main`                |
| Merge branch                    | `git merge feature/name`         |
| Rebase branch                   | `git rebase main`                |
| Cherry-pick                     | `git cherry-pick HASH`           |
| Squash commits                  | `git rebase -i HEAD~N`           |
| Stash work                      | `git stash`                      |
| Restore stash                   | `git stash pop`                  |
| Undo latest commit, keep staged | `git reset --soft HEAD~1`        |
| Undo published commit           | `git revert HASH`                |
| Recover history                 | `git reflog`                     |
| Download remote changes         | `git fetch`                      |
| Download and integrate          | `git pull`                       |
| Upload commits                  | `git push`                       |
| Add remote                      | `git remote add origin URL`      |
| Clone repository                | `git clone URL`                  |
| Create tag                      | `git tag -a v1.0.0 -m "Release"` |
| Find bug-introducing commit     | `git bisect`                     |
| Inspect line history            | `git blame FILE`                 |

# Final: How I want you to practice

I'd recommend doing this in three stages:

1. Stage 1: Spend a session revising fundamentals, branches, merging, and remote operations.
2. Stage 2: Practice reset, revert, reflog, stash, cherry-pick, interactive rebase, and conflict resolution in a disposable repository.
3. Stage 3: Contribute to an actual open-source project and set up CI/CD for one of your own projects.

One important thing: don't try to memorize 50 commands. Understand what Git is doing to your working tree, staging area, commits, and branches.

Once those concepts click again, the advanced commands become much easier.

Your first assignment: Create `git-practice-lab`, complete Exercises 1 and 2, and then we'll tackle the advanced Git scenarios with deliberately broken repositories. That's how we'll make sure you can actually recover from mistakes instead of just remembering command syntax.