# LensIQ™ Chain of Thought TourMode Storyboard

## Overview

This storyboard outlines the visual flow and narration for the LensIQ™ Chain of Thought (CoT) guided tour. It's designed for creating a Loom walkthrough or investor pitch presentation that demonstrates how the AI-guided tour enhances the user experience.

---

## Scene 1: Introduction & Tour Activation

**Visual:** LensIQ™ landing page with the tour toggle button highlighted in the top-right corner.

**UI Elements:**
- Tour toggle button with "AI-Guided Tour" text
- URL with "?tour=true" parameter highlighted

**Narration:**
> "Welcome to LensIQ™, our AI-powered sustainability investment platform. Users can activate the Chain of Thought guided tour in two ways: by clicking this toggle button in the interface or by adding '?tour=true' to any URL. This flexibility makes it easy to share guided experiences with team members."

**Developer Note:** The tour activation is non-intrusive, using conditional loading of tour resources only when needed.

---

## Scene 2: TrendRadar - Initial Trend Scanning

**Visual:** TrendRadar visualization with trends mapped across quadrants. The "Act" zone is highlighted.

**UI Elements:**
- TrendRadar visualization
- Chain of Thought tooltip appearing at the bottom-right
- Highlight overlay focusing on the "Act" zone

**Narration:**
> "I'll start by scanning the TrendRadar to identify high-priority opportunities. I see several trends in the 'Act' zone - these are mature trends with strong momentum that warrant immediate attention. Let me focus on the circular economy trend, which shows both high maturity and accelerating growth."

**Developer Note:** The tour can dynamically highlight different zones based on current data.

---

## Scene 3: TrendRadar - Trend Deep Dive

**Visual:** Circular economy trend bubble is selected, showing detailed metrics in a side panel.

**UI Elements:**
- Selected trend bubble with animation
- Metrics panel showing growth rate, maturity score, and investment volume
- Chain of Thought tooltip explaining the analysis

**Narration:**
> "The circular economy trend shows a maturity score of 78 and growth rate of +34%. With €2.3B in investment volume this quarter, it's attracting significant capital. The AI reasoning: 'This trend combines regulatory tailwinds with strong market demand, making it ideal for portfolio allocation.'"

**Developer Note:** The metrics are pulled from real data sources when available.

---

## Scene 4: VC Lens - Strategic Filtering

**Visual:** Transition to VC Lens with filters being applied automatically.

**UI Elements:**
- ESG filter dropdown (set to "Circularity")
- Region filter dropdown (set to "LATAM")
- Stage filter dropdown (set to "Series A")
- Chain of Thought tooltip explaining filter strategy

**Narration:**
> "Moving to the VC Lens, the AI explains its filtering strategy: 'I'll apply filters for ESG: Circularity, Region: LATAM, and Stage: Series A. This narrows our focus to high-alignment, high-impact startups.' The tour demonstrates how to use filters strategically rather than just showing where they are."

**Developer Note:** The tour can trigger actual filter changes to demonstrate real functionality.

---

## Scene 5: VC Lens - Company Analysis

**Visual:** Filtered results showing ReCircle as a top match with metrics displayed.

**UI Elements:**
- ReCircle company card highlighted
- ESG score (85) and growth metrics (+42%)
- Chain of Thought tooltip analyzing the company

**Narration:**
> "The AI identifies promising opportunities: 'ReCircle stands out with an ESG score of 85 and growth of +42%. Their B2B packaging solution shows strong product-market fit and scalability potential.' This demonstrates how the AI evaluates companies based on multiple factors simultaneously."

**Developer Note:** The highlighting uses subtle animations to draw attention without being distracting.

---

## Scene 6: VC Lens - ESG Compliance Panel

**Visual:** ESG Compliance panel opening with detailed metrics.

**UI Elements:**
- ESG Compliance panel with SFDR alignment indicators
- Regulatory compliance scores
- Chain of Thought tooltip explaining compliance analysis

**Narration:**
> "The AI dives deeper into compliance: 'ReCircle shows strong SFDR Article 9 alignment with verified impact metrics. Their circular business model directly addresses EU taxonomy objectives.' This level of regulatory analysis is crucial for institutional investors."

**Developer Note:** The compliance data integrates with regulatory frameworks.

---

## Scene 7: VC Lens - Portfolio Signal Analysis

**Visual:** Portfolio Signal panel showing similar companies and momentum indicators.

**UI Elements:**
- Portfolio Signal button being clicked
- Similar companies with momentum indicators
- LP-Backed portfolio companies section
- Chain of Thought tooltip analyzing portfolio patterns

**Narration:**
> "Next, the AI looks for pattern validation: 'I see similar companies with strong social momentum. There are 3 LP-backed portfolio companies in adjacent spaces, suggesting ecosystem validation.' This cross-portfolio analysis helps validate investment theses and identify potential synergies."

**Developer Note:** The panel uses consistent styling with the rest of the application.

---

## Scene 8: VC Lens - Capital & Exit Panel

**Visual:** Capital & Exit panel showing funding flows and exit pathways.

**UI Elements:**
- Capital flows visualization
- Exit pathway analysis
- Chain of Thought tooltip explaining capital strategy

**Narration:**
> "Finally, the AI analyzes capital dynamics: 'Recent Series A rounds in this space average €8M with 18-month runway. Exit multiples show 3.2x average for strategic acquisitions.' This data helps inform investment sizing and exit strategy planning."

**Developer Note:** The capital analysis uses real market data when available.

---

## Scene 9: Tour Completion & Next Steps

**Visual:** Summary overlay with key insights and recommended actions.

**UI Elements:**
- Summary card with key findings
- Recommended next steps
- Tour completion celebration
- Option to explore other features

**Narration:**
> "The AI concludes: 'Based on this analysis, ReCircle represents a strong investment opportunity with high ESG alignment, proven traction, and favorable market conditions. Recommended next steps: Schedule management presentation and conduct technical due diligence.' The tour has demonstrated how AI reasoning enhances every step of the investment process."

**Developer Note:** The summary can be exported or saved for future reference.

---

## Technical Implementation Notes

### Tour State Management
- Tour progress is tracked in localStorage
- Each step can be resumed from any point
- Tour data is cached for offline viewing

### Performance Considerations
- Tour assets are lazy-loaded
- Animations are optimized for 60fps
- Tour can be disabled for performance-critical environments

### Accessibility Features
- Full keyboard navigation support
- Screen reader compatible
- High contrast mode available
- Reduced motion options

### Analytics Integration
- Tour completion rates tracked
- Step-by-step engagement metrics
- User feedback collection
- A/B testing framework ready

---

## Customization Options

### Tour Variants
- **Investor Pitch Mode**: Focused on ROI and market opportunity
- **Technical Demo Mode**: Emphasizes platform capabilities
- **User Onboarding Mode**: Guides new users through basic features

### Personalization
- Tour content adapts to user role (LP, GP, Analyst)
- Industry-specific examples and terminology
- Customizable pacing and depth

### Integration Points
- CRM integration for lead qualification
- Calendar integration for follow-up scheduling
- Document generation for investment memos

---

## Success Metrics

### Engagement Metrics
- Tour completion rate: Target >75%
- Time spent per step: Target 30-45 seconds
- Return visits to tour: Target >25%

### Business Impact
- Demo-to-meeting conversion: Target >40%
- Meeting-to-trial conversion: Target >60%
- Trial-to-paid conversion: Target >25%

### User Feedback
- Tour helpfulness rating: Target >4.5/5
- Feature discovery improvement: Target >50%
- User confidence increase: Target >60%

---

This storyboard provides a comprehensive framework for creating an engaging, AI-native tour experience that showcases the platform's sophisticated capabilities while maintaining user engagement and driving business outcomes.
