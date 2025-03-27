/**
 * 拙园 - 主JavaScript文件
 */

// 等待DOM内容加载完成
document.addEventListener('DOMContentLoaded', () => {
  // 注册Service Worker
  registerServiceWorker();
  
  // 初始化UI组件
  initUI();
  
  // 设置事件监听器
  setupEventListeners();
});

// 注册Service Worker
function registerServiceWorker() {
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js')
      .then(registration => {
        console.log('Service Worker 注册成功，作用域：', registration.scope);
      })
      .catch(error => {
        console.error('Service Worker 注册失败：', error);
      });
  }
}

// 初始化UI组件
function initUI() {
  // 更新导航菜单显示
  updateNavigation();
  
  // 高亮当前导航项
  highlightCurrentNavItem();
  
  // 初始化主题切换
  initThemeToggle();
  
  // 如果存在编辑器，初始化编辑器
  if (document.querySelector('#note-editor')) {
    initNoteEditor();
  }
}

// 更新导航菜单显示
function updateNavigation() {
  const isAuthenticated = !!localStorage.getItem('access_token');
  const authLinks = document.querySelectorAll('.auth-link');
  
  authLinks.forEach(link => {
    const requiresAuth = link.getAttribute('data-auth') === 'true';
    if (requiresAuth === isAuthenticated) {
      link.style.display = '';
    } else {
      link.style.display = 'none';
    }
  });
}

// 设置事件监听器
function setupEventListeners() {
  // 登录表单提交
  const loginForm = document.querySelector('#login-form');
  if (loginForm) {
    loginForm.addEventListener('submit', handleLogin);
  }
  
  // 注册表单提交
  const registerForm = document.querySelector('#register-form');
  if (registerForm) {
    registerForm.addEventListener('submit', handleRegister);
  }
  
  // 笔记创建/编辑表单提交
  const noteForm = document.querySelector('#note-form');
  if (noteForm) {
    noteForm.addEventListener('submit', handleNoteSubmit);
  }
  
  // 笔记删除按钮
  const deleteButtons = document.querySelectorAll('.delete-note-btn');
  deleteButtons.forEach(button => {
    button.addEventListener('click', handleNoteDelete);
  });
  
  // 笔记搜索
  const searchInput = document.querySelector('#note-search');
  if (searchInput) {
    searchInput.addEventListener('input', debounce(handleNoteSearch, 300));
  }
}

// 高亮当前导航项
function highlightCurrentNavItem() {
  const currentPath = window.location.pathname;
  const navLinks = document.querySelectorAll('nav a');
  
  navLinks.forEach(link => {
    if (link.getAttribute('href') === currentPath) {
      link.classList.add('active');
    }
  });
}

// 初始化主题切换
function initThemeToggle() {
  const themeToggleBtn = document.getElementById('theme-toggle');
  const themeToggleBtnAuth = document.getElementById('theme-toggle-auth');
  const buttons = [themeToggleBtn, themeToggleBtnAuth];
  
  // 读取用户设置的主题或系统主题
  const savedTheme = localStorage.getItem('theme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  
  // 设置初始主题
  if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
    document.documentElement.classList.add('dark-theme');
  }
  
  // 监听主题切换
  buttons.forEach(btn => {
    if (btn) {
      btn.addEventListener('click', () => {
        const isDark = document.documentElement.classList.toggle('dark-theme');
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
      });
    }
  });
  
  // 监听系统主题变化
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
    if (!localStorage.getItem('theme')) {
      document.documentElement.classList.toggle('dark-theme', e.matches);
    }
  });
}

// 初始化笔记编辑器
function initNoteEditor() {
  // 可以集成富文本编辑器，如TinyMCE或Quill
  // 这里使用简单的textarea作为示例
  const noteEditor = document.querySelector('#note-editor');
  
  // 添加自动保存功能
  noteEditor.addEventListener('input', debounce(() => {
    const noteContent = noteEditor.value;
    localStorage.setItem('draft-note', noteContent);
  }, 1000));
  
  // 加载草稿
  const savedDraft = localStorage.getItem('draft-note');
  if (savedDraft && noteEditor.value === '') {
    noteEditor.value = savedDraft;
  }
}

// 处理登录表单提交
async function handleLogin(event) {
  event.preventDefault();
  
  const email = document.querySelector('#email').value;
  const password = document.querySelector('#password').value;
  const errorDisplay = document.querySelector('#error-message');
  
  try {
    const response = await fetch('/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        username: email,
        password: password
      })
    });
    
    const data = await response.json();
    
    if (response.ok) {
      // 保存token
      localStorage.setItem('access_token', data.access_token);
      
      // 跳转到主页
      window.location.href = '/';
    } else {
      errorDisplay.textContent = data.detail || '登录失败，请检查邮箱和密码';
      errorDisplay.classList.remove('hidden');
    }
  } catch (error) {
    console.error('登录请求失败:', error);
    errorDisplay.textContent = '登录请求失败，请稍后再试';
    errorDisplay.classList.remove('hidden');
  }
}

// 处理注册表单提交
async function handleRegister(event) {
  event.preventDefault();
  
  const email = document.querySelector('#email').value;
  const username = document.querySelector('#username').value;
  const password = document.querySelector('#password').value;
  const confirmPassword = document.querySelector('#confirm-password').value;
  const errorDisplay = document.querySelector('#error-message');
  
  // 客户端验证
  if (password !== confirmPassword) {
    errorDisplay.textContent = '两次输入的密码不一致';
    errorDisplay.classList.remove('hidden');
    return;
  }
  
  try {
    const response = await fetch('/auth/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email,
        username,
        password
      })
    });
    
    const data = await response.json();
    
    if (response.ok) {
      // 注册成功，跳转到登录页
      window.location.href = '/login?registered=true';
    } else {
      errorDisplay.textContent = data.detail || '注册失败，请稍后再试';
      errorDisplay.classList.remove('hidden');
    }
  } catch (error) {
    console.error('注册请求失败:', error);
    errorDisplay.textContent = '注册请求失败，请稍后再试';
    errorDisplay.classList.remove('hidden');
  }
}

// 处理笔记表单提交
async function handleNoteSubmit(event) {
  event.preventDefault();
  
  const noteId = document.querySelector('#note-id')?.value;
  const title = document.querySelector('#note-title').value;
  const content = document.querySelector('#note-editor').value;
  const errorDisplay = document.querySelector('#error-message');
  const token = localStorage.getItem('access_token');
  
  if (!token) {
    window.location.href = '/login?redirect=' + encodeURIComponent(window.location.pathname);
    return;
  }
  
  // 判断是创建还是更新
  const isUpdate = noteId && noteId !== 'new';
  const url = isUpdate ? `/api/notes/${noteId}` : '/api/notes/';
  const method = isUpdate ? 'PUT' : 'POST';
  
  try {
    const response = await fetch(url, {
      method,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        title,
        content
      })
    });
    
    const data = await response.json();
    
    if (response.ok) {
      // 清除草稿
      localStorage.removeItem('draft-note');
      
      // 跳转到笔记详情页或笔记列表
      window.location.href = isUpdate 
        ? `/notes/${data.id}` 
        : '/';
    } else {
      errorDisplay.textContent = data.detail || '保存笔记失败';
      errorDisplay.classList.remove('hidden');
    }
  } catch (error) {
    console.error('保存笔记请求失败:', error);
    errorDisplay.textContent = '保存请求失败，请稍后再试';
    errorDisplay.classList.remove('hidden');
  }
}

// 处理笔记删除
async function handleNoteDelete(event) {
  const noteId = event.target.dataset.noteId;
  if (!noteId) return;
  
  const confirmDelete = confirm('确定要删除这篇笔记吗？此操作不可撤销。');
  if (!confirmDelete) return;
  
  const token = localStorage.getItem('access_token');
  if (!token) {
    window.location.href = '/login';
    return;
  }
  
  try {
    const response = await fetch(`/api/notes/${noteId}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (response.ok) {
      // 从DOM中移除笔记元素
      const noteElement = event.target.closest('.note-item');
      if (noteElement) {
        noteElement.remove();
      } else {
        // 如果在笔记详情页，则跳转回列表页
        window.location.href = '/';
      }
    } else {
      alert('删除笔记失败，请稍后再试');
    }
  } catch (error) {
    console.error('删除笔记请求失败:', error);
    alert('删除请求失败，请稍后再试');
  }
}

// 处理笔记搜索
function handleNoteSearch(event) {
  const searchTerm = event.target.value.toLowerCase();
  const noteElements = document.querySelectorAll('.note-item');
  
  noteElements.forEach(note => {
    const title = note.querySelector('.note-title').textContent.toLowerCase();
    const content = note.querySelector('.note-preview').textContent.toLowerCase();
    
    if (title.includes(searchTerm) || content.includes(searchTerm)) {
      note.style.display = '';
    } else {
      note.style.display = 'none';
    }
  });
}

// 工具函数：防抖
function debounce(func, wait) {
  let timeout;
  return function(...args) {
    const context = this;
    clearTimeout(timeout);
    timeout = setTimeout(() => func.apply(context, args), wait);
  };
}

// 工具函数：格式化日期
function formatDate(dateString) {
  const date = new Date(dateString);
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  
  return `${year}-${month}-${day}`;
}

// 工具函数：截断文本
function truncateText(text, maxLength = 150) {
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '...';
}

// 工具函数：显示消息提示
function showMessage(message, type = 'info') {
  const messageContainer = document.getElementById('message-container');
  if (!messageContainer) return;
  
  const messageElement = document.createElement('div');
  messageElement.className = `alert alert-${type}`;
  messageElement.textContent = message;
  
  messageContainer.appendChild(messageElement);
  
  // 3秒后自动移除
  setTimeout(() => {
    messageElement.style.opacity = '0';
    setTimeout(() => messageElement.remove(), 300);
  }, 3000);
}

// 工具函数：从URL获取查询参数
function getQueryParam(param) {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get(param);
}

// 检查URL参数，显示相应消息
function checkURLMessages() {
  const registered = getQueryParam('registered');
  const loggedOut = getQueryParam('logged_out');
  
  if (registered === 'true') {
    showMessage('注册成功！请使用您的邮箱和密码登录。', 'success');
  }
  
  if (loggedOut === 'true') {
    showMessage('您已成功退出登录。', 'info');
  }
}

// 在页面加载时检查URL消息
checkURLMessages(); 