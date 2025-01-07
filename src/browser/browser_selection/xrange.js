"use strict";

window.browserviewscripts.xrange = (function() {

	const funcs = {};

	// get-document.js
	
	// defined by w3c
	var DOCUMENT_NODE = 9;

	function isDocument(d) {
	  return d && d.nodeType === DOCUMENT_NODE;
	};


	funcs.getDocument = (node) => {
	  if (isDocument(node)) {
		return node;

	  } else if (isDocument(node.ownerDocument)) {
		return node.ownerDocument;

	  } else if (isDocument(node.document)) {
		return node.document;

	  } else if (node.parentNode) {
		return getDocument(node.parentNode);

	  // Range support
	  } else if (node.commonAncestorContainer) {
		return getDocument(node.commonAncestorContainer);

	  } else if (node.startContainer) {
		return getDocument(node.startContainer);

	  // Selection support
	  } else if (node.anchorNode) {
		return getDocument(node.anchorNode);
	  }
	};

	// simple-xpath-position
	// dom-exceptions.js

	class DOMException {
	  constructor(message, name) {
		this.message = message
		this.name = name
		this.stack = (new Error()).stack
	  }
	}

	// DOMException.prototype = new Error()

	DOMException.prototype.toString = function () {
	  return `${this.name}: ${this.message}`
	}

	// simple-xpath-position
	// xpath.js 
	
	// https://developer.mozilla.org/en-US/docs/XPathResult
	const FIRST_ORDERED_NODE_TYPE = 9

	// Default namespace for XHTML documents
	const HTML_NAMESPACE = 'http://www.w3.org/1999/xhtml'

	// Get the XPath node name.
	function nodeName(node) {
	  switch (node.nodeName) {
	  case '#text': return 'text()'
	  case '#comment': return 'comment()'
	  case '#cdata-section': return 'cdata-section()'
	  default: return node.nodeName.toLowerCase()
	  }
	}


	// Get the ordinal position of this node among its siblings of the same name.
	function nodePosition(node) {
	  let name = node.nodeName
	  let position = 1
	  while ((node = node.previousSibling)) {
		if (node.nodeName === name) position += 1
	  }
	  return position
	}


	// Find a single node with XPath `path`
	function resolve(path, root, resolver) {
	  try {
		// Add a default value to each path part lacking a prefix.
		let nspath = path.replace(/\/(?!\.)([^\/:\(]+)(?=\/|$)/g, '/_default_:$1')
		return platformResolve(nspath, root, resolver)
	  } catch (err) {
		return fallbackResolve(path, root)
	  }
	}


	// Find a single node with XPath `path` using the simple, built-in evaluator.
	function fallbackResolve(path, root) {
	  let steps = path.split("/")
	  let node = root
	  while (node) {
		let step = steps.shift()
		if (step === undefined) break
		if (step === '.') continue
		let [name, position] = step.split(/[\[\]]/)
		name = name.replace('_default_:', '')
		position = position ? parseInt(position) : 1
		node = findChild(node, name, position)
	  }
	  return node
	}


	// Find a single node with XPath `path` using `document.evaluate`.
	function platformResolve(path, root, resolver) {
	  let document = funcs.getDocument(root)
	  let r = document.evaluate(path, root, resolver, FIRST_ORDERED_NODE_TYPE, null)
	  return r.singleNodeValue
	}


	// Find the child of the given node by name and ordinal position.
	function findChild(node, name, position) {
	  for (node = node.firstChild ; node ; node = node.nextSibling) {
		if (nodeName(node) === name && --position === 0) break
	  }
	  return node
	}


	/**
	 * Compute an XPath expression for the given node.
	 *
	 * If the optional parameter `root` is supplied, the computed XPath expression
	 * will be relative to it. Otherwise, the root element is the root of the
	 * document to which `node` belongs.
	 *
	 * @param {Node} node The node for which to compute an XPath expression.
	 * @param {Node} [root] The root context for the XPath expression.
	 * @returns {string}
	 */
	funcs.fromNode = (node, root = null) => {
	  if (node === undefined) {
		throw new Error('missing required parameter "node"')
	  }

	  root = root || funcs.getDocument(node)

	  let path = '/'
	  while (node !== root) {
		if (!node) {
		  let message = 'The supplied node is not contained by the root node.'
		  let name = 'InvalidNodeTypeError'
		  throw new DOMException(message, name)
		}
		path = `/${nodeName(node)}[${nodePosition(node)}]${path}`
		node = node.parentNode
	  }
	  return path.replace(/\/$/, '')
	};


	/**
	 * Find a node using an XPath relative to the given root node.
	 *
	 * The XPath expressions are evaluated relative to the Node argument `root`.
	 *
	 * If the optional parameter `resolver` is supplied, it will be used to resolve
	 * any namespaces within the XPath.
	 *
	 * @param {string} path An XPath String to evaluate.
	 * @param {Node} root The root context for the XPath expression.
	 * @returns {Node|null} The first matching Node or null if none is found.
	 */
	funcs.toNode = (path, root, resolver = null) => {
	  if (path === undefined) {
		throw new Error('missing required parameter "path"')
	  }
	  if (root === undefined) {
		throw new Error('missing required parameter "root"')
	  }

	  // Make the path relative to the root, if not the document.
	  let document = funcs.getDocument(root)
	  if (root !== document) path = path.replace(/^\//, './')

	  // Make a default resolver.
	  let documentElement = document.documentElement
	  if (resolver === null && documentElement.lookupNamespaceURI) {
		let defaultNS = documentElement.lookupNamespaceURI(null) || HTML_NAMESPACE
		resolver = (prefix) => {
		  let ns = {'_default_': defaultNS}
		  return ns[prefix] || documentElement.lookupNamespaceURI(prefix)
		}
	  }

	  return resolve(path, root, resolver)
	};


	// dom-seek

	const E_END = 'Iterator exhausted before seek ended.'
	const E_SHOW = 'Argument 1 of seek must use filter NodeFilter.SHOW_TEXT.'
	const E_WHERE = 'Argument 2 of seek must be an integer or a Text Node.'

	const DOCUMENT_POSITION_PRECEDING = 2
	const SHOW_TEXT = 4
	const TEXT_NODE = 3

	function isInteger(n) {
	  if (typeof n !== 'number') return false;
	  return isFinite(n) && Math.floor(n) === n;
	}


	function isText(node) {
	  return node.nodeType === TEXT_NODE
	}


	function before(ref, node) {
	  return ref.compareDocumentPosition(node) & DOCUMENT_POSITION_PRECEDING
	}


	funcs.seek = (iter, where) => {
	  if (iter.whatToShow !== SHOW_TEXT) {
		let error

		// istanbul ignore next
		try {
		  error = new DOMException(E_SHOW, 'InvalidStateError')
		} catch {
		  error = new Error(E_SHOW);
		  error.code = 11
		  error.name = 'InvalidStateError'
		  error.toString = () => `InvalidStateError: ${E_SHOW}`
		}

		throw error
	  }

	  let count = 0
	  let node = iter.referenceNode
	  let predicates = null

	  if (isInteger(where)) {
		predicates = {
		  forward: () => count < where,
		  backward: () => count > where || !iter.pointerBeforeReferenceNode,
		}
	  } else if (isText(where)) {
		let forward = before(node, where) ? () => false : () => node !== where
		let backward = () => node !== where || !iter.pointerBeforeReferenceNode
		predicates = {forward, backward}
	  } else {
		throw new TypeError(E_WHERE)
	  }

	  while (predicates.forward()) {
		node = iter.nextNode()

		if (node === null) {
		  throw new RangeError(E_END)
		}

		count += node.nodeValue.length
	  }

	  if (iter.nextNode()) {
		node = iter.previousNode()
	  }

	  while (predicates.backward()) {
		node = iter.previousNode()

		if (node === null) {
		  throw new RangeError(E_END)
		}

		count -= node.nodeValue.length
	  }

	  if (!isText(iter.referenceNode)) {
		throw new RangeError(E_END);
	  }

	  return count
	};

	// xpath-range

	// const SHOW_TEXT = 4


	/**
	 * Convert a `Range` to a pair of XPath expressions and offsets.
	 *
	 * If the optional parameter `root` is supplied, the computed XPath expressions
	 * will be relative to it.
	 *
	 * @param {Range} range The Range to convert.
	 * @param {Node} [root] The root context for the XPath expressions.
	 * @returns {{start, startOffset, end, endOffset}}
	 */
	funcs.fromRange = (range, root) => {
	  let sc = range.startContainer
	  let so = range.startOffset
	  let ec = range.endContainer
	  let eo = range.endOffset

	  let start = funcs.fromNode(sc, root)
	  let end = funcs.fromNode(ec, root)

	  return {
		start: start,
		end: end,
		startOffset: so,
		endOffset: eo,
	  }
	};


	/**
	 * Construct a `Range` from the given XPath expressions and offsets.
	 *
	 * If the optional parameter `root` is supplied, the XPath expressions are
	 * evaluated as relative to it.
	 *
	 * @param {string} startPath An XPath expression for the start container.
	 * @param {Number} startOffset The textual offset within the start container.
	 * @param {string} endPath An XPath expression for the end container.
	 * @param {Number} endOffset The textual offset within the end container.
	 * @param {Node} [root] The root context for the XPath expressions.
	 * @returns Range
	 */
	funcs.toRange = (startPath, startOffset, endPath, endOffset, root) => {
	  let document = funcs.getDocument(root)

	  let sc = funcs.toNode(startPath, root)
	  if (sc === null) throw notFound('start')

	  let si = document.createNodeIterator(sc, SHOW_TEXT)
	  let so = startOffset - funcs.seek(si, startOffset)

	  sc = si.referenceNode
	  if (!si.pointerBeforeReferenceNode) {
		if (so > 0) throw indexSize('start')
		so += sc.length
	  }

	  let ec = funcs.toNode(endPath, root)
	  if (ec === null) throw notFound('end')

	  let ei = document.createNodeIterator(ec, SHOW_TEXT)
	  let eo = endOffset - funcs.seek(ei, endOffset)

	  ec = ei.referenceNode
	  if (!ei.pointerBeforeReferenceNode) {
		if (eo > 0) throw indexSize('end')
		eo += ec.length
	  }

	  let range = document.createRange()
	  range.setStart(sc, so)
	  range.setEnd(ec, eo)

	  return range

	  function notFound(which) {
		let error = new Error(`The ${which} node was not found.`)
		error.name = 'NotFoundError'
		return error
	  }

	  function indexSize(which) {
		let error = new Error(`There is no text at the requested ${which} offset.`)
		error.name = 'IndexSizeError'
		return error
	  }
	};


	return funcs;

})();
