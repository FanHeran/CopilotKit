"""
A simple agentic chat flow.
"""

import os
from crewai.flow.flow import Flow, start
from litellm import completion
from copilotkit.crewai import copilotkit_stream, CopilotKitState


class AgenticChatFlow(Flow[CopilotKitState]):

    @start()
    async def chat(self):
        system_prompt = "You are a helpful assistant."

        # 1. Run the model and stream the response
        #    Note: In order to stream the response, wrap the completion call in
        #    copilotkit_stream and set stream=True.
        response = await copilotkit_stream(
            completion(

                # 1.1 Specify the model to use (OpenRouter format)
                model=os.getenv("OPENROUTER_MODEL", "openrouter/openai/gpt-4o"),
                api_key=os.getenv("OPENROUTER_API_KEY"),
                base_url=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
                messages=[
                    {
                        "role": "system", 
                        "content": system_prompt
                    },
                    *self.state.messages
                ],

                # 1.2 Bind the available tools to the model
                tools=[
                    *self.state.copilotkit.actions,
                ],

                # 1.3 Disable parallel tool calls to avoid race conditions,
                #     enable this for faster performance if you want to manage
                #     the complexity of running tool calls in parallel.
                parallel_tool_calls=False,
                stream=True
            )
        )

        message = response.choices[0].message

        # 2. Append the message to the messages in state
        self.state.messages.append(message)

