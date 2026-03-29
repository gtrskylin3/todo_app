# UI Bug Fix Prompt — TODO App Visual Issues

## Context
You are fixing visual bugs and inconsistencies in a PyQt6 TODO application. The app has a dark theme design system (see design.md) but current implementation has several visual artifacts and inconsistencies.

## Screenshots Analysis
Two screenshots show the current broken state:
1. **Active Tasks Tab** — Shows task list with checkbox artifacts
2. **Completed Tasks Tab** — Shows different background color, inconsistent styling

---

## Critical Issues to Fix

### 1. Tab Widget Styling (HIGH PRIORITY)
**Problem:** Tab bar has white background instead of dark theme
**Current:** White/light gray tabs with black text
**Expected:** Dark tabs matching design.md specification

**Fix Requirements:**
```css
QTabWidget::pane {
    border: none;
    background-color: #0D0D0D;  /* Void Black */
}

QTabBar::tab {
    background-color: #1A1A1A;  /* Surface Dark */
    color: #A0A0A0;  /* Muted Gray */
    padding: 12px 24px;
    border: none;
    border-bottom: 2px solid transparent;
}

QTabBar::tab:selected {
    background-color: #0D0D0D;  /* Match main background */
    color: #FFFFFF;  /* Pure White */
    border-bottom: 2px solid #8B5CF6;  /* Nebula Purple */
}

QTabBar::tab:hover:!selected {
    background-color: #242424;  /* Surface Light */
}
```

---

### 2. Checkbox Artifacts (HIGH PRIORITY)
**Problem:** White/light artifacts visible around checkbox borders
**Current:** Checkboxes have unwanted white outlines or rendering artifacts
**Expected:** Clean checkboxes with proper dark theme styling

**Fix Requirements:**
```css
QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 2px solid #6B6B6B;  /* Dim Gray */
    border-radius: 4px;
    background-color: #1A1A1A;
}

QCheckBox::indicator:hover {
    border: 2px solid #8B5CF6;  /* Nebula Purple */
}

QCheckBox::indicator:checked {
    background-color: #10B981;  /* Success Green */
    border: 2px solid #10B981;
    image: url(assets/checkmark.svg);  /* Or use Unicode ✓ */
}

QCheckBox::indicator:disabled {
    background-color: #242424;
    border: 2px solid #333333;
}
```

**Additional Fix:** Ensure no `QPalette` white colors are set on checkbox widgets. Check for:
```python
# REMOVE any code like:
checkbox.setPalette(QPalette(Qt.white))  # ❌
checkbox.setStyleSheet("background: white")  # ❌

# USE instead:
checkbox.setStyleSheet("""
    QCheckBox { color: #FFFFFF; }
    QCheckBox::indicator { ... }
""")
```

---

### 3. Background Color Inconsistency (HIGH PRIORITY)
**Problem:** Completed Tasks tab has noticeably lighter/different background
**Current:** Active = `#0D0D0D`, Completed = `#1A1A1A` (or similar mismatch)
**Expected:** Both tabs use identical `#0D0D0D` (Void Black) background

**Fix Requirements:**
```python
# In MainWindow or Tab Widget initialization:
self.central_widget.setStyleSheet("""
    background-color: #0D0D0D;
""")

self.active_tab_widget.setStyleSheet("""
    background-color: #0D0D0D;
""")

self.completed_tab_widget.setStyleSheet("""
    background-color: #0D0D0D;  /* MUST MATCH active tab */
""")
```

**Check List:**
- [ ] Main window background
- [ ] Tab widget pane background
- [ ] Individual tab page backgrounds
- [ ] Scroll area backgrounds (if used)
- [ ] Any container widgets (QFrame, QWidget)

---

### 4. Task Card Border Issues (MEDIUM PRIORITY)
**Problem:** Task cards have inconsistent or visible border artifacts
**Current:** Cards show light borders or double borders
**Expected:** Clean 1px border `#242424` with 8px radius

**Fix Requirements:**
```css
QFrame#taskCard {
    background-color: #1A1A1A;  /* Surface Dark */
    border: 1px solid #242424;  /* Surface Light */
    border-radius: 8px;
    padding: 16px;
    margin: 4px 0;
}

QFrame#taskCard:hover {
    background-color: #242424;
    border: 1px solid #333333;
}
```

---

### 5. Input Field Styling (MEDIUM PRIORITY)
**Problem:** Input field may have light artifacts or inconsistent styling
**Expected:** Match design.md specification

**Fix Requirements:**
```css
QLineEdit#taskInput {
    background-color: #1A1A1A;
    border: 1px solid #242424;
    border-radius: 8px;
    padding: 12px 16px;
    color: #FFFFFF;
    font-size: 14px;
    font-family: "Inter", sans-serif;
}

QLineEdit#taskInput:focus {
    border: 2px solid #8B5CF6;
    background-color: #1A1A1A;
}

QLineEdit#taskInput::placeholder {
    color: #6B6B6B;
}
```

---

### 6. Button Styling (MEDIUM PRIORITY)
**Problem:** Add button may not match gradient specification
**Expected:** Purple gradient per design.md

**Fix Requirements:**
```css
QPushButton#addButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #8B5CF6, stop:1 #7C3AED);
    border: none;
    border-radius: 8px;
    padding: 12px 32px;
    color: #FFFFFF;
    font-size: 14px;
    font-weight: 600;
}

QPushButton#addButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #9B6CF6, stop:1 #8C4AED);
}

QPushButton#addButton:pressed {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #7C3AED, stop:1 #6D28D9);
}
```

---

### 7. Date Badge Styling (LOW PRIORITY)
**Problem:** Date badges may have inconsistent styling
**Expected:** Subtle gray badge with proper padding

**Fix Requirements:**
```css
QLabel#dateBadge {
    background-color: #242424;
    color: #A0A0A0;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 12px;
}
```

---

### 8. Completed Task Date Header (LOW PRIORITY)
**Problem:** Date group header in Completed tab needs proper styling
**Expected:** Darker background with expand/collapse arrow

**Fix Requirements:**
```css
QFrame#dateHeader {
    background-color: #141414;
    border: 1px solid #242424;
    border-radius: 6px;
    padding: 12px 16px;
}

QLabel#dateHeaderTitle {
    color: #FFFFFF;
    font-size: 16px;
    font-weight: 600;
}

QLabel#dateHeaderCount {
    color: #A0A0A0;
    font-size: 12px;
}
```

---

## Implementation Checklist

### Step 1: Audit Current Styles
- [ ] Search all `.py` files for hardcoded colors
- [ ] Find all `setStyleSheet()` calls
- [ ] Identify QPalette modifications
- [ ] Check for any light theme remnants

### Step 2: Create Centralized Stylesheet
- [ ] Create `styles/qss/main.qss` file
- [ ] Move all QSS to single location
- [ ] Use design.md color tokens consistently
- [ ] Add comments referencing design.md sections

### Step 3: Apply Fixes
- [ ] Fix tab widget styling
- [ ] Fix checkbox rendering
- [ ] Fix background consistency
- [ ] Fix task card borders
- [ ] Fix input field styling
- [ ] Fix button gradients
- [ ] Fix date badges
- [ ] Fix completed task headers

### Step 4: Verify
- [ ] Both tabs have identical background `#0D0D0D`
- [ ] No white artifacts on any element
- [ ] Checkboxes render cleanly at all sizes
- [ ] Hover states work correctly
- [ ] Focus states visible and purple
- [ ] Test at different window sizes

### Step 5: Test Edge Cases
- [ ] Empty state (no tasks)
- [ ] Many tasks (scrolling)
- [ ] Min/max window size
- [ ] High DPI displays
- [ ] Dark/Light OS theme (should not affect app)

---

## Code Quality Requirements

1. **No Inline Styles:** All styling must be in `.qss` files or centralized style manager
2. **Color Tokens:** Use constants from `styles/colors.py`, not hardcoded hex values
3. **Documentation:** Comment each QSS section with design.md reference
4. **Testing:** Screenshot comparison before/after fixes

---

## Expected Final State

| Element | Current | Expected |
|---------|---------|----------|
| Tab Background | White `#FFFFFF` | Dark `#0D0D0D` |
| Tab Text (inactive) | Black | Muted Gray `#A0A0A0` |
| Tab Text (active) | Black | White `#FFFFFF` |
| Tab Indicator | None | Purple `#8B5CF6` |
| Checkbox Border | White artifacts | Dim Gray `#6B6B6B` |
| Checkbox Checked | Purple | Green `#10B981` |
| Active Tab BG | `#0D0D0D` | `#0D0D0D` |
| Completed Tab BG | `#1A1A1A` (wrong) | `#0D0D0D` (match) |
| Task Card Border | Inconsistent | `#242424` |
| Input Focus | Unknown | Purple glow |

---

## Deliverables

1. Fixed `main.qss` stylesheet file
2. Updated `colors.py` with all design tokens
3. Modified widget initialization code (remove inline styles)
4. Before/after screenshots for verification
5. List of all files modified

---

## Reference Files
- `design.md` — Complete design system specification
- `styles/colors.py` — Color token definitions
- `styles/qss/` — QSS stylesheet directory
- `src/presentation/widgets/` — Custom widget implementations

---

**Priority:** HIGH — These are visual bugs that affect first impressions
**Estimated Time:** 2-4 hours
**Risk:** Low — CSS/QSS changes are reversible
```

---

## Краткое резюме проблем (для быстрой передачи разработчику)

| # | Проблема | Приоритет | Решение |
|---|----------|-----------|---------|
| 1 | Белые табы (Active/Completed) | 🔴 HIGH | QTabBar QSS с тёмным фоном |
| 2 | Артефакты у чекбоксов | 🔴 HIGH | QCheckBox::indicator стили + убрать QPalette |
| 3 | Разный фон вкладок | 🔴 HIGH | Унифицировать `#0D0D0D` везде |
| 4 | Границы карточек задач | 🟡 MEDIUM | 1px solid `#242424`, radius 8px |
| 5 | Input field стили | 🟡 MEDIUM | Добавить focus glow фиолетовый |
| 6 | Градиент кнопки Add | 🟡 MEDIUM | `#8B5CF6` → `#7C3AED` |
| 7 | Date badge | 🟢 LOW | `#242424` фон, `#A0A0A0` текст |
| 8 | Заголовки дат в Completed | 🟢 LOW | `#141414` фон, стрелка expand |
