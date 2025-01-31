window.browserviewscripts.selection = (function() {

	'use strict';
	var exports = {};

	class SelectionRange {
		constructor(range, selection) {
			this.range = range;
			this.selection = selection;

			this.startContainer = this.range.startContainer;
			this.startOffset = this.range.startOffset;
			this.endContainer = this.range.endContainer;
			this.endOffset = this.range.endOffset;

			this.nodes = null;
		}

		setEnd = function(container, offset) {
			this.range.setEnd(container, offset);
			this.endContainer = this.range.endContainer;
			this.endOffset = this.range.endOffset;
			this.nodes = null;
		}

		setStart = function(container, offset) {
			this.range.setStart(container, offset);
			this.startContainer = this.range.startContainer;
			this.startOffset = this.range.startOffset;
			this.nodes = null;
		}

		fillNodes = function() {
			this.nodes = [];
			var iter = elementIterator(
				document.body, 
				this.startContainer, 
				this.endContainer, 
				false,
				this.selection.isIgnored);

			var node = iter();
			while (node) {
				this.nodes.push(node);
				node = iter();
			}
		}

		toString = function() {
			return this.range.toString();
		}

		splitBoundaries = function() {
			var sc = this.startContainer,
				so = this.startOffset,
				ec = this.endContainer,
				eo = this.endOffset;
			var startEndSame = (sc === ec);

			if (ec.nodeType == 3 && eo < ec.length) {
				ec.splitText(eo);
			}

			if (sc.nodeType == 3 && so > 0) {
				sc = sc.splitText(so);
				if (startEndSame) {
					eo -= so;
					ec = sc;
				}
				so = 0;
			}
			this.setStart(sc, so);
			this.setEnd(ec, eo);
		}

		getTextNodes = function() {
			var iterator = this.getElementIterator();
			var textNodes = [], node;
			while ((node = iterator())) {
				// XXX was there a reason to check for empty string?
				// with this check selecting two sibling words separately
				// and then selecting them both in one range doesn't work properly
				if (node.nodeType == 3) {// && !node.data.match(/^\s*$/)){
					textNodes.push(node);
				}
			}
			return textNodes;
		}

		getElementIterator = function(reversed) {
			if (!this.nodes) { this.fillNodes(); }

			if (reversed) {
				var i = this.nodes.length;
				return function() { if (i > 0) { i--; return this.nodes[i]; } }.bind(this);
			} else {
				var i = 0;
				return function() { if (i < this.nodes.length) { i++; return this.nodes[i - 1]; } }.bind(this);
			}
		};

		getTextNodeIterator = function(reversed) {
			var elemIter = this.getElementIterator(reversed);
			function next() {
				do {
					var node = elemIter();
					if (node && node.nodeType == 3) {
						return node;
					}
				} while (node);
				return node;
			}
			return next;
		}

		getWordIterator = function(regexp, reversed) {
			var elemIter = this.getElementIterator(reversed);
			var node;
			var counterAim = 0, i = 0;
			var finished = false, match, this_ = this;
			function next() {
				if (counterAim == i && !finished) {
					do {
						do {
							node = elemIter();
						} while (node && node.nodeType != 3);
						finished = !node;
						if (!finished) {
							var value = node.nodeValue;
							if (node == this_.endContainer) {
								value = value.substr(0, this_.endOffset);
							}
							if (node == this_.startContainer) {
								value = value.substr(this_.startOffset);
							}
							match = value.match(regexp);
						}
					} while (node && !match);
					if (match) {
						counterAim = reversed ? 0 : match.length - 1;
						i = reversed ? match.length - 1 : 0;
					}
				} else {
					if (reversed) { i--; } else { i++; }
				}
				if (finished) { return null; }
				return match[i];
			}
			return next;
		}

		wrapSelection = function(className) {
			this.splitBoundaries();
			var textNodes = this.getTextNodes();
			for (var i = textNodes.length; i--;) {
				// XXX wrap sibling text nodes together
				var span = document.createElement('span');
				span.className = className;
				textNodes[i].parentNode.insertBefore(span, textNodes[i]);
				span.appendChild(textNodes[i]);
			}
		}
	}

	class Selection {

		constructor(options) {
			options = options || {};
			if ('is_block' in options){
				options.isBlock = options.is_block;
			}
			this.options = extend({}, this.defaultOptions, options);
			extend(this, { counter: 0, ranges: {}, blocks: {}});
			this.init();
		}

		defaultOptions = {
			'regexp': '[^\\s,;:\u2013.!?<>\u2026\\n\u00a0\\*]+',
			'selectable': 'selectable-content',
			'ignored': null,
			'validate': false,
			'isBlock': function(el) {
				return el.nodeName == 'BR' || inArray(getCompiledStyle(el, 'display'),
					['inline', 'none']) == -1;
			}
		}

		init = function() { // domready
			this.selectable = (typeof this.options.selectable == 'string' ?
				document.getElementById(this.options.selectable) :
				this.options.selectable);
			if (typeof this.options.regexp != 'string') {
				throw 'regexp is set as string';
			}
			this.regexp = new RegExp(this.options.regexp, 'ig');
			if (!this.selectable) { return; }
			this.isIgnored = this.constructIgnored(this.options.ignored);
			// enumerate block elements containing a text
			this.enumerateElements();
		}

		destroy = function() {
			var spans = byClassName(this.selectable, 'user_selection_true');
			this.removeTextSelection(spans);
			var closes = byClassName(this.selectable, 'closewrap');
			for (var i = closes.length; i--;) {
				closes[i].parentNode.removeChild(closes[i]);
			}
			var indices = byClassName(this.selectable, 'selection_index');
			for (var i = indices.length; i--;) {
				indices[i].parentNode.removeChild(indices[i]);
			}

		}

		/*
		 * Interface functions, safe to redefine
		 */

		getPositionChecksum = function(wordsIterator) {
			/*
			 * Used in validation. This method accepts word sequence iterator (a function returning
			 * the next word of sequence on each call or null if words are) and returns a string checksum.
			 * The getPositionChecksum method is called twice for each range: one for start position and
			 * one for end position (with reversed iterator).
			 *
			 * The checksum is included into hash and it is checked on page load. If calculated checksum
			 * doesn't one from url, the selection is not restored.
			 */
			var sum = '';
			for (var i = 0; i < 3; i++) {
				var part = (wordsIterator() || '').charAt(0);
				if (part) {
					var allowedChars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890';
					var integer = part.charCodeAt(0) % allowedChars.length;
					part = allowedChars.charAt(integer);
				}
				sum += part;
			}
			return sum;
		}

		// XXX sort methods logically
		deleteSelections = function(numclasses) {
			for (var i = numclasses.length; i--;) {
				var numclass = numclasses[i];
				var spans = byClassName(this.selectable, numclass);
				var closewrap = firstWithClass(spans[spans.length - 1], 'closewrap');
				closewrap.parentNode.removeChild(closewrap);

				this.removeTextSelection(spans);
				delete this.ranges[numclass];
			}
		}

		removeTextSelection = function(spans) {
			for (var i = spans.length; i--;) {
				var span = spans[i];
				for (var j = 0; j < span.childNodes.length; j++) {
					span.parentNode.insertBefore(span.childNodes[j], span);
				}
				span.parentNode.removeChild(span);
			}
		}

		isInternal = function(node) {
			while (node.parentNode) {
				if (node == this.selectable) {
					return true;
				}
				node = node.parentNode;
			}
			return false;
		}

		_siblingNode = function(cont, reversed, regexp) {
			regexp = regexp || this.regexp;
			var node = cont;
			if (reversed && node.previousSibling) {
				node = node.previousSibling; // hack for Chrome triple click
			}

			var iter = elementIterator(this.selectable, node, undefined, reversed, this.isIgnored);
			node = iter();
			if (node == cont) { node = iter(); }

			while (node && !(node instanceof HTMLDocument)) {
				if (node.nodeType == 3 &&
					(node.data.match(regexp) != null)) {
					return { _container: node, _offset: reversed * node.data.length };
				}
				node = iter()
			}
			return null;
		}

		wordCount = function wordCount(node) {
			var _wcount = 0;
			if (node.nodeType == 3) {
				// counting words in text node
				var match = node.nodeValue.match(this.regexp);
				if (match) { _wcount += match.length; }
			} else if (node.childNodes && node.childNodes.length) { // Child element
				// counting words in element node with nested text nodes
				var alltxtNodes = textNodes(node);
				for (var i = alltxtNodes.length; i--;) {
					_wcount += alltxtNodes[i].nodeValue.match(this.regexp).length;
				}
			}
			return _wcount;
		}

		words = function(container, offset, pos) {
			// counting words in container from/untill offset position

			// Skip ignored elements at the start and at the end
			var cont = elementIterator(this.selectable, container, undefined, pos === 'end', this.isIgnored)();
			if (cont !== container) {
				offset = pos == 'end' ? (cont.nodeType == 3 ? cont.textContent.length : 0) : 0;
				container = cont;
			}

			if (container.nodeType == 1) {
				container = firstTextNode(container, this.isIgnored);
			}

			//get content part, that isn't included in selection,
			//split it with regexp and count words in it
			var wcount = container.data.substring(0, offset).match(this.regexp);

			if (wcount != null) {
				if (pos == 'start') { wcount = wcount.length + 1; }
				if (pos == 'end') { wcount = wcount.length; }
			} else {
				wcount = 1;
			}

			var node = container;
			var selectionIndex = this.getNum(container);
			var firstNode = this.getFirstTextNode(selectionIndex);

			while (node && node != firstNode) {
				node = this._siblingNode(node, 1, /.*/);
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
		}

		symbols = function(_node) {
			var _count = 0;
			if (_node.nodeType == 3) {
				_count = _node.nodeValue.length;
			} else if (_node.childNodes && _node.childNodes.length) {
				var allnodes = textNodes(_node);
				for (var i = allnodes.length; i--;) {
					_count += allnodes[i].nodeValue.length;
				}
			}
			return _count;
		}

		deserializeSelection = function(serialized) {
			var sel = window.getSelection();
			if (sel.rangeCount > 0) { sel.removeAllRanges(); }

			var range = this.deserializeRange(serialized);
			if (range) {
				this.addSelection(range);
			}
		}

		deserializeRange = function(serialized) {
			var result = /^([0-9A-Za-z:]+)(?:,|%2C)([0-9A-Za-z:]+)$/.exec(serialized);
			var bits1 = result[1].split(':');
			var bits2 = result[2].split(':');
			// XXX this if is ugly
			if (parseInt(bits1[0], 10) < parseInt(bits2[0], 10) ||
				(bits1[0] == bits2[0] && parseInt(bits1[1], 10) <= parseInt(bits2[1], 10))) {

				var start = this.deserializePosition(bits1, 'start'),
					end = this.deserializePosition(bits2, 'end');

				if (start.node && end.node) {
					var range = document.createRange();
					range.setStart(start.node, start.offset);
					range.setEnd(end.node, end.offset);
					range = new SelectionRange(range, this);
					if (!this.options.validate || this.validateRange(range, bits1[2], bits2[2])) {
						return range;
					}
				}
			}

			if (window.console && (typeof window.console.warn == 'function')) {
				window.console.warn('Cannot deserialize range: ' + serialized);
			}
			return null;
		}

		validateRange = function(range, sum1, sum2) {
			var valid = true, sum;
			if (sum1) {
				sum = this.getPositionChecksum(range.getWordIterator(this.regexp));
				valid = valid && sum1 == sum;
			}
			if (sum2) {
				sum = this.getPositionChecksum(range.getWordIterator(this.regexp, true));
				valid = valid && sum2 == sum;
			}
			return valid;
		}

		getRangeChecksum = function(range) {
			return [this.getPositionChecksum(range.getWordIterator(this.regexp)),
			this.getPositionChecksum(range.getWordIterator(this.regexp, true))];
		}

		deserializePosition = function(bits, pos) {
			// deserializes #OfBlock:#OfWord pair
			// getting block
			var node = this.blocks[parseInt(bits[0], 10)];

			var offset, stepCount = 0;
			// getting word in all text nodes
			while (node) {
				var re = new RegExp(this.options.regexp, 'ig'),
					myArray;
				while ((myArray = re.exec(node.data)) != null) {
					stepCount++;
					if (stepCount == bits[1]) {
						if (pos == 'start') { offset = myArray.index; }
						if (pos == 'end') { offset = re.lastIndex; }

						return { node: node, offset: parseInt(offset, 10) };
					}

				}
				// word not found yet, trying next container
				node = this._siblingNode(node, 0, /.*/);
				node = node ? node._container : null;
				if (node && this.isFirstTextNode(node)) {
					node = null;
				}
			}
			return { node: null, offset: 0 };
		}

		serializeRange = function(range) {
			var start = this.words(range.startContainer, range.startOffset, 'start');
			var end = this.words(range.endContainer, range.endOffset, 'end');
			if (this.options.validate) {
				var sums = this.getRangeChecksum(range);
				start += ':' + sums[0];
				end += ':' + sums[1];
			}
			return start + ',' + end;
		}

		checkSelection = function(range) {
			/*
			 * Corrects selection.
			 * Returns range object
			 */
			this.checkPosition(range, range.startOffset, range.startContainer, 'start');
			this.checkPosition(range, range.endOffset, range.endContainer, 'end');

			this.checkBrackets(range);
			this.checkSentence(range);

			return range;
		}

		checkPosition = function(range, offset, container, position) {
			var this_ = this, newdata;

			function isWord(str) {
				return str.match(this_.regexp) != null;
			}

			function isNotWord(str) {
				return str.match(this_.regexp) == null;
			}

			function stepBack(container, offset, condition) {
				// correcting selection stepping back and including symbols
				// that match a given condition
				while (offset > 0 && condition(container.data.charAt(offset - 1))) {
					offset--;
				}
				return offset;
			}

			function stepForward(container, offset, condition) {
				// correcting selection stepping forward and including symbols
				// that match a given condition
				while (offset < container.data.length && condition(container.data.charAt(offset))) {
					offset++;
				}
				return offset;
			}
			if (container.nodeType == 1 && offset > 0) {
				// Triple click handling for elements like <br>
				if (offset < container.childNodes.length) {
					container = container.childNodes[offset];
					offset = 0;
				} else {
					// XXX what is the case for this code?
					var containerTextNodes = textNodes(container); // XXX lastTextNode
					if (containerTextNodes.length) { // this if fixes regressionSelectionStartsAtImage test
						container = containerTextNodes[containerTextNodes.length - 1];
						offset = container.data.length;
					}
				}
			}

			if (position == 'start') {

				if (container.nodeType == 1 && trim(textContent(container)) != '') {
					container = firstTextNode(container);
					offset = 0;
				}
				if (container.nodeType != 3 ||
					container.data.substring(offset).match(this.regexp) == null) {
					newdata = this._siblingNode(container, 0);
					container = newdata._container;
					offset = newdata._offset;
				}

				// Important! Shorten the selection first and then extend it!
				offset = stepForward(container, offset, isNotWord);
				offset = stepBack(container, offset, isWord);

				range.setStart(container, offset);
			}

			if (position == 'end') {
				if (container.nodeType == 1 && trim(textContent(container)) != '' && offset != 0) {
					container = container.childNodes[range.endOffset - 1];

					var containerTextNodes = textNodes(container); // XXX lastTextNode
					container = containerTextNodes[containerTextNodes.length - 1];

					offset = container.data.length;
				}

				if (container.nodeType != 3 ||
					container.data.substring(0, offset).match(this.regexp) == null) {
					newdata = this._siblingNode(container, 1);
					container = newdata._container;
					offset = newdata._offset;
				}

				// Important! Shorten the selection first and then extend it!
				offset = stepBack(container, offset, isNotWord);
				offset = stepForward(container, offset, isWord);

				range.setEnd(container, offset);
			}
		}

		checkBrackets = function(range) {
			this._checkBrackets(range, '(', ')', /\(|\)/g, /\(x*\)/g);
			this._checkBrackets(range, '\u00ab', '\u00bb', /\\u00ab|\\u00bb/g, /\u00abx*\u00bb/g);
			// XXX Double brackets?
		}

		_checkBrackets = function(range, ob, cb, matchReg, replReg) {
			// XXX Needs cleanup!
			var text = range.toString();//getTextNodes(range).map(function(x){return x.data;}).join('');
			var brackets = text.match(matchReg);
			var newData;
			if (brackets) {
				brackets = brackets.join('');
				var l = brackets.length + 1;
				while (brackets.length < l) {
					l = brackets.length;
					brackets = brackets.replace(replReg, 'x');
				}
				if (brackets.charAt(brackets.length - 1) == cb &&
					text.charAt(text.length - 1) == cb) {
					if (range.endOffset == 1) {
						newData = this._siblingNode(range.endContainer, 1);
						range.setEnd(newData.container, newData.offset);
					} else {
						range.setEnd(range.endContainer, range.endOffset - 1);
					}
				}
				if (brackets.charAt(0) == ob &&
					text.charAt(0) == ob) {
					if (range.startOffset == range.startContainer.data.length) {
						newData = this._siblingNode(range.endContainer, 0);
						range.setStart(newData.container, newData.offset);
					} else {
						range.setStart(range.startContainer, range.startOffset + 1);
					}
				}
			}

		}

		checkSentence = function(range) {
			var data, nextAfterRange;
			if (range.endOffset == range.endContainer.data.length) {
				data = this._siblingNode(range.endContainer, 0, /.*/);
				if (!data) { return null; }
				nextAfterRange = data._container.data.charAt(0);
			} else {
				data = { _container: range.endContainer, _offset: range.endOffset };
				nextAfterRange = range.endContainer.data.charAt(range.endOffset);
			}

			if (nextAfterRange.match(/\.|\?|\!/)) {
				// sentence end detected
				// XXX rewrite
				var text = range.toString();
				// XXX support not only latin and russian?
				if (text.match(/(\.|\?|\!)\s+[A-Z\u0410-\u042f\u0401]/)) {
					return apply();
				}

				if (range.startOffset == 0 &&
					range.startContainer.previousSibling &&
					range.startContainer.previousSibling.nodeType == 1 &&
					hasClass(range.startContainer.previousSibling, 'selection_index')) {
					return apply();
				}

				var node, iterator = range.getElementIterator();
				while ((node = iterator())) {
					if (node.nodeType == 1 && hasClass(node, 'selection_index')) {
						return apply();
					}
				}

				if (text.charAt(0).match(/[A-Z\u0410-\u042f\u0401]/)) {
					var pre = range.startContainer.data.substring(0, range.startOffset);
					if (!pre.match(/\S/)) {
						var preData = this._siblingNode(range.startContainer, 1, /\W*/);
						pre = preData._container.data;
					}
					pre = trim(pre);
					if (pre.charAt(pre.length - 1).match(/(\.|\?|\!)/)) {
						return apply();
					}
				}
				return null;
			}

			function apply() {
				range.setEnd(data._container, data._offset + 1);
			}
		}

		mergeSelections = function(range) {
			var merges = [];
			var iterator = range.getElementIterator();
			var node = iterator();
			var parent_ = parentWithClass(node, 'user_selection_true');
			if (parent_) {
				parent_ = /(num\d+)(?:$| )/.exec(parent_.className)[1];
				range.setStart(firstTextNode(firstWithClass(this.selectable, parent_)), 0);
				merges.push(parent_);
			}

			iterator = range.getElementIterator();
			node = iterator();
			var last = node;
			while (node) {
				if (node.nodeType == 1 && hasClass(node, 'user_selection_true')) {
					var cls = /(num\d+)(?:$|)/.exec(node.className)[0];
					if (inArray(cls, merges) == -1) {
						merges.push(cls);
					}
				}
				last = node;
				node = iterator();
			}
			var last = parentWithClass(last, 'user_selection_true');

			if (last) {
				last = /(num\d+)(?:$| )/.exec(last.className)[1];
				var tnodes = textNodes(lastWithClass(this.selectable, last)); // XXX lastTextNode
				var lastNode = tnodes[tnodes.length - 1];
				range.setEnd(lastNode, lastNode.length);
			}

			if (merges.length) {
				// this breaks selection, so we need to dump a range and restore it after DOM changes
				var sc = range.startContainer, so = range.startOffset,
					ec = range.endContainer, eo = range.endOffset;
				this.deleteSelections(merges);
				range.setStart(sc, so);
				range.setEnd(ec, eo);
			}
			return range;
		}

		setSelection = function(serialized) {
			var sel = window.getSelection();
			if (sel.rangeCount > 0) { sel.removeAllRanges(); }
			var range = this.deserializeRange(serialized);
			if (range) {
				sel.addRange(range.range);
			}
		}

		getSelection = function() {
			var range = this.getFirstRange();
			if (range) {
				range = this.checkSelection(range);
				range = this.mergeSelections(range);
				var srange = this.serializeRange(range);
				return srange
			}
		}

		addSelection = function(range) {
			range = range || this.getFirstRange();
			range = this.checkSelection(range);
			range = this.mergeSelections(range);

			var className = 'num' + this.counter;
			// generating hash part for this range
			this.ranges[className] = this.serializeRange(range);

			range.wrapSelection(className + ' user_selection_true');
			this.addSelectionEvents(className);
		}

		addSelectionEvents = function(className) {
			var timeoutHover = false;
			var this_ = this;

			var wrappers = byClassName(this.selectable, className);
			for (var i = wrappers.length; i--;) {
				addEvent(wrappers[i], 'mouseover', function() {
					for (var i = wrappers.length; i--;) {
						addClass(wrappers[i], 'hover');
					}
					window.clearTimeout(timeoutHover);
				});
				addEvent(wrappers[i], 'mouseout', function(e) {
					// mouseleave
					var t = e.relatedTarget;
					while (t && t.parentNode && t.className != this.className) {
						t = t.parentNode;
					}
					if (!t || t.className != this.className) {
						timeoutHover = window.setTimeout(function() {
							for (var i = wrappers.length; i--;) {
								removeClass(wrappers[i], 'hover');
							}
						}, 2000);
					}
				});
			}

			var closer = document.createElement('a');
			closer.className = 'txtsel_close';
			closer.href = '#';
			var closerSpan = document.createElement('span');
			closerSpan.className = 'closewrap';
			closerSpan.appendChild(closer);
			addEvent(closer, 'click', function(e) {
				preventDefault(e);
				this_.deleteSelections([className]);
			});
			wrappers[wrappers.length - 1].appendChild(closerSpan);

			this.counter++;
			window.getSelection().removeAllRanges();
		}

		getFirstRange = function() {
			var sel = window.getSelection();
			var res = sel.rangeCount ? sel.getRangeAt(0) : null;
			if (res === null) {
				return null;
			}
			if (this.lastRange && res &&
				res.endContainer == res.startContainer &&
				res.endOffset == res.startOffset) {
				return this.lastRange
			}

			return new SelectionRange(res, this);
		}

		enumerateElements = function() {
			// marks first text node in each visual block element:
			// inserts a span with special class and ID before it
			var node = this.selectable;
			this.captureCount = this.captureCount || 0;
			var this_ = this;

			enumerate(node);

			function enumerate(node) {
				var children = node.childNodes;
				var hasBlocks = false;
				var blockStarted = false;

				for (var idx = 0; idx < children.length; ++idx) {
					var child = children.item(idx);
					var nodeType = child.nodeType;
					if (nodeType == 3 && !child.nodeValue.match(this_.regexp)) {
						// ..if it is a textnode that is logically empty, ignore it
						continue;
					} else if (nodeType == 3) {
						if (!blockStarted) {
							// remember the block
							this_.captureCount++;
							var indexSpan = document.createElement('span');
							// XXX prefix all class and id attributes with "selection"
							indexSpan.className = 'selection_index selection_index' + this_.captureCount;
							indexSpan.setAttribute('rel', this_.captureCount);
							child.parentNode.insertBefore(indexSpan, child);

							idx++;
							this_.blocks[this_.captureCount] = child;
							hasBlocks = blockStarted = true;
						}
					} else if (nodeType == 1) {
						// XXX check if this is correct
						if (!this_.isIgnored(child)) {
							var isBlock = this_.options.isBlock(child);

							if (isBlock) {
								var childHasBlocks = enumerate(child);
								hasBlocks = hasBlocks || childHasBlocks;
								blockStarted = false;
							} else if (!blockStarted) {
								blockStarted = enumerate(child);
								hasBlocks = hasBlocks || blockStarted;
							}
						}
					}
				}
				return hasBlocks;
			}
		}

		isFirstTextNode = function(textNode) {
			var prevs = [textNode.previousSibling, textNode.parentNode.previousSibling];
			for (var i = prevs.length; i--;) {
				if (prevs[i] && prevs[i].nodeType == 1 && prevs[i].className == 'selection_index') {
					return true;
				}
			}
			return false;
		}

		getFirstTextNode = function(numclass) {
			if (!numclass) { return null; }
			var tnode = byClassName(this.selectable, 'selection_index' + numclass)[0];
			if (tnode) {
				var iter = elementIterator(document.body, tnode, undefined, false, this.isIgnored);
				var node;
				while (node = iter()) {
					if (node.nodeType === 3) { return node; }
				}
			}
			return null;
		}

		getNum = function(cont) {
			while (cont.parentNode) {
				while (cont.previousSibling) {
					cont = cont.previousSibling;
					while (cont.nodeType == 1 && cont.childNodes.length) {
						cont = cont.lastChild;
					}
					if (cont.nodeType == 1 && hasClass(cont, 'selection_index')) {
						return cont.getAttribute('rel');
					}
				}
				cont = cont.parentNode;
			}
			return null;
		}

		constructIgnored = function(selector) {
			if (typeof selector == 'function') {
				return selector;
			} else if (typeof selector == 'string') {
				// supports simple selectors by class, by tag and by id
				var byId = [], byClass = [], byTag = [];
				var selectors = selector.split(',');
				for (var i = 0; i < selectors.length; i++) {
					var sel = trim(selectors[i]);
					if (sel.charAt(0) == '#') {
						byId.push(sel.substr(1));
					} else if (sel.charAt(0) == '.') {
						byClass.push(sel.substr(1));
					} else {
						byTag.push(sel);
					}
				}

				return function(node) {
					var i;
					for (i = byId.length; i--;) {
						if (node.id == byId[i]) { return true; }
					}
					for (i = byClass.length; i--;) {
						if (hasClass(node, byClass[i])) { return true; }
					}
					for (i = byTag.length; i--;) {
						if (node.tagName == byTag[i].toUpperCase()) { return true; }
					}
					return false;
				};
			} else {
				return function() { return false; };
			}
		}

		rangeIsSelectable = function() {
			var range = this.getFirstRange();
			if (!range) { return false; }

			var iterator = range.getTextNodeIterator();
			var firstNode = iterator();
			if (!firstNode) { return false; }

			var firstSelection = parentWithClass(firstNode, 'user_selection_true');
			var lastNode = range.getTextNodeIterator(true)();
			var lastSelection = parentWithClass(lastNode, 'user_selection_true');
			if (firstSelection && lastSelection) {
				var reg = /(?:^| )(num\d+)(?:$| )/;
				var cls1 = reg.exec(firstSelection.className)[1];
				var cls2 = reg.exec(lastSelection.className)[1];
				return cls1 !== cls2;
			}

			var nodes = [firstNode, lastNode];
			for (var i = nodes.length; i--;) {
				var node = nodes[i];
				while (node != this.selectable) {
					node = node.parentNode;
					if (!node || node instanceof HTMLDocument) {
						return false;
					}
				}
			}

			return true;
		}
	}


	function removeClass(elem, cls) {
		// XXX attention! NOT UNIVERSAL!
		// don't use for classes with non-literal symbols
		var reg = _classRegExp(cls);
		if (reg.test(elem.className)) {
			elem.className = trim(elem.className.replace(reg, '$1'));
		}
	}

	function inArray(elem, array) {
		// from jQuery
		// Hate IE
		for (var i = 0, length = array.length; i < length; i++) {
			if (array[i] === elem) { return i; }
		}
		return -1;
	}

	function preventDefault(e) {
		if (e.preventDefault) { e.preventDefault(); }
		else { e.returnValue = false; }
	}

	function textNodes(elem) {
		var ret = [], node;
		var iter = elementIterator(elem);
		while ((node = iter())) {
			if (node.nodeType === 3) {
				ret.push(node);
			}
		}
		return ret;
	}

	function _classRegExp(cls) {
		return new RegExp('(^|\\s+)' + cls + '(?:$|\\s+)', 'g');
	}

	function hasClass(elem, cls) {
		var reg = _classRegExp(cls);
		return reg.test(elem.className);
	}

	function addClass(elem, cls) {
		// XXX attention! NOT UNIVERSAL!
		// don't use for classes with non-literal symbols
		var reg = _classRegExp(cls);
		if (!reg.test(elem.className)) {
			elem.className = elem.className + ' ' + cls;
		}
	}

	function trim(text) {
		return (text || '').replace(/^\s+|\s+$/g, '');
	}

	function getCompiledStyle(elem, strCssRule) {
		// copypasted from Internets
		var strValue = '';
		if (document.defaultView && document.defaultView.getComputedStyle) {
			strValue = document.defaultView.getComputedStyle(elem, '').getPropertyValue(strCssRule);
		}
		else if (elem.currentStyle) {
			strCssRule = strCssRule.replace(/\-(\w)/g, function(_, p1) {
				return p1.toUpperCase();
			});
			strValue = elem.currentStyle[strCssRule];
		}
		return strValue;
	}

	function textContent(elem) {
		return elem.textContent || elem.innerText;
	}

	function parentWithClass(p, cls) {
		while (p && !hasClass(p, cls)) { p = p.parentNode; }
		return p || null;
	}

	function firstWithClass(elem, cls) {
		var iter = elementIterator(elem);
		var node = null;
		while ((node = iter())) {
			if (node.nodeType === 1 && hasClass(node, cls)) { return node; }
		}
		return null;
	}

	function lastWithClass(elem, cls) {
		var elems = byClassName(elem, cls);
		if (elems) {
			return elems[elems.length - 1];
		}
		return null;
	}

	function firstTextNode(elem, isIgnored) {
		var iter = elementIterator(elem, undefined, undefined, undefined, isIgnored);
		var node = null;
		while ((node = iter())) {
			if (node.nodeType === 3) { return node; }
		}
		return node;
	}

	function byClassName(elem, cls) {
		if (elem.getElementsByClassName) {
			return elem.getElementsByClassName(cls);
		} else {
			var ret = [], node;
			var iter = elementIterator(elem);
			while ((node = iter())) {
				if (node.nodeType == 1 && hasClass(node, cls)) {
					ret.push(node);
				}
			}
			return ret;
		}
	}

	function extend(obj) {
		for (var i = 1; i < arguments.length; i++) {
			for (var key in arguments[i]) {
				obj[key] = arguments[i][key];
			}
		}
		return obj;
	}

	function getIgnoredParent(iterNode, isIgnored) {
		if (!isIgnored) { return null; }

		var ignoredParent = null;
		while (iterNode && !(iterNode.parentNode instanceof HTMLDocument)) {
			if (isIgnored(iterNode)) {
				ignoredParent = iterNode;
			}
			iterNode = iterNode.parentNode;
		}

		return ignoredParent;
	}

	function elementIterator(parent, cont, end, reversed, isIgnored) {
		reversed = !!reversed;
		cont = cont || parent[reversed ? 'lastChild' : 'firstChild'];
		var finished = !cont;
		var up = false;

		var ignoredParent = getIgnoredParent(cont, isIgnored);

		function getNext() {
			if (cont.childNodes && cont.childNodes.length && !up) {
				cont = cont[reversed ? 'lastChild' : 'firstChild'];
			} else if (cont[reversed ? 'previousSibling' : 'nextSibling']) {
				cont = cont[reversed ? 'previousSibling' : 'nextSibling'];
				up = false;
			} else if (cont.parentNode) {
				cont = cont.parentNode;
				if (cont === parent || cont === end) { finished = true; }
				if (cont === ignoredParent) { ignoredParent = null; }
				up = true;
				getNext();
			}
		}

		function next() {
			do {
				if (finished) { return null; }

				var result = cont;
				var resultIgnored = !!ignoredParent;

				getNext();

				if (isIgnored && isIgnored(result) && !resultIgnored) { ignoredParent = result; }
				if (result === end && !(result.nodeType == 1 && result.childNodes.length && !up)) {
					finished = true;
				}
			} while ((resultIgnored || ignoredParent) && result !== document && result);
			return result;
		}
		return next;
	}

	function addEvent(elem, type, fn) {
		if (elem.addEventListener) {
			elem.addEventListener(type, fn, false);
		} else if (elem.attachEvent) {
			elem.attachEvent('on' + type, fn);
		}
	}

	if (window.addEventListener) {
		window.addEventListener(
			'load', 
			()=>{
				if (!window.hasOwnProperty('selection_loaded')) {
					Selection.instance = new Selection({ 'selectable': document });
					window.selection_loaded = true;
				}
			},
			false);
	}

	exports.Selection=Selection;
	exports.SelectionRange=SelectionRange;
	exports.get_selection = function() {
		var srange = Selection.instance.getSelection();
		return srange;
	};

	exports.set_selection = function(range) {
		Selection.instance.setSelection(range);
	};

	exports.get_selection_instance = function(){
		return Selection.instance;
	}

	return exports;

})();
