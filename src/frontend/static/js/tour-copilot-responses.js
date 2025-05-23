/**
 * TourMode Co-Pilot Response Map
 * 
 * This file contains predefined responses for the Co-Pilot to use when
 * users encounter common issues during the TourMode experience.
 * 
 * The responses are organized by issue type and include both general
 * responses and specific responses based on keywords in the user's description.
 */

const tourCopilotResponses = {
  // Navigation Issues
  'tour-navigation': {
    // General responses for navigation issues
    general: [
      {
        title: "Tour Navigation Problem",
        suggestion: "Try refreshing the page and restarting the tour by adding ?tour=true to the URL.",
        steps: [
          "Click the browser's refresh button or press F5",
          "Add ?tour=true to the end of the URL in your address bar",
          "Press Enter to reload the page with the tour enabled"
        ]
      },
      {
        title: "Step Sequence Issue",
        suggestion: "Try clicking the 'Previous' button to go back one step, then proceed forward again.",
        steps: [
          "Click the 'Previous' button in the tour controls",
          "Review the previous step's instructions",
          "Click 'Next' to continue the tour"
        ]
      },
      {
        title: "Tour Controls Not Responding",
        suggestion: "Check if you're logged in. Some tour features require authentication.",
        steps: [
          "Click the login button in the top-right corner",
          "Enter your credentials and log in",
          "Restart the tour after logging in"
        ]
      }
    ],
    
    // Keyword-specific responses
    keywords: {
      'stuck': {
        title: "Tour Stuck on Current Step",
        suggestion: "The tour might be stuck due to a timing issue. Try refreshing the page and restarting from the current step.",
        steps: [
          "Note your current step number",
          "Refresh the page",
          "Add ?tour=true&step=[your step number] to the URL"
        ]
      },
      'button': {
        title: "Tour Buttons Not Working",
        suggestion: "If tour buttons aren't responding, try clicking elsewhere on the page first, then try again.",
        steps: [
          "Click on an empty area of the page",
          "Wait a moment for any background processes to complete",
          "Try clicking the tour button again"
        ]
      },
      'skip': {
        title: "Need to Skip a Step",
        suggestion: "You can skip the current step by manually advancing to the next step.",
        steps: [
          "Click the 'Next' button to skip the current step",
          "If that doesn't work, try refreshing and adding ?tour=true&step=[next step number] to the URL"
        ]
      }
    }
  },
  
  // Content Missing Issues
  'content-missing': {
    // General responses for content missing issues
    general: [
      {
        title: "Content Not Loading",
        suggestion: "Ensure your browser window is maximized or try a different browser.",
        steps: [
          "Maximize your browser window",
          "Check if content appears after resizing",
          "If not, try using Chrome, Firefox, or Edge"
        ]
      },
      {
        title: "Dynamic Content Issues",
        suggestion: "Check your internet connection as some content may be loading dynamically.",
        steps: [
          "Verify your internet connection is stable",
          "Wait a few moments for content to load",
          "Try refreshing the page if content still doesn't appear"
        ]
      },
      {
        title: "Content Blocked",
        suggestion: "Try disabling browser extensions that might be blocking content.",
        steps: [
          "Open your browser's extension menu",
          "Temporarily disable ad blockers or privacy extensions",
          "Refresh the page and try again"
        ]
      }
    ],
    
    // Keyword-specific responses
    keywords: {
      'image': {
        title: "Images Not Loading",
        suggestion: "Images may be blocked by your network or browser settings.",
        steps: [
          "Check if images are enabled in your browser settings",
          "Verify that your network doesn't block image content",
          "Try using a different network connection if possible"
        ]
      },
      'chart': {
        title: "Charts or Visualizations Missing",
        suggestion: "Charts require JavaScript and may take time to render.",
        steps: [
          "Ensure JavaScript is enabled in your browser",
          "Wait a few moments for complex visualizations to render",
          "Try zooming out if charts are rendering outside the visible area"
        ]
      },
      'text': {
        title: "Text Content Missing",
        suggestion: "Text content might be affected by font loading or CSS issues.",
        steps: [
          "Check if you have custom font settings in your browser",
          "Try disabling custom fonts temporarily",
          "Adjust your zoom level to ensure text is within visible bounds"
        ]
      }
    }
  },
  
  // Feature Access Issues
  'feature-access': {
    // General responses for feature access issues
    general: [
      {
        title: "Permission Required",
        suggestion: "Verify you have the necessary permissions for this feature.",
        steps: [
          "Check your user role in your account settings",
          "Contact your administrator if you need additional permissions",
          "Try logging out and back in to refresh your session"
        ]
      },
      {
        title: "Feature Navigation",
        suggestion: "Try navigating to the feature directly from the main menu.",
        steps: [
          "Go to the main dashboard",
          "Look for the feature in the main navigation menu",
          "Access the feature directly rather than through the tour"
        ]
      },
      {
        title: "Sequential Access Required",
        suggestion: "Some features may require completing previous steps in the tour first.",
        steps: [
          "Go back to the beginning of the tour",
          "Complete each step in sequence",
          "Try accessing the feature again after completing previous steps"
        ]
      }
    ],
    
    // Keyword-specific responses
    keywords: {
      'login': {
        title: "Login Required",
        suggestion: "This feature requires you to be logged in with a valid account.",
        steps: [
          "Click the login button in the top-right corner",
          "Enter your credentials and log in",
          "Try accessing the feature again after logging in"
        ]
      },
      'premium': {
        title: "Premium Feature Access",
        suggestion: "This may be a premium feature that requires a subscription.",
        steps: [
          "Check your account subscription level",
          "Consider upgrading your account if this is a premium feature",
          "Contact support for more information about feature access"
        ]
      },
      'error': {
        title: "Error When Accessing Feature",
        suggestion: "An error might be preventing access to this feature.",
        steps: [
          "Check your browser console for error messages (F12 > Console)",
          "Try clearing your browser cache and cookies",
          "Restart your browser and try again"
        ]
      }
    }
  },
  
  // Unclear Instructions Issues
  'unclear-instructions': {
    // General responses for unclear instructions issues
    general: [
      {
        title: "Review Previous Steps",
        suggestion: "Click the 'Previous' button to review earlier instructions.",
        steps: [
          "Click the 'Previous' button in the tour controls",
          "Read through the instructions carefully",
          "Click 'Next' when you're ready to continue"
        ]
      },
      {
        title: "Additional Tooltips",
        suggestion: "Try hovering over highlighted elements for additional tooltips.",
        steps: [
          "Move your cursor over the highlighted element",
          "Look for tooltips that appear on hover",
          "Read the tooltip information for additional guidance"
        ]
      },
      {
        title: "Chain of Thought Explanation",
        suggestion: "The Chain of Thought panel explains the AI's reasoning for each step.",
        steps: [
          "Look for the Chain of Thought panel (usually in the bottom-right)",
          "Read the AI's reasoning process",
          "Follow the logical steps outlined in the explanation"
        ]
      }
    ],
    
    // Keyword-specific responses
    keywords: {
      'confus': {
        title: "Confused About Instructions",
        suggestion: "Break down the instructions into smaller steps and focus on one at a time.",
        steps: [
          "Read each sentence of the instruction separately",
          "Complete one action before moving to the next",
          "Look at the highlighted element for context"
        ]
      },
      'understand': {
        title: "Difficulty Understanding Concept",
        suggestion: "The Chain of Thought panel provides detailed explanations of concepts.",
        steps: [
          "Focus on the Chain of Thought explanation",
          "Look for definitions of technical terms",
          "Try relating the concept to something familiar"
        ]
      },
      'complex': {
        title: "Complex Instructions",
        suggestion: "Complex steps can be broken down into simpler actions.",
        steps: [
          "Identify the main action required",
          "Look for visual cues like highlighted elements",
          "Complete one part of the instruction before moving to the next"
        ]
      }
    }
  },
  
  // Other Issues
  'other': {
    // General responses for other issues
    general: [
      {
        title: "General Troubleshooting",
        suggestion: "Try refreshing the page and restarting the tour.",
        steps: [
          "Refresh your browser page",
          "Add ?tour=true to the URL if needed",
          "Start the tour again from the beginning"
        ]
      },
      {
        title: "Browser Console Check",
        suggestion: "Check your browser console for any error messages.",
        steps: [
          "Press F12 to open developer tools",
          "Click on the 'Console' tab",
          "Look for red error messages that might explain the issue"
        ]
      },
      {
        title: "Session Reset",
        suggestion: "Consider logging out and back in to reset your session.",
        steps: [
          "Click the logout button",
          "Log back in with your credentials",
          "Try the tour again after logging in"
        ]
      }
    ],
    
    // Keyword-specific responses
    keywords: {
      'slow': {
        title: "Performance Issues",
        suggestion: "The application might be running slowly due to your connection or device.",
        steps: [
          "Check your internet connection speed",
          "Close other browser tabs and applications",
          "Try using a device with more processing power if available"
        ]
      },
      'crash': {
        title: "Application Crash",
        suggestion: "If the application crashed, it might be due to a browser or memory issue.",
        steps: [
          "Restart your browser completely",
          "Clear your browser cache and cookies",
          "Try using a different browser if the issue persists"
        ]
      },
      'bug': {
        title: "Potential Bug",
        suggestion: "You may have encountered a bug in the application.",
        steps: [
          "Note the exact steps that led to the issue",
          "Include these details in your bug report",
          "Try a different approach to accomplish the same task"
        ]
      }
    }
  }
};

// Export the responses
window.tourCopilotResponses = tourCopilotResponses;
