// troca login / register
const btnLogin = document.getElementById('btn-login');
const btnRegister = document.getElementById('btn-register');
const forms = document.querySelector('.forms');

btnRegister.addEventListener('click', () => {
    forms.style.transform = 'translateX(-50%)';
    btnRegister.classList.add('active');
    btnLogin.classList.remove('active');
});

btnLogin.addEventListener('click', () => {
    forms.style.transform = 'translateX(0)';
    btnLogin.classList.add('active');
    btnRegister.classList.remove('active');
});

// toggle senha (login)
const senhaInput = document.getElementById('senha');
const toggleBtn = document.querySelector('.toggle-password');

toggleBtn.addEventListener('click', () => {
    const isPassword = senhaInput.type === 'password';
    senhaInput.type = isPassword ? 'text' : 'password';
    toggleBtn.textContent = isPassword ? '🙈' : '👁';
});
