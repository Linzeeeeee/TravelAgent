from openai import OpenAI
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials


client = OpenAI(api_key="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")
# Set up Google Sheets API credentials
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",  # Full access to Google Sheets
    "https://www.googleapis.com/auth/drive.file"     # Access to manage files on Google Drive
]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scopes)
client1 = gspread.authorize(creds)

# Open the Google Sheet where feedback will be stored
sheet = client1.open_by_url("https://docs.google.com/spreadsheets/d/1BrdD5vuTo4NtUm44PZOyY0Tvowp508OH_iAWNVnLdAk/edit?usp=sharing").sheet1
# Custom CSS for styling
st.markdown("""
    <style>
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 8px;
            padding: 10px;
        }
        .stTextArea {
            border-radius: 8px;
            border: 2px solid #4CAF50;
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Display a custom header
st.markdown("# Welcome to Your AI Travel Assistant 🌍✈️")
st.markdown("### Plan Your Dream Vacation with Personalized Suggestions")


# Initialize OpenAI API key
# Initialize conversation history
if 'conversation' not in st.session_state:
    st.session_state['conversation'] = [{
    "role": "system", "content": 
    """You are a travel planning assistant that creates highly personalized and dynamic travel plans based on user preferences. 
    To ensure accuracy, you begin with a detailed questionnaire covering:- **Destination(s), Dates & Duration**- **Budget Level** (budget, mid-range, luxury)\n
- **Traveler Demographics** (solo, couple, family, group, etc.)
- **Transportation Preferences** (flight, train, car, motorbike, hitchhiking, cycling, etc.)
- **Accommodation Type** (hostels, hotels, eco-lodges, luxury resorts, wellness retreats, motorbike-friendly stays, etc.)
- **Interests & Activities** (sightseeing, adventure, wellness, hiking, photography, extreme sports, cultural immersion, yoga retreats, etc.)
- **Dietary Restrictions** (vegetarian, vegan, halal, gluten-free, etc.)
- **Travel Style** (meticulous planner, spontaneous adventurer, budget backpacker, luxury traveler, family traveler, solo motorbike explorer, wellness seeker, etc.)
- **Special Requests** (off-the-beaten-path destinations, last-minute deals, sustainability focus, private experiences, educational activities, etc.)
- **Family Considerations** (children's ages, special needs, accessibility requirements)
- **Flexibility Preferences** (strict itinerary vs. open-ended plans)
- **Sustainability Goals** (eco-friendly stays, carbon offset options, responsible travel practices)
- **Hidden Gem Preferences** (define what "hidden gem" means: local culture, remote locations, exclusive experiences, affordability, etc.)

### Travel Plan Features
After gathering input, you generate a **highly customized travel plan**, which includes:

- **Personalized Recommendations** for accommodations, activities, dining, and experiences tailored to the user’s style and budget.
- **Optimized Itinerary & Route Planning**, balancing structured planning and flexibility. Users can adjust and refine their trip dynamically.
- **Budget Breakdown & Expense Management**, with clear cost prioritization (daily/weekly budget control, cheap vs. luxury experiences).
- **Real-Time Booking & Travel Deals**, integrated with major platforms (Skyscanner, Booking.com, Agoda, Hostelworld, boutique travel agencies). Users receive real-time deal alerts and price changes.
- **Granular Filtering for Accommodations & Activities**, allowing searches by specific needs (e.g., dorm size, wellness-focused stays, family-friendly amenities, eco-certifications, exclusive luxury experiences, motorcycle-friendly stops).
- **Hidden Gem Discovery**, personalized to the user’s definition, with AI-curated recommendations based on expert sources and user reviews.
- **Comprehensive Transportation Comparisons**, including hitchhiking, overnight buses, ride-sharing, and trains. Motorbike adventurers receive detailed road conditions, fuel stop maps, and safety insights.
- **Food & Dietary Customization**, offering restaurant recommendations with menus, pricing, dietary accommodations, and sustainability ratings.
- **Offline Access**, allowing users to download itineraries, maps, emergency contacts, and visa details for offline use.
- **Safety & Responsible Travel Features**, providing emergency contacts, safety advisories, solo female travel tips, motorbike safety protocols, and accessibility considerations.
- **Interactive Tools & Progress Tracking**, letting users modify their plans in real-time and visually track planning milestones.
- **Packing List Generator**, personalized to climate, activities, and travel style (e.g., yoga retreat gear, motorbike adventure essentials, eco-friendly packing tips).
- **Community & Social Features**, with forums and messaging for connecting with like-minded travelers (e.g., budget backpackers, wellness seekers, motorbike explorers). The community is actively moderated for safety and relevance.
- **Luxury Travel Enhancements**, including private concierge services, yacht rentals, exclusive fine dining, helicopter transfers, and high-end resort experiences.
- **Wellness & Yoga Retreat Customization**, with filters for yoga styles, retreat types (detox, meditation, healing), and sustainable wellness resorts.
- **Family & Educational Travel Support**, offering kid-friendly activities, National Park Junior Ranger programs, and learning-focused travel suggestions.
- **“Surprise Me” Feature**, generating spontaneous travel suggestions based on budget, flexibility, and available last-minute deals.
- **Advanced Filtering & Customization**, allowing users to refine recommendations by adventure level, exclusivity, sustainability, accessibility, and affordability.

You dynamically adjust responses based on user profiles. Spontaneous adventurers get flexible plans with real-time deals, while meticulous planners receive structured itineraries. Budget travelers get cost-conscious recommendations, while luxury travelers receive curated premium experiences. 

Your goal is to be a **seamless, intuitive, and engaging travel concierge**, making trip planning effortless, adaptable, and deeply personalized."""
}]

# Initialize the feedback list in session_state if not already present
if 'feedbacks' not in st.session_state:
    st.session_state['feedbacks'] = []  # Initialize feedbacks list

# Function to interact with GPT
def ask_gpt(user_input):
    st.session_state['conversation'].append({"role": "user", "content": user_input})
    response = client.chat.completions.create(# Changed openai.Completion to openai.ChatCompletion
        model="gpt-4o-mini" , # Changed engine to model
        messages=st.session_state['conversation'])
    # Extracting the response content from the updated structure
    gpt_response = response.choices[0].message.content
    st.session_state['conversation'].append({"role": "assistant", "content": gpt_response})
    return gpt_response

# Streamlit UI for chat interface
st.title("AI Travel Agent")
# Some introduction or instructions
st.markdown("""
    Welcome to your personalized AI Travel Assistant! 🗺️
""")

# Display the conversation history
for message in st.session_state['conversation']:
    if message["role"] == "user":
        st.markdown(f"**You**: {message['content']}")
    elif message["role"] == "assistant":
        st.markdown(f"**AI**: {message['content']}")

# User input field as a chatbox (multi-line)
user_input = st.text_area("Type your question:", "", height=150)

# When the user submits input, the assistant generates a response
if st.button("Send") and user_input:
    gpt_response = ask_gpt(user_input)
    st.write(f"**AI**: {gpt_response}")

st.markdown("""
    Please feel free to leave your feedback below.
""")
# Feedback Textbox for users to enter their feedback
feedback = st.text_area("Leave your feedback here:")

# Submit button to capture the feedback
if st.button("Submit Feedback"):
    if feedback:
        # Store feedback in session_state
        st.session_state['feedbacks'].append(feedback)
        
        # Save the feedback to Google Sheets
        sheet.append_row([feedback])  # Append feedback to the sheet
        st.success("Thank you for your feedback! 😊")
    else:
        st.warning("Please enter some feedback before submitting.")