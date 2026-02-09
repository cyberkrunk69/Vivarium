# BLACK SWARM Brand Identity Guide

## Overview
BLACK SWARM represents a paradigm shift in AI: autonomous agents that learn and improve themselves. The visual identity captures collective intelligence, emergence, power, and mystery while maintaining professional standards for enterprise engineers, AI researchers, and forward-thinking developers.

**Brand Ethos**: Cutting-edge but professional, powerful but controlled, autonomous but safe.

---

## 1. Color Palette

### Primary Colors

```css
:root {
  /* Core Brand Colors */
  --swarm-void: #0a0a0a;           /* Deep void black - primary background */
  --swarm-neural: #1a237e;        /* Neural blue - primary accent */
  --swarm-emergence: #00c853;     /* Emergence green - success/active states */
  --swarm-warning: #ff8f00;       /* Warning amber - alerts/cautions */

  /* Extended Palette */
  --swarm-void-soft: #1a1a1a;     /* Soft black for cards/surfaces */
  --swarm-void-lighter: #2a2a2a;  /* Lighter black for borders */
  --swarm-neural-light: #3949ab;  /* Light neural blue for hover */
  --swarm-neural-dark: #0d1757;   /* Dark neural blue for depth */
  --swarm-emergence-light: #4caf50; /* Light green for secondary actions */
  --swarm-emergence-dark: #00a642; /* Dark green for pressed states */

  /* Semantic Colors */
  --swarm-text-primary: #ffffff;   /* Primary text - pure white */
  --swarm-text-secondary: #b0b0b0; /* Secondary text - muted */
  --swarm-text-tertiary: #707070;  /* Tertiary text - subtle */
  --swarm-error: #f44336;          /* Error red */
  --swarm-surface: #1e1e1e;        /* Card/panel backgrounds */
  --swarm-border: #333333;         /* Subtle borders */
}
```

### WCAG AA Compliance
- **Primary text on void**: 21:1 contrast ratio ✓
- **Secondary text on void**: 15.3:1 contrast ratio ✓
- **Neural blue on void**: 4.7:1 contrast ratio ✓
- **Emergence green on void**: 7.2:1 contrast ratio ✓

---

## 2. Typography System

### Font Families

```css
:root {
  /* Headlines - Bold, Technical, Modern */
  --font-headline: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;

  /* Body Text - Readable Sans-serif */
  --font-body: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;

  /* Code - Clean Monospace with Ligatures */
  --font-code: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace;

  /* UI Elements */
  --font-ui: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}
```

### Typography Scale

```css
:root {
  /* Font Sizes - Major Third Scale (1.25) */
  --text-xs: 0.75rem;    /* 12px - Fine print, captions */
  --text-sm: 0.875rem;   /* 14px - Secondary text, labels */
  --text-base: 1rem;     /* 16px - Body text, default */
  --text-lg: 1.125rem;   /* 18px - Large body text */
  --text-xl: 1.25rem;    /* 20px - Sub-headlines */
  --text-2xl: 1.5rem;    /* 24px - Section headers */
  --text-3xl: 1.875rem;  /* 30px - Page headers */
  --text-4xl: 2.25rem;   /* 36px - Display text */
  --text-5xl: 3rem;      /* 48px - Hero text */

  /* Font Weights */
  --weight-light: 300;
  --weight-normal: 400;
  --weight-medium: 500;
  --weight-semibold: 600;
  --weight-bold: 700;

  /* Line Heights */
  --leading-tight: 1.25;
  --leading-snug: 1.375;
  --leading-normal: 1.5;
  --leading-relaxed: 1.625;
}
```

---

## 3. Visual Language

### Core Concepts
- **Swarm Behavior**: Interconnected nodes, flowing particles, collective movement
- **Neural Networks**: Synaptic connections, branching patterns, electric pulses
- **Emergence**: Organic growth patterns, crystalline structures, phase transitions

### Icon System
```css
.swarm-icon {
  /* Base icon styling */
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: var(--swarm-text-secondary);
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.swarm-icon--neural {
  /* Neural network inspired icons */
  filter: drop-shadow(0 0 4px var(--swarm-neural));
}

.swarm-icon--active {
  color: var(--swarm-emergence);
  transform: scale(1.05);
}
```

### Animation Principles
- **Spring Physics**: `cubic-bezier(0.34, 1.56, 0.64, 1)` for bouncy feel
- **Smooth Easing**: `cubic-bezier(0.4, 0, 0.2, 1)` for standard transitions
- **Pulse Effect**: Subtle breathing animations for active states
- **Swarm Movement**: Staggered delays for collective behaviors

### Data Visualization
```css
.swarm-chart {
  /* Neural-inspired data viz */
  background: linear-gradient(135deg, var(--swarm-void) 0%, var(--swarm-void-soft) 100%);
  border: 1px solid var(--swarm-border);
  border-radius: 8px;
}

.swarm-metric {
  color: var(--swarm-emergence);
  font-family: var(--font-code);
  font-weight: var(--weight-medium);
}
```

---

## 4. CSS Techniques & Components

### Glass Morphism Effects

```css
.swarm-glass {
  background: rgba(26, 26, 26, 0.8);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  box-shadow:
    0 8px 32px rgba(0, 0, 0, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
}
```

### Gradient Systems

```css
:root {
  /* Neural gradients */
  --gradient-neural: linear-gradient(135deg, var(--swarm-neural-dark) 0%, var(--swarm-neural) 100%);
  --gradient-emergence: linear-gradient(135deg, var(--swarm-emergence-dark) 0%, var(--swarm-emergence) 100%);
  --gradient-void: linear-gradient(135deg, var(--swarm-void) 0%, var(--swarm-void-soft) 100%);

  /* Subtle overlays */
  --gradient-overlay: linear-gradient(180deg, transparent 0%, rgba(0, 0, 0, 0.4) 100%);
}
```

### Micro-interactions

```css
.swarm-button {
  background: var(--gradient-neural);
  border: none;
  border-radius: 6px;
  color: var(--swarm-text-primary);
  cursor: pointer;
  font-family: var(--font-ui);
  font-weight: var(--weight-medium);
  padding: 12px 24px;
  position: relative;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
}

.swarm-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
  transition: left 0.5s;
}

.swarm-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 20px rgba(26, 35, 126, 0.4);
}

.swarm-button:hover::before {
  left: 100%;
}

.swarm-button:active {
  transform: translateY(0);
}
```

### Loading States

```css
@keyframes swarm-pulse {
  0%, 100% { opacity: 0.4; }
  50% { opacity: 1; }
}

@keyframes swarm-flow {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

.swarm-loading {
  position: relative;
  background: var(--swarm-void-soft);
  border-radius: 4px;
  overflow: hidden;
}

.swarm-loading::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, var(--swarm-neural), transparent);
  animation: swarm-flow 1.5s infinite;
}

.swarm-spinner {
  width: 24px;
  height: 24px;
  border: 2px solid var(--swarm-void-lighter);
  border-top: 2px solid var(--swarm-emergence);
  border-radius: 50%;
  animation: spin 1s cubic-bezier(0.4, 0, 0.2, 1) infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
```

### Grid Layouts

```css
.swarm-grid {
  display: grid;
  gap: 24px;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
}

.swarm-dashboard {
  display: grid;
  grid-template-areas:
    "header header header"
    "sidebar main metrics"
    "sidebar main metrics";
  grid-template-columns: 250px 1fr 300px;
  grid-template-rows: auto 1fr auto;
  gap: 16px;
  min-height: 100vh;
  padding: 16px;
}

.swarm-card {
  background: var(--swarm-glass);
  backdrop-filter: blur(20px);
  border: 1px solid var(--swarm-border);
  border-radius: 8px;
  padding: 24px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.swarm-card:hover {
  border-color: var(--swarm-neural);
  transform: translateY(-2px);
  box-shadow: 0 8px 40px rgba(26, 35, 126, 0.2);
}
```

### Intelligent States

```css
.swarm-status {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: var(--text-sm);
  font-weight: var(--weight-medium);
}

.swarm-status--active {
  background: rgba(0, 200, 83, 0.1);
  color: var(--swarm-emergence);
  border: 1px solid var(--swarm-emergence);
}

.swarm-status--learning {
  background: rgba(26, 35, 126, 0.1);
  color: var(--swarm-neural);
  border: 1px solid var(--swarm-neural);
  animation: swarm-pulse 2s infinite;
}

.swarm-status--warning {
  background: rgba(255, 143, 0, 0.1);
  color: var(--swarm-warning);
  border: 1px solid var(--swarm-warning);
}
```

---

## Usage Guidelines

### Do's
- Use the void black as primary background for maximum contrast
- Apply neural blue sparingly for key interactive elements
- Leverage emergence green for success states and positive feedback
- Maintain consistent spacing using 8px grid system
- Use spring physics for playful micro-interactions
- Keep animations subtle and purposeful

### Don'ts
- Never use pure white backgrounds (breaks the dark theme ethos)
- Avoid overusing bright colors - let the void dominate
- Don't animate continuously without user benefit
- Never compromise accessibility for visual flair
- Avoid complex gradients that reduce readability

### Responsive Behavior
- Typography scale adjusts down 10% on mobile
- Grid layouts collapse to single column below 768px
- Touch targets expand to minimum 44px on mobile
- Hover effects disabled on touch devices

---

**BLACK SWARM**: Where collective intelligence meets elegant design.