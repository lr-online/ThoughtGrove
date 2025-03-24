/**
 * 拙园 - Service Worker
 */

// 缓存名称 - 更新版本号会清除旧缓存
const CACHE_NAME = 'thoughtgrove-v1';

// 需要缓存的资源 - 仅保留基本UI资源，不缓存页面内容
const RESOURCES_TO_CACHE = [
  '/static/css/styles.css',
  '/static/js/main.js',
  '/static/icons/favicon.ico',
  '/static/icons/icon-192x192.png',
  '/static/icons/icon-512x512.png',
  '/manifest.json'
];

// 安装事件 - 预缓存资源
self.addEventListener('install', event => {
  console.log('Service Worker: 安装中');
  
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Service Worker: 开始缓存资源');
        return cache.addAll(RESOURCES_TO_CACHE);
      })
      .then(() => {
        console.log('Service Worker: 资源缓存完成');
        return self.skipWaiting();
      })
  );
});

// 激活事件 - 清理旧缓存
self.addEventListener('activate', event => {
  console.log('Service Worker: 激活中');
  
  event.waitUntil(
    caches.keys()
      .then(cacheNames => {
        return Promise.all(
          cacheNames
            .filter(cacheName => cacheName !== CACHE_NAME)
            .map(cacheName => {
              console.log('Service Worker: 清除旧缓存', cacheName);
              return caches.delete(cacheName);
            })
        );
      })
      .then(() => {
        console.log('Service Worker: 现在控制客户端');
        return self.clients.claim();
      })
  );
});

// 请求拦截策略 - 简化版，仅缓存静态资源，不处理离线
self.addEventListener('fetch', event => {
  // 忽略非GET请求
  if (event.request.method !== 'GET') return;
  
  // 忽略API请求和HTML页面
  if (event.request.url.includes('/api/')) return;
  if (event.request.url.includes('/auth/')) return;
  if (event.request.headers.get('accept').includes('text/html')) return;
  
  // 只处理静态资源
  if (event.request.url.includes('/static/')) {
    event.respondWith(
      caches.match(event.request)
        .then(cachedResponse => {
          // 如果存在缓存，返回缓存的资源
          if (cachedResponse) {
            return cachedResponse;
          }
          
          // 否则请求网络
          return fetch(event.request)
            .then(response => {
              // 确保响应有效
              if (!response || response.status !== 200 || response.type !== 'basic') {
                return response;
              }
              
              // 克隆响应，因为响应流只能使用一次
              const responseToCache = response.clone();
              
              // 缓存网络响应
              caches.open(CACHE_NAME)
                .then(cache => {
                  cache.put(event.request, responseToCache);
                });
              
              return response;
            });
        })
    );
  }
});

// 推送通知事件
self.addEventListener('push', event => {
  if (!event.data) return;
  
  const notification = event.data.json();
  
  self.registration.showNotification('拙园', {
    body: notification.message,
    icon: '/static/icons/icon-192x192.png',
    badge: '/static/icons/badge-72x72.png',
    data: {
      url: notification.url || '/'
    }
  });
});

// 点击通知事件
self.addEventListener('notificationclick', event => {
  event.notification.close();
  
  if (event.notification.data && event.notification.data.url) {
    event.waitUntil(
      clients.openWindow(event.notification.data.url)
    );
  }
}); 