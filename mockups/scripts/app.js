import { TOKEN } from './constants.js';

const token = localStorage.getItem(TOKEN);
const auth = document.querySelector('.header-auth');

if (token) {
	const logoutBtn = document.createElement('button');
	logoutBtn.setAttribute('type', 'button');
	logoutBtn.setAttribute('class', 'btn');
	logoutBtn.textContent = 'Logout';
	logoutBtn.addEventListener('click', (e) => {
		e.preventDefault();

		localStorage.clear(TOKEN);
		window.location.reload();
	});

	auth.children[0].remove();
	auth.append(logoutBtn);
}
