# Grash

![GitHub Workflow Status](https://img.shields.io/github/workflow/status/colin-pm/grash/Python%20package)


A dependency analysis tool for bash scripts.

## Purpose

This tool was created as a way to quickly evaluate the executables a bash script depends on.  It works by parsing one or more scripts and finding the names of everything that is executed.  It then compares that list against the files in the environment's path and returns the common set.

## Installation

### From PyPi

```shell
pip install grash
grash -h
```

### From source

Clone down the project and install with Poetry.

```shell
git clone git@github.com:colin-pm/grash.git
cd grash
poetry install
poetry shell
grash -h
```

## Usage

Currently, Grash only supports printing out the dependencies for the selected script.  Future functionality is intended to be implemented to generate a visual network graph of dependencies.

To evaluate the dependencies in a script, execute a command like the one below.

With foo.sh...
```shell
#!/usr/bin/env bash
for FILE in $(ls $1); do
  if [ ${FILE: -4} == .txt ]; then
    rm $FILE
  fi
done
echo "Cleared out all .txt files"
```

Run...
```shell
$ grash inspect foo.sh
Script: foo.sh
has dependencies...
echo
ls
rm
```

Several scripts can be evaluated at the same time.

```shell
$ echo '#!/usr/bin/env bash' > bar.sh
$ echo 'echo "This is a test"' >> bar.sh
$ grash inspect foo.sh bar.sh
Script: foo.sh
has dependencies...
echo
ls
mkdir
rm

Script: bar.sh
has dependencies...
echo
```

If you want to use a PATH other than the PATH provided by the system.  The ```-p``` flag can be used to specify an exclusive PATH for grash to use.

The ```-p``` flag is intended for evaluating scripts that may be used on a separate root filesystem, like the target root filesystem within Buildroot.

```shell
$ grash inspect -p "~/.local/bin:/usr/sbin" foo.sh
Script: foo.sh
has dependencies...
my-script.sh
```

## Variable expansion

Grash will recognize evaluation of variables. For example, Grash will recognize ```my_script``` and ```bar``` as dependencies in the example below.
```shell
COMMAND='my_script foo | bar'
eval $COMMAND
```

Nested variables are also supported. For example, both ```my_script``` and ```bar``` are recognized as dependencies by Grash in the example below.
```shell
COMMAND_ONE='bar'
COMMAND_TWO="my_script foo | ${COMMAND_ONE}"
eval $COMMAND_TWO
```

## Caveats

## Calling other scripts

Scripts called with source will be recognized as a dependency, but evaluating contents from another file will not be recognized as a dependency

```eval $(cat foo.sh)``` will not recognize foo.sh as a dependency. However, ```source foo.sh``` will recognize foo.sh as a dependency.

## Case statements

Case statements are not supported by bashlex, the parser used by Grash.  Grash's preprocessor will remove the case-specific lines from the script.  However, since control flow is not needed for parsing dependencies, the code for each case is left.  If you use case statments in your script, ensure the case syntax is on separate lines like the example below.

```shell
case "$1" in
        start)
            start
            ;;
         
        stop)
            stop
            ;;
         
        status)
            status anacron
            ;;
        restart)
            stop
            start
            ;;
        condrestart)
            if test "x`pidof anacron`" != x; then
                stop
                start
            fi
            ;;
         
        *)
            echo $"Usage: $0 {start|stop|restart|condrestart|status}"
            exit 1
esac
```
