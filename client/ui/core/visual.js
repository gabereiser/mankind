import { Animator } from "./animation.js";

class UIVisual extends Eventable {
	constructor() {
		this.visual = document.createElement("div");
		this.visual.className = "ui-visual";
		this._dirty = false;
	}

	render(parent) {
		this.parent = parent;
		parent.visual.appendChild(this.visual);
	}

	async animate(property, options) {
		options.target = this;
		options.property = property;
		return new Animator(options).animate();
	}

	async update() { }
}