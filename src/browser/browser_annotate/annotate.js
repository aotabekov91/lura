"use strict";

window.browserviewscripts.annotate = (function() {
    const funcs = {};

	funcs.test_get_selection = () => {
		var i,
			len,
			ranges = [],
			rangesToIgnore = [],
			selection = window.getSelection();

		if (selection.isCollapsed) {
			return [];
		}

		for (i = 0; i < selection.rangeCount; i++) {
			var r = selection.getRangeAt(i),


				browserRange = new xpathRange.Range.BrowserRange(r),
				normedRange = browserRange.normalize().limit(document);

			// If the new range falls fully outside our this.element, we should
			// add it back to the document but not return it from this method.
			if (normedRange === null) {
				rangesToIgnore.push(r);
			} else {
				ranges.push(normedRange);
			}
		}

		// BrowserRange#normalize() modifies the DOM structure and deselects the
		// underlying text as a result. So here we remove the selected ranges and
		// reapply the new ones.
		selection.removeAllRanges();

		for (i = 0, len = rangesToIgnore.length; i < len; i++) {
			selection.addRange(rangesToIgnore[i]);
		}

		// Add normed ranges back to the selection
		for (i = 0, len = ranges.length; i < len; i++) {
			var range = ranges[i],
				drange = document.createRange();
			drange.setStartBefore(range.start);
			drange.setEndAfter(range.end);
			selection.addRange(drange);
		}


		return ranges;
	};

    return funcs;
})();
