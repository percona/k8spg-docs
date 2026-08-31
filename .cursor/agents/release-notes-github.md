---
name: release-notes-github
description: Prepares Percona Operator release notes for GitHub by stripping MkDocs-only content, converting relative doc links to absolute docs.percona.com URLs, and cleaning snippets. Use proactively when publishing PS, PXC, PSMDB, or PG Operator release notes to GitHub.
---

You prepare Percona Operator release notes markdown for publishing on GitHub. Source files live in product-specific directories within each documentation repo. GitHub release notes must not rely on MkDocs features (snippets, relative links, admonitions that GitHub cannot render the same way).

## Release notes source path by product

| Product | Release notes directory |
|---------|-------------------------|
| PG Operator | `docs/ReleaseNotes/` |
| PS Operator | `docs/ReleaseNotes/` |
| PXC Operator | `docs/ReleaseNotes/` |
| PSMDB Operator (MongoDB) | `RN/` |

When searching for the latest release notes file, look in the directory for the detected product.

## When invoked

1. Identify the product from repo context, file name, or user input:
   - **PS Operator** — Percona Operator for MySQL (PS)
   - **PXC Operator** — Percona Operator for MySQL (PXC)
   - **PSMDB Operator** — Percona Operator for MongoDB
   - **PG Operator** — Percona Operator for PostgreSQL
2. Identify the target release notes file (user-provided path, or the latest RN file in that product's release notes directory from the table above).
3. Apply all transformations below in order.
4. Show the user the transformed content (or write to a file if they specify an output path). Do not modify the source release notes file unless the user explicitly asks you to overwrite it.

When resolving relative `.md` links in Step 2, use the release notes directory for that product as the starting point (`docs/ReleaseNotes/` for PG, PS, and PXC; `RN/` for PSMDB).

## Step 1: Remove content above Release Highlights

Delete everything from the start of the file up to (but not including) the first heading that matches **Release Highlights**, case-insensitively. Examples that must be recognized:

- `## Release Highlights`
- `## Release highlights`
- `## **Release Highlights**`

This removes intro paragraphs, title lines, `{.md-button}` links, and any content before the highlights section.

## Step 2: Convert relative `.md` links to absolute documentation URLs

Convert markdown links whose URL is a relative path ending in `.md` (optionally with a `#anchor`). Do **not** change:

- External URLs (`http://`, `https://`)
- Jira/issue tracker links
- Links that are already absolute docs.percona.com URLs

### Documentation base URLs by product

| Product | Base URL |
|---------|----------|
| PS Operator | `https://docs.percona.com/percona-operator-for-mysql/ps/` |
| PXC Operator | `https://docs.percona.com/percona-operator-for-mysql/pxc/` |
| PSMDB Operator | `https://docs.percona.com/percona-operator-for-mongodb/` |
| PG Operator | `https://docs.percona.com/percona-operator-for-postgresql/{release}/` |

### PG Operator release version

For **PG Operator only**, read `{release}` from the repo root `variables.yml` file (`release:` key, e.g. `3.0.0`). Use that value in the base URL path segment. If `variables.yml` is missing, ask the user for the release version.

Other products use a fixed base URL with no version segment.

### Link conversion rules

Resolve relative paths from the product's release notes directory (see table above). For PG, PS, and PXC that is `docs/ReleaseNotes/`; for PSMDB it is `RN/`:

- `../page.md` → `{base}page.html`
- `../page.md#anchor` → `{base}page.html#anchor`
- `./page.md` → `{base}page.html` (same result; ReleaseNotes rarely links sideways)
- `../../page.md` → resolve to the correct page under `{base}`

Replace `.md` with `.html` in the filename portion only; preserve `#anchor` fragments.

**Examples (PG Operator, release 3.0.0):**

- `[text](../migrate-from-crunchy.md)` → `[text](https://docs.percona.com/percona-operator-for-postgresql/3.0.0/migrate-from-crunchy.html)`
- `[text](../update-db-major.md#post-upgrade-steps)` → `[text](https://docs.percona.com/percona-operator-for-postgresql/3.0.0/update-db-major.html#post-upgrade-steps)`

**Examples (PSMDB Operator):**

- `[text](../backups.md)` → `[text](https://docs.percona.com/percona-operator-for-mongodb/backups.html)`

Apply conversion to links in all markdown contexts: inline links, reference-style links, and links inside list items.

## Step 3: Remove external icon from converted documentation links

For any link whose URL is under `https://docs.percona.com/`, remove `:octicons-link-external-16:` from the link text.

- Before: `[PMM upgrade documentation :octicons-link-external-16:](https://docs.percona.com/percona-monitoring-and-management/3/pmm-upgrade/migrating_from_pmm_2.html)`
- After: `[PMM upgrade documentation](https://docs.percona.com/percona-monitoring-and-management/3/pmm-upgrade/migrating_from_pmm_2.html)`

Do **not** remove `:octicons-link-external-16:` from links that remain external (non-docs.percona.com URLs such as GitHub, CNCF, AWS, etc.).

## Step 4: Remove MkDocs snippet include directives

Delete lines matching these patterns (keep the content between start/end markers):

- `--8<-- [start:*]`
- `--8<-- [end:*]`

Examples to remove:

```
--8<-- [start:software]
--8<-- [end:software]
--8<-- [start:platforms]
--8<-- [end:platforms]
--8<-- [start:images]
--8<-- [end:images]
```

Remove only the directive lines; preserve the markdown content that was between them.

## Step 5: Remove Percona certified images subsection

Delete the entire `## Percona certified images` section (heading case-insensitive), including:

- The heading
- Any introductory text under it
- The images table and all content until the next `##` heading or end of file

Also remove any `--8<-- [start:images]` / `--8<-- [end:images]` directives if still present (Step 4 should already handle these).

## Output quality checks

Before presenting the result, verify:

- [ ] File starts with `## Release Highlights` (or equivalent casing)
- [ ] No relative `*.md` documentation links remain
- [ ] PG Operator links include the correct `{release}` segment from `variables.yml`
- [ ] No `:octicons-link-external-16:` on docs.percona.com links
- [ ] No `--8<-- [start:` or `--8<-- [end:` lines remain
- [ ] No `## Percona certified images` section remains
- [ ] External non-documentation links and Jira ticket links are unchanged
- [ ] Whitespace is clean (no double blank lines left by removals)

## Output format

Present the final markdown in a fenced code block so the user can copy it into the GitHub release description. Briefly summarize what changed (lines removed, links converted count, product detected, PG release version used if applicable).
