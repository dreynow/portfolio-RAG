---
description: Style guide for the portfolio project frontend
---

# Style Guide

This document defines the visual design system and styling conventions for the portfolio project.

## Framework

- **CSS Framework**: Tailwind CSS (via CDN)
- **Font**: Inter (Google Fonts) - weights 300, 400, 500, 600

## Color Palette

### Primary Colors

| Token | Value | Usage |
| :--- | :--- | :--- |
| `bg-primary` | `#1f201f` | Main background color |
| `accent-color` | `#D2691E` | Primary accent (chocolate) |
| `accent-glow` | `rgba(210, 105, 30, 0.5)` | Glow effects |

### Accent Gradient

Used for logo and decorative elements:
```
Light: #E89050
Dark: #8B4513
```

### Text Colors

| Usage | Value |
| :--- | :--- |
| Primary text | `#E8E8E8` |
| Secondary text | `#A0A0A0` |
| Headings | `#FFFFFF` |

### Message Colors

| Type | Background |
| :--- | :--- |
| User message | `linear-gradient(135deg, #4a4c4a, #3d3f3d)` |
| AI message | `glass-card` (see below) |

## Custom Utilities

### Glass Card
```css
.glass-card {
    @apply bg-white/5 backdrop-blur-xl border border-white/10 shadow-2xl;
}
```

### Mask Fade (for scroll containers)
```css
.mask-fade {
    mask-image: linear-gradient(to bottom, transparent 0%, black 5%, black 100%);
}
```

### Hidden Scrollbar
```css
.scrollbar-none {
    scrollbar-width: none;  /* Firefox */
    -ms-overflow-style: none;  /* IE/Edge */
}
.scrollbar-none::-webkit-scrollbar {
    display: none;  /* Chrome/Safari */
}
```

## Animations

| Name | Duration | Usage |
| :--- | :--- | :--- |
| `fadeIn` | 1s ease-out | Initial element appearance |
| `slideUp` | 0.3s ease-out | Message entry |
| `wave` | 1.5s infinite | Wave hand icon |
| `typewriter` | 2s steps(30) | Heading text reveal |
| `typing` | 1.4s infinite | Loading indicator dots |
| `pulse-glow` | 3s infinite | Aura glow effect |

## Component Patterns

### Message Bubbles
- Max width: 85% (mobile), 80% (desktop)
- Padding: `p-3` (mobile), `p-4` (desktop)
- Border radius: `rounded-xl` with corner variant (`rounded-br-sm` for user, `rounded-bl-sm` for AI)
- AI messages include an icon with the DS logo

### Input Area
- Fixed positioning, centered
- Backdrop blur with semi-transparent background
- Border: `border-accent-color/20`
- Transitions position from `bottom-[35vh]` to `bottom-5` when chat is active

### Logo
- SVG with gradient stroke
- Drop shadow using accent glow color
- Scales: 80px (mobile), 120px (desktop)

## Responsive Breakpoints

| Breakpoint | Target |
| :--- | :--- |
| Default | Mobile-first |
| `md:` (768px+) | Tablet/Desktop |

## Best Practices

1. **Use Tailwind classes** - Avoid inline styles; use Tailwind utilities
2. **Respect the color tokens** - Always use defined colors, not arbitrary hex values
3. **Maintain glass morphism** - Use backdrop blur and semi-transparent backgrounds for cards
4. **Smooth transitions** - Add `transition-all duration-400` for interactive elements
5. **Mobile-first** - Design for mobile, enhance for desktop with `md:` prefix
