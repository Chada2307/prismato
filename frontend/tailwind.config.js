/** @type {import('tailwindcss').Config} */
export default {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {
			colors: {
				'main-bg': '#f7fff7',
				'dark-text': '#343434',
				brand: {
					DEFAULT: '#489fb5',
					light: '#6dbbc8'
				},
				danger: '#da3e52',
				warning: '#ffa62b'
			},
			fontFamily: {
				inter: ['Inter', 'sans-serif']
			},
			borderRadius: {
				prismato: '12px'
			}
		}
	},
	plugins: []
};
