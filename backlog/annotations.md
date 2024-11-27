[Index](product.md)

# Annotations

## Doing

* [ ] Annotate
	* [ ] reannotate

## Todo

* [ ] Factor goto from all views out
* [ ] Refactor bar
* [ ] Edit mode :current:
* [ ] Exec mode
* [ ] Input mode
	* [ ] As a plug container
	* [ ] ListWidgetView
* [ ] Outline
	* [ ] Two-way syncing
* [o] Separate all view mixins [fitz] into a its own class 
	* [ ] Factor layout from fitzView[Scene]
* [.] Engineer Sqlite annotation database
	* [x] As simple as possible with extensions in mind
	* [ ] Metadata field parsing format :next:

## Done

* [x] FilesTree
	* [x] Partially NerdTree like functionality with keybindings
* [x] Docks view css
	* [x] Bookmark/quickmark/etc css 
* [x] Deannotate
* [x] Factor tags from docks out
	* [x] Add/finish normal mode for docks
* [x] Enable mouse scrolling to change item visibility
* [x] Add a toggle for cursor is visible
* [x] Annotation hinting 
* [x] Separate selection into a its own class
* [x] Adjust bookmarks/quickmarks to the annotation model version
* [x] Support saving states
	* [x] Save last opened page
	* [x] Save last view/window layout
* [x] Overlaying
	* [x] Factoring overlay out from app view
* [x] Support different types of annotation
	* [x] Text annotation with an overlay text editor :current:
* [x] Enable activating annotation mode in visual mode

# Miscellenuos
 
* [ ] Dictionary lookup plugin

# Bugs
	
## Doing

* [ ] Outline [i.g. all dock views] dock view is not totally fitting sometimes
* [ ] Selection's text is only the first word of whole selection regardless how long it actually is
	* [ ] For example, see annotations
* [ ] Fullscreen plug
	* [ ] Tab view app.view.main cannot restore previous layout
		* [ ] Add placeholder for a view that is being fullscreened
	* [x] Pane fullscreening changes position/on second try throws an error
 
## Todo

* [ ] Toggle gray scale does not change some items when they only partially visible
* [ ] Some pages do not act on widewise fit zw
* [ ] Link hint escaping without choosing is not working
* [ ] Outline syncing with index changes
* [ ] Autosave go/zoom does not always open last state
* [ ] Statusbar not redrawing after moving tab
* [ ] Bookmarks view is not showing anything if a model is annotated for the first time

## Done

* [x] Selection.setValue is removed but plugs are adjusted, some throw errors
* [x] Search is not jumping, i.e., showing pages
* [x] Annotation mode should change to normal after annotating
* [x] Normal mode <c-[> clean up selection
* [x] view.select :bug:
* [x] FilesTree.view.activate :bug: view dock resize
* [x] annotation selection does not draw after the first annotation select
* [x] Search index is not changing when jumping to the first/end
* [x] Visual word exiting without choosing a hint
* [x] TreeView normal jumping with gg/G calls an error 
* [x] View/tab/base tags are not working
* [x] View.Locate/Scale/Pos/Go should be factored out to its own class
* [x] Closing a pane is not working
