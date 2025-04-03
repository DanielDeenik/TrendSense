# SustainaTrend™ Intelligence Platform - Visual UI Design

This document outlines the current visual design and user interface organization of the SustainaTrend™ Intelligence Platform.

## Core Design System

The platform implements a cohesive dark-themed design system inspired by financial and analytics interfaces, with a focus on sustainability data visualization and user-friendly navigation.

### Design Principles

1. **Data-Forward**: Key metrics and visualizations take center stage
2. **Consistent Structure**: Common UI components and patterns across all sections
3. **Dark Theme**: Optimized for data visualization and extended usage
4. **Responsive Layout**: Adapts to different screen sizes and contexts
5. **Modular Components**: Card-based design for flexible arrangement

### Color System

- **Primary**: Teal (#3dd598 - rgb(61, 213, 152)) - Symbolizing sustainability
- **Background Layers**: Layered dark backgrounds (#121212, #1a1a1a, #222222)
- **Card Background**: Subtle elevation (#1d1d1d)
- **Text Hierarchy**: White/near-white primary text (#e4e6eb), secondary text (#a0a0a0), and muted text (#666666)
- **Status Colors**: Positive (#3dd598), Negative (#ff6b81), Warning (#ffad63), Info (#34c3ff)
- **Borders**: Subtle separation (#333333)

### Typography

- **Primary Font**: System fonts stack with -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial
- **Font Size Scale**: Base size of 14px with modular scaling
- **Weights**: Regular (400) for body text, Medium (500) for section titles, Semibold (600) for headings

### Iconography

- **UI Icons**: Font Awesome icons for interface elements
- **Category Icons**: Context-specific icons for different metric categories
- **Charts**: Chart.js for data visualization

## Interface Structure

### Global Layout

The application uses a grid-based layout with the following structure:

```
┌─────────────────────────────────────────────────────────────┐
│                       Header                                │
├────────────────┬────────────────────────────────────────────┤
│                │                                            │
│                │                                            │
│                │                                            │
│    Sidebar     │             Main Content Area              │
│                │                                            │
│                │                                            │
│                │                                            │
├────────────────┴────────────────────────────────────────────┤
└─────────────────────────────────────────────────────────────┘
```

#### Sidebar

The sidebar provides primary navigation with collapsible sections:

```
┌────────────────────────────┐
│ ◆ SustainaTrend™           │
├────────────────────────────┤
│ PLATFORM                   │
│ ○ Dashboard                │
│ ○ Performance              │
│ ○ Overview                 │
├────────────────────────────┤
│ INTELLIGENCE               │
│ ○ Trend Analysis           │
│ ○ Strategy Hub             │
├────────────────────────────┤
│ DOCUMENTS                  │
│ ○ Document Hub             │
│ ○ Regulatory Timeline      │
├────────────────────────────┤
│ SETTINGS                   │
│ ○ Configuration            │
│ ○ API Access               │
└────────────────────────────┘
```

The sidebar can be collapsed to save space:

```
┌─────────┐
│    ◆    │
├─────────┤
│    ○    │
│    ○    │
│    ○    │
├─────────┤
│    ○    │
│    ○    │
├─────────┤
│    ○    │
│    ○    │
├─────────┤
│    ○    │
│    ○    │
└─────────┘
```

### Core Pages

#### 1. Dashboard

The dashboard serves as the primary entry point to the platform, displaying key sustainability metrics and performance indicators.

```
┌─────────────────────────────────────────────────────────────┐
│ Sustainability Dashboard                      ⟳ Export ⬇    │
├─────────────────────────────────────────────────────────────┤
│ ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐  │
│ │ Carbon    │  │ Energy    │  │ Water     │  │ Waste     │  │
│ │ Emissions │  │ Consump.  │  │ Usage     │  │ Generated │  │
│ │           │  │           │  │           │  │           │  │
│ │ 78.5 t    │  │ 342 MWh   │  │ 1.28M L   │  │ 56.3 t    │  │
│ │ CO₂e      │  │           │  │           │  │           │  │
│ │ ▼ 12.3%   │  │ ▼ 8.7%    │  │ ▼ 4.2%    │  │ ▼ 15.8%   │  │
│ └───────────┘  └───────────┘  └───────────┘  └───────────┘  │
├─────────────────────────────────────────────────────────────┤
│ ┌─────────────────────────┐  ┌─────────────────────────┐    │
│ │ ESG Scores              │  │ Emissions Trend         │    │
│ │                         │  │                         │    │
│ │  [Radar Chart]          │  │  [Line Chart]           │    │
│ │                         │  │                         │    │
│ │                         │  │                         │    │
│ └─────────────────────────┘  └─────────────────────────┘    │
├─────────────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Performance Against Targets                             │ │
│ │ ┌───────────────┐  ┌───────────────┐  ┌───────────────┐ │ │
│ │ │ Carbon        │  │ Renewable     │  │ Zero Waste    │ │ │
│ │ │ Neutrality    │  │ Energy        │  │               │ │ │
│ │ │ [68%] ━━━━━━━○│  │ [42%] ━━━━○━━━│  │ [35%] ━━━○━━━━│ │ │
│ │ │ Target: 2030  │  │ Target: 100%  │  │ Target: 2035  │ │ │
│ │ └───────────────┘  └───────────────┘  └───────────────┘ │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

#### 2. Document Hub

The Document Hub provides a central interface for document upload, regulatory analysis, and document processing through a tabbed interface.

```
┌─────────────────────────────────────────────────────────────┐
│ Document & Regulatory Intelligence                          │
├─────────────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Regulatory Timeline                                     │ │
│ │ ┌───────────────────────────────────────────────────────┐ │
│ │ │  [Horizontal Timeline of Regulatory Deadlines]        │ │
│ │ │  ● CSRD      ● SEC Climate      ● ISSB Standards      │ │
│ │ │  Jan 2025    June 2025          Dec 2025              │ │
│ │ └───────────────────────────────────────────────────────┘ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ ┌─────────┬───────────────┬─────────────┐                   │
│ │ Upload  │ Regulatory    │ Analysis    │                   │
│ └─────────┴───────────────┴─────────────┘                   │
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ [Active Tab Content]                                    │ │
│ │                                                         │ │
│ │ ┌─────────────────────────────────────────────────────┐ │ │
│ │ │ Drop Sustainability Document Here                   │ │ │
│ │ │                                                     │ │ │
│ │ │ [Upload Zone with Drag & Drop Support]              │ │ │
│ │ │                                                     │ │ │
│ │ │ Or                                                  │ │ │
│ │ │                                                     │ │ │
│ │ │ [Select Files]                                      │ │ │
│ │ └─────────────────────────────────────────────────────┘ │ │
│ │                                                         │ │
│ │ ┌─────────────────────────────────────────────────────┐ │ │
│ │ │ Recent Documents                                    │ │ │
│ │ │                                                     │ │ │
│ │ │ [Grid of Recent Document Cards]                     │ │ │
│ │ └─────────────────────────────────────────────────────┘ │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

#### 3. Trend Analysis

The Trend Analysis page displays sustainability trends and allows for deep analysis of metrics over time.

```
┌─────────────────────────────────────────────────────────────┐
│ Sustainability Trend Analysis                  Filter ▾     │
├─────────────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Trend Overview                                          │ │
│ │ ┌───────────────┐  ┌───────────────┐  ┌───────────────┐ │ │
│ │ │ Carbon        │  │ Energy        │  │ Industry      │ │ │
│ │ │ Intensity     │  │ Efficiency    │  │ Benchmarks    │ │ │
│ │ │ [Chart]       │  │ [Chart]       │  │ [Chart]       │ │ │
│ │ │ ▼ 8.2% YoY    │  │ ▲ 12.3% YoY   │  │ 15% better    │ │ │
│ │ └───────────────┘  └───────────────┘  └───────────────┘ │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Historical Performance                                  │ │
│ │                                                         │ │
│ │ [Time Series Chart with Multiple Metrics]               │ │
│ │                                                         │ │
│ │ [Time Range Selector]                                   │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ AI Trend Analysis                                       │ │
│ │                                                         │ │
│ │ Ask a question about your sustainability trends:        │ │
│ │ [What's driving the reduction in carbon emissions?    ] │ │
│ │                                                         │ │
│ │ [AI Response with Insights and Visualization]           │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

#### 4. Strategy Hub

The Strategy Hub (formerly Stories) provides AI-driven strategic recommendations and storytelling capabilities.

```
┌─────────────────────────────────────────────────────────────┐
│ Sustainability Strategy Hub                  New Strategy ＋ │
├─────────────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Strategic Frameworks                                    │ │
│ │ ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌─────────┐ │ │
│ │ │ McKinsey  │  │ BCG       │  │ ESG       │  │ Circular│ │ │
│ │ │ Framework │  │ Framework │  │ Framework │  │ Economy │ │ │
│ │ └───────────┘  └───────────┘  └───────────┘  └─────────┘ │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Recent Strategies                                       │ │
│ │                                                         │ │
│ │ ┌─────────────────────────────────────────────────────┐ │ │
│ │ │ Housing Sector Carbon Neutrality Strategy           │ │ │
│ │ │                                                     │ │ │
│ │ │ Industry: Real Estate                              │ │ │
│ │ │ Created: March 15, 2025                            │ │ │
│ │ │                                                     │ │ │
│ │ │ [Key Recommendations Preview]                       │ │ │
│ │ │                                                     │ │ │
│ │ │ [View Strategy]  [Share]  [Export]                  │ │ │
│ │ └─────────────────────────────────────────────────────┘ │ │
│ │                                                         │ │
│ │ [Additional Strategy Cards]                             │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Component Library

#### Cards

The primary content containers:

```
┌─────────────────────────────────────────┐
│ Card Title                     •••      │
├─────────────────────────────────────────┤
│                                         │
│ [Card Content]                          │
│                                         │
└─────────────────────────────────────────┘
```

#### Metric Cards

For displaying key performance indicators:

```
┌─────────────────────────────────────────┐
│ ■                                        │
│ Metric Title                             │
│                                          │
│ 123.4                                    │
│ units                                    │
│                                          │
│ ▼ 5.2%                                   │
└─────────────────────────────────────────┘
```

#### Progress Indicators

For displaying progress against targets:

```
┌─────────────────────────────────────────┐
│ Progress Title                           │
│                                          │
│ [━━━━━━━━━━━○━━━━━] 64%                  │
│                                          │
│ Target: 100% by 2030                     │
└─────────────────────────────────────────┘
```

#### Tabbed Interface

For switching between related content sections:

```
┌─────────┬───────────────┬─────────────┐
│ Active  │ Inactive      │ Inactive    │
└─────────┴───────────────┴─────────────┘
┌─────────────────────────────────────────┐
│                                         │
│ [Content for active tab]                │
│                                         │
└─────────────────────────────────────────┘
```

#### Timeline Component

Horizontal timeline for regulatory deadlines:

```
    ●             ●              ●
    │             │              │
────┼─────────────┼──────────────┼────────
    │             │              │
 Jan 2025     June 2025      Dec 2025
    │             │              │
  CSRD      SEC Climate     ISSB Standards
```

## Responsive Behavior

The interface adapts to different screen sizes with the following approaches:

1. **Desktop (1200px+)**: Full sidebar with text labels, multi-column card layouts
2. **Tablet (768px-1199px)**: Collapsed sidebar with icons only, 2-column card layouts
3. **Mobile (< 768px)**: Hidden sidebar (toggle with menu button), single-column layouts

## State Management

The interface handles several user-controlled states:

1. **Sidebar Collapse**: Toggle between full and icon-only sidebar
2. **Theme Preference**: Light and dark mode support (dark is default)
3. **Tab Selection**: Active tab highlighting and content display
4. **Document Upload States**: Idle, dragging, uploading, processing, complete
5. **AI Interaction States**: Input, processing, response display

## Accessibility Considerations

The interface incorporates accessibility features:

1. **Color Contrast**: Ensuring text readability (WCAG AA compliance)
2. **Keyboard Navigation**: Tab order and focus indicators
3. **Screen Reader Support**: Semantic HTML and ARIA attributes
4. **Responsive Text**: Scaling for different screen sizes and zoom levels

## Interactive Elements

The interface includes various interactive components:

1. **Charts**: Hover for detailed values, click for expanded view
2. **AI Input**: Natural language query input for AI-driven insights
3. **Filters**: Date ranges, metric categories, framework selection
4. **Upload Zone**: Drag and drop or file selection
5. **Document Chat**: Conversational interface for document analysis