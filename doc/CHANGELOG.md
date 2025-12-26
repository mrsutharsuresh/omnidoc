# Changelog

All notable changes to the Markdown Documentation Viewer project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.4.0] - 2025-12-24

### Added
- **Word Document Input Support**
  - Accept .docx files as input in addition to Markdown files
  - Automatic conversion of Word documents to HTML using mammoth library
  - Real-time rendering of Word documents in the viewer
  - Support for Word files in both Browse and Preview modes
  - Seamless integration with existing document viewer features

- **In-Browser Document Editor**
  - Monaco Editor integration for live document editing
  - Edit button in document viewer for Markdown and text files
  - Syntax highlighting and autocompletion for Markdown
  - Automatic backup creation before saving (.bak files)
  - Save and reload functionality with real-time preview
  - Security validation to prevent unsafe file operations
  - Edit mode disabled for Word documents (view-only)

- **User Log Collection System**
  - Rotating log file system (10 MB per file, 7 backups retained)
  - Centralized logging for all application operations
  - Download logs button (📋) in navigation bar
  - Automatic log sanitization (removes IP addresses and file paths)
  - ZIP archive generation for easy sharing with developers
  - Comprehensive error tracking and debugging information

- **Clickable Document Links**
  - Automatic link detection and processing in rendered content
  - External links open in new tabs with `target="_blank"`
  - Relative links resolved based on document location
  - Broken link detection and visual indicators
  - Smart link processing for Word document HTML output
  - Maintains link functionality in Browse and Preview modes

- **Relative Link Resolution**
  - Context-aware link resolution based on current document path
  - Session-based tracking of preview file base paths
  - Correct relative path handling for Browse feature
  - Base path inheritance for nested documents
  - Prevents broken links when switching between documents

- **Custom Workspace Selection**
  - Workspace settings modal (⚙️) for managing document directories
  - Add, switch, and remove custom workspace folders
  - JSON-based configuration storage (config.json)
  - Active workspace persistence across sessions
  - Security validation to block system directories (Windows/Program Files)
  - Multiple workspace support for different document sets

- **PDF Export Auto-Installation**
  - Automatic detection of wkhtmltopdf availability
  - One-click installation of portable wkhtmltopdf (no admin rights)
  - GitHub-based download of official wkhtmltopdf binaries
  - Installation progress dialog with status updates
  - Graceful fallback with manual installation instructions
  - PATH and common locations search for existing installations

### Changed
- **Updated Dependencies**
  - Added mammoth>=1.6.0 for Word document conversion
  - Added html2text>=2020.1.16 for HTML to Markdown conversion
  - Added lxml>=4.9.0 for fast HTML parsing
  - Updated requirements.txt with new dependencies

- **File Input Handling**
  - Extended ALLOWED_EXTENSIONS to include .docx files
  - Updated file input accept attribute to ".md,.markdown,.txt,.docx"
  - Enhanced preview_file() route for Word document handling
  - Modified render_document_from_file() for multi-format support

- **Application Architecture**
  - Added Flask session management with secret key
  - Implemented centralized logging system
  - Created workspace configuration management
  - Added 7 new API endpoints for editing, logging, and workspace management

### Fixed
- **Editor Button Functionality**
  - Fixed null reference errors when toggling edit mode
  - Added proper null checks for editor and document containers
  - Corrected initial state detection for empty display strings
  
- **Syntax Errors**
  - Removed duplicate closing brace in view.html (line 975)
  - Fixed JavaScript syntax issues in toggleEditMode function

- **Workspace Selector UX**
  - Made workspace selector prominent with dedicated section below hero
  - Added large, bordered card design showing current workspace
  - Implemented browse button for easier folder selection
  - Added File System Access API integration with manual fallback
  - Enhanced modal with improved layout and delete functionality

- **PDF Export Reliability**
  - Fixed "wkhtmltopdf not found" errors on fresh installations
  - Implemented automatic wkhtmltopdf installation workflow
  - Added portable installation option for non-admin users
  - Better error messages with installation guidance

- **Link Navigation Issues**
  - Fixed broken relative links in Browse mode
  - Corrected link resolution for uploaded/preview files
  - Maintained link context when switching documents

### Technical Details
- **New API Endpoints**
  - `GET /api/get-source/<path>` - Retrieve file content for editing
  - `POST /api/save-document` - Save edited document with backup
  - `GET /api/download-logs` - Download sanitized logs as ZIP
  - `GET /api/workspaces` - List all configured workspaces
  - `POST /api/workspaces` - Add new workspace
  - `POST /api/workspaces/active` - Switch active workspace
  - `DELETE /api/workspaces/<path>` - Remove workspace
  - `POST /api/install-wkhtmltopdf` - Install PDF export dependencies

- **Helper Functions**
  - `convert_docx_to_html()` - Word to HTML conversion using mammoth
  - `process_links_in_html()` - Link detection and processing with BeautifulSoup
  - `is_safe_workspace()` - Security validation for workspace paths
  - `sanitize_log_content()` - Remove sensitive data from logs
  - `find_wkhtmltopdf()` - Search for wkhtmltopdf executable
  - `install_wkhtmltopdf_portable()` - Download and install portable version

- **Frontend Enhancements**
  - Monaco Editor CDN integration for code editing
  - Workspace settings modal with dynamic content
  - PDF installation dialog with progress indicators
  - Edit mode toggle with save/cancel controls
  - Enhanced navigation with workspace and logs buttons

## [1.3.1] - 2025-12-24

### Fixed
- **Word Export Improvements**
  - Fixed TOC (Table of Contents) hyperlinks - now properly navigate to sections instead of document top
  - Implemented Word bookmarks for internal navigation using `w:bookmarkStart` and `w:bookmarkEnd` XML elements
  - Fixed table formatting in Word exports with proper purple headers (#6366f1) and cell backgrounds
  - Added post-processing to apply table styles that htmldocx library doesn't handle correctly
  - Table headers now display with correct purple background, white text, uppercase, and bold formatting
  - Alternating row colors in tables for better readability

- **Large File Support**
  - Fixed "Request Entity Too Large" error when loading files via Browse Files button
  - Switched from URL-encoded form POST to multipart/form-data for efficient file uploads
  - Implemented intelligent file size validation at application level (20 MB for files, 50 MB for exports)
  - Removed blanket HTTP request size limit that was causing false rejections
  - Client-side file size check before upload to provide immediate feedback
  - Files up to 20 MB now load without errors (previously failed due to form encoding overhead)

- **Performance Optimizations**
  - Used lxml parser for faster HTML processing on large documents
  - Added progress logging for Word export operations
  - Streaming file upload handling for better memory efficiency
  - Better error messages with actual file sizes and actionable suggestions

### Technical Details
- Root cause: htmldocx library doesn't support internal anchor links (always sets `is_external=True`)
- Solution: Post-processing Word documents to manually add bookmarks and convert external links to internal `w:anchor` references
- File upload encoding issue: 692 KB file became 1.04 MB when URL-encoded (1.5x overhead), triggering false size limit errors
- Solution: Changed to multipart/form-data which sends raw file bytes without encoding overhead

## [1.3.0] - 2025-12-24

### Added
- **Word Export Feature**
  - New export dropdown menu replacing single PDF export button
  - Export to Word (.docx) format with exact formatting preservation
  - Export to PDF option moved into dropdown menu
  - HTML to Word conversion using htmldocx library
  - Maintains all formatting: headings, bold/italic, tables, lists, colors, fonts
  - Modern dropdown UI with smooth animations
  - Color-coded export options (red for PDF, blue for Word)
  - Both export formats remove UI elements (buttons, toggles) from output
  - Loading states during document generation
  - Graceful error handling with user-friendly messages

### Changed
- Replaced single "Export PDF" button with "Export" dropdown menu
- Export functionality now categorized into "Export to PDF" and "Export to Word"
- Enhanced export UI with better visual hierarchy

### Dependencies
- Added htmldocx==0.0.6 for HTML to Word conversion
- Added python-docx==1.1.0 for Word document manipulation

## [1.2.1] - 2025-12-23

### Fixed
- **Search Path Encoding**
  - Fixed search results not navigating correctly to files in subfolders
  - Paths now use forward slashes (/) instead of backslashes (\) for proper URL encoding
  - Search result file names and paths properly escaped in HTML for XSS protection
  - Files in subfolders like "Sample/filename.md" now open correctly when clicked from search results

## [1.2.0] - 2025-12-23

### Added
- **Search Feature**
  - Full-text search across all markdown and text files in the gallery
  - Search modal with beautiful UI matching the application theme
  - Real-time search with 300ms debouncing for optimal performance
  - Keyboard navigation support (Arrow keys to navigate, Enter to open, Escape to close)
  - Global keyboard shortcut (Cmd/Ctrl+K) to open search
  - Dual search modes: filename matching and content searching
  - Context snippets showing surrounding text for content matches
  - Match type badges distinguishing filename vs content results
  - Result count display
  - Click outside modal to close functionality
  - Accessible and responsive design
  - XSS protection with HTML escaping

### Changed
- Replaced "Search feature coming soon!" alert with fully functional search
- Search trigger now opens interactive search modal

## [1.1.0] - 2025-12-23

### Added
- **Text File Support**
  - Added support for .txt file browsing and viewing alongside markdown files
  - File browser now accepts .md, .markdown, and .txt extensions
  - Text files rendered with markdown formatting support
  - Updated file validation to include text file extensions

- **PDF Export Feature**
  - Professional PDF export button in document view (top-right navigation)
  - High-quality PDF generation using pdfkit with wkhtmltopdf (WebKit rendering engine)
  - Perfect Unicode symbol and emoji rendering in exported PDFs
  - Browser-quality output with exact visual reproduction
  - A4 page size with professional margins (20mm)
  - 300 DPI high-resolution output for print-ready documents
  - Automatic filename generation based on source document
  - Export button with loading state feedback
  - Comprehensive error handling with user-friendly messages

- **PDF Export Configuration**
  - Automatic detection of wkhtmltopdf installation path
  - Support for both 64-bit and 32-bit Windows installations
  - Graceful fallback with installation instructions if wkhtmltopdf not found
  - Print media type support for optimal PDF rendering
  - Local file access enabled for embedded resources

### Changed
- Updated file input validation to accept text files
- Enhanced file browser to display .txt files alongside markdown files
- Improved error messages for PDF generation failures
- Updated requirements.txt with pdfkit dependency

### Technical Details
- **Dependencies Added**: pdfkit==1.0.0
- **External Requirements**: wkhtmltopdf (WebKit HTML to PDF converter)
- **API Changes**: New /export-pdf POST endpoint for PDF generation
- **Frontend Updates**: Export functionality with JavaScript fetch API

## [1.0.0] - 2025-12-15

### Added
- **Core Functionality**
  - Flask-based web server for viewing markdown documentation
  - Recursive folder scanning to automatically detect markdown files
  - Real-time markdown rendering with support for tables, code blocks, and formatting
  - Support for nested folder structures with automatic organization

- **User Interface**
  - Professional light theme as default with clean, distraction-free design
  - Dark theme toggle button for comfortable reading in low-light environments
  - Theme persistence using browser localStorage
  - Responsive tile-based grid layout (4/3/2/1 columns based on screen size)
  - Collapsible folder sections for better navigation
  - File cards with metadata display (size, modified date)
  - Smooth animations and transitions

- **Document Viewer**
  - Collapsible H1 and H2 sections with toggle icons
  - Clickable table of contents with smart header matching
  - Automatic section expansion when navigating from TOC
  - Syntax highlighting for code blocks (theme-aware)
  - Styled tables, blockquotes, and lists
  - Sticky navigation bar with back button
  - Smooth scrolling behavior

- **Developer Experience**
  - One-click startup script (start.bat) for Windows
  - Automatic dependency installation
  - Auto-opens browser to localhost:8000
  - Hot reload support in debug mode

- **Markdown Extensions**
  - Fenced code blocks with syntax highlighting
  - Tables with proper formatting
  - Table of contents generation
  - Extra markdown features (definition lists, footnotes, etc.)
  - Attribute lists for enhanced styling

### Fixed
- **Table of Contents Positioning**
  - Fixed TOC HTML being escaped instead of rendered
  - Implemented placeholder-based approach to inject TOC after markdown rendering
  - Added smart positioning logic: TOC at top for conversational documents (H1 after line 50)
  - TOC appears after first H1 for standard documents (H1 within first 50 lines)
  - Improved code block detection to prevent false heading detection from code comments
  - Now correctly skips lines inside ``` code fences when detecting headings
  - Prevents bash/python comments (# lines) from being treated as markdown headings

### Technical Details
- Python 3.7+ compatibility
- Flask 3.0.0 web framework
- Markdown 3.5.1 with multiple extensions
- Pygments 2.17.2 for syntax highlighting
- Highlight.js for client-side code highlighting
- Inter font family for modern typography
- JetBrains Mono for code blocks

### Files Structure
```
Md_File_Reader/
├── app.py                  # Flask application
├── requirements.txt        # Python dependencies
├── start.bat              # Windows startup script
├── VERSION                # Version information
├── CHANGELOG.md           # This file
├── markdown_files/        # Your markdown documents
│   └── sample.md
└── templates/
    ├── index.html         # File browser page
    └── view.html          # Document viewer page
```

### Configuration
- Server runs on localhost:8000
- Debug mode enabled for development
- Supports .md and .markdown file extensions
- Automatic file discovery in markdown_files/ directory

---

## Release Notes

**Version 1.0.0** represents the first stable release of the Markdown Documentation Viewer. This release provides a complete, production-ready solution for viewing and organizing markdown documentation with a professional user interface and comprehensive feature set.

### Upgrade Notes
- First release - no upgrade path needed
- To start using: run `start.bat` or `python app.py`
- Add your markdown files to the `markdown_files/` directory

### Known Limitations
- Currently supports local file system only
- No authentication or user management
- Single-user application (not designed for concurrent users)

### Future Roadmap
- Search functionality across all documents
- Custom themes and styling options
- Export to PDF
- Markdown editing capabilities
- Multi-language support
