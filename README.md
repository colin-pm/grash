# Grash

A dependency analysis tool for bash scripts


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

Scripts called with source will be recognized as a dependency, but evaluating contents from another file will not be recognized as a dependency

```eval $(cat foo.sh)``` will not recognize foo.sh as a dependency. However, ```source foo.sh``` will recognize foo.sh as a dependency.
