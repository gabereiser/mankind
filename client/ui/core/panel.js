import { UIVisual } from "./visual.js";

class UIPanel extends UIVisual {
	constructor(x, y, width, height) {
		super();
		this.x = x;
		this.y = y;
		this.width = width;
		this.height = height;
		this.visual.className = "ui-panel";
		resize();
	}

	resize() {
		this.visual.clientLeft = this.x;
		this.visual.clientTop = this.y;
		this.visual.clientWidth = this.width;
		this.visual.clientHeight = this.height;
	}

}