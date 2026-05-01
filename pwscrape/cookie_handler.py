# cookie_handler.py
import logging
def get_cookiebot_handling_methods():
    """
    Returns a list of Playwright page methods to handle different CookieBot button interactions.
    """
    logging.info("Accessing cookiebot handling methods from cookie_handler.py")

    return [
        # Attempt to click the "Allow All" button by ID
        {
            "method": "evaluate",
            "args": ["document.getElementById('CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll')?.click();"]
        },
        # Attempt to click the "OK" button by ID
        {
            "method": "evaluate",
            "args": ["document.getElementById('CybotCookiebotDialogBodyLevelButtonAccept')?.click();"]
        },
        # Try clicking any button with class that has "OK" text
        {
            "method": "evaluate",
            "args": ["""
                Array.from(document.querySelectorAll('button.CybotCookiebotDialogBodyButton'))
                .filter(btn => btn.innerText.trim().toLowerCase() === 'ok')[0]?.click();
            """]
        },
        # Scroll the button into view in case it's hidden or out of focus
        {
            "method": "evaluate",
            "args": ["""
                const btn = document.getElementById('CybotCookiebotDialogBodyLevelButtonAccept');
                if (btn) btn.scrollIntoView({ behavior: 'smooth', block: 'center' });
            """]
        },
        # Wait a little to make sure the button click has time to take effect
        {
            "method": "wait_for_timeout",
            "args": [2000]  # Wait 2 seconds to ensure the pop-up disappears
        }
    ]


