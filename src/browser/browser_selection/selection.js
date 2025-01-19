"use strict";

window.browserviewscripts.select = (function) () {
	const funcs = {};

	funcs.select = (box={}) => {
		return box;
	};

	funcs.serialize: function(range) {
		var start = this.wordize(range.startContainer, range.startOffset, 'start');
		var end = this.wordize(range.endContainer, range.endOffset, 'end');
		if (this.options.validate) {
			var sums = this.getRangeChecksum(range);
			start += ':' + sums[0];
			end += ':' + sums[1];
		}
		return start + ',' + end;
	},

	wordize = function(container, offset, pos) {
		// counting words in container from/untill offset position

		// Skip ignored elements at the start and at the end
		var cont = elementIterator(this.selectable, container, undefined, pos === 'end', this.isIgnored)();
		if (cont !== container) {
			offset = pos == 'end' ? (cont.nodeType == 3? cont.textContent.length : 0) : 0;
			container = cont;
		}

		if (container.nodeType == 1) {
			container = firstTextNode(container, this.isIgnored);
		}

		//get content part, that isn't included in selection,
		//split it with regexp and count words in it
		var wcount = container.data.substring(0, offset).match(this.regexp);

		if (wcount != null) {
			if (pos == 'start') {wcount = wcount.length + 1;}
			if (pos == 'end') {wcount = wcount.length;}
		} else {
			wcount = 1;
		}

		var node = container;
		var selectionIndex = this.getNum(container);
		var firstNode = this.getFirstTextNode(selectionIndex);

		while (node && node != firstNode) {
			node = this.prevNode(node, /.*/);
			if (node !== null) {
				node = node._container;
				wcount += this.wordCount(node);
			}
		}

		/*
		n = container.previousSibling;
		// FIXME! Required word count outside of inner <b></b>
		while (n) {
			var onei = wordCount(n);
			wcount += onei;
			n = n.previousSibling;
		}
		*/
		return selectionIndex + ':' + wcount;
	},

	symbols: function(_node) {
		var _count = 0;
		if (_node.nodeType == 3) {
			_count = _node.nodeValue.length;
		} else if (_node.childNodes && _node.childNodes.length) {
			var allnodes = textNodes(_node);
			for (var i = allnodes.length; i--; ) {
				_count += allnodes[i].nodeValue.length;
			}
		}
		return _count;
	},


	return funcs;
})();


