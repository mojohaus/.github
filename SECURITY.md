# Security Policy

This policy covers every repository in the [mojohaus](https://github.com/mojohaus) organization that has no `SECURITY.md` of its own.

## Report a vulnerability

**Please don't open a public issue or pull request for a security problem.**

Report it privately through GitHub, using the **Report a vulnerability** button on the Security tab of the affected repository. That opens a private advisory visible only to the maintainers:

> `https://github.com/mojohaus/<repository>/security/advisories/new`

If you aren't sure which repository is affected, report against the one you believe is closest and say so in the report; we will move it.

A report is most useful when it includes the affected plugin and version, how the issue can be triggered, and what an attacker gains. A reproducer is worth a great deal.

## What happens next

We will confirm the report, work on a fix privately, and publish a GitHub Security Advisory when the fix is released. Where a fix isn't possible or the report turns out not to be a vulnerability, we will tell you that and why.

MojoHaus is maintained by volunteers on a best-effort basis, so we cannot promise a response time. If a report goes unacknowledged for a couple of weeks, please nudge us in the advisory thread.

We are glad to credit reporters in the advisory. Tell us how you would like to be named, or that you would rather not be.

## Which versions get fixes

Fixes go into the next release of the affected plugin. Older releases are not patched; upgrade to get the fix.

## Scope

This policy covers the code in this organization's repositories and the artifacts published from them to Maven Central under `org.codehaus.mojo`.

Archived repositories receive no fixes of any kind, including security fixes. If you find a vulnerability in one, we would still like to know, so we can point people away from it, but the answer will be to migrate rather than to patch.
