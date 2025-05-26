// Form validation and interaction handling
document.addEventListener('DOMContentLoaded', function() {
  const loginForm = document.getElementById('loginForm');
  const supportBtn = document.getElementById('supportBtn');
  const usernameInput = document.getElementById('username');
  const passwordInput = document.getElementById('password');

  // Form submission handler
  loginForm.addEventListener('submit', function(e) {
    e.preventDefault();
    
    const username = usernameInput.value.trim();
    const password = passwordInput.value.trim();

    // Basic validation
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

    // Simulate login process
    showMessage('Signing up...', 'info');
    
    setTimeout(() => {
      showMessage('Welcome to LuxBeauty Lab! Registration successful.', 'success');
      // Here you would typically redirect to the dashboard
      // window.location.href = '/dashboard';
    }, 1500);
  });

  // Support button handler
  supportBtn.addEventListener('click', function() {
    showMessage('Support request submitted. We will contact you soon.', 'info');
  });

  // Input focus effects
  [usernameInput, passwordInput].forEach(input => {
    input.addEventListener('focus', function() {
      this.parentElement.classList.add('ring-2', 'ring-blue-500');
    });

    input.addEventListener('blur', function() {
      this.parentElement.classList.remove('ring-2', 'ring-blue-500');
    });
  });

  // Show message function
  function showMessage(message, type) {
    // Remove existing messages
    const existingMessage = document.querySelector('.message-toast');
    if (existingMessage) {
      existingMessage.remove();
    }

    // Create message element
    const messageEl = document.createElement('div');
    messageEl.className = `message-toast fixed top-4 left-1/2 transform -translate-x-1/2 px-6 py-3 rounded-lg text-white font-medium z-50 transition-all duration-300`;
    
    // Set color based on type
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

    // Animate in
    setTimeout(() => {
      messageEl.style.opacity = '1';
      messageEl.style.transform = 'translateX(-50%) translateY(0)';
    }, 100);

    // Remove after 3 seconds
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

  // Add smooth animations to form elements
  const formElements = document.querySelectorAll('input, button');
  formElements.forEach(element => {
    element.addEventListener('mouseenter', function() {
      this.style.transform = 'translateY(-1px)';
    });

    element.addEventListener('mouseleave', function() {
      this.style.transform = 'translateY(0)';
    });
  });

  // Logo animation on page load
  const logo = document.querySelector('svg');
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

// Responsive behavior
window.addEventListener('resize', function() {
  // Adjust layout for mobile devices
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
