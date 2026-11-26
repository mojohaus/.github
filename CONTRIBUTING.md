# Contributing to MojoHaus

This applies to every repository in the [mojohaus](https://github.com/mojohaus) organization that has no `CONTRIBUTING.md` of its own.

MojoHaus plugins run inside other people's builds, often pinned for years. A change that breaks a parameter, a default, or the Java or Maven versions a plugin runs on reaches users who never asked for it, and that shapes most of the advice below.

## Where to ask

Open an issue on the repository concerned; that is where the maintainers are. Each plugin's site also lists its mailing lists. If you aren't sure which repository owns the behavior you see, open the issue wherever seems closest and we'll move it.

## Build a project

To build any repository here:

```
mvn verify
```

Most repositories keep their integration tests, run by the maven-invoker-plugin, behind a profile:

```
mvn -P run-its verify
```

Building needs a current Maven 3.9.x or later; the enforcer plugin stops the build early if yours is too old. CI runs on Linux, Windows, and macOS with JDK 8, 21, and 25, on Maven 3.10 and Maven 4. If your change builds on your machine but you can't test the other platforms, open the pull request anyway and read the CI result.

Each repository's `AGENTS.md` file describes its modules, the commands its build needs, and its own conventions.

## Java and Maven baseline

Most plugins target Java 8, set by `mojo.java.target` in the parent POM, and declare Maven 3.9.0 as their minimum through `<prerequisites>`. A few have moved on; mrm, for example, requires Java 17. Check the project's `pom.xml` before reaching for a newer API.

Raising either baseline is a deliberate, separate decision, not something to slip into a feature pull request.

## Format your code

The build enforces formatting, so don't hand-format, and don't reformat code you aren't otherwise touching. To format:

```
mvn spotless:apply
```

That applies [palantir-java-format](https://github.com/palantir/palantir-java-format), sorts imports, and tidies the POM. When CI fails on `spotless:check`, running the command and committing the result is the whole fix.

## License headers

Don't change the license or the owner in an existing file's header, and keep a replaced file's original header as it was. A new file takes the header convention of the files next to it in that repository. Where that convention names an owner, it is `MojoHaus and Contributors`, never an individual.

## Pull requests

A pull request is easier to review when it does the following:

- Covers one concern. Mechanical cleanups and behavior changes in the same diff are harder to review and slower to merge.
- Explains why in the description. The what is visible in the diff.
- Adds a test, usually an integration test under `src/it`. If the change is genuinely untestable, say so and say why.
- Keeps the plugin compatible. Goal names, parameters, their property names, and their defaults are public API; deprecate before removing, and say in the deprecation what to use instead.
- Has a title that describes the change for a user. Release notes are built from pull request titles and labels.
- References the issue it addresses, if there is one.

## Report a bug

The most useful reports say which plugin version you use, which JDK and Maven version, what you expected, and what happened instead. A short reproducer is worth more than a long description. For a build failure, include the output of `mvn -e`.

## Security

Don't open a public issue for a vulnerability. For the process, see [SECURITY.md](SECURITY.md).

## CI infrastructure failures

A red build is not always a bad change. These failures recur across the org and are **not** reasons to patch the pull request:

- **Maven Central HTTP 429** while resolving dependencies (often on the Maven 4 / JDK 25 cell). Re-run the failed jobs once.
- **macOS arm64 runner capacity** — a job stays queued or is cancelled by GitHub's capacity notice. Re-run once.
- **Dead third-party repositories** in integration-test fixtures (for example `repo.spring.io/milestone`). This is fixture drift, not a code failure; fix it in a separate change.
- **Windows post-build cleanup** ("Ensuring no file handle remains open") — a known runner flake. Re-run once.
- **Retired action versions** such as `actions/cache@v1` — GitHub disables them server-side. Fix the pin in its own change.

Read the failed job log before calling anything flaky. If the failure is one of the above, report it and re-run; if it comes from your change, add a follow-up commit. A skipped check is not a failure: GitHub reports skipped jobs as successful, even when required.

## For maintainers

The release steps are in [Performing a Release](https://www.mojohaus.org/development/performing-a-release.html) and in the [mojo-parent README](https://github.com/mojohaus/mojo-parent#releasing). The release checklist is owned by the MojoHaus maintainers and reviewed annually; the next scheduled review is November 2027.
