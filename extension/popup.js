document.addEventListener('DOMContentLoaded', () => {
  const statusIndicator = document.getElementById('status-indicator');
  const statusText = document.getElementById('status-text');
  const toggleBtn = document.getElementById('toggle-btn');
  
  let isActive = true;

  // Load state from storage
  chrome.storage.local.get(['isActive'], (result) => {
    if (result.isActive !== undefined) {
      isActive = result.isActive;
      updateUI();
    }
  });

  toggleBtn.addEventListener('click', () => {
    isActive = !isActive;
    chrome.storage.local.set({ isActive: isActive });
    updateUI();
    
    // Notify background script
    chrome.runtime.sendMessage({ 
      action: "toggleState", 
      state: isActive 
    });
  });

  function updateUI() {
    if (isActive) {
      statusIndicator.classList.remove('inactive');
      statusText.textContent = "Active";
      toggleBtn.textContent = "Deactivate";
      toggleBtn.style.backgroundColor = getComputedStyle(document.documentElement).getPropertyValue('--danger-color');
    } else {
      statusIndicator.classList.add('inactive');
      statusText.textContent = "Inactive";
      toggleBtn.textContent = "Activate";
      toggleBtn.style.backgroundColor = getComputedStyle(document.documentElement).getPropertyValue('--primary-color');
    }
  }
});
