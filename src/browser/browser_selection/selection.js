"use strict";

window.browserviewscripts.selection = (function () {

	Range = function(range){
		this.range=range;
		this.startContainer=range.startContainer;
		this.endContainer=range.endContainer;
		this.startOffset=range.startOffset;
		this.endOffset=range.endOffset;
		this.nodes=null;
	}

	Range.prototype.toString = function(){
		return this.range.toString();
	}

	const selection = {

		blocks: {},
		captureCount: 0,
		regex: new RegExp('[^\\s,;:\u2013.!?<>\u2026\\n\u00a0\\*]+', 'ig'),

		getSelection: function(selection){
			selection = selection || window.getSelection();
			if (selection.rangeCount>0){
				var selrange=selection.getRangeAt(0);
				var range=new Range(selrange);
				var srange=this.serializeRange(range);
				return srange;
			}
		},

		setSelection: function(srange){
			var selection=window.getSelection();
			if (selection.rangeCount>0){ selection.removeAllRanges(); }
			var range=this.deserializeRange(srange);
			if (range && range.length){ this.selectRange(range); }
		},

		deserializeRange: function(srange){
			var result=/^([0-9a-zA-Z:]+)(?:,|%2c)([0-9a-zA-Z:]+)$/.exec(srange);
			if (result){
				var start_point=result[1].split(':');
				var end_point=result[2].split(':');
				
			}
			// todo
		},

		selectRange: function(range){
			//
		},

		serializeRange: function(range){
			var start=this.words(range, 'start');
			var end = this.words(range, 'end');
			var sRange = start+','+end;
			return sRange;
		},

		words: function(range, pos){
			var container, offset;
			if (pos==='start'){
				container=range.startContainer;
				offset=range.startOffset;
			} else if (pos==='end'){
				container=range.endContainer;
				offset=range.endOffset;
			}
			var wcount=container.data.substring(0, offset).match(this.regex);
			if (wcount!=null){
				if (pos==='start'){wcount=wcount.length+1;}
				if (pos==='end'){wcount=wcount.length;}
			} else {
				wcount=1;
			}
			var selectionIndex=this.getNum(container);

			// var node=container;
			// var firstNode=this.getFirstTextNode(selectionIndex);

			// while (node && node!=firstNode){
			// 	node=this.prevNode(node, /.*/);
			// 	if (node!=null){
			// 		node=node._container;
			// 		wcount+=this.wordCount(node);
			// 	}
			// }

			return selectionIndex+':'+wcount;
		},

		prevNode: function(cont, regex){
			return _siblingNode(cont, 1, regex);

			function _siblingNode(cont, reversed, regex){
				var node=cont;
				if (reversed && node.previousSibling){
					node=node.previousSibling;
				}
			// todo
			}
		},

		elementIterator: function(parent, cont, end, reversed, isIgnored){
			reversed=!!reversed;
			cont=cont||parent[childKind];
			var finished=!cont;
			var up=false;
			const childKind=reversed?'lastChild':'firstChild';
			const siblingKind=reversed?'previousSibling':'nextSibling';

			function getNext(){
				if (cont.childNodes && cont.childNodes.length && !up){
					cont=cont[childKind];
				} else if (cont[siblingKind]){
					cont=cont[siblingKind];
					up=false;
				} else if (cont.parentNode){
					cont=cont.parentNode;
					if (cont==parent || cont==end){ finished=true; }
					up=true;
					getNext();
				}
			}

			function next(){
				do {
					if (finished) {return null;}
					
					var result=cont;
					getNext();
					alert(result);

					if (result===end && !(result.nodeType==1 && result.childNodes.length && !up)){
						finished=true;
					}
				} while (result!== document && result);
				return result;
			}
			return next;
		},

		getFirstTextNode: function(idx){
			if (!idx) { return null; }
			var class_name='selection-index'+idx;
			var tnode=document.getElementsByClassName(class_name)[0];

			if (tnode){
				var next=tnode['nextSibling'];
				return next;
			}

			// if (tnode){
			// 	var iter=this.elementIterator(document.body, tnode, undefined, false);
			// 	var node=iter();
			// 	alert(node.nodeType);
			// 	while (node){
			// 		if (node.nodeType===3){return node;}
			// 		node=iter();
			// 	}
			// }

			return null;
		},

		getNum: function(container){
			while (container.parentNode){
				while (container.previousSibling){
					container=container.previousSibling;
					while (container.nodeType==1 && container.childNodes.length){
						container = container.lastChild;
					}
					if (container.nodeType==1){
						if (container.classList.contains('selection-index')){
							return container.getAttribute('rel');
						}
					}
				}
				container=container.parentNode;
			}
		},

		getCompiledStyle: function(elem, strCssRule) {
			// copypasted from Internets
			var strValue = '';
			if (document.defaultView && document.defaultView.getComputedStyle) {
				strValue = document.defaultView.getComputedStyle(elem, '').getPropertyValue(strCssRule);
			}
			else if (elem.currentStyle) {
				strCssRule = strCssRule.replace(/\-(\w)/g, function(strMatch, p1) {
					return p1.toUpperCase();
				});
				strValue = elem.currentStyle[strCssRule];
			}
			return strValue;
		},

		isBlock: function(element){
			if (element.nodeName=='BR'){return true;}
			const test=['inline', 'none'];
			const style=this.getCompiledStyle(element, 'display');
			return test.includes('style')==-1;
		},

		enumerate: function(node){
			var children=node.childNodes;
			const regex=new RegExp('[^\\s,;:\u2013.!?<>\u2026\\n\u00a0\\*]+', 'ig');
			for (let idx=0; idx<children.length; ++idx){
				var child=children[idx];
				var nodeType=child.nodeType;
				if (nodeType==3){// && child.nodeValue.match(regex)){
					this.blocks[this.captureCount]=child;
					this.captureCount++;
				}
			}
			for (let [idx, child] of Object.entries(this.blocks)){
				var span=document.createElement('span');
				span.className='selection-index selection-index' + idx;
				span.setAttribute('rel', idx);
				child.parentNode.insertBefore(span, child);
			}
		},

	}

	window.addEventListener('DOMContentLoaded', ()=>selection.enumerate(document.body));
	return selection;

})();


