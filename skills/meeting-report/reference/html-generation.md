# HTML Meeting Report Generation Guide

## Overview

The meeting-report skill can optionally generate modern HTML reports alongside Markdown, featuring:
- Responsive design with dark/light mode toggle
- Modern aesthetics with smooth transitions
- CSS-based diagram rendering
- Mobile-first approach

## Enabling HTML Generation

Create `.meeting-reports.json` in project root:

```json
{
  "htmlGeneration": true
}
```

Or add to `package.json`:

```json
{
  "meetingReports": {
    "htmlGeneration": true
  }
}
```

## Design System

### Color Palette

**Light Mode:**
- Background: #f9fafb
- Content: #ffffff
- Text: #1f2937
- Accent: #3b82f6
- Success: #10b981
- Warning: #f59e0b  
- Error: #ef4444

**Dark Mode:**
- Background: #111827
- Content: #1f2937
- Text: #f3f4f6
- Accent: #60a5fa
- Success: #34d399
- Warning: #fbbf24
- Error: #f87171

### Typography

- Body: Segoe UI, Helvetica, Arial, sans-serif
- Headings: Georgia, serif
- Line height: 1.6
- Responsive font sizes

### Components

1. **Header** - Meeting title, date, organizer with theme toggle button
2. **Participants** - Highlighted section with accent border
3. **Topics** - Card-based layout with sections for decisions, attention points, problems
4. **Diagrams** - CSS-based flowcharts replacing Mermaid

## Implementation Details

### Theme Toggle

- Button in top-right corner (sun/moon icon)
- Persists choice in localStorage
- Respects system preference as default
- Smooth 200ms transitions

### Diagram Conversion

Mermaid flowcharts are converted to HTML/CSS:

**Input (Mermaid):**
```
flowchart TD
  A[Step 1] --> B[Step 2]
  B --> C[Step 3]
```

**Output (HTML/CSS):**
- Vertical flex layout
- Rounded boxes for steps
- Arrow indicators between steps
- Color-coded by type

### Responsive Design

- Container max-width: 900px
- Mobile breakpoint: 768px
- Flexible metadata layout
- Touch-friendly buttons (44px min)

## File Output

HTML file is written to same location as Markdown:
- Same filename (replace .md with .html)
- Same collision handling (append -2, -3 if exists)
- Silent generation (no workflow interruption)

## Error Handling

If HTML generation fails:
- Log warning internally
- Continue with Markdown delivery
- Markdown is always the source of truth
- HTML is enhancement, not requirement
