# Product backlog [Fitzview]

* [ ] Should support annotations
* [ ] Should support plugin system
* [ ] Should support tiling
* [ ] Should support visual mode
* [ ] Should support different layout types 
	* [ ] Single/Double page view, etc.

## Sprint.Annotations backlog: Should support annotations

* [ ] Input mode
	* [ ] As a plug container
* [ ] Support different types of annotation
	* [ ] Text annotation with an overlay text editor :current:
* [ ] Outline
	* [ ] Two-way syncing
* [ ] FilesTree
	* [ ] NerdTree like functionality with keybindings
* [o] Separate all view mixins [fitz] into a its own class 
	* [ ] Factor layout from fitzView[Scene]
* [.] Engineer Sqlite annotation database
	* [x] As simple as possible with extensions in mind
	* [ ] Metadata field parsing format :next:
* [ ] Docks view css
	* [ ] Bookmark/quickmark/etc css 
* [ ] Finish picky
* [x] Annotation hinting 
* [x] Separate selection into a its own class
* [x] Adjust bookmarks/quickmarks to the annotation model version
* [x] Support saving states
	* [x] Save last opened page
	* [x] Save last view/window layout
* [x] Overlaying
	* [x] Factoring overlay out from app view

## Sprint.VisualMode backlog: Should support visual mode

* [ ] Visual band mode
* [ ] Visual word mode
* [ ] Input mode
	* [ ] ListWidgetView

## Sprint.Miscellenous


## Bugs

* [ ] view/tab/base tags are not working
* [ ] Search index is not changing when jumping to the first/end
* [ ] Visual word exiting without choosing a hint
* [ ] Some pages do not act on widewise fit zw
* [ ] Pane fullscreening changes position/on second try throws an error
* [ ] Normal mode <c-[> clean up selection
* [ ] View.Locate/Scale/Pos/Go should be factored out to its own class
* [ ] Closing a pane is not working
* [ ] Link hint escaping without choosing is not working
* [ ] Outline syncing with index changes
* [ ] Autosave go/zoom does not always open last state
* [x] view.select :bug:
* [x] FilesTree.view.activate :bug: view dock resize
