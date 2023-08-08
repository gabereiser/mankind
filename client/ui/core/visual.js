
class UIVisual {
	constructor() {
		this.visual = document.createElement("div");
		this.visual.className = "ui-visual";
		this._dirty = false;
	}

	render(parent) {
		this.parent = parent;
		parent.visual.appendChild(this.visual);
	}
}