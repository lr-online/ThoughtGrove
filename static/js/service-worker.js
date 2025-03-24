// Service Worker for 拙园 (ThoughtGrove) PWA
const CACHE_NAME = 'thoughtgrove-cache-v1';

// 需要缓存的资源清单
const CACHE_ASSETS = [
  '/',
  '/offline',
  '/static/css/style.css',
  '/static/js/main.js',
  '/static/js/api.js',
  '/static/images/logo.svg',
  '/static/images/icons/icon-192x192.png',
  '/static/images/icons/icon-512x512.png',
  '/static/manifest.json'
];

// 安装Service Worker时预缓存资源
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('缓存打开成功');
        return cache.addAll(CACHE_ASSETS);
      })
      .then(() => self.skipWaiting())
  );
});

// 激活Service Worker时清理旧缓存
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            console.log('清理旧缓存:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// 拦截网络请求并处理
self.addEventListener('fetch', (event) => {
  // 只处理GET请求
  if (event.request.method !== 'GET') return;
  
  // API请求不缓存，直接使用网络
  if (event.request.url.includes('/api/') || event.request.url.includes('/auth/')) {
    return;
  }
  
  event.respondWith(
    // 尝试从缓存获取
    caches.match(event.request)
      .then((response) => {
        // 如果缓存中有响应，则返回缓存的内容
        if (response) {
          return response;
        }
        
        // 否则尝试从网络获取
        return fetch(event.request)
          .then((networkResponse) => {
            // 检查响应是否有效
            if (!networkResponse || networkResponse.status !== 200 || networkResponse.type !== 'basic') {
              return networkResponse;
            }
            
            // 将网络响应克隆一份，一份返回，一份缓存
            const responseToCache = networkResponse.clone();
            caches.open(CACHE_NAME)
              .then((cache) => {
                cache.put(event.request, responseToCache);
              });
              
            return networkResponse;
          })
          .catch(() => {
            // 网络请求失败，且请求为HTML页面，返回离线页面
            if (event.request.headers.get('Accept').includes('text/html')) {
              return caches.match('/offline');
            }
          });
      })
  );
});

// 后台同步事件处理
self.addEventListener('sync', (event) => {
  if (event.tag === 'sync-notes') {
    event.waitUntil(syncNotes());
  }
});

// 推送通知事件处理
self.addEventListener('push', (event) => {
  if (!event.data) return;
  
  const data = event.data.json();
  const options = {
    body: data.body,
    icon: '/static/images/icons/icon-192x192.png',
    badge: '/static/images/icons/badge-72x72.png',
    data: {
      url: data.url
    }
  };
  
  event.waitUntil(
    self.registration.showNotification('拙园通知', options)
  );
});

// 点击通知事件处理
self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  
  if (event.notification.data && event.notification.data.url) {
    event.waitUntil(
      clients.openWindow(event.notification.data.url)
    );
  }
});

// 笔记同步函数
async function syncNotes() {
  // 从IndexedDB获取未同步的笔记
  const notesToSync = await getNotesToSync();
  
  // 遍历每个笔记并尝试同步
  for (const note of notesToSync) {
    try {
      await syncNote(note);
      await markNoteSynced(note.id);
    } catch (error) {
      console.error('同步笔记失败:', error);
    }
  }
}

// 这些函数需要在实际使用IndexedDB时实现
async function getNotesToSync() {
  // 从IndexedDB获取未同步的笔记
  return [];
}

async function syncNote(note) {
  // 将笔记同步到服务器
}

async function markNoteSynced(noteId) {
  // 标记笔记已同步
} 