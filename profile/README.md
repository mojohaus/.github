# MojoHaus

MojoHaus is a collection of plugins for [Apache Maven](https://maven.apache.org/), published to
Maven Central under the `org.codehaus.mojo` group id. The project was previously hosted on Codehaus
and known as Mojo@Codehaus.

Documentation for every plugin lives at **[www.mojohaus.org](https://www.mojohaus.org/)**, and the
[full plugin list](https://www.mojohaus.org/plugins.html) marks which ones are production-ready,
pre-release, or retired.

## Frequently used plugins

| Plugin | What it does |
| --- | --- |
| [versions](https://www.mojohaus.org/versions/versions-maven-plugin/) | Manage the versions of artifacts in a project POM |
| [flatten](https://www.mojohaus.org/flatten-maven-plugin/) | Generate a POM with build-time-only content resolved away |
| [exec](https://www.mojohaus.org/exec-maven-plugin/) | Run system and Java programs from a build |
| [build-helper](https://www.mojohaus.org/build-helper-maven-plugin/) | Attach extra source directories, resources and artifacts |
| [license](https://www.mojohaus.org/license-maven-plugin/) | Download, collect and check dependency licenses |
| [aspectj](https://www.mojohaus.org/aspectj-maven-plugin/) | Weave AspectJ aspects into a project |
| [jaxb2](https://www.mojohaus.org/jaxb2-maven-plugin/) | Generate Java from XML schemas, and schemas from Java |
| [buildnumber](https://www.mojohaus.org/buildnumber-maven-plugin/) | Stamp a build with an SCM revision or timestamp |
| [animal-sniffer](https://www.mojohaus.org/animal-sniffer/) | Check API signature compatibility against a target Java release |
| [extra-enforcer-rules](https://www.mojohaus.org/extra-enforcer-rules/) | Additional rules for maven-enforcer-plugin |
| [properties](https://www.mojohaus.org/properties-maven-plugin/) | Read and write project properties from and to files |
| [buildplan](https://www.mojohaus.org/buildplan-maven-plugin/) | Inspect a project's lifecycle bindings |

All of them share [mojo-parent](https://www.mojohaus.org/mojo-parent/) as their parent POM.

## Getting support

Each plugin has its own repository in this organization; report bugs and feature requests in that
repository's issue tracker. See [reporting an issue](https://www.mojohaus.org/contribution/reporting-an-issue.html)
for what to include. General Maven questions belong on the
[Maven users list](https://www.mojohaus.org/mailing-lists.html), and the
[FAQ](https://www.mojohaus.org/faq.html) covers the recurring ones.

## Contributing

Pull requests are welcome. Start with the
[project guidelines](https://www.mojohaus.org/development/guidelines.html), then
[submitting a patch](https://www.mojohaus.org/contribution/submitting-a-patch.html). To donate a new
plugin to the project, see [submitting a plugin](https://www.mojohaus.org/contribution/submitting-a-plugin.html).

## Verifying releases

Release bundles are signed. Check them against the
[MojoHaus KEYS](https://www.mojohaus.org/KEYS) file before use.
