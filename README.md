# Grash

A dependency analysis tool for bash scripts


## Variable expansion

Grash will recognize evaluation of variables, for example...

```shell
COMMAND='my_script foo | bar'
eval $COMMAND
```

my_script and bar will be recognized as dependencies.

Nested variables are also supported.  For example, both my_script and bar are recognized in the example below.

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


