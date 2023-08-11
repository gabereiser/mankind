
class Router {
	constructor() {
		this.routes = {};
		this.currentRoute = null;

		// Bind the 'popstate' event to handle back/forward navigation
		window.addEventListener('popstate', this.handlePopState.bind(this));
	}

	register(route, callback) {
		if (route.includes(':')) {
			const routePattern = new RegExp('^' + route.replace(/:[^\s/]+/g, '([\\w-]+)') + '$');
			this.routes[routePattern] = { callback, keys: this.extractKeys(route) };
		} else {
			this.routes[route] = { callback };
		}
	}

	navigateTo(route) {
		for (const pattern of Object.keys(this.routes)) {
			const match = route.match(pattern);
			if (match) {
				const { callback, keys } = this.routes[pattern];
				const params = this.extractParams(match, keys);
				this.currentRoute = route;
				callback(params);
				window.history.pushState({ route }, '', route);
				return;
			}
		}
		console.error(`Route '${route}' not found`);
	}

	handlePopState(event) {
		const route = event.state.route;
		if (route) {
			this.navigateTo(route);
		}
	}

	extractKeys(route) {
		return route.match(/:([^/]+)/g).map(key => key.slice(1));
	}

	extractParams(match, keys) {
		const params = {};
		keys.forEach((key, index) => {
			params[key] = match[index + 1];
		});
		return params;
	}

	bind() {
		let routes = Array.from(document.querySelectorAll('[router-link]'));
		routes.forEach(route => {
			route.addEventListener('click', navigate, false)
		});
		this.handlePopState({ state: { route: window.location.pathname } });
	}
}