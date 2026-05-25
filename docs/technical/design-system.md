# Design System

## CSS Custom Properties (Design Tokens)

All design values are defined as CSS custom properties in the `:root` selector of `styles.css`.

### Colors

```css
--pid-sage:         #7DA69E   /* Primary brand color */
--pid-sage-light:   #A8C4BE   /* Hover/light variant */
--pid-sage-dark:    #5B8880   /* Active/dark variant */
--pid-navy:         #1E3A5F   /* Secondary, headers */
--pid-navy-light:   #2D5080
--pid-navy-dark:    #0F1E30
--pid-gold:         #C4973B   /* Accent, highlights */
--pid-gold-light:   #D4AB57
--pid-cream:        #F9F6F1   /* Section backgrounds */
--pid-cream-dark:   #EDE8E0
--pid-white:        #FFFFFF
--pid-text:         #1C1C1E   /* Body text */
--pid-text-muted:   #717171   /* Secondary text */
```

### Typography

```css
--font-display:  'Playfair Display', Georgia, serif
--font-body:     'Lato', 'Helvetica Neue', sans-serif

/* Fluid sizes using clamp() */
--text-xs:    clamp(0.75rem, 1vw, 0.875rem)
--text-sm:    clamp(0.875rem, 1.2vw, 1rem)
--text-base:  clamp(1rem, 1.5vw, 1.125rem)
--text-lg:    clamp(1.125rem, 2vw, 1.375rem)
--text-xl:    clamp(1.375rem, 2.5vw, 1.75rem)
--text-2xl:   clamp(1.75rem, 3.5vw, 2.25rem)
--text-3xl:   clamp(2.25rem, 5vw, 3rem)
--text-4xl:   clamp(3rem, 6vw, 4rem)
```

### Spacing Scale

```css
--space-1:   0.25rem   /*  4px */
--space-2:   0.5rem    /*  8px */
--space-3:   0.75rem   /* 12px */
--space-4:   1rem      /* 16px */
--space-6:   1.5rem    /* 24px */
--space-8:   2rem      /* 32px */
--space-12:  3rem      /* 48px */
--space-16:  4rem      /* 64px */
--space-24:  6rem      /* 96px */
--space-32:  8rem      /* 128px */
```

### Shadows

```css
--shadow-sm:    0 1px 3px rgba(0,0,0,0.08)
--shadow-md:    0 4px 16px rgba(0,0,0,0.10)
--shadow-lg:    0 8px 32px rgba(0,0,0,0.12)
--shadow-xl:    0 16px 48px rgba(0,0,0,0.16)
--shadow-navy:  0 8px 32px rgba(30,58,95,0.25)
--shadow-sage:  0 8px 24px rgba(125,166,158,0.30)
```

## Component Classes

| Class | Description |
|-------|-------------|
| `.btn-primary` | Sage green filled button |
| `.btn-secondary` | Outline button |
| `.btn-ghost` | Transparent button, white text |
| `.section` | Standard section padding |
| `.container` | Max-width centered container |
| `.section-title` | Playfair Display heading |
| `.section-subtitle` | Lato muted subtitle |
| `.card` | Standard card with shadow |
| `.badge` | Small label/tag element |
