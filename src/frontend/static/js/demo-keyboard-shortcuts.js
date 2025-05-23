/**
 * Demo Mode Keyboard Shortcuts
 *
 * This module provides keyboard shortcuts for controlling the demo mode.
 */

document.addEventListener('DOMContentLoaded', function() {
    // Define keyboard shortcuts
    let shortcuts = {
        toggleControlPanel: {
            key: 'D',
            modifiers: {
                ctrl: true,
                shift: true
            },
            description: 'Toggle demo control panel',
            action: () => {
                const controlPanel = document.getElementById('demo-control-panel');
                if (controlPanel) {
                    const isHidden = controlPanel.classList.contains('hidden');
                    window.demoMode.toggleControlPanel(!isHidden);
                }
            }
        },
        startDemo: {
            key: 'S',
            modifiers: {
                ctrl: true,
                shift: true
            },
            description: 'Start demo with selected scenario',
            action: () => {
                const scenarioSelect = document.getElementById('demo-scenario');
                if (scenarioSelect) {
                    const scenarioName = scenarioSelect.value;
                    window.demoMode.startDemo(scenarioName);
                }
            }
        },
        stopDemo: {
            key: 'X',
            modifiers: {
                ctrl: true,
                shift: true
            },
            description: 'Stop demo',
            action: () => {
                window.demoMode.stopDemo();
            }
        },
        nextStep: {
            key: 'N',
            modifiers: {
                ctrl: true,
                shift: true
            },
            description: 'Go to next step',
            action: () => {
                if (window.demoMode.isActive) {
                    window.demoMode.nextStep();
                }
            }
        },
        toggleAutoplay: {
            key: 'A',
            modifiers: {
                ctrl: true,
                shift: true
            },
            description: 'Toggle autoplay',
            action: () => {
                const autoplayCheckbox = document.getElementById('demo-autoplay');
                if (autoplayCheckbox) {
                    autoplayCheckbox.checked = !autoplayCheckbox.checked;
                    window.demoMode.toggleAutoplay(autoplayCheckbox.checked);
                }
            }
        },
        toggleRecordingIndicator: {
            key: 'R',
            modifiers: {
                ctrl: true,
                shift: true
            },
            description: 'Toggle recording indicator',
            action: () => {
                const recordingIndicator = document.getElementById('recording-indicator');
                if (recordingIndicator) {
                    const isHidden = recordingIndicator.classList.contains('hidden');
                    window.demoMode.toggleRecordingIndicator(!isHidden);
                }
            }
        }
    };

    // Override with config if available
    if (window.demoConfig && window.demoConfig.keyboardShortcuts) {
        // For each shortcut in the config
        Object.keys(window.demoConfig.keyboardShortcuts).forEach(shortcutName => {
            // If this shortcut exists in our defaults
            if (shortcuts[shortcutName]) {
                // Override the key and modifiers
                const configShortcut = window.demoConfig.keyboardShortcuts[shortcutName];
                shortcuts[shortcutName].key = configShortcut.key;
                shortcuts[shortcutName].modifiers = configShortcut.modifiers;
                shortcuts[shortcutName].description = configShortcut.description || shortcuts[shortcutName].description;
            }
        });

        console.log('Loaded keyboard shortcuts from config');
    } else {
        console.log('Using default keyboard shortcuts');
    }

    // Add keyboard event listener
    document.addEventListener('keydown', function(event) {
        // Only process if demo mode controller exists
        if (!window.demoMode) return;

        // Check each shortcut
        Object.values(shortcuts).forEach(shortcut => {
            // Check if this event matches the shortcut
            if (
                event.key === shortcut.key &&
                (!shortcut.modifiers.ctrl || event.ctrlKey) &&
                (!shortcut.modifiers.shift || event.shiftKey) &&
                (!shortcut.modifiers.alt || event.altKey) &&
                (!shortcut.modifiers.meta || event.metaKey)
            ) {
                event.preventDefault();
                shortcut.action();
            }
        });
    });

    // Log available shortcuts
    console.log('Demo Mode Keyboard Shortcuts:');
    Object.values(shortcuts).forEach(shortcut => {
        const modifiers = [];
        if (shortcut.modifiers.ctrl) modifiers.push('Ctrl');
        if (shortcut.modifiers.shift) modifiers.push('Shift');
        if (shortcut.modifiers.alt) modifiers.push('Alt');
        if (shortcut.modifiers.meta) modifiers.push('Meta');

        console.log(`- ${modifiers.join('+')}+${shortcut.key}: ${shortcut.description}`);
    });
});
