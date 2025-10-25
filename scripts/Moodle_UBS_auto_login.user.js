// ==UserScript==
// @name        Moodle UBS auto login
// @namespace   Violentmonkey Scripts
// @author      EDM115
// @match       *://moodle.univ-ubs.fr/*
// @match       *://cas.univ-ubs.fr/*
// @grant       none
// @run-at      document-end
// @downloadURL https://raw.githubusercontent.com/EDM115/useful-stuff/refs/heads/main/scripts/Moodle_UBS_auto_login.user.js
// @updateURL   https://raw.githubusercontent.com/EDM115/useful-stuff/refs/heads/main/scripts/Moodle_UBS_auto_login.meta.js
// @homepageURL https://github.com/EDM115/useful-stuff/blob/main/scripts/Moodle_UBS_auto_login.user.js
// @supportURL  https://github.com/EDM115/useful-stuff/issues
// @version     1.2
// @icon        https://moodle.org/theme/moodleorg/pix/favicons/favicon-270.png
// @description Automatically logs into UBS's Moodle
// ==/UserScript==

(function() {
    "use strict";

    // Helper function to wait for the page to be fully loaded
    function waitForElement(selector, callback, interval = 300, timeout = 10000) {
        const startTime = new Date().getTime();
        const timer = setInterval(function() {
            const element = document.querySelector(selector);
            if (element) {
                clearInterval(timer);
                callback(element);
            } else if (new Date().getTime() - startTime > timeout) {
                clearInterval(timer);
            }
        }, interval);
    }

    function submitLoginForm() {
        const loginButton = document.querySelector("form#fm1 button[type='submit']");
        if (loginButton) {
            loginButton.click();
        }
    }

    // Handle form selection and submission for Shibboleth
    function handleShibbolethForm() {
        const idpSelect = document.getElementById("idp");
        const ubsOption = idpSelect.querySelector('option[value="urn:mace:cru.fr:federation:univ-ubs.fr"]');
        if (ubsOption) {
            if (!ubsOption.selected) {
                ubsOption.selected = true;
                console.log("Selected Université Bretagne Sud - UBS");
            }

            const submitButton = document.querySelector("form#login button[type='submit']");
            if (submitButton) {
                submitButton.click();
                console.log("Submitted UBS selection form");
            }
        }
    }

    // Handle the final login form with username and password
    function handleCASLoginForm() {
        const usernameField = document.getElementById("username");
        const passwordField = document.getElementById("password");

        if (usernameField && passwordField) {
            usernameField.click();
            passwordField.click();

            if (usernameField.value === "" || passwordField.value === "") {
                setTimeout(() => {
                    if (usernameField.value !== "" && passwordField.value !== "") {
                        submitLoginForm();
                    }
                }, 2000);
            } else {
                setTimeout(() => {
                    submitLoginForm();
                }, 300);
            }
        }
    }

    // Function to check which page we're on and take action accordingly
    function checkForPageActions() {
        const currentUrl = window.location.href;

        if (currentUrl.includes("/auth/shibboleth/login.php")) {
            // Only attempt to handle the Shibboleth form if the user isn't already authenticated
            waitForElement("#idp", handleShibbolethForm);
        } else if (currentUrl.includes("/cas.univ-ubs.fr/login")) {
            // Wait for the CAS login form to load, then handle it
            waitForElement("#fm1", handleCASLoginForm);
        }
    }

    // Function to detect URL changes based on the hostname
    function detectURLChange() {
        let lastHostname = window.location.hostname;

        const observer = new MutationObserver(() => {
            const currentHostname = window.location.hostname;

            // Trigger actions when the hostname changes
            if (currentHostname !== lastHostname) {
                lastHostname = currentHostname;
                console.log(`Hostname changed to : ${currentHostname}`);
                checkForPageActions();
            }
        });

        // Observe the entire document for changes
        observer.observe(document, {
            childList: true,
            subtree: true
        });

        // Run the check initially on page load
        checkForPageActions();
    }

    // Initialize the URL change detection
    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", (event) => {
            console.log("DOM fully loaded");
            detectURLChange();
        });
    } else {
        detectURLChange();
    }
})();
