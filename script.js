document.addEventListener('DOMContentLoaded', function() {
  const loginForm = document.getElementById('loginForm');
  const supportBtn = document.getElementById('supportBtn');
  const usernameInput = document.getElementById('username');
  const passwordInput = document.getElementById('password');

  loginForm.addEventListener('submit', async function(e) { // Added 'async'
    e.preventDefault();
    
    const username = usernameInput.value.trim();
    const password = passwordInput.value.trim();

    if (!username || !password) {
      showMessage('Please fill in all fields', 'error');
      return;
    }

    if (username.length < 3) {
      showMessage('Username must be at least 3 characters long', 'error');
      return;
    }

    if (password.length < 6) {
      showMessage('Password must be at least 6 characters long', 'error');
      return;
    }

    showMessage('Signing up...', 'info');

    try {
      const response = await fetch('/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();

      if (response.ok) {
        showMessage(data.message, 'success');
        // window.location.href = '/dashboard';
      } else {
        showMessage(data.message, 'error');
      }
    } catch (error) {
      console.error('Error during login:', error);
      showMessage('An error occurred during login. Please try again.', 'error');
    }
  });

  supportBtn.addEventListener('click', function() {
    showMessage('Support request submitted. We will contact you soon.', 'info');
  });

  [usernameInput, passwordInput].forEach(input => {
    input.addEventListener('focus', function() {
    });

    input.addEventListener('blur', function() {
    });
  });

  function showMessage(message, type) {
    const existingMessage = document.querySelector('.message-toast');
    if (existingMessage) {
      existingMessage.remove();
    }

    const messageEl = document.createElement('div');
    messageEl.className = `message-toast fixed top-4 left-1/2 transform -translate-x-1/2 px-6 py-3 rounded-lg text-white font-medium z-50 transition-all duration-300`;
    
    switch(type) {
      case 'success':
        messageEl.classList.add('bg-green-500');
        break;
      case 'error':
        messageEl.classList.add('bg-red-500');
        break;
      case 'info':
        messageEl.classList.add('bg-blue-500');
        break;
      default:
        messageEl.classList.add('bg-gray-500');
    }

    messageEl.textContent = message;
    document.body.appendChild(messageEl);

    setTimeout(() => {
      messageEl.style.opacity = '1';
      messageEl.style.transform = 'translateX(-50%) translateY(0)';
    }, 100);

    setTimeout(() => {
      messageEl.style.opacity = '0';
      messageEl.style.transform = 'translateX(-50%) translateY(-20px)';
      setTimeout(() => {
        if (messageEl.parentNode) {
          messageEl.remove();
        }
      }, 300);
    }, 3000);
  }

  const formElements = document.querySelectorAll('input, button');
  formElements.forEach(element => {
    element.addEventListener('mouseenter', function() {
      this.style.transform = 'translateY(-1px)';
    });

    element.addEventListener('mouseleave', function() {
      this.style.transform = 'translateY(0)';
    });
  });

  const logo = document.querySelector('img[alt="LuxBeauty Lab Logo"]');
  if (logo) {
    logo.style.opacity = '0';
    logo.style.transform = 'scale(0.8)';
    
    setTimeout(() => {
      logo.style.transition = 'all 0.8s ease-out';
      logo.style.opacity = '1';
      logo.style.transform = 'scale(1)';
    }, 300);
  }
});

window.addEventListener('resize', function() {
  const isMobile = window.innerWidth < 1024;
  const mainContainer = document.querySelector('main > div');
  
  if (isMobile) {
    mainContainer.classList.remove('grid-cols-2');
    mainContainer.classList.add('grid-cols-1');
  } else {
    mainContainer.classList.remove('grid-cols-1');
    mainContainer.classList.add('lg:grid-cols-2');
  }
});