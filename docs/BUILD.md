# Production Build Instructions - OmniDoc v1.0.0

## Prerequisites

Install PyInstaller:
```bash
pip install pyinstaller
```

## Build Executable

### Option 1: Using Spec File (Recommended)
```bash
pyinstaller OmniDoc.spec
```

### Option 2: Direct Build
```bash
pyinstaller --onefile --name OmniDoc --add-data "doc_viewer/templates;doc_viewer/templates" --add-data "examples;examples" --add-data "docs;docs" --hidden-import flask --hidden-import markdown run.py
```

## Output

The executable will be created in:
- `dist/OmniDoc.exe` (Windows)
- `dist/OmniDoc` (Linux/Mac)

## Distribution Package

Create a distribution folder with:
```
OmniDoc-v1.0.0/
├── OmniDoc.exe          # Main executable
├── workspace/              # Sample markdown files
│   └── (your .md files)
├── README.md               # Documentation
└── LICENSE.txt             # License file
```

## Usage

### End Users
1. Extract the OmniDoc-v1.0.0.zip
2. Add your .md files to the `workspace/` folder
3. Run `OmniDoc.exe`
4. Browser opens at http://localhost:8000

### Command Line Options
```bash
# Start with default settings
OmniDoc.exe

# Custom port
OmniDoc.exe --port 8080

# Custom host and port
OmniDoc.exe --host 0.0.0.0 --port 8080

# Debug mode
OmniDoc.exe --debug
```

## Testing the Executable

1. Build the executable
2. Copy it to a clean directory
3. Create a `workspace` folder (copy contents from `examples/`)
4. Run the executable
5. Verify all features work correctly

## Troubleshooting

### Missing Templates Error
If you get "Template not found" errors, ensure the spec file includes:
```python
datas = [
    ('doc_viewer/templates', 'doc_viewer/templates'),
    ...
]
```

### Missing Markdown Extensions
If rendering fails, add missing extensions to `hiddenimports` in the spec file.

### Large Executable Size
The executable includes Python runtime and all dependencies (~30-50 MB). This is normal for PyInstaller builds.

To reduce size:
- Remove unused markdown extensions
- Exclude development dependencies
- Use UPX compression (enabled by default)

## Version Info

To create a Windows version info file:

1. Create `version_info.txt`:
```
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Your Company'),
        StringStruct(u'FileDescription', u'OmniDoc - Executive Documentation Platform'),
        StringStruct(u'FileVersion', u'1.0.0'),
        StringStruct(u'InternalName', u'OmniDoc'),
        StringStruct(u'LegalCopyright', u'Copyright (c) 2025'),
        StringStruct(u'OriginalFilename', u'OmniDoc.exe'),
        StringStruct(u'ProductName', u'OmniDoc'),
        StringStruct(u'ProductVersion', u'1.0.0')])
      ]
    ),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
```

2. Update spec file:
```python
exe = EXE(
    ...
    version_file='version_info.txt',
    icon='icon.ico',  # Optional
)
```

## Distribution Checklist

- [ ] Test executable on clean Windows machine
- [ ] Verify all markdown rendering works
- [ ] Test smart conversion toggle
- [ ] Check theme switching
- [ ] Verify file browser and navigation
- [ ] Test with various document types
- [ ] Include README.md with usage instructions
- [ ] Include sample markdown files
- [ ] Add LICENSE.txt file
- [ ] Create version-tagged release (v1.0.0)
- [ ] Generate SHA256 checksums for security

## Release Artifacts

Create these files for release:
- `OmniDoc-v1.0.0-Windows-x64.zip`
- `OmniDoc-v1.0.0-Linux-x64.tar.gz`
- `OmniDoc-v1.0.0-MacOS-x64.tar.gz`
- `SHA256SUMS.txt`
- `RELEASE_NOTES.md`
