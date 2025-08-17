# LLM Python Boilerplate

A comprehensive AI personal assistant with support for multiple LLM providers, tool integration, and various deployment options.

## Project Structure

```
LLM-Python-Boilerplate/
├── src/                    # Core source code
│   └── ultimate_llm_toolkit/  # Main package with LLM tools
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
├── config/                # Configuration files
└── docs/                  # Documentation files
```

## Quick Start

### Installation

```bash
# From local development
git clone https://github.com/AlessioGrespi/LLM-Python-Boilerplate.git
cd LLM-Python-Boilerplate
pip install -e .

# From GitHub
pip install git+https://github.com/AlessioGrespi/LLM-Python-Boilerplate.git
```

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

- **Azure OpenAI** - Configure in `src/ultimate_llm_toolkit/azure.py`
- **AWS Bedrock** - Configure in `src/ultimate_llm_toolkit/aws_bedrock.py`
- **Model Router** - Unified interface in `src/ultimate_llm_toolkit/model_router.py`

## Features

- 🤖 Multi-provider LLM support
- 🛠️ Tool integration (RSS feeds, Wikipedia, web search)
- 💬 Conversation management
- 🌐 Flask API server
- 🎤 Text-to-Speech capabilities
- 🧪 Comprehensive test suite
- 📚 Interactive demos

## Documentation

- [System Documentation](SYSTEM_DOCUMENTATION.md) - Comprehensive technical overview and architecture
- [Quick Reference](QUICK_REFERENCE.md) - Fast access to common commands and patterns
- [Usage Examples](USAGE_EXAMPLES.md) - Practical examples for integrating the library
- [Environment Setup](ENV_SETUP.md) - Step-by-step environment configuration
- [Migration Guide](MIGRATION_SUMMARY.md) - Project structure changes and updates
- [Chained Tools Summary](CHAINED_TOOLS_SUMMARY.md) - Tool orchestration and workflows
- [Conversation Testing](CONVERSATION_TESTING_SUMMARY.md) - Testing conversation capabilities

## Development

### Adding New Tools

1. Create your tool module in `src/ultimate_llm_toolkit/`
2. Register it in the tool router
3. Add tests in `tests/integration/`

### Adding New Demos

1. Create your demo in the appropriate `demos/` subdirectory
2. Add documentation
3. Update this README

## License

This project is licensed under the MIT License. 