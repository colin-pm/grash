# Grash

A graphical dependency analysis tool for bash scripts


## Variable expansion

Grash will recognize evaluation of variables, for example...

```shell
COMMAND='my_script foo | bar'
eval $COMMAND
```

my_script and bar will be recognized as dependencies.

Testing has not been added for nested variable expansion.  The example below may or may not currently work.

```shell
COMMAND_ONE='bar'
COMMAND_TWO="my_script foo | ${COMMAND_ONE}"
eval $COMMAND_TWO
```

## Caveats

Scripts called with source will be recognized as a dependency, but evaluating contents from another file will not be recognized as a dependency

Do not do this:
```shell
eval $(cat foo.sh) 
```

Instead, do this:
```shell
source foo.sh
```


