"use strict";

window.browserviewscripts.selection = (function () {

	var funcs = {

		blocks: {},
		captureCount: 0,

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
				span.className='browserviewscript selection-index' + idx;
				span.setAttribute('rel', idx);
				child.parentNode.insertBefore(span, child);
			}
		},

		get_selection: function(){
			this.enumerate(document.body);
			alert(Object.keys(this.blocks).length);
			return this.blocks.length;
		},

		// set_selection: function(data){},
	}

	return funcs;

})();
