# Coding Agent Implementation Plan: Folder Management Tool Enhancement

---

# PHASE 0: Research & Discovery

**Purpose:** Document the research journey that led to this implementation plan.

---

## 0.1: Exploration of Existing Codebase (Prompt 1)

### Files Explored

**Core Agent Architecture:**
- `src/agent/agent.py` - Agent initialization and tool registration patterns
  - Pattern: Tools registered via `@agent.tool` decorator
  - Pattern: Agent uses Pydantic AI for tool orchestration

**Similar Existing Tool:**
- `src/tools/obsidian_note_manager/` - Pattern to follow for folder management
  - `tool.py`: Enhanced agent-friendly docstrings with "Use this when" / "Do NOT use" sections
  - `schemas.py`: Pydantic models with validation (@model_validator)
  - `service.py`: Business logic with structured logging, async operations

**Shared Utilities:**
- `src/shared/vault_security.py` - Path validation (`validate_vault_path()`)
- `src/shared/logging.py` - Structured logging (`get_logger()`)
- `src/shared/config.py` - Configuration and system prompt

### Key Patterns Discovered

**Pattern 1: Agent-Friendly Tool Docstrings**
- Comprehensive "Use this when" section (3-5 specific scenarios)
- Strong "Do NOT use this for" section pointing to correct alternatives
- Performance notes with token estimates
- Examples with realistic data (not "foo"/"bar")

**Pattern 2: Path Validation**
- All paths validated via `validate_vault_path(vault_root, user_path)`
- Security checks prevent path traversal, absolute paths
- Vault boundary enforcement

**Pattern 3: Async Operations**
- `aioshutil` for async file operations
- `aiofiles` for async file I/O
- No blocking operations

**Pattern 4: Cross-Platform Compatibility**
- Use `pathlib.Path` (not `os.path`)
- Normalize paths to forward slashes
- Validate Windows reserved names

---

## 0.2: Implementation Options Analysis (Prompt 2)

### Research Question
How should we build folder operations for the Obsidian vault? What are the tradeoffs?

### Option 1: Extend Existing note_manage Tool
- **Description:** Add folder operations to the existing `obsidian_note_manage` tool
- **Pros:**
  - Single tool for all file system operations
  - No need to teach agent about tool boundaries
  - Simpler mental model (one tool for vault manipulation)
- **Cons:**
  - Tool confusion - agent may use wrong operations
  - Mixed responsibilities (content vs. structure)
  - Harder to maintain clear boundaries
  - Risk of breaking existing note operations
- **Effort:** Medium (modifying existing tool)
- **Precedent:** No precedent in codebase (each tool has clear scope)

### Option 2: Create Dedicated folder_manage Tool ✅ RECOMMENDED
- **Description:** Build a new `obsidian_folder_manage` tool specifically for folder operations
- **Pros:**
  - Clear separation of concerns (folders vs. notes)
  - Agent can select tool based on path (.md extension → note_manage, no extension → folder_manage)
  - Easier to maintain and test separately
  - Follows existing pattern of focused, single-purpose tools
  - No risk of breaking existing functionality
- **Cons:**
  - Agent needs to learn when to use which tool
  - More tools in the system
- **Effort:** Medium (new tool creation)
- **Precedent:** ✅ Follows pattern from note_manage, vault_query, graph_analyze

### Option 3: Generic Resource Manager
- **Description:** Create a generic tool that handles both files and folders
- **Pros:**
  - Most flexible
  - Could handle any vault resource
- **Cons:**
  - Too abstract - agent will be confused
  - Harder to provide clear guidance
  - Goes against single-responsibility principle
- **Effort:** High (complex abstraction)
- **Precedent:** ❌ No precedent in codebase

### Selected Approach: Option 2 (Dedicated folder_manage Tool)

**Rationale:**
1. **Separation of concerns:** Folders = structure, Notes = content
2. **Clear tool selection:** Path extension determines tool (`.md` → note_manage, no extension → folder_manage)
3. **Maintainability:** Easier to test and modify in isolation
4. **Consistency:** Follows existing codebase pattern of focused tools
5. **Lower risk:** No impact on existing note operations

**Tool Boundaries:**
- `obsidian_folder_manage`: CREATE, RENAME, MOVE, DELETE, LIST, ARCHIVE folders
- `obsidian_note_manage`: CREATE, READ, UPDATE, PATCH, APPEND, DELETE notes
- Path validation layer rejects `.md` files from folder_manage

---

## 0.3: Technology & Library Research (Prompt 3)

### Required Libraries

**1. aioshutil**
- **Purpose:** Async file system operations (move, copy, delete folders)
- **Why Needed:** Non-blocking folder operations for archive/move/delete
- **Already in Project:** ✅ Yes (check `pyproject.toml`)
- **Cross-Platform:** ✅ Windows, Linux, macOS
- **Async Support:** ✅ Yes (primary purpose)
- **Documentation:** https://aioshutil.readthedocs.io/
  - Key sections: `async def move()`, `async def copytree()`, `async def rmtree()`
  - Relevant features: Async wrappers for all shutil operations
- **Usage in feature:**
  - Archive operation: `await aioshutil.move(source, destination)`
  - Move operation: `await aioshutil.move(source, destination)`
  - Delete operation: `await aioshutil.rmtree(path)`

**2. pathlib (Built-in)**
- **Purpose:** Cross-platform path handling
- **Why Needed:** Windows uses backslashes, Unix uses forward slashes - pathlib abstracts this
- **Already in Project:** ✅ Yes (built-in Python library)
- **Cross-Platform:** ✅ Windows, Linux, macOS
- **Documentation:** https://docs.python.org/3/library/pathlib.html
  - Key sections: `Path` class, `resolve()`, `relative_to()`
  - Best practices: Always use `pathlib.Path`, not `os.path`
- **Usage in feature:**
  - Path manipulation: `full_path = Path(vault_root) / Path(user_path)`
  - Normalization: `str(path).replace("\\", "/")`

**3. datetime (Built-in)**
- **Purpose:** Generate date-based archive paths
- **Why Needed:** Archive operation creates `archive/YYYY-MM-DD/folder` structure
- **Already in Project:** ✅ Yes (built-in)
- **Cross-Platform:** ✅ Windows, Linux, macOS
- **Usage in feature:**
  - Archive paths: `datetime.now().strftime("%Y-%m-%d")`
  - Custom formats: Configurable via `date_format` parameter

**4. pydantic (Already in Project)**
- **Purpose:** Request/response validation
- **Why Needed:** Validate folder operation requests, enum validation
- **Already in Project:** ✅ Yes (core dependency)
- **Usage in feature:**
  - Schema validation: `ManageFolderRequest` model
  - Enum validation: `FolderOperation` enum

### Cross-Platform Compatibility

**Windows:**
- ✅ aioshutil works on Windows
- ✅ pathlib handles backslashes automatically
- ⚠️ Must validate Windows reserved names (CON, PRN, AUX, NUL, COM1-9, LPT1-9)
- ⚠️ Must normalize paths to forward slashes for Obsidian compatibility

**macOS:**
- ✅ All libraries compatible
- ⚠️ Unicode normalization (NFD vs NFC for accented characters)
- ✅ Case-sensitive filesystem (APFS)

**Linux:**
- ✅ All libraries compatible
- ✅ Case-sensitive filesystem
- ✅ Symlink support with `pathlib.Path.is_symlink()`

**Implementation Considerations:**
1. Always normalize paths to forward slashes (Obsidian standard)
2. Validate against most restrictive platform (Windows) even on Linux/macOS
3. Use async operations throughout (no blocking I/O)
4. Test on all three platforms via CI/CD matrix

---

## 0.4: Constraints & Requirements (Prompt 4)

### Security Constraints

**Vault Boundary Enforcement:**
- ✅ All folder operations MUST be restricted to vault path specified in `.env`
- ✅ Load vault path from `VAULT_PATH` environment variable
- ✅ Validate all paths using `validate_vault_path(vault_root, user_path)`
- ✅ Reject absolute paths outside vault (`/etc/passwd`, `C:\Windows`)
- ✅ Reject path traversal attempts (`../../../etc/passwd`)
- ✅ Protect sensitive folders (`.obsidian`, `.git`, `.env`)

**Implementation:**
```python
# In service.py
full_path_str = validate_vault_path(vault_path, request.path)  # Raises SecurityError if invalid
full_path = Path(full_path_str)
vault_root = Path(vault_path).resolve()

# Ensure operation stays within vault
if not full_path.resolve().is_relative_to(vault_root):
    raise SecurityError("Operation outside vault boundary")
```

### Input Validation

**Path Validation:**
- Reject paths with `.md` extension (those belong to note_manage)
- Reject paths with any file extension (folders don't have extensions)
- Validate Windows reserved names (even on Linux/macOS)
- Validate invalid characters (`<>:"|?*`)

**Operation-Specific Validation:**
- DELETE: Require `confirm_path` matching `path` (prevent accidental deletions)
- RENAME: Validate `new_name` doesn't contain path separators
- MOVE: Detect circular moves (moving folder into itself)
- ARCHIVE: Prevent archiving to existing destination

### Technical Constraints

**Performance Requirements:**
- CREATE: < 50ms target
- RENAME/MOVE/ARCHIVE: < 500ms target (depends on wikilink scanning)
- DELETE: < 200ms target
- LIST: < 100ms for immediate children, < 500ms for recursive

**Token Efficiency:**
- Minimal format: ~50 tokens (operation status only)
- Concise format: ~150 tokens (status + key metadata)
- Detailed format: ~300+ tokens (full details + listings)

**Resource Limits:**
- Wikilink scan: Limited to 1000 notes (configurable)
- LIST recursive: Max depth 5 levels (prevent infinite recursion)
- LIST pagination: Max 200 folders per request

### Business Requirements

**User Story:**
```
As an Obsidian user
I want to archive old project folders with automatic date-based organization
So that I can keep my vault organized without manually creating dated folders
```

**Success Criteria:**
- ✅ Agent reliably distinguishes folder operations from note operations
- ✅ Archive operation creates `archive/YYYY-MM-DD/folder` structure
- ✅ Wikilinks automatically updated on folder rename/move/archive
- ✅ Path validation prevents operations on `.md` files with helpful errors
- ✅ All operations work on Windows, macOS, Linux
- ✅ 90%+ test coverage with comprehensive edge case handling

---

# Implementation Plan

## Mission

Enhance the existing `obsidian_folder_manage` tool to ensure **complete separation** from `obsidian_note_manage` and add **archive operation** with automatic date-based organization. The LLM must reliably distinguish between folder operations (structure) and note operations (content).

---

## Context

### Current State
- ✅ `obsidian_folder_manage` tool exists in `src/tools/obsidian_folder_manager/`
- ✅ Supports: CREATE, RENAME, MOVE, DELETE, LIST operations
- ✅ Has wikilink update functionality
- ✅ 20 passing tests in `tests/tools/obsidian_folder_manager/`
- ⚠️ **Problem**: LLM may confuse folder_manage with note_manage
- ❌ Missing: ARCHIVE operation with auto-dating

### Architecture
```
src/tools/obsidian_folder_manager/
├── tool.py          # Agent tool registration + docstring
├── schemas.py       # Pydantic models (FolderOperation, ManageFolderRequest, etc.)
├── service.py       # Business logic (_create_folder, _rename_folder, etc.)

tests/tools/obsidian_folder_manager/
├── test_service.py  # Unit tests for service operations
```

---

## Objectives

1. **Enforce complete separation** between folder_manage and note_manage (6-layer strategy)
2. **Implement ARCHIVE operation** with automatic date-based paths (`archive/YYYY-MM-DD/folder`)
3. **Ensure cross-platform compatibility** (Windows, macOS, Linux)
4. **Enhance LLM guidance** with strong negative guidance and wrong-tool detection
5. **Add comprehensive tests** for archive operation and separation validation

---

## Part 1: Tool Separation Strategy (6 Layers)

### Layer 1: Path-Level Validation

**File**: `src/tools/obsidian_folder_manager/service.py`

Add validation function at the top of the file:

```python
def validate_folder_path(path: str) -> None:
    """Validate that path is a folder, not a file.

    Args:
        path: Path to validate.

    Raises:
        ValueError: If path appears to be a file (has .md or other extension).
    """
    # Reject paths with note extensions
    if path.endswith(('.md', '.markdown', '.txt')):
        msg = (
            f"❌ Invalid path for folder operation: '{path}'\n\n"
            f"This tool operates on FOLDERS only.\n"
            f"To work with note files, use:\n\n"
            f"obsidian_note_manage(\n"
            f"    path='{path}',\n"
            f"    operation='read',  # or 'update', 'delete', etc.\n"
            f"    response_format='concise'\n"
            f")\n\n"
            f"Tool selection guide:\n"
            f"• Paths ending in .md → obsidian_note_manage\n"
            f"• Paths without extension → obsidian_folder_manage"
        )
        raise ValueError(msg)

    # Also reject if path has any file extension (not just .md)
    path_obj = Path(path)
    if '.' in path_obj.name and not path.endswith('/'):
        extension = path_obj.suffix
        msg = (
            f"❌ Path '{path}' appears to be a file (has extension '{extension}').\n\n"
            f"This tool operates on FOLDERS (directories without extensions).\n"
            f"For file operations, use obsidian_note_manage instead.\n\n"
            f"Examples:\n"
            f"• Folder: 'projects/2025' → obsidian_folder_manage\n"
            f"• File: 'projects/alpha.md' → obsidian_note_manage"
        )
        raise ValueError(msg)
```

**Integration**: Call this function in `manage_folder_service()` right after logging starts:

```python
async def manage_folder_service(
    request: ManageFolderRequest,
    vault_path: str,
    max_folder_depth: int,
    max_wikilink_scan_notes: int,
) -> FolderOperationResult:
    """Execute folder management operation."""
    start_time = time.perf_counter()

    # NEW: Validate this is a folder path, not a file path
    validate_folder_path(request.path)

    # Validate and resolve path
    full_path_str = validate_vault_path(vault_path, request.path)
    # ... rest of function
```

---

### Layer 2: Enhanced Docstring with Strong Negative Guidance

**File**: `src/tools/obsidian_folder_manager/tool.py`

**Replace the entire docstring** for `obsidian_folder_manage` with this enhanced version:

```python
async def obsidian_folder_manage(
    ctx: RunContext["AgentDependencies"],
    path: str,
    operation: str,
    new_name: str | None = None,
    destination: str | None = None,
    create_parents: bool = True,
    force: bool = False,
    confirm_path: str | None = None,
    check_wikilinks: bool = True,
    update_wikilinks: bool = True,
    recursive: bool = False,
    include_stats: bool = True,
    max_results: int = 50,
    offset: int = 0,
    dry_run: bool = False,
    archive_base: str = "archive",
    date_format: str = "%Y-%m-%d",
    response_format: str = "concise",
) -> str:
    """Manage vault folder structure with create, rename, move, delete, list, and archive operations.

    ⚠️ FOLDER OPERATIONS ONLY - This tool operates on DIRECTORIES, not files.

    This consolidated tool enables folder organization and automatically updates
    wikilinks when folders are renamed, moved, or archived to prevent broken links.

    Use this when you need to:
    - Create folder structures for projects or organization (e.g., "projects/2025/website")
    - Rename folders when project names change (auto-updates all wikilinks)
    - Move folders to reorganize vault hierarchy (auto-updates wikilinks)
    - Archive old folders with automatic date-based organization (archive/YYYY-MM-DD/folder)
    - Delete old or empty folders during cleanup
    - List folders with statistics (note count, size, modified date)
    - Reorganize vault structure without manually updating references

    ❌ Do NOT use this for:
    - Reading note content → Use obsidian_note_manage(operation="read") instead
    - Creating/updating note files → Use obsidian_note_manage(operation="update") instead
    - Modifying note frontmatter/metadata → Use obsidian_note_manage(metadata_updates=...) instead
    - Searching for notes → Use obsidian_vault_query instead
    - Batch note operations → Use obsidian_vault_organizer instead
    - ANY operation on .md files → Use obsidian_note_manage instead
    - Finding folders (use LIST operation on this tool, not vault_query)

    🔍 Path Format Rules:
    - ✅ Folder paths: "projects/2025" or "archive" (NO .md extension)
    - ❌ Note paths: "projects/alpha.md" (HAS .md extension) → WRONG TOOL!

    If your path ends in .md, STOP and use obsidian_note_manage instead.

    Args:
        path: Relative path from vault root to the folder.
            Examples: "projects/2025", "archive", "daily/2025/01"
            DO NOT include .md extension - this tool is for folders only.
            DO NOT include vault path - just the relative path within vault.

        operation: Folder operation - "create", "rename", "move", "delete", "list", or "archive".
            - "create": Create new folder (optionally create parent directories)
            - "rename": Rename folder in place (updates wikilinks automatically)
            - "move": Move folder to new location (updates wikilinks automatically)
            - "delete": Delete folder (requires confirmation for safety)
            - "list": List folder contents with optional stats and pagination
            - "archive": Archive folder with automatic date-based path (archive/YYYY-MM-DD/folder)

        new_name: For "rename": new folder name (single component, not full path).
            Example: "website-redesign" not "projects/website-redesign"
            Automatically validates against Windows reserved names (CON, PRN, etc.)
            and invalid characters (<>:"|?*).

        destination: For "move": destination folder path relative to vault root.
            Example: "archive/2024" to move folder into archive/2024/
            Creates destination parent directories automatically if needed.
            Detects and rejects circular moves (moving folder into itself).

        create_parents: For "create": whether to create parent directories.
            - True: Creates all missing parent directories (DEFAULT)
                Example: "projects/2025/new-project" creates all levels
            - False: Fails if parent directory doesn't exist
                Use when: You want to ensure parent structure exists first

        force: For "delete": whether to delete non-empty folders.
            - False: Only delete empty folders, error if contains files (DEFAULT - SAFER)
            - True: Delete folder and all contents recursively (USE WITH CAUTION)
            Safety: Always use False unless you're certain folder should be deleted.

        confirm_path: Required for "delete": must match path parameter exactly.
            Safety mechanism to prevent accidental deletions.
            Example: if path="old-projects", must set confirm_path="old-projects"
            Operation will fail if confirm_path doesn't match path.

        check_wikilinks: For "delete": whether to check for incoming wikilinks.
            - True: Scans vault for notes linking to folder contents, warns about broken links (DEFAULT)
            - False: Skip wikilink check (faster but may break links)
            Returns list of affected notes that would have broken links after deletion.

        update_wikilinks: For "rename"/"move"/"archive": whether to update wikilinks in vault.
            - True: Automatically updates all wikilinks referencing folder contents (DEFAULT)
                Scans all notes and replaces [[old-path/file]] with [[new-path/file]]
            - False: Skip wikilink updates (faster but will break links)
            Token cost: Scan limited to max_wikilink_scan_notes setting (default: 1000 notes)

        recursive: For "list": whether to list subfolders recursively.
            - False: Only immediate children (1 level) (DEFAULT)
            - True: Recursive listing up to max depth (5 levels for safety)
            Use False for quick folder overview, True for complete structure.

        include_stats: For "list": whether to include folder statistics.
            - True: Include note count, total size, modified date (DEFAULT)
                ~20 tokens per folder (slower but informative)
            - False: Only folder names and paths (~10 tokens per folder)
                Use when: Just need folder names, not statistics

        max_results: For "list": maximum folders to return (pagination).
            Range: 1-200, Default: 50
            Use lower values (10-20) for quick overview, higher for complete listing.
            Prevents token explosion on large vault structures.

        offset: For "list": number of results to skip (pagination).
            Default: 0 (start from beginning)
            Use with max_results for pagination: offset=50, max_results=50 for page 2

        dry_run: Simulate operation without making changes.
            - False: Execute operation normally (DEFAULT)
            - True: Show what would happen without modifying vault
            Use for: Testing rename/move/archive operations before executing

        archive_base: For "archive": base folder for archived items.
            Default: "archive" (creates archive/YYYY-MM-DD/folder)
            Custom: "old-projects" (creates old-projects/YYYY-MM-DD/folder)

        date_format: For "archive": date format for archive path.
            Default: "%Y-%m-%d" (ISO format: 2025-01-16)
            Custom: "%Y/%m" (year/month: 2025/01)

        response_format: Control output verbosity to save tokens.
            - "minimal": Operation status only (~50 tokens)
                Use when: Just need confirmation of success
            - "concise": Status + key metadata (~150 tokens)
                Use when: Need summary of what changed (DEFAULT)
            - "detailed": Status + full metadata + folder listings (~300+ tokens)
                Use when: Need complete operation details

    Returns:
        Formatted string with operation result:
        - Success/failure status
        - New path for rename/move/archive operations
        - Wikilink update count for rename/move/archive operations
        - Folder list with stats for list operation
        - Warnings about broken links for delete operation
        - Token estimate for optimization tracking

    Performance Notes:
        - CREATE: 10-50ms, ~50 tokens
        - RENAME: 50-500ms (depends on wikilink scan), ~80 tokens
        - MOVE: 50-500ms (depends on wikilink scan), ~80 tokens
        - ARCHIVE: 50-500ms (depends on wikilink scan), ~80 tokens
        - DELETE: 50-200ms, ~50-100 tokens (more if wikilinks checked)
        - LIST minimal: 50-100ms, ~50 tokens + 10 per folder
        - LIST detailed: 100-500ms, ~150 tokens + 40 per folder
        - Wikilink updates: Limited to max_wikilink_scan_notes (default: 1000 notes)
        - LIST recursive: Depth limited to 5 levels (safety)
        - Max results: Capped at 200 folders per request

    Examples:
        # Create nested project structure
        obsidian_folder_manage(
            path="projects/2025/website-redesign",
            operation="create",
            create_parents=True
        )

        # Rename folder and update all wikilinks
        obsidian_folder_manage(
            path="projects/alpha",
            operation="rename",
            new_name="website-redesign",
            update_wikilinks=True
        )

        # Move folder to archive (with wikilink updates)
        obsidian_folder_manage(
            path="projects/completed-project",
            operation="move",
            destination="archive/2024",
            update_wikilinks=True
        )

        # Archive old project with automatic dating
        obsidian_folder_manage(
            path="projects/2023/old-website",
            operation="archive"
        )
        # → Moves to: archive/2025-01-16/old-website
        # → Updates all wikilinks automatically

        # Archive with custom base folder
        obsidian_folder_manage(
            path="drafts/abandoned-idea",
            operation="archive",
            archive_base="old-drafts"
        )
        # → Moves to: old-drafts/2025-01-16/abandoned-idea

        # Delete empty folder
        obsidian_folder_manage(
            path="drafts/old",
            operation="delete",
            confirm_path="drafts/old",
            force=False
        )

        # Delete non-empty folder with wikilink check
        obsidian_folder_manage(
            path="projects/abandoned",
            operation="delete",
            confirm_path="projects/abandoned",
            force=True,
            check_wikilinks=True
        )

        # List immediate children with stats
        obsidian_folder_manage(
            path="projects",
            operation="list",
            recursive=False,
            include_stats=True,
            response_format="concise"
        )

        # List all subfolders recursively (up to depth 5)
        obsidian_folder_manage(
            path="projects",
            operation="list",
            recursive=True,
            include_stats=True,
            max_results=100
        )

        # Quick folder overview without stats (minimal tokens)
        obsidian_folder_manage(
            path=".",
            operation="list",
            recursive=False,
            include_stats=False,
            response_format="minimal"
        )

        # Test archive operation without executing (dry run)
        obsidian_folder_manage(
            path="projects/test",
            operation="archive",
            dry_run=True
        )
        # → Shows where folder would be archived without moving it

        # Paginated listing (page 2: folders 51-100)
        obsidian_folder_manage(
            path="projects",
            operation="list",
            offset=50,
            max_results=50,
            include_stats=True
        )
    """
```

**Note**: Add `archive_base` and `date_format` parameters to the function signature as shown above.

---

### Layer 3: System Prompt Enhancement

**File**: `src/shared/config.py`

Add this section to `agent_system_prompt` (around line 100, after the tool descriptions):

```python
agent_system_prompt: str = (
    # ... existing prompt ...

    "# Tool Selection Decision Tree\n\n"
    "When user asks to work with something, follow this logic:\n\n"
    "1. Does the path end in .md or have a file extension?\n"
    "   YES → Use obsidian_note_manage\n"
    "   NO → Continue\n\n"
    "2. Does the request mention 'folder', 'directory', 'structure', or 'organize folders'?\n"
    "   YES → Use obsidian_folder_manage\n"
    "   NO → Continue\n\n"
    "3. Does the request want to read/write CONTENT or update METADATA?\n"
    "   YES → Use obsidian_note_manage\n"
    "   NO → Continue\n\n"
    "4. Does the request want to list, create, move, rename, or archive a CONTAINER?\n"
    "   YES → Use obsidian_folder_manage\n\n"
    "# Tool Categories\n\n"
    "STRUCTURE TOOLS (operate on containers):\n"
    "- obsidian_folder_manage: Create, rename, move, delete, list, archive FOLDERS\n\n"
    "CONTENT TOOLS (operate on files):\n"
    "- obsidian_note_manage: Create, read, update, patch, append, delete NOTES\n\n"
    "DISCOVERY TOOLS (find things):\n"
    "- obsidian_vault_query: Search for notes by content/tags/properties\n\n"
    "RELATIONSHIP TOOLS (analyze connections):\n"
    "- obsidian_graph_analyze: Traverse wikilinks and backlinks\n\n"

    # ... rest of existing prompt ...
)
```

---

## Part 2: Archive Operation Implementation

### Step 1: Update Schemas

**File**: `src/tools/obsidian_folder_manager/schemas.py`

Add ARCHIVE to the `FolderOperation` enum (around line 35):

```python
class FolderOperation(str, Enum):
    """Folder operation types for folder management."""

    CREATE = "create"
    """Create a new folder with optional parent directory creation."""

    RENAME = "rename"
    """Rename a folder and update all wikilinks that reference files within it."""

    MOVE = "move"
    """Move a folder to a new location and update all wikilinks."""

    DELETE = "delete"
    """Delete a folder (requires confirmation for safety)."""

    LIST = "list"
    """List folder contents with optional statistics and pagination."""

    ARCHIVE = "archive"
    """Archive a folder with automatic date-based organization (archive/YYYY-MM-DD/folder)."""
```

Add archive parameters to `ManageFolderRequest` (around line 110, after `dry_run`):

```python
class ManageFolderRequest(BaseModel):
    """Request for managing a folder with various operations."""

    # ... existing fields ...

    dry_run: bool = Field(
        default=False,
        description="Simulate operation without making changes (for testing)",
    )

    # ARCHIVE parameters (NEW)
    archive_base: str = Field(
        default="archive",
        description="For ARCHIVE: base folder for archived items (default: 'archive')",
    )

    date_format: str = Field(
        default="%Y-%m-%d",
        description="For ARCHIVE: date format for archive path (default: ISO format YYYY-MM-DD)",
    )

    response_format: ResponseFormat = Field(
        default=ResponseFormat.CONCISE,
        description="Response verbosity: minimal (~50 tokens), concise (~150 tokens), detailed (~300 tokens)",
    )
```

---

### Step 2: Implement Archive Service Function

**File**: `src/tools/obsidian_folder_manager/service.py`

Add the archive operation handler in `manage_folder_service()` (around line 98, after LIST):

```python
async def manage_folder_service(
    request: ManageFolderRequest,
    vault_path: str,
    max_folder_depth: int,
    max_wikilink_scan_notes: int,
) -> FolderOperationResult:
    """Execute folder management operation."""
    start_time = time.perf_counter()

    # NEW: Validate this is a folder path, not a file path
    validate_folder_path(request.path)

    # Validate and resolve path
    full_path_str = validate_vault_path(vault_path, request.path)
    full_path = Path(full_path_str)
    vault_root = Path(vault_path).resolve()

    # ... existing security checks ...

    logger.info(
        "folder_operation_started",
        path=request.path,
        operation=request.operation.value,
        dry_run=request.dry_run,
    )

    # Execute operation
    if request.operation == FolderOperation.CREATE:
        result = await _create_folder(full_path, request, vault_root)

    elif request.operation == FolderOperation.RENAME:
        result = await _rename_folder(
            full_path, request, vault_root, max_wikilink_scan_notes
        )

    elif request.operation == FolderOperation.MOVE:
        result = await _move_folder(
            full_path, request, vault_path, vault_root, max_wikilink_scan_notes
        )

    elif request.operation == FolderOperation.DELETE:
        result = await _delete_folder(full_path, request, vault_root)

    elif request.operation == FolderOperation.LIST:
        result = await _list_folder(full_path, request, vault_root, max_folder_depth)

    elif request.operation == FolderOperation.ARCHIVE:
        result = await _archive_folder(
            full_path, request, vault_path, vault_root, max_wikilink_scan_notes
        )

    duration_ms = (time.perf_counter() - start_time) * 1000

    logger.info(
        "folder_operation_completed",
        path=request.path,
        operation=request.operation.value,
        success=result.success,
        duration_ms=duration_ms,
    )

    return result
```

Add the `_archive_folder()` function at the end of the file (after `_check_incoming_wikilinks`):

```python
async def _archive_folder(
    full_path: Path,
    request: ManageFolderRequest,
    vault_path: str,
    vault_root: Path,
    max_wikilink_scan_notes: int,
) -> FolderOperationResult:
    """Archive folder with automatic date-based organization.

    Creates archive path: {archive_base}/{date_format}/{folder_name}
    Example: archive/2025-01-16/old-project

    Args:
        full_path: Absolute path to folder to archive.
        request: Archive request with archive_base and date_format.
        vault_path: Vault path string for validation.
        vault_root: Vault root path.
        max_wikilink_scan_notes: Maximum notes to scan for wikilink updates.

    Returns:
        FolderOperationResult with archive path and wikilink update count.

    Raises:
        FileNotFoundError: If source folder doesn't exist.
        ValueError: If archive destination already exists.
    """
    # Validate source exists
    if not full_path.exists():
        msg = f"Folder not found: {request.path}"
        raise FileNotFoundError(msg)

    if not full_path.is_dir():
        msg = f"Path is not a folder: {request.path}"
        raise ValueError(msg)

    # Generate archive destination with current date
    from datetime import datetime

    date_str = datetime.now().strftime(request.date_format)
    archive_base = request.archive_base.strip()

    # Build archive path: archive_base/date/folder_name
    archive_dest = Path(archive_base) / date_str / full_path.name
    archive_dest_full = vault_root / archive_dest

    # Check if destination exists
    if archive_dest_full.exists():
        msg = (
            f"Archive destination already exists: {archive_dest}\n"
            f"This folder may have been archived already today.\n"
            f"Options:\n"
            f"  1. Use a different archive_base\n"
            f"  2. Delete the existing archive first\n"
            f"  3. Use operation='move' to manually specify destination"
        )
        raise ValueError(msg)

    # Dry run check
    if request.dry_run:
        return FolderOperationResult(
            success=True,
            path=request.path,
            operation=FolderOperation.ARCHIVE,
            message=f"[DRY RUN] Would archive to {archive_dest}",
            new_path=str(archive_dest).replace("\\", "/"),
            metadata={
                "dry_run": True,
                "archive_path": str(archive_dest).replace("\\", "/"),
                "date": date_str,
            },
            token_estimate=80,
        )

    # Create archive date folder (create parents)
    archive_dest_full.parent.mkdir(parents=True, exist_ok=True)

    # Move folder to archive
    await aioshutil.move(str(full_path), str(archive_dest_full))
    logger.info(
        "folder_archived",
        old_path=str(full_path),
        archive_path=str(archive_dest),
        date=date_str,
    )

    # Update wikilinks if requested
    links_updated = 0
    if request.update_wikilinks:
        old_relative = full_path.relative_to(vault_root)
        new_relative = archive_dest_full.relative_to(vault_root)
        links_updated = await _update_wikilinks_for_folder_rename(
            vault_root, old_relative, new_relative, max_wikilink_scan_notes
        )

    return FolderOperationResult(
        success=True,
        path=request.path,
        operation=FolderOperation.ARCHIVE,
        message=f"Successfully archived {request.path} to {archive_dest}",
        new_path=str(archive_dest).replace("\\", "/"),
        metadata={
            "archive_path": str(archive_dest).replace("\\", "/"),
            "date": date_str,
            "archive_base": archive_base,
            "links_updated": links_updated,
        },
        token_estimate=80,
    )
```

---

### Step 3: Update Tool Registration

**File**: `src/tools/obsidian_folder_manager/tool.py`

Update the function signature to include archive parameters (around line 37):

```python
@agent.tool
async def obsidian_folder_manage(
    ctx: RunContext["AgentDependencies"],
    path: str,
    operation: str,
    new_name: str | None = None,
    destination: str | None = None,
    create_parents: bool = True,
    force: bool = False,
    confirm_path: str | None = None,
    check_wikilinks: bool = True,
    update_wikilinks: bool = True,
    recursive: bool = False,
    include_stats: bool = True,
    max_results: int = 50,
    offset: int = 0,
    dry_run: bool = False,
    archive_base: str = "archive",        # NEW
    date_format: str = "%Y-%m-%d",        # NEW
    response_format: str = "concise",
) -> str:
```

Update the request creation to include archive parameters (around line 270):

```python
# Create request
try:
    request = ManageFolderRequest(
        path=path,
        operation=folder_operation,
        new_name=new_name,
        destination=destination,
        create_parents=create_parents,
        force=force,
        confirm_path=confirm_path,
        check_wikilinks=check_wikilinks,
        update_wikilinks=update_wikilinks,
        recursive=recursive,
        include_stats=include_stats,
        max_results=max_results,
        offset=offset,
        dry_run=dry_run,
        archive_base=archive_base,        # NEW
        date_format=date_format,          # NEW
        response_format=response_format,  # type: ignore[arg-type]
    )
except ValueError as e:
    logger.error("invalid_folder_request", error=str(e), path=path)
    return f"Invalid request: {e}"
```

Update the response formatting section to handle ARCHIVE operation (around line 315):

```python
# Add operation-specific details
if result.new_path:
    response_parts.append(f"New path: {result.new_path}")

# Add metadata based on operation
if folder_operation in {FolderOperation.RENAME, FolderOperation.MOVE, FolderOperation.ARCHIVE}:
    links_updated = result.metadata.get("links_updated", 0)
    if links_updated:
        response_parts.append(f"Wikilinks updated: {links_updated} notes")

    # For ARCHIVE, add date information
    if folder_operation == FolderOperation.ARCHIVE:
        archive_date = result.metadata.get("date")
        if archive_date:
            response_parts.append(f"Archive date: {archive_date}")
```

---

## Part 3: Testing & Validation

### Pre-Deployment Test Suite

| Test Category | # Tests | Duration | Automated | Command |
|---------------|---------|----------|-----------|---------|
| **Path Validation** | 3 tests | ~5 sec | ✅ Yes | `pytest test_service.py::TestSecurityValidation -v` |
| **Archive Operation** | 7 tests | ~10 sec | ✅ Yes | `pytest test_service.py::TestArchiveFolderOperation -v` |
| **Unit Tests (Existing)** | 20+ tests | ~30 sec | ✅ Yes | `pytest tests/tools/obsidian_folder_manager/ -m unit` |
| **Integration Tests** | 10 tests | ~10 sec | ✅ Yes | `pytest tests/integration/ -k folder` |
| **Security Tests** | 6 tests | ~5 sec | ✅ Yes | `pytest tests/security/ -k folder` |
| **Platform Tests** | 9 tests | ~15 min | ✅ Yes (CI/CD) | GitHub Actions matrix |
| **Linting & Type Check** | 4 checks | ~1 min | ✅ Yes | `ruff check` + `mypy --strict` |
| **TOTAL** | **55+ tests** | **~17 min** | **All automated** | See sections below |

**Success Criteria:** All automated tests pass

---

### Test 1: Archive Operation Tests

**File**: `tests/tools/obsidian_folder_manager/test_service.py`

Add a new test class at the end of the file (after existing test classes):

```python
class TestArchiveFolderOperation:
    """Tests for ARCHIVE folder operation."""

    async def test_archive_simple_folder(self, tmp_path):
        """Test archiving folder with default date path."""
        vault = tmp_path / "vault"
        vault.mkdir()
        (vault / "old-project").mkdir()

        request = ManageFolderRequest(
            path="old-project",
            operation=FolderOperation.ARCHIVE,
        )

        result = await manage_folder_service(
            request=request,
            vault_path=str(vault),
            max_folder_depth=10,
            max_wikilink_scan_notes=1000,
        )

        assert result.success is True
        assert "archive/" in result.new_path
        assert "old-project" in result.new_path

        # Verify archive path format: archive/YYYY-MM-DD/old-project
        from datetime import datetime

        date_str = datetime.now().strftime("%Y-%m-%d")
        expected_path = f"archive/{date_str}/old-project"
        assert result.new_path == expected_path

        # Verify folder was moved
        assert not (vault / "old-project").exists()
        assert (vault / "archive" / date_str / "old-project").exists()

    async def test_archive_with_wikilink_updates(self, tmp_path):
        """Test archive updates wikilinks in other notes."""
        vault = tmp_path / "vault"
        vault.mkdir()

        # Create folder with note
        (vault / "projects" / "alpha").mkdir(parents=True)
        (vault / "projects" / "alpha" / "overview.md").write_text("# Overview\n\nContent here")

        # Create note that links to it
        (vault / "index.md").write_text("See [[projects/alpha/overview]] for details")

        request = ManageFolderRequest(
            path="projects/alpha",
            operation=FolderOperation.ARCHIVE,
            update_wikilinks=True,
        )

        result = await manage_folder_service(
            request=request,
            vault_path=str(vault),
            max_folder_depth=10,
            max_wikilink_scan_notes=1000,
        )

        assert result.success is True
        assert result.metadata["links_updated"] == 1

        # Check wikilink was updated
        index_content = (vault / "index.md").read_text()
        from datetime import datetime

        date_str = datetime.now().strftime("%Y-%m-%d")
        assert f"archive/{date_str}/alpha/overview" in index_content
        assert "projects/alpha/overview" not in index_content

    async def test_archive_custom_base(self, tmp_path):
        """Test archive with custom base folder."""
        vault = tmp_path / "vault"
        vault.mkdir()
        (vault / "drafts").mkdir()

        request = ManageFolderRequest(
            path="drafts",
            operation=FolderOperation.ARCHIVE,
            archive_base="old-drafts",
        )

        result = await manage_folder_service(
            request=request,
            vault_path=str(vault),
            max_folder_depth=10,
            max_wikilink_scan_notes=1000,
        )

        assert result.success is True
        assert result.new_path.startswith("old-drafts/")
        assert result.metadata["archive_base"] == "old-drafts"

        # Verify folder was moved to custom base
        from datetime import datetime

        date_str = datetime.now().strftime("%Y-%m-%d")
        assert (vault / "old-drafts" / date_str / "drafts").exists()

    async def test_archive_custom_date_format(self, tmp_path):
        """Test archive with custom date format."""
        vault = tmp_path / "vault"
        vault.mkdir()
        (vault / "temp").mkdir()

        request = ManageFolderRequest(
            path="temp",
            operation=FolderOperation.ARCHIVE,
            date_format="%Y/%m",  # Year/Month instead of Year-Month-Day
        )

        result = await manage_folder_service(
            request=request,
            vault_path=str(vault),
            max_folder_depth=10,
            max_wikilink_scan_notes=1000,
        )

        assert result.success is True

        # Verify custom date format
        from datetime import datetime

        date_str = datetime.now().strftime("%Y/%m")
        expected_path = f"archive/{date_str}/temp"
        assert result.new_path == expected_path

    async def test_archive_dry_run(self, tmp_path):
        """Test dry run shows archive destination without moving."""
        vault = tmp_path / "vault"
        vault.mkdir()
        (vault / "temp").mkdir()

        request = ManageFolderRequest(
            path="temp",
            operation=FolderOperation.ARCHIVE,
            dry_run=True,
        )

        result = await manage_folder_service(
            request=request,
            vault_path=str(vault),
            max_folder_depth=10,
            max_wikilink_scan_notes=1000,
        )

        assert result.success is True
        assert result.metadata["dry_run"] is True
        assert (vault / "temp").exists()  # Not moved
        assert "archive/" in result.new_path  # Shows where it would go

    async def test_archive_destination_exists_error(self, tmp_path):
        """Test error when archive destination already exists."""
        vault = tmp_path / "vault"
        vault.mkdir()
        (vault / "project").mkdir()

        # Create archive destination
        from datetime import datetime

        date_str = datetime.now().strftime("%Y-%m-%d")
        archive_path = vault / "archive" / date_str / "project"
        archive_path.mkdir(parents=True)

        request = ManageFolderRequest(
            path="project",
            operation=FolderOperation.ARCHIVE,
        )

        with pytest.raises(ValueError, match="Archive destination already exists"):
            await manage_folder_service(
                request=request,
                vault_path=str(vault),
                max_folder_depth=10,
                max_wikilink_scan_notes=1000,
            )

    async def test_archive_folder_not_found(self, tmp_path):
        """Test error when folder to archive doesn't exist."""
        vault = tmp_path / "vault"
        vault.mkdir()

        request = ManageFolderRequest(
            path="nonexistent",
            operation=FolderOperation.ARCHIVE,
        )

        with pytest.raises(FileNotFoundError, match="Folder not found"):
            await manage_folder_service(
                request=request,
                vault_path=str(vault),
                max_folder_depth=10,
                max_wikilink_scan_notes=1000,
            )
```

---

### Test 2: Path Validation Tests

**File**: `tests/tools/obsidian_folder_manager/test_service.py`

Add to the `TestSecurityValidation` class (around line 500):

```python
class TestSecurityValidation:
    """Tests for security validation and path checks."""

    # ... existing tests ...

    async def test_rejects_file_path_with_md_extension(self, tmp_path):
        """Test that file paths with .md extension are rejected."""
        vault = tmp_path / "vault"
        vault.mkdir()

        request = ManageFolderRequest(
            path="projects/note.md",  # File path, not folder
            operation=FolderOperation.CREATE,
        )

        with pytest.raises(ValueError, match="operates on FOLDERS only"):
            await manage_folder_service(
                request=request,
                vault_path=str(vault),
                max_folder_depth=10,
                max_wikilink_scan_notes=1000,
            )

    async def test_rejects_file_path_with_any_extension(self, tmp_path):
        """Test that file paths with any extension are rejected."""
        vault = tmp_path / "vault"
        vault.mkdir()

        request = ManageFolderRequest(
            path="projects/config.json",  # File with extension
            operation=FolderOperation.CREATE,
        )

        with pytest.raises(ValueError, match="appears to be a file"):
            await manage_folder_service(
                request=request,
                vault_path=str(vault),
                max_folder_depth=10,
                max_wikilink_scan_notes=1000,
            )

    async def test_accepts_folder_path_without_extension(self, tmp_path):
        """Test that folder paths without extension are accepted."""
        vault = tmp_path / "vault"
        vault.mkdir()

        request = ManageFolderRequest(
            path="projects/2025",  # Folder path, no extension
            operation=FolderOperation.CREATE,
        )

        # Should not raise
        result = await manage_folder_service(
            request=request,
            vault_path=str(vault),
            max_folder_depth=10,
            max_wikilink_scan_notes=1000,
        )

        assert result.success is True
```

---

### Cross-Platform Testing Setup

**File**: `.github/workflows/test.yml` (create if doesn't exist)

```yaml
name: Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    name: Test on ${{ matrix.os }} - Python ${{ matrix.python-version }}
    runs-on: ${{ matrix.os }}

    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: ['3.11', '3.12']

    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v3
        with:
          version: "latest"

      - name: Set up Python ${{ matrix.python-version }}
        run: uv python install ${{ matrix.python-version }}

      - name: Install dependencies
        run: uv sync

      - name: Run linting
        run: |
          uv run ruff check src/
          uv run mypy src/

      - name: Run folder manager tests
        run: uv run pytest tests/tools/obsidian_folder_manager/ -v

      - name: Run all tests
        run: uv run pytest tests/ -v
```

---

## Validation Commands Reference

### Step 1: Linting & Type Checking
```bash
uv run ruff check src/tools/obsidian_folder_manager/
uv run ruff check --fix src/tools/obsidian_folder_manager/
uv run mypy src/tools/obsidian_folder_manager/ --strict
```

### Step 2: Unit Tests
```bash
uv run pytest tests/tools/obsidian_folder_manager/ -v -m unit \
    --cov=src/tools/obsidian_folder_manager \
    --cov-report=term-missing \
    --cov-fail-under=90
```

### Step 3: Archive Operation Tests
```bash
uv run pytest tests/tools/obsidian_folder_manager/test_service.py::TestArchiveFolderOperation -v
```

### Step 4: Path Validation Tests
```bash
uv run pytest tests/tools/obsidian_folder_manager/test_service.py::TestSecurityValidation -v
```

### Step 5: All Folder Manager Tests
```bash
uv run pytest tests/tools/obsidian_folder_manager/ -v
```

### Step 6: Integration Tests
```bash
uv run pytest tests/integration/ -v -k folder
```

---

## Expected Test Results

After implementation, running tests should show:

```bash
uv run pytest tests/tools/obsidian_folder_manager/ -v

# Expected output:
TestCreateFolderOperation::test_create_simple_folder PASSED
TestRenameFolderOperation::test_rename_simple_folder PASSED
TestMoveFolderOperation::test_move_folder_to_existing_destination PASSED
TestDeleteFolderOperation::test_delete_empty_folder PASSED
TestListFolderOperation::test_list_immediate_children PASSED
TestArchiveFolderOperation::test_archive_simple_folder PASSED
TestArchiveFolderOperation::test_archive_with_wikilink_updates PASSED
TestArchiveFolderOperation::test_archive_custom_base PASSED
TestArchiveFolderOperation::test_archive_custom_date_format PASSED
TestArchiveFolderOperation::test_archive_dry_run PASSED
TestArchiveFolderOperation::test_archive_destination_exists_error PASSED
TestArchiveFolderOperation::test_archive_folder_not_found PASSED
TestSecurityValidation::test_rejects_file_path_with_md_extension PASSED
TestSecurityValidation::test_rejects_file_path_with_any_extension PASSED
TestSecurityValidation::test_accepts_folder_path_without_extension PASSED

============================== 35+ passed in 0.5s ==============================
```

---

## Implementation Checklist

### Phase 1: Path Validation & Separation (Priority)
- [ ] Add `validate_folder_path()` function to `service.py`
- [ ] Integrate validation in `manage_folder_service()`
- [ ] Update docstring in `tool.py` with strong negative guidance
- [ ] Add decision tree to system prompt in `config.py`
- [ ] Add path validation tests to `test_service.py`
- [ ] Test with paths ending in `.md` - should reject with helpful error

### Phase 2: Archive Operation
- [ ] Add `ARCHIVE` to `FolderOperation` enum in `schemas.py`
- [ ] Add `archive_base` and `date_format` fields to `ManageFolderRequest`
- [ ] Implement `_archive_folder()` in `service.py`
- [ ] Update `manage_folder_service()` to handle ARCHIVE operation
- [ ] Update tool registration in `tool.py` (parameters + response formatting)
- [ ] Add 7+ archive tests to `test_service.py`
- [ ] Test dry-run mode
- [ ] Test wikilink updates
- [ ] Test custom archive_base and date_format

### Phase 3: Cross-Platform Testing
- [ ] Create `.github/workflows/test.yml` for CI/CD
- [ ] Run tests on Linux, macOS, Windows
- [ ] Verify path normalization (backslashes → forward slashes)
- [ ] Test unicode folder names
- [ ] Test Windows reserved names (CON, PRN, etc.)

### Phase 4: Documentation & Polish
- [ ] Update README.md with archive examples
- [ ] Run linters: `uv run ruff check src/ && uv run mypy src/`
- [ ] Run all tests: `uv run pytest tests/ -v`
- [ ] Verify 90%+ test coverage on service layer

---

## Success Criteria

After implementation:

✅ Path validation rejects `.md` files with helpful error
✅ Docstring has strong negative guidance preventing tool confusion
✅ System prompt includes decision tree
✅ Archive operation creates `archive/YYYY-MM-DD/folder` paths
✅ Archive updates wikilinks automatically
✅ All 35+ tests pass
✅ Tests pass on Linux, macOS, Windows (CI/CD)
✅ Linters pass: `ruff check` and `mypy` with no errors
✅ Documentation updated in README

---

## Common Pitfalls to Avoid

❌ Don't use `os.path` - use `pathlib.Path` for cross-platform compatibility
❌ Don't forget to normalize paths to forward slashes before returning
❌ Don't skip the validation tests - they're critical for tool separation
❌ Don't use blocking I/O - use async operations (`aioshutil`, `aiofiles`)
❌ Don't forget to import `datetime` for archive operation
❌ Don't skip type hints - mypy strict mode requires them
❌ Don't forget to add archive handling in tool.py response formatting

---

## Next Steps

1. Start with Phase 1 (path validation) - this is the foundation
2. Run tests frequently: `uv run pytest tests/tools/obsidian_folder_manager/ -v`
3. Run linters after each phase: `uv run ruff check src/ && uv run mypy src/`
4. Commit after each working phase
5. Set up CI/CD early to catch cross-platform issues

**Begin implementation with Phase 1 path validation!**
