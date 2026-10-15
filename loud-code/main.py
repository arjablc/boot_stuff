import sys
from google import genai
import argparse
from google.genai import types
import os
from dotenv import load_dotenv

from functions.call_function import call_function
from prompts import system_prompt
from function_calls import available_functions


load_dotenv()


def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("gemini api key not found")
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    for _ in range(20):
        # create a new client
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0,
                tools=[available_functions],
            ),
        )
        func_results = []
        if response.usage_metadata is None:
            raise RuntimeError("Usages metadata is null")
        if args.verbose is True:
            print("User prompt: ", args.user_prompt)
            print("Prompt tokens: ", response.usage_metadata.prompt_token_count)
            print("Response tokens: ", response.usage_metadata.candidates_token_count)
        if response.candidates is not None:
            for candidate in response.candidates:
                messages.append(candidate.content)
        if not response.function_calls or len(response.function_calls) == 0:
            print("Response:")
            print(response.text)
            return

        for call in response.function_calls:
            function_call_result = call_function(call, verbose=(args.verbose is True))
            if len(function_call_result.parts) == 0:
                raise Exception("Empty parts from function call")
            first_part = function_call_result.parts[0]
            if first_part.function_response is None:
                raise Exception("Function response was null")
            func_response = first_part.function_response
            if func_response.response is None:
                raise Exception("Function response's response was null")
            print(f"-> {function_call_result.parts[0].function_response.response}")
            func_results.append(first_part)
        messages.append(types.Content(role="user", parts=func_results))
    sys.exit(1)


if __name__ == "__main__":
    main()
