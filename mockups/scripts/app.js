import { TOKEN } from './constants.js';
import { isJwtExpired } from './utils.js';

const token = localStorage.getItem(TOKEN);
const auth = document.querySelector('.header-auth');
const loginBtn = document.querySelector('.login-btn');

if (token) {
	if (!isJwtExpired()) {
		const logoutBtn = document.createElement('button');
		logoutBtn.setAttribute('type', 'button');
		logoutBtn.setAttribute('class', 'btn');
		logoutBtn.textContent = 'Logout';
		logoutBtn.addEventListener('click', (e) => {
			e.preventDefault();

			localStorage.clear(TOKEN);
			window.location.reload();
		});

		loginBtn.remove();
		auth.append(logoutBtn);
	} else {
		localStorage.removeItem(TOKEN);
		alert('You token has expired, please login again.');
	}
}

loginBtn.addEventListener('click', (e) => {
	e.preventDefault();
	window.location = `login.html?redirect=${window.location.href}`;
});
