// Font Sizer Control
let currentFontSizeStep = 0;
const baseFontSize = 14;

function changeFontSize(step) {
    if (step === 0) {
        currentFontSizeStep = 0;
    } else {
        currentFontSizeStep = Math.max(-2, Math.min(3, currentFontSizeStep + step));
    }
    document.documentElement.style.setProperty('--base-font-size', (baseFontSize + currentFontSizeStep * 1.5) + 'px');
}

// Language Switcher (English / Hindi / Telugu)
const langOrder = ['en', 'hi', 'te'];
let currentLangIndex = 0;

const i18n = {
    en: {
        nextLangText: 'हिंदी',
        title: 'PolicyGPT <span>Portal</span>',
        subtitle: 'Government Policy & Public Scheme Intelligence Platform',
        breadcrumb: 'Citizen Access Portal',
        infoTitle: 'Welcome to PolicyGPT Portal',
        infoDesc: 'Access unified information on Central & State Government Welfare Schemes, eligibility rules, and policy insights powered by AI.',
        loginTab: '🔑 Sign In',
        registerTab: '📝 Register'
    },
    hi: {
        nextLangText: 'తెలుగు',
        title: 'नीतिजीपीटी <span>| PolicyGPT</span>',
        subtitle: 'सरकारी नीति और सार्वजनिक योजना बुद्धिमत्ता मंच',
        breadcrumb: 'नागरिक पहुंच पोर्टल',
        infoTitle: 'नीतिजीपीटी पोर्टल में आपका स्वागत है',
        infoDesc: 'एआई द्वारा संचालित केंद्रीय और राज्य सरकारी कल्याणकारी योजनाओं, पात्रता नियमों और नीतिगत जानकारियों तक पहुंच प्राप्त करें।',
        loginTab: '🔑 साइन इन (Login)',
        registerTab: '📝 पंजीकरण (Register)'
    },
    te: {
        nextLangText: 'English',
        title: 'పాలసీజీపీటీ <span>| PolicyGPT</span>',
        subtitle: 'ప్రభుత్వ పాలసీ & ప్రజా సంక్షేమ పథకాల సమాచార వేదిక',
        breadcrumb: 'పౌర ప్రవేశ పోర్టల్',
        infoTitle: 'పాలసీజీపీటీ పోర్టల్‌కు స్వాగతం',
        infoDesc: 'కేంద్ర మరియు రాష్ట్ర ప్రభుత్వ సంక్షేమ పథకాలు, అర్హత నిబంధనలు మరియు ఏఐ ఆధారిత పాలసీ వివరాలను పొందుపరచండి.',
        loginTab: '🔑 లాగిన్ (Login)',
        registerTab: '📝 రిజిస్ట్రేషన్ (Register)'
    }
};

function toggleLanguage() {
    currentLangIndex = (currentLangIndex + 1) % langOrder.length;
    const langKey = langOrder[currentLangIndex];
    const langData = i18n[langKey];
    
    document.getElementById('lang-btn').innerText = langData.nextLangText;
    document.getElementById('txt-title').innerHTML = langData.title;
    document.getElementById('txt-subtitle').innerText = langData.subtitle;
    document.getElementById('txt-breadcrumb').innerText = langData.breadcrumb;
    document.getElementById('txt-info-title').innerText = langData.infoTitle;
    document.getElementById('txt-info-desc').innerText = langData.infoDesc;
    document.getElementById('tab-login').innerHTML = langData.loginTab;
    document.getElementById('tab-register').innerHTML = langData.registerTab;
}

// Tab Switching
function switchTab(mode) {
    const tabLogin = document.getElementById('tab-login');
    const tabRegister = document.getElementById('tab-register');
    const formLogin = document.getElementById('login-form');
    const formRegister = document.getElementById('register-form');
    
    if (mode === 'login') {
        tabLogin.classList.add('active');
        tabRegister.classList.remove('active');
        formLogin.classList.add('active');
        formRegister.classList.remove('active');
        window.history.pushState({}, '', '/login');
    } else {
        tabLogin.classList.remove('active');
        tabRegister.classList.add('active');
        formLogin.classList.remove('active');
        formRegister.classList.add('active');
        window.history.pushState({}, '', '/register');
    }
}

// Initial Tab Setup
window.addEventListener('DOMContentLoaded', () => {
    const path = window.location.pathname;
    if (path.includes('/register')) {
        switchTab('register');
    } else {
        switchTab('login');
    }
});

// Toast System
function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    let icon = 'ℹ️';
    if (type === 'success') icon = '✅';
    if (type === 'error') icon = '❌';
    
    toast.innerHTML = `<span>${icon}</span><span>${message}</span>`;
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transition = 'opacity 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

// API Login Handler
async function handleLogin(event) {
    event.preventDefault();
    
    const email = document.getElementById('login-email').value.trim();
    const password = document.getElementById('login-password').value;
    const submitBtn = document.getElementById('login-submit-btn');
    
    submitBtn.classList.add('loading');
    submitBtn.disabled = true;
    
    try {
        const response = await fetch('/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Authentication failed. Please verify credentials.');
        }
        
        localStorage.setItem('access_token', data.access_token);
        localStorage.setItem('token_type', data.token_type);
        
        showToast('Login Successful! Redirecting to Portal...', 'success');
        
        setTimeout(() => {
            window.location.href = '/';
        }, 1200);
        
    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        submitBtn.classList.remove('loading');
        submitBtn.disabled = false;
    }
}

// API Register Handler
async function handleRegister(event) {
    event.preventDefault();
    
    const name = document.getElementById('register-name').value.trim();
    const email = document.getElementById('register-email').value.trim();
    const password = document.getElementById('register-password').value;
    const submitBtn = document.getElementById('register-submit-btn');
    
    if (password.length < 8) {
        showToast('Password must be at least 8 characters long.', 'error');
        return;
    }
    
    submitBtn.classList.add('loading');
    submitBtn.disabled = true;
    
    try {
        const response = await fetch('/auth/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ full_name: name, email: email, password: password })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Registration failed. Email may already be registered.');
        }
        
        showToast('Registration Successful! Please Sign In.', 'success');
        
        setTimeout(() => {
            switchTab('login');
            document.getElementById('login-email').value = email;
            document.getElementById('register-name').value = '';
            document.getElementById('register-email').value = '';
            document.getElementById('register-password').value = '';
        }, 1200);
        
    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        submitBtn.classList.remove('loading');
        submitBtn.disabled = false;
    }
}
