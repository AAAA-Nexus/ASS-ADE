# Prompt Governance Skill

Use this skill when changing ASS-ADE prompt, agent, hook, tool, skill, MCP, or
capability-inventory artifacts.

## When to Use

- Creating or editing `agents/*.agent.md`
- Creating or editing `skills/*.skill.md`
- Editing prompt files in `prompts/`
- Adding prompt, agent, hook, or skill capabilities to the dynamic inventory
- Preparing a prompt artifact for deployment, review, or rollback

## Steps

1. Inventory the affected files with `list_directory`, `search_files`, or:
   `ass-ade prompt sync-agent --path <repo> --json` when capability discovery changed.
2. Read the affected artifact before editing.
3. Classify the change as one of:
   `new-agent`, `new-skill`, `prompt-edit`, `hook-change`, `tool-change`,
   `capability-sync`, or `security-hardening`.
4. For prompt-like files, compute a hash:
   `ass-ade prompt hash <file> --path <repo> --json`.
5. If a baseline exists, review a redacted diff:
   `ass-ade prompt diff <baseline> --prompt-path <current> --path <repo>`.
6. Check public-safety boundaries:
   no credentials, hidden host prompts, private implementation identifiers, or instructions
   to bypass approval gates.
7. Preserve cross-surface consistency:
   update the matching agent, skill, hook docs, tool docs, and capability inventory
   when the change affects more than one surface.
8. Run targeted tests for changed Python modules and a discovery check for changed
   prompt assets.
9. Report changed files, validation commands, and any residual risk.

## Useful Commands

| Task | Command |
|------|---------|
| Hash prompt artifact | `ass-ade prompt hash <file> --path <repo> --json` |
| Validate against manifest | `ass-ade prompt validate <manifest> --prompt-path <file> --path <repo> --json` |
| Extract a section | `ass-ade prompt section <section> --prompt-path <file> --path <repo> --json` |
| Redacted diff | `ass-ade prompt diff <baseline> --prompt-path <file> --path <repo>` |
| Propose improvements | `ass-ade prompt propose "<objective>" --prompt-path <file> --path <repo> --json` |
| Refresh live inventory | `ass-ade prompt sync-agent --path <repo> --json` |

## Output Interpretation

- `prompt hash` records identity only. It does not prove quality.
- `prompt validate` passes only when the manifest hash matches the artifact.
- `prompt diff` is for human review and should stay redacted unless the user asks
  for raw output and secrets are known to be absent.
- `prompt propose` is a proposal, not an applied change.

## Error Handling

- If a prompt path escapes the repo root, stop and ask for a repo-local path.
- If a manifest is missing or has no hash, report that validation is not possible
  and fall back to hash plus diff review.
- If a scan finds secrets or hidden prompt leakage, block deployment until removed.
- If tests cannot run, report the exact command attempted and the failure.
