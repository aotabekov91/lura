"use strict";

window.browserviewscripts.normal = (function() {
    const funcs = {};

    funcs.current_position = () => {
        let x_px = window.scrollX;
        let y_px = window.scrollY;

        const width = Math.max(
            document.body.scrollWidth,
            document.body.offsetWidth,
            document.documentElement.scrollWidth,
            document.documentElement.offsetWidth
        );
        const height = Math.max(
            document.body.scrollHeight,
            document.body.offsetHeight,
            document.documentElement.scrollHeight,
            document.documentElement.offsetHeight
        );

		return {"x": x_px / width, "y": y_px / height};
	};

	funcs.set_current_position = (x, y) => {
        const width = Math.max(
            document.body.scrollWidth,
            document.body.offsetWidth,
            document.documentElement.scrollWidth,
            document.documentElement.offsetWidth
        );
        const height = Math.max(
            document.body.scrollHeight,
            document.body.offsetHeight,
            document.documentElement.scrollHeight,
            document.documentElement.offsetHeight
        );
		window.scroll(x*width, y*height);
	};

    return funcs;
})();
