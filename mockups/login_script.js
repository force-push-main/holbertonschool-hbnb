document.addEventListener('DOMContentLoaded', () => {
      const loginForm = document.getElementById('login-form');

      if (loginForm) {
          loginForm.addEventListener('submit', async (event) => {
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
        localStorage.setItem('access_token', data.access_token);
          
        window.location.href = 'home.html';
      } else {
          alert('Login failed: ' + (data.error || response.statusText));
      }
  }
