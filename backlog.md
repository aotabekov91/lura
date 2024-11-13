# Product backlog [Fitzview]

* [ ] Should support annotations
* [ ] Should support plugin system
* [ ] Should support tiling
* [ ] Should support visual mode

## Sprint.Annotations backlog: Should support annotations

* [.] Separate all view mixins [fitz] into a its own class :current:
* [x] Annotation hinting 
* [x] Separate selection into a its own class
* [x] Adjust bookmarks/quickmarks to the annotation model version
* [.] Engineer Sqlite annotation database
	* [x] As simple as possible with extensions in mind
	* [ ] Metadata field parsing format :next:
* [.] Support different types of annotation
	* [ ] Text annotation with an overlay text editor
* [ ] Finish picky

## Sprint.VisualMode backlog: Should support visual mode

* [ ] Visual band mode
* [ ] Visual word mode

## Sprint.Miscellenous

* [ ] Support saving states
	* [ ] Save last opened page
	* [ ] Save last view/window layout

## Bugs

* [x] view.select :bug:
* [ ] Search index is not changing when jumping to the first/end
* [ ] Visual word exiting without choosing a hint
* [ ] Some pages do not act on widewise fit zw
* [ ] Pane fullscreening changes position/on second try throws an error
* [ ] Normal mode <c-[> clean up selection
* [ ] View.Locate/Scale/Pos/Go should be factored out to its own class
* [ ] Closing a pane is not working
