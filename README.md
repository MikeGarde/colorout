# inkwell
Retain Bash Color Output for MD or HTML files.

## Install

Check for the [latest release](https://github.com/MikeGarde/inkwell/releases) and download.

```shell
curl -L https://github.com/MikeGarde/inkwell/releases/download/latest/inkwell > /usr/local/bin/inkwell
chmod +x /usr/local/bin/inkwell
```

### Usage

```shell
ls -la --color=always | inkwell > ls.html
```

<pre>
total 120
drwxr-xr-x  13 me  staff    416 Apr 17 17:00 <span style="color:blue">.</span>
drwxr-xr-x@ 78 me  staff   2496 Apr 17 16:44 <span style="color:blue">..</span>
-rwx------@  1 me  staff   6148 Dec 12 12:25 <span style="color:red">.DS_Store</span>
drwxr-xr-x  14 me  staff    448 Apr 17 16:50 <span style="color:blue">.git</span>
-rwx------   1 me  staff     28 Jan 17 10:30 <span style="color:red">.gitignore</span>
drwxr-xr-x   9 me  staff    288 Apr 17 17:02 <span style="color:blue">.idea</span>
-rwx------@  1 me  staff  35149 Dec  8 21:45 <span style="color:red">LICENSE</span>
-rwx------@  1 me  staff    534 Apr 17 16:56 <span style="color:red">README.md</span>
-rwx------@  1 me  staff   1825 Apr 17 17:00 <span style="color:red">Taskfile.yml</span>
drwx------   4 me  staff    128 Dec 11 13:50 <span style="color:blue">build</span>
drwx------   5 me  staff    160 Apr 17 17:03 <span style="color:blue">dist</span>
-rwx------@  1 me  staff    666 Apr 17 17:03 <span style="color:red">inkwell.spec</span>
drwx------@  7 me  staff    224 Dec 12 09:13 <span style="color:blue">src</span>
</pre>

## Develop / Build

 - Install [Taskfile](https://taskfile.dev/installation/)
 - Install [pipreqs](https://pypi.org/project/pipreqs/) `pip install pipreqs`
 - Install [pyinstaller](https://pyinstaller.org/en/stable/) `pip install pyinstaller`

```shell
python3 -m venv .venv
source .venv/bin/activate
task make
```

### Test

```shell
ls -la --color=always | python src/inkwell.py
```

### Release

Version bumping is done using [patch, minor, major] as arguments to the `release` task.

```shell
task release -- minor
```
