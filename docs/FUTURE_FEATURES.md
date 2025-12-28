# Future Features - DocNexus

> **These features are planned for future releases and are currently in development.**

## Smart Document Conversion (Coming Soon)

DocNexus includes an advanced conversion pipeline that will intelligently transform text-based diagrams and data into rich, interactive visualizations. This feature is being refined and will be enabled in a future release.

### 🎨 Smart Features Overview

#### 1. ASCII Table Conversion
**What it does**: Automatically detects ASCII-formatted tables and converts them to proper Markdown tables.

**Example Input**:
```
+----------+--------+
| Name     | Age    |
+----------+--------+
| Alice    | 30     |
| Bob      | 25     |
+----------+--------+
```

**Becomes**: Clean, sortable Markdown table with proper formatting.

---

#### 2. SIP Signaling Diagrams
**What it does**: Recognizes SIP call flows in text format and generates Mermaid sequence diagrams.

**Use Case**: Network engineers documenting VoIP systems can write simple text flows that automatically become professional diagrams.

**Example Input**:
```
Alice -> Server: INVITE
Server -> Bob: INVITE
Bob -> Server: 200 OK
Server -> Alice: 200 OK
```

**Becomes**: Interactive Mermaid sequence diagram showing the call flow.

---

#### 3. Network Topology Visualization
**What it does**: Detects network topology descriptions (routers, switches, connections) and creates visual network diagrams.

**Use Case**: IT administrators documenting infrastructure can describe networks in text and get automatic topology visualizations.

**Example Input**:
```
Router1 --- Switch1
Switch1 --- PC1
Switch1 --- PC2
Router1 --- Router2
```

**Becomes**: Professional network topology diagram with proper icons and connections.

---

## Technical Details

### Implementation Status
- ✅ **Code Complete**: All smart conversion functions are implemented in `DocNexus/features/smart_convert.py`
- ⏳ **UI Integration**: Temporarily disabled while we refine the user experience
- 📋 **Documentation**: Being finalized
- 🧪 **Testing**: Undergoing additional validation

### Architecture
Smart features use a **pipeline architecture**:
1. **Detection**: Pattern matching identifies convertible content
2. **Extraction**: Relevant data is extracted from text
3. **Transformation**: Data is converted to target format (Mermaid, Markdown, etc.)
4. **Rendering**: Final output is injected into the document

### Backend Modules
- `DocNexus/features/smart_convert.py` - Core conversion logic
- `DocNexus/features/standard.py` - Baseline features (already active)
- `DocNexus/core/renderer.py` - Markdown rendering engine

---

## Why Not Enabled Now?

We're committed to delivering a polished, professional experience. The smart features work well but need:

1. **Better UX**: More intuitive controls and visual feedback
2. **Performance**: Optimization for large documents
3. **Edge Cases**: Handling more varied input formats
4. **Documentation**: Comprehensive guides and examples

---

## When Will This Be Available?

**Target**: Version 1.1.0 or 1.2.0

We'll announce the release date once testing is complete. Follow the project on GitHub for updates!

---

## Want to Try It Early?

Developers can test smart features by:

1. Setting `enable_experimental = True` in `DocNexus/app.py` (line 893)
2. Accessing documents with `?smart=true` query parameter
3. Reviewing the code in `DocNexus/features/smart_convert.py`

**Note**: This is for development/testing only. The API may change before official release.

---

## Contributing

Interested in helping refine these features? Check out [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines!
