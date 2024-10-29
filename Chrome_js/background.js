

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
          });
      });
  }, intervalInSeconds * 1000);
}

chrome.storage.onChanged.addListener((changes, areaName) => {
  if (areaName === 'local' && changes.interval) {
      intervalInSeconds = changes.interval.newValue;
      startInterval(); // インターバルを再設定
  }
});
