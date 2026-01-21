// Background Service Worker

// Initialize default state on install
chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.local.set({ isActive: true });
  console.log("Shield Extension Installed");
});

// Listen for messages from popup or content scripts
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "toggleState") {
    console.log("State changed to:", request.state);
    // Broadcast state change to all tabs/content scripts if needed
    // This is where you'd trigger global enable/disable logic
  }
});
