import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import spacy
import re
import os
import requests # Placeholder for actual API calls

# Load English tokenizer, tagger, parser, NER
nlp = spacy.load("en_core_web_sm")

app = FastAPI()

# Store API key securely
RAPIDAPI_KEY = os.environ.get("RAPIDAPI_KEY", "YOUR_DEFAULT_API_KEY")
if RAPIDAPI_KEY == "YOUR_DEFAULT_API_KEY":
    print("Warning: RAPIDAPI_KEY environment variable not set. Using default placeholder.")


class HotelQuery(BaseModel):
    query: str

def extract_travel_info(text: str):
    """
    Extracts destination city and number of travelers from a natural language query.
    """
    doc = nlp(text)
    destination = None
    num_travelers = 1  # Default to 1 traveler

    # Basic entity recognition for cities (GPE - Geopolitical Entity)
    for ent in doc.ents:
        if ent.label_ == "GPE":
            destination = ent.text
            break # Take the first GPE found

    # Regex to find number of friends/people
    # "with 5 of my friends", "for 6 people"
    traveler_match = re.search(r"(?:with|for)\s+(\d+)\s+(?:of my friends|friends|people|travelers)", text, re.IGNORECASE)
    if traveler_match:
        num_travelers = int(traveler_match.group(1))
        if "friends" in traveler_match.group(0).lower(): # "5 of my friends" means 6 people total (user + friends)
             num_travelers += 1


    # More specific pattern for "plan a trip with X friends"
    friends_match = re.search(r"plan a trip with (\d+) of my friends", text, re.IGNORECASE)
    if friends_match:
        num_travelers = int(friends_match.group(1)) + 1 # Add the user

    # Look for number of travelers if not found by "friends"
    if not traveler_match and not friends_match:
        number_match = re.search(r"(\d+)\s*(?:people|travelers|guests)", text, re.IGNORECASE)
        if number_match:
            num_travelers = int(number_match.group(1))

    # If no city is found via NER, try a regex for "in [CITY]"
    if not destination:
        destination_match = re.search(r"in\s+([A-Za-z\s]+)(?:\.|,|\?|$)", text, re.IGNORECASE)
        if destination_match:
            destination = destination_match.group(1).strip()

    return {"destination": destination, "num_travelers": num_travelers}

def get_hotel_suggestions_from_api(city: str, num_guests: int):
    """
    Fetches hotel suggestions from a public API.
    This is a MOCK implementation. Replace with actual API calls.
    """
    print(f"Mock API: Searching for hotels in {city} for {num_guests} guests...")

    # --- Start of example Booking.com API call (Illustrative - Untested) ---
    # This is a conceptual example. You'll need to:
    # 1. Sign up for RapidAPI and subscribe to a hotel API (e.g., Booking.com)
    # 2. Get your RAPIDAPI_KEY
    # 3. Find the correct endpoint and parameters from the API documentation.

    url = "https://booking-com.p.rapidapi.com/v1/hotels/search" # Example endpoint
    querystring = {
        "city_name": city,
        "adults_number": str(num_guests),
        "order_by": "popularity", # or "price", "review_score"
        "units": "metric", # or "imperial"
        "room_number": "1", # Assuming one room for all guests for simplicity
        "checkout_date": "2025-09-28", # Placeholder - ideally get from user
        "checkin_date": "2025-09-27",   # Placeholder - ideally get from user
        "locale": "en-gb",
        "page_number": "0",
        "filter_by_currency": "USD" # Or your preferred currency
    }
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "booking-com.p.rapidapi.com" # Example host
    }

    try:
        # --- MOCK RESPONSE ---
        # In a real scenario, you would make the API call here:
        # response = requests.get(url, headers=headers, params=querystring)
        # response.raise_for_status() # Raise an exception for HTTP errors
        # data = response.json()
        # hotels = data.get("result", []) # Adjust based on actual API response structure

        # For now, returning mock data:
        print(f"Using MOCK data because RAPIDAPI_KEY is '{RAPIDAPI_KEY[:5]}...' or API call is commented out.")
        mock_hotels = [
            {"name": f"Grand Hotel {city}", "price": "150 USD", "link": f"http://example.com/grandhotel{city.lower()}", "rating": "4.5/5"},
            {"name": f"Comfy Inn {city}", "price": "80 USD", "link": f"http://example.com/comfyinn{city.lower()}", "rating": "4.0/5"},
            {"name": f"Luxury Suites {city}", "price": "300 USD", "link": f"http://example.com/luxurysuites{city.lower()}", "rating": "4.8/5"},
            {"name": f"Budget Stay {city}", "price": "50 USD", "link": f"http://example.com/budgetstay{city.lower()}", "rating": "3.5/5"},
            {"name": f"The {city} Resort", "price": "220 USD", "link": f"http://example.com/theresort{city.lower()}", "rating": "4.2/5"},
            {"name": f"Another Option {city}", "price": "120 USD", "link": f"http://example.com/anotheroption{city.lower()}", "rating": "4.1/5"}
        ]
        # Simulate taking top 5
        hotels_to_return = mock_hotels[:5]

        # --- End of MOCK RESPONSE ---


        # --- PROCESSING REAL API RESPONSE (Conceptual) ---
        # processed_hotels = []
        # for hotel in hotels[:5]: # Limiting to 5 results
        #     processed_hotels.append({
        #         "name": hotel.get("name", "N/A"),
        #         "price": f"{hotel.get('min_total_price', 0)} {hotel.get('currencycode', 'USD')}", # Example, adjust to API
        #         "link": hotel.get("url", "N/A"),
        #         "rating": f"{hotel.get('review_score', 'N/A')}/{hotel.get('review_score_word', 'N/A')}" # Example
        #     })
        # return processed_hotels
        # --- End of PROCESSING REAL API RESPONSE ---

        return hotels_to_return # Returning mock data for now

    except requests.exceptions.RequestException as e:
        print(f"Error calling hotel API: {e}")
        # Fallback to more generic mock data if API fails
        return [
            {"name": "Fallback Hotel 1", "price": "100 USD", "link": "http://example.com/fallback1", "rating": "4.0/5"},
            {"name": "Fallback Hotel 2", "price": "120 USD", "link": "http://example.com/fallback2", "rating": "4.1/5"},
        ]
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []


@app.post("/getHotelRecommendations")
async def get_hotel_recommendations_endpoint(hotel_query: HotelQuery):
    """
    Endpoint to get hotel recommendations.
    """
    query = hotel_query.query
    print(f"Received query: {query}")

    extracted_info = extract_travel_info(query)
    print(f"Extracted info: {extracted_info}")

    destination = extracted_info.get("destination")
    num_travelers = extracted_info.get("num_travelers", 1)

    if not destination:
        raise HTTPException(status_code=400, detail="Could not extract destination city from the query. Please specify a city, for example: 'hotels in London'.")

    # Use the mock function for now
    recommendations = get_hotel_suggestions_from_api(destination, num_travelers)

    if not recommendations:
        raise HTTPException(status_code=404, detail=f"Could not find hotel recommendations for {destination}.")

    return recommendations

if __name__ == "__main__":
    # Pass the RAPIDAPI_KEY to the environment for the server
    # In a real deployment, you would set this in your server environment
    os.environ["RAPIDAPI_KEY"] = "36fb8aceaemsh7368d9642bccf00p11b299jsn3846ac2a6ea7" # Set your key here
    print(f"Starting server. RAPIDAPI_KEY set to: {os.environ.get('RAPIDAPI_KEY')[:10]}...") # Print part of the key for confirmation
    uvicorn.run(app, host="127.0.0.1", port=8000) 