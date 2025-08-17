# Interactive Demo Scripts

## 🎭 Overview

This directory contains interactive demo scripts that allow you to test the LLM Python Boilerplate tools and conversation capabilities in real-time.

## 📋 Available Demos

### 1. **Interactive Tools Demo** (`interactive_tools_demo.py`)
**Purpose**: Test tools directly and see their input/output in real-time.

**Features**:
- Direct tool execution with detailed logging
- Real-time input/output visualization
- Execution time tracking
- Chained tool execution demo
- Interactive parameter input

**Usage**:
```bash
python tests/interactive_tools_demo.py
```

**Available Tools**:
1. `get_bbc_public_figures` - Get public figures from BBC RSS feed
2. `get_bbc_rss_feed` - Get raw BBC RSS feed data
3. `find_person_wikipedia_page` - Find Wikipedia page for a specific person
4. `search_wikipedia` - Search Wikipedia for any topic
5. `get_wikipedia_page` - Get Wikipedia page by exact title
6. `chained_demo` - Demo: Get public figures and find their Wikipedia pages

**Commands**:
- `/help` - Show help message
- `/stats` - Show execution statistics
- `/quit` or `/exit` - Exit the demo

### 2. **Interactive Chat Demo** (`interactive_chat_demo.py`)
**Purpose**: Chat with the LLM and see tool calls in real-time.

**Features**:
- Real-time conversation with the LLM
- Tool call visualization
- Message history management
- Usage statistics tracking

**Usage**:
```bash
python tests/interactive_chat_demo.py
```

**Note**: This demo currently shows the conversation framework but tool calling through the model router needs implementation.

## 🚀 Quick Start

### For Tool Testing:
```bash
# Start the interactive tools demo
python tests/interactive_tools_demo.py

# Select tool 1 to test BBC public figures
# Select tool 3 to test Wikipedia person search
# Select tool 6 to see chained execution demo
```

### For Conversation Testing:
```bash
# Start the interactive chat demo
python tests/interactive_chat_demo.py

# Try prompts like:
# - "Get me the public figures from BBC news"
# - "Find Wikipedia page for Donald Trump"
# - "What's the weather like?" (no tools available)
```

## 📊 Example Output

### Tool Execution:
```
🔧 EXECUTING: get_bbc_public_figures
============================================================
📥 Input: No parameters required
⏱️  Execution time: 0.11 seconds
📤 Output: Found 43 public figures

📋 Sample public figures:
    1. Mary Sheikh
       Context: Gaza aid site offered a 'women only' day...
       Article: https://www.bbc.com/news/articles/c74z4gy5g31o
```

### Wikipedia Search:
```
🔧 EXECUTING: find_person_wikipedia_page
============================================================
📥 Input: person_name = 'Donald Trump'
⏱️  Execution time: 1.23 seconds
📤 Output: Found page 'Donald Trump'
   📖 URL: https://en.wikipedia.org/wiki/Donald_Trump
   📄 Page ID: 46603496
   📝 Summary: Donald John Trump (born June 14, 1946) is an American politician...
```

### Chained Demo:
```
🔧 EXECUTING: Chained Demo - Get public figures and find Wikipedia pages
============================================================
📥 Input: No parameters required

🔄 Step 1: Getting public figures from BBC...
✅ Found 3 public figures

🔄 Step 2: Getting Wikipedia pages...
   Processing 1/3: Mary Sheikh
   ✅ Found: Mohammed bin Rashid Al Maktoum
      URL: https://en.wikipedia.org/wiki/Mohammed_bin_Rashid_Al_Maktoum

⏱️  Total execution time: 3.45 seconds
✅ Chained demo completed successfully!
```

## 🎯 Use Cases

### 1. **Tool Development**
- Test individual tools in isolation
- Verify input/output formats
- Measure performance metrics
- Debug tool functionality

### 2. **Integration Testing**
- Test tool chaining workflows
- Verify data flow between tools
- Test error handling scenarios
- Validate tool responses

### 3. **User Experience**
- Demonstrate tool capabilities
- Show real-time tool execution
- Provide interactive learning experience
- Test conversation flows

## 🔧 Technical Details

### Tool Execution Flow:
1. **Input Validation** - Check required parameters
2. **Tool Execution** - Call the actual tool function
3. **Output Processing** - Format and display results
4. **Statistics Tracking** - Record execution metrics

### Error Handling:
- Graceful error recovery
- Detailed error messages
- Execution time tracking
- Success/failure indicators

### Performance Metrics:
- Execution time per tool
- Total execution time
- Tool call count
- Average response time

## 🚨 Known Limitations

### Interactive Chat Demo:
- Model router tool calling needs implementation
- AWS Bedrock API integration requires refinement
- Message history format issues

### Interactive Tools Demo:
- ✅ Fully functional
- ✅ All tools working
- ✅ Real-time visualization
- ✅ Performance tracking

## 🎯 Recommendations

### For Immediate Use:
1. **Use Interactive Tools Demo** for testing individual tools
2. **Use Chained Demo** for testing tool workflows
3. **Monitor execution times** for performance optimization

### For Future Development:
1. **Fix model router tool calling** for full conversation capabilities
2. **Add more tools** to the interactive demos
3. **Implement conversation history** in chat demo
4. **Add streaming responses** for better UX

## 📚 Related Files

- `interactive_tools_demo.py` - Main tools testing interface
- `interactive_chat_demo.py` - Conversation testing interface
- `test_conversation_with_tools.py` - Automated tool testing
- `test_specific_use_cases.py` - Specific use case testing

## 🎉 Getting Started

1. **Choose your demo** based on what you want to test
2. **Run the script** and follow the interactive prompts
3. **Explore different tools** and see their capabilities
4. **Try the chained demo** to see tool workflows in action
5. **Check statistics** to understand performance characteristics

Happy testing! 🚀 