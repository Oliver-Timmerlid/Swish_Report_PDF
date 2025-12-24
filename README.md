# Swish CSV to PDF Converter

A modern desktop application for converting Swish transaction CSV files into formatted PDF documents suitable for accounting and bookkeeping purposes.

## Features

- **Drag and drop** CSV file input with click-to-browse fallback
- **Comprehensive validation** of CSV format and content
- **Live preview** showing report overview and transaction table
- **Configurable PDF settings** (page size, orientation, font size)
- **Professional PDF output** with proper formatting and margins
- **Detailed logging** for troubleshooting
- **Swedish localization** for UI and messages
- **Modern dark UI** with Slate + Emerald color scheme

## Architecture

The application follows an MVC-inspired component-based architecture with clean separation of concerns:

- **UI Layer**: CustomTkinter components (display only)
  - Component-based architecture with reusable modules
  - No `__init__.py` files - uses namespace packages
  - Components located in `ui/components/` (header, preview, settings, footer)
  - Centralized theme system in `ui/theme.py`
- **Controller Layer**: Coordinates UI events with business logic
- **Service Layer**: Business logic (CSV parsing, validation, PDF generation)
- **Model Layer**: Data structures (dataclasses for Swish data)
- **Storage Layer**: File I/O operations
- **Core**: Configuration and logging

**Key principles:**

- All imports use explicit module paths
- Single-window application with frame composition
- UI components are presentation-only (no business logic)

## Requirements

- Python 3.12+
- Windows (primary platform)

### Dependencies

- customtkinter 5.2.2 - Modern UI framework
- reportlab - PDF generation
- tkinterdnd2 - Drag and drop support

## UI Components

The application uses a modular component architecture:

- **HeaderComponent**: Application title bar with clean branding
- **PreviewComponent**: Displays overview and transaction table with alternating row colors
- **SettingsComponent**: Sidebar with PDF configuration controls
- **FooterComponent**: Action buttons ("Ladda fil", "Skapa PDF")

### Theme

- **Color scheme**: Neutral grey backgrounds with Emerald + Sky blue accents
- **Typography**: 12-13pt readable text with proper hierarchy
- **Spacing**: Generous padding for comfortable reading
- **Contrast**: Subtle alternating table rows for easy scanning

## Configuration

PDF settings available in the sidebar:

- **Sidformat**: A4 or Letter
- **Orientering**: Portrait or Landscape
- **Textstorlek**: 6-12 points (adjustable slider)

## Logging

All application activity is logged to `logs/swish_converter.log` for troubleshooting. Log level is configurable in `core/config.py`.

## Project Structure

```
src/
├── app.py                      # Application entry point
├── controllers/
│   └── main_controller.py      # UI event coordination
├── core/
│   ├── config.py              # Application configuration
│   └── logging_config.py      # Logging setup
├── models/
│   └── swish_data.py          # Data models (SwishReport, SwishTransaction, etc.)
├── services/
│   ├── csv_parser.py          # CSV parsing logic
│   ├── pdf_generator.py       # PDF creation
│   └── validator.py           # Data validation
├── storage/
│   └── file_handler.py        # File I/O operations
└── ui/
    ├── theme.py               # Centralized color constants
    ├── main_window.py         # Main window composition
    └── components/
        ├── header_component.py
        ├── preview_component.py
        ├── settings_component.py
        └── footer_component.py
```

### Building Executable (Optional)

To create a standalone executable:

```bash
pip install pyinstaller
pyinstaller src/app.spec
```

The executable will be created in the `dist/` folder.

## License

MIT License (or your preferred license)

## Author

Oliver Timmerlid

## Version

1.2.0
