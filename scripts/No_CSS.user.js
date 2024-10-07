// ==UserScript==
// @name        No CSS
// @namespace   Violentmonkey Scripts
// @author      EDM115
// @match       *://*/*
// @grant       GM_setValue
// @grant       GM_getValue
// @grant       GM_registerMenuCommand
// @grant       GM_unregisterMenuCommand
// @run-at      document-end
// @downloadURL https://raw.githubusercontent.com/EDM115/useful-stuff/refs/heads/main/scripts/No_CSS.user.js
// @updateURL   https://raw.githubusercontent.com/EDM115/useful-stuff/refs/heads/main/scripts/No_CSS.meta.js
// @homepageURL https://github.com/EDM115/useful-stuff/blob/main/scripts/No_CSS.user.js
// @supportURL  https://github.com/EDM115/useful-stuff/issues
// @version     1.0
// @icon        https://raw.githubusercontent.com/EDM115/useful-stuff/refs/heads/main/scripts/No_CSS_logo.png
// @description Adds a button to toggle all CSS on the current page. If you ever wanted to break a website design...
// ==/UserScript==

(function() {
    "use strict";

    const defaultSettings = {
        showButton: false
    };

    // Retrieve the current setting or use default
    let button;
    let showButton = GM_getValue("showButton", defaultSettings.showButton);

    // Function to save the current setting
    function saveSetting(setting, value) {
        GM_setValue(setting, value);
    }

    // Function to create the button
    function createButton() {
        button = document.createElement("button");
        button.innerText = "Toggle CSS";
        button.style.position = "fixed";
        button.style.top = "10px";
        button.style.right = "10px";
        button.style.zIndex = "9999";
        button.style.padding = "10px 15px";
        button.style.backgroundColor = "#282a36";
        button.style.border = "1px solid #6272a4";
        button.style.color = "#f8f8f2";
        button.style.borderRadius = "12px";
        button.style.cursor = "pointer";
        button.style.boxShadow = "0 4px 6px rgba(0, 0, 0, 0.1)";

        document.body.appendChild(button);

        let stylesDisabled = false;

        button.addEventListener("click", () => {
            if (!stylesDisabled) {
                // Disable all stylesheets
                document.querySelectorAll("link[rel='stylesheet'], style").forEach(styleSheet => {
                    styleSheet.disabled = true;
                });
                stylesDisabled = true;
                button.innerText = "Enable CSS";
            } else {
                // Re-enable all stylesheets
                document.querySelectorAll("link[rel='stylesheet'], style").forEach(styleSheet => {
                    styleSheet.disabled = false;
                });
                stylesDisabled = false;
                button.innerText = "Disable CSS";
            }
        });
    }

    // Function to toggle the display of the button
    function toggleShowButton() {
        showButton = !showButton;
        saveSetting("showButton", showButton);

        if (showButton) {
            createButton();
        } else if (button) {
            button.remove();
        }
    }

    // Add the menu command to toggle button visibility
    GM_registerMenuCommand(showButton ? "Hide CSS Toggle Button" : "Show CSS Toggle Button", toggleShowButton);

    // Initially add the button if the setting is enabled
    if (showButton) {
        createButton();
    }
})();
