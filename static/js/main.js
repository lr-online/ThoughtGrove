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
  
  // 初始化移动端导航
  initMobileNav();
  
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

// 初始化移动端导航
function initMobileNav() {
  const menuToggle = document.querySelector('#menu-toggle');
  const mobileMenu = document.querySelector('#mobile-menu');
  
  if (!menuToggle || !mobileMenu) return;
  
  menuToggle.addEventListener('click', () => {
    mobileMenu.classList.toggle('hidden');
    document.body.classList.toggle('overflow-hidden');
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
      const data = await response.json();
      alert(data.detail || '删除笔记失败');
    }
  } catch (error) {
    console.error('删除笔记请求失败:', error);
    alert('删除请求失败，请稍后再试');
  }
}

// 处理笔记搜索
function handleNoteSearch(event) {
  const searchTerm = event.target.value.toLowerCase();
  const noteCards = document.querySelectorAll('.note-card');
  
  noteCards.forEach(card => {
    const title = card.querySelector('.note-title').textContent.toLowerCase();
    const content = card.querySelector('.note-excerpt').textContent.toLowerCase();
    
    if (title.includes(searchTerm) || content.includes(searchTerm)) {
      card.style.display = 'block';
    } else {
      card.style.display = 'none';
    }
  });
}

// 防抖函数
function debounce(func, wait) {
  let timeout;
  return function(...args) {
    clearTimeout(timeout);
    timeout = setTimeout(() => func.apply(this, args), wait);
  };
}

// API请求工具
const api = {
  baseUrl: '/api',
  
  async request(endpoint, options = {}) {
    const url = this.baseUrl + endpoint;
    
    // 默认配置
    const defaultOptions = {
      headers: {
        'Content-Type': 'application/json',
      },
    };
    
    // 合并选项
    const requestOptions = { ...defaultOptions, ...options };
    
    // 添加身份验证令牌（如果存在）
    const token = localStorage.getItem('authToken');
    if (token) {
      requestOptions.headers['Authorization'] = `Bearer ${token}`;
    }
    
    try {
      const response = await fetch(url, requestOptions);
      
      // 处理未授权错误
      if (response.status === 401) {
        // 清除令牌并重定向到登录页面
        localStorage.removeItem('authToken');
        window.location.href = '/login';
        return null;
      }
      
      // 解析响应
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.detail || '请求失败');
      }
      
      return data;
    } catch (error) {
      console.error('API请求错误:', error);
      showToast(error.message || '请求失败，请稍后重试', 'error');
      return null;
    }
  },
  
  // GET请求
  get(endpoint) {
    return this.request(endpoint, { method: 'GET' });
  },
  
  // POST请求
  post(endpoint, data) {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },
  
  // PUT请求
  put(endpoint, data) {
    return this.request(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  },
  
  // DELETE请求
  delete(endpoint) {
    return this.request(endpoint, { method: 'DELETE' });
  },
};

// 身份验证功能
const auth = {
  // 用户注册
  async register(userData) {
    const result = await api.post('/auth/register', userData);
    
    if (result) {
      showToast('注册成功，请登录', 'success');
      return true;
    }
    
    return false;
  },
  
  // 用户登录
  async login(credentials) {
    try {
      const response = await fetch('/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          username: credentials.email,
          password: credentials.password,
        }),
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.detail || '登录失败');
      }
      
      // 保存令牌
      localStorage.setItem('authToken', data.access_token);
      return true;
    } catch (error) {
      console.error('登录错误:', error);
      showToast(error.message || '登录失败，请检查您的凭据', 'error');
      return false;
    }
  },
  
  // 注销
  logout() {
    localStorage.removeItem('authToken');
    window.location.href = '/login';
  },
  
  // 检查用户是否已认证
  isAuthenticated() {
    return !!localStorage.getItem('authToken');
  },
};

// 笔记功能
const notes = {
  // 获取用户所有笔记
  async getAllNotes() {
    return await api.get('/notes/');
  },
  
  // 获取笔记详情
  async getNote(id) {
    return await api.get(`/notes/${id}`);
  },
  
  // 创建笔记
  async createNote(noteData) {
    return await api.post('/notes/', noteData);
  },
  
  // 更新笔记
  async updateNote(id, noteData) {
    return await api.put(`/notes/${id}`, noteData);
  },
  
  // 删除笔记
  async deleteNote(id) {
    return await api.delete(`/notes/${id}`);
  },
};

// 辅助函数
function showFieldError(field, message) {
  // 清除可能存在的错误
  clearFieldError(field);
  
  // 创建错误消息元素
  const errorElement = document.createElement('div');
  errorElement.className = 'field-error';
  errorElement.textContent = message;
  
  // 添加错误样式到字段
  field.classList.add('has-error');
  
  // 插入错误消息
  field.parentNode.appendChild(errorElement);
}

function clearFieldError(field) {
  field.classList.remove('has-error');
  
  // 删除可能存在的错误消息
  const existingError = field.parentNode.querySelector('.field-error');
  if (existingError) {
    existingError.remove();
  }
}

function isValidEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

function isValidPassword(password) {
  // 至少8个字符，包含大小写字母和数字
  const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/;
  return passwordRegex.test(password);
}

function showToast(message, type = 'info') {
  // 检查是否存在toast容器
  let toastContainer = document.querySelector('.toast-container');
  
  if (!toastContainer) {
    // 创建toast容器
    toastContainer = document.createElement('div');
    toastContainer.className = 'toast-container';
    document.body.appendChild(toastContainer);
  }
  
  // 创建toast元素
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.textContent = message;
  
  // 添加到容器
  toastContainer.appendChild(toast);
  
  // 淡出动画
  setTimeout(() => {
    toast.classList.add('fade-out');
    
    // 移除元素
    setTimeout(() => {
      toast.remove();
    }, 300);
  }, 3000);
}

// 服务工作线程注册 (PWA支持)
if ('serviceWorker' in navigator) {
  window.addEventListener('load', function() {
    navigator.serviceWorker.register('/sw.js').then(function(registration) {
      console.log('ServiceWorker注册成功，范围: ', registration.scope);
    }).catch(function(error) {
      console.log('ServiceWorker注册失败: ', error);
    });
  });
} 