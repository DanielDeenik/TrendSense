# TrendSense Demo Mode Guide

This guide explains how to use the Demo Mode feature to create demo-ready videos showcasing TrendSense's features, particularly the guided tour and error handling capabilities.

## Overview

The Demo Mode provides a controlled environment for creating demonstration videos by:

1. Orchestrating a series of predefined actions
2. Simulating API responses
3. Controlling the timing of interactions
4. Highlighting key features like error handling and guided tours

## Getting Started

### Activating Demo Mode

There are three ways to activate Demo Mode:

1. **URL Parameters**: Add `?demo=true` to any URL
   ```
   http://localhost:5050/trendradar/?demo=true
   ```

2. **Demo Button**: Click the "Demo Mode" button in the top-right corner of the screen

3. **Keyboard Shortcut**: Press `Ctrl+Shift+D` to toggle the Demo Mode control panel

### Demo Mode Control Panel

The control panel provides the following controls:

- **Scenario**: Select a predefined demo scenario
- **Autoplay Delay**: Set the delay between automated steps (in milliseconds)
- **Autoplay**: Toggle automatic progression through demo steps
- **Start**: Start the selected demo scenario
- **Next**: Manually advance to the next step
- **Stop**: Stop the current demo

### Keyboard Shortcuts

The following keyboard shortcuts are available in Demo Mode:

- `Ctrl+Shift+D`: Toggle Demo Mode control panel
- `Ctrl+Shift+S`: Start demo with selected scenario
- `Ctrl+Shift+X`: Stop demo
- `Ctrl+Shift+N`: Go to next step
- `Ctrl+Shift+A`: Toggle autoplay
- `Ctrl+Shift+R`: Toggle recording indicator

## Demo Scenarios

### Error Handling Demo

This scenario demonstrates how the guided tour handles API errors:

1. Starts the guided tour
2. Navigates to the TrendRadar page
3. Triggers an API error
4. Shows the error handling tour
5. Navigates through the error handling steps
6. Opens the help modal
7. Shows the Co-Pilot suggestions
8. Closes the help modal
9. Ends the demo

### Guided Tour Demo

This scenario demonstrates the AI-guided tour feature:

1. Starts the guided tour
2. Navigates through the tour steps
3. Highlights key features
4. Ends the demo

## Creating Custom Scenarios

You can create custom demo scenarios by modifying the `defineScenarios` method in `demo-mode-controller.js`:

```javascript
defineScenarios() {
    // Custom scenario
    this.scenarios.customScenario = {
        name: 'Custom Scenario',
        description: 'Description of your custom scenario',
        steps: [
            {
                name: 'Step 1',
                action: () => {
                    // Action to perform
                },
                delay: 2000 // Delay before next step (ms)
            },
            // Add more steps as needed
        ]
    };
}
```

## Simulating API Responses

The Demo API Simulator allows you to simulate API responses for demo purposes:

### URL Parameters

- `?simulate-api=true`: Enable API simulation
- `?error-rate=50`: Set error rate to 50% (0-100)
- `?response-delay=2000`: Set response delay to 2000ms

Example:
```
http://localhost:5050/trendradar/?demo=true&simulate-api=true&error-rate=50
```

### Adding Custom Endpoints

You can add custom simulated endpoints by modifying the `defineEndpoints` method in `demo-api-simulator.js`:

```javascript
defineEndpoints() {
    // Custom endpoint
    this.endpoints['/api/custom-endpoint'] = {
        method: 'POST',
        response: {
            // Custom response data
        }
    };
}
```

## Recording Demo Videos

To create a demo-ready video:

1. **Prepare Your Environment**:
   - Use a clean browser window
   - Set the browser to an appropriate size (1920x1080 recommended)
   - Ensure all necessary components are loaded

2. **Set Up Screen Recording**:
   - Use a screen recording tool like OBS Studio, Camtasia, or built-in OS recording
   - Configure to capture the browser window
   - Test audio if you plan to narrate

3. **Run the Demo**:
   - Navigate to the starting page with demo parameters:
     ```
     http://localhost:5050/trendradar/?demo=true&autoplay=true
     ```
   - The recording indicator will appear in the top-right corner
   - The demo will automatically progress through the steps

4. **Post-Processing**:
   - Edit the video to add titles, transitions, and captions
   - Add voiceover narration if needed
   - Export in an appropriate format (MP4 recommended)

## Tips for Creating Professional Demo Videos

1. **Narrate with Purpose**:
   - Explain what's happening on screen
   - Highlight key features and benefits
   - Keep narration concise and focused

2. **Control the Pace**:
   - Adjust the autoplay delay to match your narration
   - Use manual stepping for complex features
   - Pause at important points

3. **Highlight Key Features**:
   - Focus on the guided tour and error handling
   - Show how the system helps users recover from errors
   - Demonstrate the Chain of Thought narration

4. **Keep It Short**:
   - Aim for 2-5 minutes total
   - Focus on one or two key features
   - Cut unnecessary steps in post-processing

## Troubleshooting

### Demo Mode Not Working

- Check browser console for errors
- Ensure all required JavaScript files are loaded
- Try refreshing the page

### API Simulator Not Working

- Check if the simulator is enabled (`?simulate-api=true`)
- Verify the endpoint is defined in `defineEndpoints`
- Check browser console for errors

### Demo Steps Not Advancing

- Check if autoplay is enabled
- Try manually advancing with the "Next" button
- Check for JavaScript errors in the console

## Support

For additional help or to report issues with the Demo Mode, please contact the development team.
