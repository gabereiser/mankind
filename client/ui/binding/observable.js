import { Eventable } from "./eventable.js";

class Observable extends Eventable {
	constructor(element, value) {
		super();
		this.value = value;
		this.element = element;
		this.listeners = {};
		Object.defineProperty(property, 'value', {
			get: function () {
				return this.value;
			},
			set: function (value) {
				if (this.value !== value) {
					this.emit('changed', {
						sender: this,
						value: value
					});
				}
				this.value = value;
				element.value = value;
			}
		});
	}
}