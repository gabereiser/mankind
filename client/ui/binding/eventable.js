class Eventable {

	constructor() {
		this.listeners = {};
	}

	addEventListener(name, callback) {
		if (this.listeners[name] !== null) {
			this.listeners[name].push(callback);
		} else {
			this.listeners[name] = [];
			this.listeners[name].push(callback);
		}
	}

	removeEventListener(name, callback) {
		if (this.listeners[name] !== null) {
			const array = this.listeners[name];
			const index = array.indexOf(callback);
			if (index > -1) {
				array.splice(index, 1);
			}
		}
	}

	emit(name, event) {
		if (this.listeners[name] !== null) {
			const array = this.listeners[name];
			for (const callback in array) {
				callback(event);
			}
		}
	}
}