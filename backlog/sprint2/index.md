[Index](../index.md)

# Sprint

Status:
Work done:
Actual time:
Estimated time:
Date: 2.12.2024-31.12.2024

## Objectives

* [ ] [Sprint 1: Plugins](objectives/s1_plugins.md)
* [x] [Sprint 1: Support annotation](objectives/s1_annotation.md)
* [x] [Sprint 1: Bugs](objectives/s1_bugs.md)
* [x] [Sprint 1: Separate mixins](objectives/s1_mixins.md)

* [ ] [Visual mode](objectives/visual.md)
* [ ] [View layout](objectives/view_layout.md)
* [x] [Help mode](objectives/help_mode.md)
* [x] [Bugs](objectives/bugs.md)
* [x] [Input mode](objectives/input_mode.md)
* [x] [Plugin system](objectives/plugin_system.md)
* [x] [Factoring out](objectives/factoring_out.md)
* [x] [Plugins](objectives/plugins.md)
* [x] [Exec mode](objectives/exec_mode.md)


## Todos

* pure python standard events
* non-blocking pure python timer
* app indexing
* app keyer
* terminal view 
  * direct all stdout/stdin to a terminal in app
* QWebView -> WebView full features as View (e.g., goto, split, copy, etc)
* tag key placeholder
	* "<placeholder:dock>z<placeholder:tab>J(normal)"
	* data={'dock': '<c-d>', 'tab': '<c-t>'}
	* earman.updateKeyPlaceholders(data)
	* earman.replacePlaceholder-> '<c-d>z<c-t>J(normal)'

## Bugs

* normal window tile goto last does not work
