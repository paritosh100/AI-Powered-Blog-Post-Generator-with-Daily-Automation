import os
from openai import OpenAI
from openai import RateLimitError, APIConnectionError, OpenAIError
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_blog_post(keyword, seo_data):
    prompt = f"""
Write a detailed SEO-optimized blog post about '{keyword}'.
Use headings, bullet points, and include {{AFF_LINK_1}}, {{AFF_LINK_2}}, etc.
Mention:
- Search Volume: {seo_data['search_volume']}
- Keyword Difficulty: {seo_data['keyword_difficulty']}
- CPC: ${seo_data['avg_cpc']}

Make it informative and persuasive.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        return response.choices[0].message.content

    except RateLimitError as e:
        return "Error: Rate limit exceeded or quota exhausted. Please check your API usage."

    except APIConnectionError:
        return "Error: Failed to connect to OpenAI. Please check your internet connection or try again later."

    except OpenAIError as e:
        return f"OpenAI API error: {str(e)}"

    except Exception as e:
        return f"Unexpected error: {str(e)}"
