let intervalInSeconds = 3;
let intervalId;

chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.local.set({ interval: 3, urls: [] }); // デフォルト3秒と空のURLリスト
  startInterval();
});
chrome.runtime.onStartup.addListener(() => {
  chrome.storage.local.set({ interval: 3, urls: [] });
  startInterval();
});

function startInterval() {
  if (intervalId) {
    clearInterval(intervalId);
  }

  intervalId = setInterval(() => {
    chrome.tabs.query({ url: "*://*.atcoder.jp/*" }, (tabs) => {
      let urlsWithStatus = [];

      tabs.forEach(tab => {
        urlsWithStatus.push([tab.url, tab.active]);
      });

      chrome.storage.local.set({ urls: urlsWithStatus }, () => {
        console.log("URLs with status saved:", urlsWithStatus);
        sendDataToServer(urlsWithStatus);
      });
    });
  }, intervalInSeconds * 1000);
}

function sendDataToServer(data) {
  console.log("OK")
  fetch('http://localhost:5000/receive_data', {
    method: 'HEAD' // サーバーの状態を確認するためにHEADリクエストを使用
  })
  .then(() => {
    // サーバーがオンラインの場合のみデータを送信
    return fetch('http://localhost:5000/receive_data', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    });
  })
  .then(response => response.json())
  .then(data => console.log('Data sent successfully:', data))
  .catch((error) => console.error('Error sending data:', error));
}

chrome.storage.onChanged.addListener((changes, areaName) => {
  if (areaName === 'local' && changes.interval) {
    intervalInSeconds = changes.interval.newValue;
    startInterval(); // インターバルを再設定
  }
});
