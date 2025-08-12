import { TOKEN } from './constants.js';

if (localStorage.getItem(TOKEN)) window.location = 'home.html';

document.getElementById('login-form').addEventListener('submit', async (event) => {
	event.preventDefault();
	// Your code to handle form submission

	const email = document.getElementById('email').value;
	const password = document.getElementById('password').value;

	try {
		await loginUser(email, password);
	} catch (err) {
		console.error('Login error:', err);
		alert('Wrong credentials.');
	}
});

async function loginUser(email, password) {
	const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({ email, password })
	});
	// Handle the response
	const data = await response.json();

	if (response.ok) {
		//store JWT securely in localStorage
		localStorage.setItem(TOKEN, data.access_token);
		const redirect = new URL(window.location.href).searchParams.get('redirect');
		if (redirect) {
			window.location = redirect;
			return;
		}

		window.location.href = 'home.html';
	} else {
		alert('Login failed: ' + (data.error || response.statusText));
	}
}
