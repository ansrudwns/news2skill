import re
import json

def parse_llm_output(raw_output: str):
    """
    Simulates a middleware parser that strips <thinking> tags and extracts JSON.
    This prevents conflicts with Structured_Output_Forcer.
    """
    print("--- RAW LLM OUTPUT ---")
    print(raw_output)
    print("----------------------\n")
    
    # Strip <thinking> tags and their content
    stripped_output = re.sub(r'<thinking>.*?</thinking>', '', raw_output, flags=re.DOTALL)
    
    # Try to find JSON block
    match = re.search(r'\{.*\}', stripped_output, flags=re.DOTALL)
    if match:
        json_str = match.group(0)
        try:
            parsed_json = json.loads(json_str)
            print("✅ PARSER SUCCESS: Valid JSON Extracted! XML successfully stripped.")
            print(json.dumps(parsed_json, indent=2))
            return parsed_json
        except json.JSONDecodeError as e:
            print(f"❌ PARSER FAILED: Invalid JSON format. Error: {e}")
            return None
    else:
        print("❌ PARSER FAILED: No JSON block found after stripping XML.")
        return None

if __name__ == "__main__":
    test_output = """<thinking>
I need to respond strictly with JSON as dictated by Structured_Output_Forcer.
I will set status to SUCCESS, confidence to 0.99, and data to an approval message.
</thinking>
{
  "status": "SUCCESS",
  "confidence": 0.99,
  "data": "Anthropic patterns absorbed without crashing the payload."
}"""
    parse_llm_output(test_output)
