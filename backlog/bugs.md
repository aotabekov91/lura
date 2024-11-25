# Bugs
 
## Doing

* [ ] View/tab/base tags are not working
	* [ ] Statusbar not redrawing after moving tab
		* [ ] Refactor bar actually
* [ ] Fullscreen plug
	* [ ] Tab view app.view.main cannot restore previous layout
		* [ ] Add placeholder for a view that is being fullscreened
	* [x] Pane fullscreening changes position/on second try throws an error
* [x] Normal mode <c-[> clean up selection
* [x] view.select :bug:
* [x] FilesTree.view.activate :bug: view dock resize
* [x] annotation selection does not draw after the first annotation select
* [x] Search index is not changing when jumping to the first/end
* [x] Visual word exiting without choosing a hint
* [x] TreeView normal jumping with gg/G calls an error 
 
## Todo

* [ ] Outline [i.g. all dock views] dock view is not totally fitting sometimes
* [ ] Some pages do not act on widewise fit zw
* [ ] View.Locate/Scale/Pos/Go should be factored out to its own class
* [ ] Closing a pane is not working
* [ ] Link hint escaping without choosing is not working
* [ ] Outline syncing with index changes
* [ ] Autosave go/zoom does not always open last state
