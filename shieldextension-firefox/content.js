console.log("Shield Extension Content Script Loaded");

const url = window.location.href;

chrome.runtime.sendMessage(
  { action: "getCookies", url: window.location.href },
//   (res) => {
//     console.log("Cookie: ",cookies);
//     console.log("Response from backend:", res);
//   }
);