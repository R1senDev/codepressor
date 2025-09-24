# Codepressor

A script that will effectively compress your code!

# We need **you**

As you can see, Codepressor has only a few plugins. And let me introduce you *The Formula*:

```python
if len(plugins) is few:
    r1sendev.feel(SAD)
else:
    r1sendev.feel(HAPPY)
```

## What you can do in order to make `r1sendev.feel(HAPPY)`

1. [Fork this repo](https://github.com/R1senDev/codepressor/fork);
2. Write some good new plugins;
3. Create a pull request;
4. Wait some time;
5. Wait some time;
6. Wait some time;
7. Wait some more time;
8. Wait some more time;
9. *«Oh dang he noticed»*;
10. **Voila!**

# How to create plugins

## What is plugin

**Plugin** is basically a file that located in `plugins/` folder. ***TODO***

## Basic plugin structure

Every plugin should have an attibutes in order to pluginning correctly.  
To be specific, here you are: The Table of anything required.

| Attribute Name | Required Type          | Description | Notes |
| -------------- | ---------------------- | ----------- | ----- |
| `__title__`    | `str`                  | The title of your plugin. **Should be short and stout,** `snake_styled`. | A plugin with an empty title will pass staging, but it won't actually work. |
| `__desc__`     | `str`                  | A short description of the plugin (about what it does to the file). | Empty description is acceptable, but morally condemned. |
| `__authors__`  | `tuple[str, ...]`      | Plugin authors. | - |
| `__ver__`      | `tuple[int, ...]`      | Plugin version. | - |
| `__exts__`     | `tuple[str, ...]`      | A tuple of file extensions (with dots) that are supported by this plugin. | It can be empty: in this case, the plugin can only be selected manually by passing the `--plugin=its_title` argument at startup. |
| `process`      | `Callable[[str], str]` | The main function. | Accepts the original source code, should return the processed source code. |