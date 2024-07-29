# inkwell

Retain Bash Color Output for use in MD or HTML files.

## Install

Check for the [latest release](https://github.com/MikeGarde/inkwell/releases) and download.

```shell
curl -L https://github.com/MikeGarde/inkwell/releases/download/latest/inkwell > /usr/local/bin/inkwell
chmod +x /usr/local/bin/inkwell
```

### Examples

```shell
ls -la --color=always | inkwell
```

With output to file
 * [examples / ls-wls.html](https://mikegarde.github.io/inkwell/examples/ls-wls.html)

```shell
COMMAND="ls -la --color"
$COMMAND | inkwell --title $COMMAND > examples/ls-wls.html
```

## Develop / Build

 - Install [Taskfile](https://taskfile.dev/installation/)
 - Install [pipreqs](https://pypi.org/project/pipreqs/)
 - Install [pyinstaller](https://pyinstaller.org/en/stable/)

```shell
# First time setup
python3 -m venv .venv
source .venv/bin/activate
pip install pipreqs pyinstaller
pip install -r src/requirements.txt
# And make
task make
```

### Release

Version bumping is done using [patch, minor, major] as arguments to the `release` task.

```shell
task release -- minor
```
