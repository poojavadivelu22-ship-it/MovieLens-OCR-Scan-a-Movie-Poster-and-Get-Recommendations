import streamlit as st
from PIL import Image

from ocr import extract_text_from_image
from recommender import find_closest_title, recommend_movies


st.set_page_config(
    page_title="MovieLens OCR",
    page_icon=""
)

st.title(" MovieLens OCR")
st.write("Upload a movie poster and get movie recommendations")


# Upload movie poster
uploaded_file = st.file_uploader(
    "Upload Movie Poster",
    type=["jpg", "jpeg", "png"]
)


if uploaded_file is not None:

    # Display uploaded image
    image = Image.open(uploaded_file)

    st.image(
        image,
        caption="Uploaded Movie Poster",
        width=300
    )

    # Extract text button
    if st.button(" Detect Movie"):

        with st.spinner("Reading movie poster..."):

            extracted_text = extract_text_from_image(image)

        st.subheader(" Detected Text")

        st.write(extracted_text)

        # Find closest movie title
        matched_title, score = find_closest_title(extracted_text)

        if matched_title and score >= 30:

            st.success(
                f" Movie Found: {matched_title}"
            )

            st.write(
                f"Matching Score: {score:.2f}%"
            )

            # Recommendations
            recommendations = recommend_movies(
                matched_title,
                5
            )

            st.subheader(" Top 5 Movie Recommendations")

            for i, movie in enumerate(
                recommendations,
                start=1
            ):

                st.write(
                    f"### {i}. {movie['title']}"
                )

                st.write(
                    f"Similarity: {movie['score']}%"
                )

                st.write(
                    f"Genre: {movie['genres']}"
                )

                st.write(
                    f"Overview: {movie['overview']}"
                )

                st.divider()

        else:

            st.error(
                " Movie title could not be detected."
            )

            st.info(
                "Try uploading a clear movie poster."
            )