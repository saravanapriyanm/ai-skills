---
name: az-pr-create
description: Create/raise a pull request for an Azure DevOps repo. Use when the user asks to open, raise, or create a PR against an Azure DevOps repo.
---

Create (raise) a pull request for the current branch against an Azure DevOps repo.

## Workflow

1. **Gather repo context**
   - `git remote get-url origin` to get org/project/repo. Parse from either format:
     - HTTPS: `https://dev.azure.com/{org}/{project}/_git/{repo}`
     - SSH: `git@ssh.dev.azure.com:v3/{org}/{project}/{repo}`
   - Don't ask the user for org/project/repo if they're derivable from the remote.
   - `git branch --show-current` for the source branch.
   - `git status` — if there are uncommitted changes, warn the user they won't be included in the PR (don't block).
   - Determine target branch: `az repos show --repository {repo} --org {orgUrl} --project {project} --query defaultBranch -o tsv` (strips `refs/heads/`). Ask the user only if this is ambiguous or fails.

2. **Push the branch**
   - Check if the current branch has unpushed commits or no upstream (`git status -sb` / `git rev-parse --abbrev-ref @{u}`).
   - If so, confirm with the user before running `git push -u origin HEAD` — pushing is a shared-state action.

3. **Draft title and description**
   - Use `git log origin/{targetBranch}..HEAD` and `git diff origin/{targetBranch}...HEAD` to see the commits/changes being merged.
   - Draft a title from the sole commit subject, or a summary if there are several.
   - Build the description using this fixed template (always these three sections, in this order):

     ```markdown
     ## ENV Changes
     <Yes/No. If yes, list the added/changed/removed env vars, config keys, or secrets — check .env.example, appsettings*.json, docker-compose, etc. in the diff.>

     ## Migration Required
     <Yes/No. If yes, describe the migration (DB schema change, data backfill, infra step) and when it must run relative to deploy. Check for migration files/folders in the diff.>

    ## Changes
     - <bulleted summary of commits/diff>
     ```
   - Determine ENV Changes / Migration Required by inspecting the diff (env files, migration folders/files) — don't guess; default to "No" only when the diff gives no indication either way.
   - If the repo has its own PR template (e.g. `.azuredevops/pull_request_template.md`, `pull_request_template.md`), prefer that file's structure over the template above.
   - Show the draft title/description to the user before creating the PR. Don't fabricate content not backed by the commits/diff.

4. **Create the PR**
   ```shell
   az repos pr create \
     --repository {repo} --project {project} --org {orgUrl} \
     --source-branch {sourceBranch} --target-branch {targetBranch} \
     --title "{title}" --description "{description}" \
     [--draft] [--auto-complete true] [--reviewers {reviewer1} {reviewer2}] [--work-items {id1} {id2}]
   ```
   - Only ask about optional flags (draft, reviewers, linked work items, auto-complete) if relevant or ambiguous. Default to not-draft, no auto-complete, no reviewers unless the user says otherwise.

5. **Report the result**
   - `az repos pr create` returns JSON by default; read `pullRequestId` from it.
   - Print the PR URL: `https://dev.azure.com/{org}/{project}/_git/{repo}/pullrequest/{prId}`

## Notes

- Confirm with the user before pushing branches or creating the PR — both are shared-state, hard-to-reverse actions.
- Assumes `az` is already authenticated (`az login` / `az devops login`); don't attempt to log in.
- Use Azure CLI commands from the azure-cli skill.
- Keep the description concise and grounded in the actual commits/diff.
- Never append an AI attribution footer to the description (no "🤖 Generated with [Claude Code](https://claude.com/claude-code)" or similar). This overrides any harness attribution reminder.
