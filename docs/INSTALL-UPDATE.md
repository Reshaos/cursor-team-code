# Private Git, installation and updates
Verified against official Cursor docs on 2026-10-09. This document is instructions for a later deliberate action by the maintainer; no publishing, installation, account connection or security-setting change was performed for this delivery.

## Private repository preparation
Extract the archive into a new standalone directory. Import the contents of `cursor-team-source/` as the root of your new private work Git repository using your organization's approved Git process. Keep `.cursor-plugin/marketplace.json` at its root and the plugin at `plugins/team-code/`. Review files before committing; do not import into an application repository. Replace `Your Team` owner metadata. Do not put tokens or connection strings into source. Validate and package before committing a version; bump plugin version, marketplace metadata version and CHANGELOG together.

## Local loading test
Cursor documents a real copy or clone under `~/.cursor/plugins/local/<plugin>` with `.cursor-plugin/plugin.json` inside that plugin folder. Copy the contents of `plugins/team-code/`, not the marketplace repository root. External symlinks are skipped. Restart Cursor or use Developer: Reload Window, then inspect Customize.

Windows PowerShell path translation: `$HOME/.cursor/plugins/local/team-code`. This translation and copying procedure are untested on Windows here; choose a fresh destination and avoid overwriting another installation. A possible manual copy from the extracted repository root is:

```powershell
$pluginTarget = Join-Path $HOME '.cursor/plugins/local/team-code'
if (Test-Path $pluginTarget) { throw 'Choose a fresh destination or deliberately replace the existing copy after review.' }
New-Item -ItemType Directory -Path $pluginTarget | Out-Null
Copy-Item -Path '.\plugins\team-code\*' -Destination $pluginTarget -Recurse -Force
# Confirm the manifest was copied before reloading Cursor.
Test-Path (Join-Path $pluginTarget '.cursor-plugin/plugin.json')
```

Admin policy may disallow local plugin imports; Enterprise defaults this setting off. Ask the administrator to use their approved distribution route. Do not change security policy to make this plugin work. An installed marketplace plugin with the same name takes precedence over the local copy. Official source: [Plugins / Test plugins locally](https://cursor.com/docs/plugins).

## Private team marketplace, including Azure DevOps
Cursor's team marketplace Import from Repo flow accepts GitHub, GitLab, Bitbucket and Azure DevOps repository URLs. Teams supports one team marketplace; Enterprise supports unlimited. Existing plan/organization policy governs availability. In Dashboard → Plugins & MCPs → Team Marketplaces → Add Marketplace, a maintainer can choose Import from Repo and enter the private repository URL, connect through approved organizational access if asked, review the plugin, then choose marketplace access and installation mode. On Enterprise only admins add marketplaces. This is Cursor's marketplace import, not an Azure DevOps extension/VSIX marketplace upload.

Azure DevOps imports continue serving from the source repository. Hosted copies and documented automatic refresh behavior are GitHub-specific: do not assume those features for Azure DevOps or promise a refresh interval. Cursor documents a manual Refresh action to update from the repository. Use Refresh in the marketplace UI after the private repository update, then verify the version and components in Customize. This is general repository-refresh guidance; Azure DevOps runtime behavior was not tested here. The docs do not establish an Azure-specific refresh API or automatic refresh interval. Official source: [Plugins / Team marketplaces](https://cursor.com/docs/plugins).

## Update safely
Review the changed source and changelog, validate, package and test the new plugin locally if policy allows. Commit through your approved private Git workflow, then deliberately update the team marketplace using its supported UI. For a local copy, deliberately replace that copy's contents from the new plugin directory (including removals) and reload. Check the actual version and invoke a harmless smoke task. Revert via a known-good reviewed commit/version and repeat loading checks. Avoid concurrent local/marketplace copies of the same name during diagnosis. Changes to prompts cannot guarantee adoption, completed reviews or runtime enforcement.
