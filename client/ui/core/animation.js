class Animator {
	constructor(options) {
		this.target = options.target;
		this.property = options.property;
		this.startValue = options.startValue || '0';
		this.endValue = options.endValue || '100';
		this.duration = options.duration || 1000; // in milliseconds
		this.easingFunction = options.easingFunction || 'ease';
		this.delay = options.delay || 0;
		this.animation = null;
	}

	animate() {
		return new Promise((resolve) => {
			setTimeout(() => {
				const animationProperties = {};
				animationProperties[this.property] = [this.startValue, this.endValue];

				this.animation = this.target.animate(
					animationProperties,
					{
						duration: this.duration,
						easing: this.easingFunction
					}
				);

				this.animation.onfinish = () => {
					resolve();
				};
			}, this.delay);
		});
	}

	stop() {
		if (this.animation) {
			this.animation.cancel();
			this.animation = null;
		}
	}
}
