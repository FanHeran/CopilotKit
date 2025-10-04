# OpenRouter Migration Guide

This document outlines the changes made to migrate the CopilotKit demo-viewer from OpenAI to OpenRouter.

## Overview

The demo-viewer has been updated to use OpenRouter instead of OpenAI directly. OpenRouter provides access to multiple AI models through a unified API, including OpenAI models.

## Changes Made

### 1. Frontend Changes

**File: `src/app/api/copilotkit/route.ts`**

- Added OpenRouter client configuration
- Updated OpenAIAdapter to use custom OpenAI client with OpenRouter base URL
- Added required headers for OpenRouter (HTTP-Referer and X-Title)

### 2. Backend Agent Changes

#### CrewAI Agents

Updated the following CrewAI agent files:

- `agent/demo/crewai_agentic_chat/agent.py`
- `agent/demo/crewai_human_in_the_loop/agent.py`
- `agent/demo/crewai_tool_based_generative_ui/agent.py`
- `agent/demo/crewai_agentic_generative_ui/agent.py`

Changes made:

- Added `import os` for environment variable access
- Added OpenRouter configuration for litellm
- Updated model calls from `model="openai/gpt-4o"` to `model="openrouter/openai/gpt-4o"`
- Added `api_key` and `base_url` parameters to completion calls

#### LangGraph Agents

Updated the following LangGraph agent files:

- `agent/demo/langgraph_agentic_chat/agent.py`
- `agent/demo/langgraph_tool_based_generative_ui/agent.py`
- `agent/demo/langgraph_human_in_the_loop/agent.py`

Changes made:

- Added `import os` for environment variable access
- Updated `ChatOpenAI` initialization to include OpenRouter configuration
- Added `api_key`, `base_url`, and `default_headers` parameters

### 3. Environment Variables

**New Environment Variables:**

- `OPENROUTER_API_KEY` - Your OpenRouter API key (replaces OPENAI_API_KEY)
- `YOUR_SITE_URL` - Your site URL for OpenRouter headers (optional, defaults to localhost:3000)
- `YOUR_SITE_NAME` - Your site name for OpenRouter headers (optional, defaults to "CopilotKit Demo Viewer")

**Files Updated:**

- `README.md` - Updated setup instructions
- `.env.example` - Created example environment files for both root and agent directories

### 4. Documentation

**File: `README.md`**

- Updated environment setup section
- Changed from OPENAI_API_KEY to OPENROUTER_API_KEY
- Added instructions for obtaining OpenRouter API key

## Setup Instructions

1. **Get OpenRouter API Key:**

   - Visit [OpenRouter](https://openrouter.ai/)
   - Create an account and generate an API key

2. **Set Environment Variables:**

   ```bash
   # In the root directory
   echo "OPENROUTER_API_KEY=your_openrouter_api_key_here" > .env
   echo "OPENROUTER_BASE_URL=https://openrouter.ai/api/v1" >> .env
   echo "OPENROUTER_MODEL=openrouter/openai/gpt-4o" >> .env
   echo "YOUR_SITE_URL=http://localhost:3000" >> .env
   echo "YOUR_SITE_NAME=CopilotKit Demo Viewer" >> .env

   # In the agent directory
   cd agent
   echo "OPENROUTER_API_KEY=your_openrouter_api_key_here" > .env
   echo "OPENROUTER_BASE_URL=https://openrouter.ai/api/v1" >> .env
   echo "OPENROUTER_MODEL=openrouter/openai/gpt-4o" >> .env
   echo "YOUR_SITE_URL=http://localhost:3000" >> .env
   echo "YOUR_SITE_NAME=CopilotKit Demo Viewer" >> .env
   cd ..
   ```

3. **Environment Variables Explained:**

   - `OPENROUTER_API_KEY`: Your OpenRouter API key
   - `OPENROUTER_BASE_URL`: OpenRouter API base URL (configurable for different endpoints)
   - `OPENROUTER_MODEL`: The model to use (easily switch between different models)
   - `YOUR_SITE_URL`: Your site URL for OpenRouter headers
   - `YOUR_SITE_NAME`: Your site name for OpenRouter headers

4. **Install and Run:**
   Follow the existing installation instructions in README.md

## Benefits of OpenRouter

1. **Multiple Model Access:** Access to various AI models through a single API
2. **Cost Optimization:** Compare prices across different providers
3. **Reliability:** Fallback options if one provider is unavailable
4. **Unified Interface:** Same API format for different models

## Model Compatibility

The migration maintains compatibility with GPT-4o and other OpenAI models through OpenRouter. You can also experiment with other models available on OpenRouter by changing the model parameter in the agent files.

## Troubleshooting

1. **API Key Issues:** Ensure your OpenRouter API key is correctly set in both .env files
2. **Model Access:** Verify your OpenRouter account has access to the models you're trying to use
3. **Headers:** The HTTP-Referer and X-Title headers are required by OpenRouter for tracking

## Batch Update Completed

✅ **All agent files have been successfully updated!**

The `update_agents_to_openrouter.py` script has processed and updated **15 agent files**:

**CrewAI Agents (7 files):**

- crewai_agentic_chat
- crewai_agentic_generative_ui
- crewai_human_in_the_loop
- crewai_multi_agent_flows
- crewai_predictive_state_updates
- crewai_shared_state
- crewai_tool_based_generative_ui

**LangGraph Agents (8 files):**

- langgraph_agentic_chat
- langgraph_agentic_generative_ui
- langgraph_human_in_the_loop
- langgraph_multi_agent_flows
- langgraph_no_chat
- langgraph_predictive_state_updates
- langgraph_shared_state
- langgraph_tool_based_generative_ui

All hardcoded model names, API keys, and base URLs have been replaced with environment variables for maximum flexibility.
