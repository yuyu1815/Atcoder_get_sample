document.addEventListener('DOMContentLoaded', () => {
  const urlList = document.getElementById('urlList');
  const intervalInput = document.getElementById('interval');
  const saveIntervalButton = document.getElementById('saveInterval');

  chrome.storage.local.get({ urls: [], interval: 3 }, (result) => {
      const urls = result.urls;
      intervalInput.value = result.interval;

      urls.forEach((url) => {
          const li = document.createElement('li');
          li.textContent = url[0] || 'URLが不明です';
          if (url[1]) { // url[1]が存在する場合
              li.style.color = 'green';
          }
          urlList.appendChild(li);
      });
  });

  saveIntervalButton.addEventListener('click', () => {
      const interval = parseInt(intervalInput.value, 10);
      if (interval >= 1) {
          chrome.storage.local.set({ interval: interval }, () => {
              alert('保存間隔が設定されました。');
          });
      } else {
          alert('間隔は1秒以上に設定してください。');
      }
  });
});