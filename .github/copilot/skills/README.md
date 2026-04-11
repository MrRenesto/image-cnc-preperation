# Senior Engineer Code Refactoring Skill

A custom GitHub Copilot skill that reviews your codebase from a senior engineer's perspective, identifying opportunities for refactoring and improving code organization.

## What It Does

This skill analyzes your codebase and:
- ✅ Identifies files that are too large (exceeding recommended line counts)
- ✅ Detects violations of Single Responsibility Principle
- ✅ Finds code duplication and opportunities for extraction
- ✅ Suggests better file and directory organization
- ✅ Proposes refactoring following SOLID principles and best practices
- ✅ Implements refactoring while preserving functionality

## How to Use

### Basic Usage

Simply mention the skill in your conversation with Copilot:

```
@senior-engineer-refactor
```

This will trigger a comprehensive code review of your project.

### With Parameters

You can customize the behavior with parameters:

```
@senior-engineer-refactor --max_lines 200
```

This sets a stricter line limit (200 instead of default 300).

```
@senior-engineer-refactor --auto_implement
```

This automatically implements refactoring suggestions without asking for confirmation.

### Example Conversations

**Example 1: Basic Review**
```
You: @senior-engineer-refactor
Copilot: I'll review your codebase as a senior engineer...
         
         Current Analysis:
         - main.py: 298 lines ✅ (under 300 limit)
         - image_processor.py: 99 lines ✅
         
         Observations:
         - main.py contains both UI and business logic
         - Multiple edge detection algorithms could be organized better
         
         Refactoring Proposal:
         1. Extract edge detection algorithms to separate module
         2. Create services layer for image processing logic
         3. Keep UI-only code in main.py
```

**Example 2: Specific Request**
```
You: The main.py file is getting large. Can you refactor it?
     @senior-engineer-refactor
     
Copilot: I'll refactor main.py with a senior engineer's approach...
```

**Example 3: After Adding New Features**
```
You: I just added a lot of new features. Please review and refactor if needed.
     @senior-engineer-refactor --max_lines 250
```

## What Gets Checked

### File Size Limits
- **Python**: 300 lines per file (configurable)
- **JavaScript/TypeScript**: 250 lines per file
- **Java/C#**: 400 lines per file

### Code Quality Checks
- Single Responsibility Principle adherence
- Separation of concerns (UI vs. business logic vs. data)
- Code duplication
- Proper use of directories and modules
- SOLID principles
- DRY (Don't Repeat Yourself)

### Refactoring Strategies Applied
- Extract classes/modules
- Apply design patterns (Strategy, Factory, etc.)
- Organize by feature or architectural layer
- Extract common utilities
- Improve naming and documentation

## Expected Output

When you use this skill, you'll receive:

1. **Current State Analysis**
   - File sizes and line counts
   - Issues identified
   - Code smells detected

2. **Refactoring Proposal**
   - Proposed new structure
   - Files to create/modify
   - Clear rationale for changes

3. **Implementation Plan**
   - Step-by-step actions
   - Order of operations
   - Risk assessment

4. **Implementation** (if confirmed or auto_implement is true)
   - Creates new files
   - Moves code to appropriate locations
   - Updates imports
   - Validates functionality

## File Structure

```
.github/copilot/skills/
├── senior-engineer-refactor.yml     # Skill configuration
├── senior-engineer-refactor.md      # Detailed guidelines and instructions
└── README.md                        # This file
```

## Typical Refactoring Example

**Before:**
```
project/
└── src/
    ├── main.py (500 lines - UI + business logic + utilities)
    └── image_processor.py (150 lines)
```

**After:**
```
project/
└── src/
    ├── ui/
    │   └── main_window.py (200 lines - UI only)
    ├── services/
    │   ├── image_service.py (150 lines - business logic)
    │   └── edge_detection_service.py (100 lines)
    ├── processors/
    │   └── image_processor.py (150 lines)
    ├── utils/
    │   └── image_utils.py (50 lines)
    └── main.py (50 lines - entry point)
```

## Best Practices Enforced

- **DRY**: No code duplication
- **SOLID**: Following object-oriented design principles
- **Clear Naming**: Descriptive and unambiguous names
- **Consistent Style**: Following language-specific conventions (PEP 8 for Python)
- **Documentation**: Proper docstrings and comments
- **Testing**: Ensures tests pass after refactoring

## Notes

- The skill will always ask for confirmation before making major changes (unless `--auto_implement` is used)
- All refactoring preserves existing functionality
- Tests are run after refactoring to ensure nothing broke
- Changes are made incrementally with clear commit messages

## Contributing

Found an issue or want to improve this skill? The skill files are located in `.github/copilot/skills/`.

## Version

Current version: 1.0.0
