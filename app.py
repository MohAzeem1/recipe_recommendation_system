import streamlit as st
import pandas as pd
from recommender import recommend_recipes, recommend_by_ingredients

# Load dataset
df = pd.read_csv("recipes_small.csv")

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Recipe Recommendation System",
    page_icon="🍲",
    layout="centered"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.main-title{
    font-size:40px;
    font-weight:bold;
    text-align:center;
}
.subtitle{
    text-align:center;
    color:gray;
    margin-bottom:30px;
}
.recipe-card{
    padding:15px;
    border-radius:10px;
    background-color:#1e1e1e;
    margin-bottom:15px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown('<p class="main-title">🍲 Recipe Recommendation System</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Find recipes based on recipe name or ingredients</p>', unsafe_allow_html=True)

# ---------------- MODE SELECTION ----------------
mode = st.selectbox(
    "Choose Recommendation Type",
    ["Recipe Search", "Ingredient Search"]
)

# ---------------- RECIPE SEARCH ----------------
if mode == "Recipe Search":

    recipe_name = st.text_input("Enter Recipe Name")

    if st.button("Recommend Recipes"):

        if recipe_name.strip() == "":
            st.warning("Please enter a recipe name.")
        else:

            recommendations = recommend_recipes(recipe_name)

            if len(recommendations) == 0:
                st.error("No recipes found.")
            else:
                st.subheader("🍽 Recommended Recipes")

                for recipe in recommendations:

                    row = df[df["name"] == recipe]

                    if not row.empty:
                        row = row.iloc[0]

                        st.markdown("---")

                        col1, col2 = st.columns([1,2])

                        with col1:
                            st.image(
                                "https://source.unsplash.com/400x300/?food",
                                use_container_width=True
                            )

                        with col2:
                            st.markdown(f"### {row['name']}")
                            st.write("⏱ Cooking Time:", row["minutes"], "minutes")

                            ingredients = str(row["ingredients"])
                            st.write("🧂 Ingredients:", ingredients[:200], "...")

# ---------------- INGREDIENT SEARCH ----------------
else:

    ingredient_input = st.text_input("Enter Ingredients (space separated)")

    if st.button("Find Recipes"):

        if ingredient_input.strip() == "":
            st.warning("Please enter ingredients.")
        else:

            recipes = recommend_by_ingredients(ingredient_input)

            if len(recipes) == 0:
                st.error("No recipes found.")
            else:
                st.subheader("🍳 Recipes You Can Cook")

                for recipe in recipes:

                    row = df[df["name"] == recipe]

                    if not row.empty:
                        row = row.iloc[0]

                        st.markdown("---")

                        col1, col2 = st.columns([1,2])

                        with col1:
                            st.image(
                                "https://source.unsplash.com/400x300/?dish",
                                use_container_width=True
                            )

                        with col2:
                            st.markdown(f"### {row['name']}")
                            st.write("⏱ Cooking Time:", row["minutes"], "minutes")

                            ingredients = str(row["ingredients"])
                            st.write("🧂 Ingredients:", ingredients[:200], "...")
