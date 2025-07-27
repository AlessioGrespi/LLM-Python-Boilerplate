# Ultimate AI Personal Assistant

A comprehensive AI personal assistant with support for multiple LLM providers, tool integration, and various deployment options.

## Project Structure

```
Ultimate-AI-Personal-Assistant/
├── src/                    # Core source code
│   ├── core/              # Core functionality (model router, configs, tools)
│   ├── agents/            # AI agent implementations
│   └── utils/             # Utility functions
├── demos/                 # Demo applications
│   ├── flask/            # Flask API demos
│   ├── interactive/      # Interactive CLI demos
│   └── tts/              # Text-to-Speech demos
├── tests/                 # Test suite
│   ├── api/              # API tests
│   ├── integration/      # Integration tests
│   ├── unit/             # Unit tests
│   ├── debug/            # Debug utilities
│   └── run_all_tests.py  # Test runner
├── docs/                  # Documentation
├── legacy/               # Legacy code (deprecated)
└── v0.1/                 # Legacy version (ignored by git)
```

## Quick Start

### Running Demos

1. **Flask API Demo:**
   ```bash
   cd demos/flask
   python flask_chat_server.py
   ```

2. **Interactive Demo:**
   ```bash
   cd demos/interactive
   python interactive_chat_demo.py
   ```

3. **TTS Demo:**
   ```bash
   cd demos/tts
   python tts_demo.py
   ```

### Running Tests

```bash
# Run all tests
python tests/run_all_tests.py

# Run specific test categories
python -m pytest tests/unit/
python -m pytest tests/integration/
python -m pytest tests/api/
```

## Configuration

The assistant supports multiple LLM providers:

- **Azure OpenAI** - Configure in `src/core/azure.py`
- **AWS Bedrock** - Configure in `src/core/aws_bedrock.py`
- **Model Router** - Unified interface in `src/core/model_router.py`

## Features

- 🤖 Multi-provider LLM support
- 🛠️ Tool integration (RSS feeds, Wikipedia, web search)
- 💬 Conversation management
- 🌐 Flask API server
- 🎤 Text-to-Speech capabilities
- 🧪 Comprehensive test suite
- 📚 Interactive demos

## Documentation

- [System Documentation](SYSTEM_DOCUMENTATION.md)
- [Quick Reference](QUICK_REFERENCE.md)
- [Migration Guide](MIGRATION_SUMMARY.md)
- [Chained Tools Summary](CHAINED_TOOLS_SUMMARY.md)

## Development

### Adding New Tools

1. Create your tool module in `src/core/`
2. Register it in the tool router
3. Add tests in `tests/integration/`

### Adding New Demos

1. Create your demo in the appropriate `demos/` subdirectory
2. Add documentation
3. Update this README

## License

This project is licensed under the MIT License. 