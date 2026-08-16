import os
from dotenv import load_dotenv
import streamlit as st
from google import genai

# Load API key
load_dotenv()

api_key = os.getenv("API_KEY")

if not api_key:
    st.error("API_KEY not found in .env file")
    st.stop()

client = genai.Client(api_key=api_key)


def generate_recipe(ingredients, cuisine, diet):
    prompt = f"""
    Generate one delicious recipe using these ingredients:
    {", ".join(ingredients)}

    Requirements:
    - Cuisine: {cuisine}
    - Diet: {diet}
    - Recipe should be under 150 words.
    - Include:
        1. Recipe Name
        2. Ingredients
        3. Steps
        4. Cooking Time
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    return response.text


# ---------------- UI ---------------- #

st.set_page_config(
    page_title="AI Recipe Generator",
    page_icon="🍲",
    layout="centered"
)

st.title("🍲 AI Recipe Generator")

st.write("Generate recipes using ingredients you already have!")

ingredient_text = st.text_area(
    "Enter ingredients (comma separated)",
    placeholder="tomato, onion, garlic, rice"
)

cuisine = st.selectbox(
    "Cuisine",
    [
        "Any",
        "Indian",
        "Italian",
        "Chinese",
        "Mexican",
        "Thai",
        "Mediterranean"
    ]
)

diet = st.selectbox(
    "Diet",
    [
        "Any",
        "Vegetarian",
        "Vegan",
        "Jain",
        "Gluten Free",
        "Keto"
    ]
)

if st.button("Generate Recipe", type="primary"):

    if ingredient_text.strip() == "":
        st.warning("Please enter at least one ingredient.")
    else:
        ingredients = [
            item.strip()
            for item in ingredient_text.split(",")
            if item.strip()
        ]

        with st.spinner("Cooking something delicious... 👨‍🍳"):

            recipe = generate_recipe(
                ingredients,
                cuisine,
                diet
            )

        st.success("Recipe Generated!")

        st.markdown(recipe)