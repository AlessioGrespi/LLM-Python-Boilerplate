# Flask REST API Demo

This demo provides a REST API version of the interactive chat functionality, allowing you to test conversations and tool calling through HTTP requests instead of direct function calls.

## Overview

The Flask REST API demo consists of three main components:

1. **Flask Server** (`flask_chat_server.py`) - REST API server that handles chat sessions and tool execution
2. **Flask Client** (`flask_chat_client.py`) - Command-line client for interactive chat via HTTP
3. **API Tester** (`test_flask_api.py`) - Test script for demonstrating API usage

## Features

- ✅ Session-based chat conversations
- ✅ Tool calling with BBC news and Wikipedia APIs
- ✅ Conversation history management
- ✅ Session statistics and monitoring
- ✅ RESTful API design
- ✅ CORS support for web clients
- ✅ Comprehensive error handling
- ✅ Interactive command-line client

## Setup

### Prerequisites

1. Install required Python packages:
```bash
pip install flask flask-cors requests
```

2. Make sure the BBC RSS and Wikipedia API tools are available in the `tools/tool_modules/` directory.

### Starting the Server

1. Start the Flask server:
```bash
cd tests
python flask_chat_server.py
```

The server will start on `http://localhost:5001` with the following endpoints:

- `GET /api/health` - Health check
- `POST /api/sessions` - Create new session
- `GET /api/sessions` - List all sessions
- `POST /api/sessions/<id>/chat` - Send message
- `GET /api/sessions/<id>/history` - Get conversation history
- `POST /api/sessions/<id>/clear` - Clear history
- `GET /api/sessions/<id>/stats` - Get session stats
- `DELETE /api/sessions/<id>` - Delete session
- `GET /api/tools` - Get available tools

## Usage

### Interactive Client

The easiest way to test the API is using the interactive client:

```bash
cd tests
python flask_chat_client.py
```

This starts an interactive chat session similar to `interactive_chat_demo.py` but communicates via HTTP.

**Available Commands:**
- `/help` - Show help
- `/health` - Check server health
- `/new` - Create new session
- `/history` - Show conversation history
- `/stats` - Show session statistics
- `/clear` - Clear conversation history
- `/tools` - Show available tools
- `/sessions` - List all sessions
- `/delete` - Delete current session
- `/quit` or `/exit` - Exit the client

### API Testing

Run comprehensive API tests:

```bash
# Run full test suite
python test_flask_api.py --full

# Run specific scenario tests
python test_flask_api.py --scenarios
```

### Direct API Usage

You can also make direct HTTP requests to the API:

#### 1. Create a Session
```bash
curl -X POST http://localhost:5001/api/sessions \
  -H "Content-Type: application/json"
```

Response:
```json
{
  "success": true,
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Session created successfully",
  "stats": {
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "messages_exchanged": 0,
    "tool_calls_made": 0,
    "total_tokens": 0,
    "created_at": "2024-01-01T12:00:00",
    "last_activity": "2024-01-01T12:00:00"
  }
}
```

#### 2. Send a Message
```bash
curl -X POST http://localhost:5001/api/sessions/550e8400-e29b-41d4-a716-446655440000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Get me the latest BBC news",
    "model": "mistral-small",
    "max_tokens": 500,
    "temperature": 0.7
  }'
```

Response:
```json
{
  "success": true,
  "response": "Here are the latest BBC news headlines...",
  "tool_calls": [
    {
      "name": "get_bbc_latest_news",
      "input": {}
    }
  ],
  "tool_results": [
    {
      "success": true,
      "result": { /* BBC news data */ },
      "execution_time": 1.23,
      "tool_name": "get_bbc_latest_news",
      "input": {},
      "output_summary": "BBC Latest News (25 articles)"
    }
  ],
  "processing_time": 2.45,
  "usage": {
    "prompt_tokens": 150,
    "completion_tokens": 200,
    "total_tokens": 350
  },
  "session_stats": {
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "messages_exchanged": 2,
    "tool_calls_made": 1,
    "total_tokens": 350,
    "created_at": "2024-01-01T12:00:00",
    "last_activity": "2024-01-01T12:00:05"
  }
}
```

#### 3. Get Conversation History
```bash
curl -X GET http://localhost:5001/api/sessions/550e8400-e29b-41d4-a716-446655440000/history
```

#### 4. Get Session Statistics
```bash
curl -X GET http://localhost:5001/api/sessions/550e8400-e29b-41d4-a716-446655440000/stats
```

#### 5. Clear History
```bash
curl -X POST http://localhost:5001/api/sessions/550e8400-e29b-41d4-a716-446655440000/clear
```

#### 6. Delete Session
```bash
curl -X DELETE http://localhost:5001/api/sessions/550e8400-e29b-41d4-a716-446655440000
```

## Available Tools

The API supports the following tools:

### 1. BBC Latest News
- **Function**: `get_bbc_latest_news`
- **Description**: Get the latest BBC news headlines and summaries
- **Parameters**: None

### 2. BBC News Summary
- **Function**: `get_bbc_news_summary`
- **Description**: Get a summary of current BBC news with categorized articles
- **Parameters**:
  - `category` (optional): Filter by category (politics, technology, sports, business)
  - `max_articles` (optional): Maximum number of articles (default: 10)

### 3. Wikipedia Person Search
- **Function**: `find_person_wikipedia_page`
- **Description**: Find Wikipedia page for a specific person
- **Parameters**:
  - `person_name` (required): Name of the person to search for

## Example Conversations

### BBC News Request
```
User: "Get me the latest BBC news"
Assistant: [Calls get_bbc_latest_news tool and provides summary]
```

### Wikipedia Search
```
User: "Find Wikipedia page for Albert Einstein"
Assistant: [Calls find_person_wikipedia_page tool and provides page info]
```

### Multi-tool Request
```
User: "Get BBC news and find Wikipedia pages for the first 3 people mentioned"
Assistant: [Calls get_bbc_latest_news, then find_person_wikipedia_page for each person]
```

### Parameterized Request
```
User: "Get BBC news summary for technology category with maximum 5 articles"
Assistant: [Calls get_bbc_news_summary with category="technology" and max_articles=5]
```

## Architecture

### Server Architecture
```
Flask Server
├── ChatSession (per session)
│   ├── Conversation History
│   ├── Tool Functions
│   ├── Statistics Tracking
│   └── Session Management
├── REST API Endpoints
├── Tool Execution Engine
└── Error Handling
```

### Client Architecture
```
Flask Client
├── HTTP Request Handler
├── Response Parser
├── Interactive Chat Interface
├── Command Processor
└── Session Management
```

## Error Handling

The API includes comprehensive error handling:

- **400 Bad Request**: Invalid request data
- **404 Not Found**: Session not found
- **500 Internal Server Error**: Server-side errors
- **Connection Errors**: Network/connectivity issues

All errors return JSON responses with error details:

```json
{
  "success": false,
  "error": "Error description"
}
```

## Session Management

- Sessions are stored in memory (for production, use Redis or database)
- Each session has a unique UUID
- Sessions track conversation history, tool calls, and usage statistics
- Sessions can be created, managed, and deleted via API
- Session data persists until explicitly deleted or server restart

## Performance Considerations

- Tool execution times are tracked and reported
- Token usage is monitored per session
- Processing times are measured and included in responses
- Sessions are lightweight and efficient

## Security Notes

- CORS is enabled for development (configure appropriately for production)
- No authentication implemented (add for production use)
- Input validation is basic (enhance for production)
- Session IDs are UUIDs for security

## Troubleshooting

### Common Issues

1. **Server won't start**
   - Check if port 5001 is available
   - Ensure all dependencies are installed
   - Verify Python path includes required modules

2. **Client can't connect**
   - Verify server is running on correct port
   - Check firewall settings
   - Ensure correct base URL in client

3. **Tool execution fails**
   - Check BBC RSS feed availability
   - Verify Wikipedia API access
   - Review error messages in server logs

4. **Session not found**
   - Sessions are in-memory only
   - Server restart clears all sessions
   - Use correct session ID from create response

### Debug Mode

Start the server with debug mode for detailed logging:

```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

## Future Enhancements

- [ ] Database persistence for sessions
- [ ] Authentication and authorization
- [ ] Rate limiting
- [ ] WebSocket support for real-time chat
- [ ] Additional tools and integrations
- [ ] Metrics and monitoring
- [ ] Docker containerization
- [ ] Load balancing support

## Comparison with Direct Function Calls

| Aspect | Direct Calls | REST API |
|--------|-------------|----------|
| **Setup** | Simple import | Server + client setup |
| **Scalability** | Single process | Multi-client support |
| **Persistence** | None | Session-based |
| **Network** | None | HTTP overhead |
| **Debugging** | Direct | Network debugging |
| **Integration** | Code-level | API-level |
| **Deployment** | Local only | Network accessible |

The REST API approach provides better scalability, persistence, and integration capabilities while maintaining the same core functionality as the direct function calls. 