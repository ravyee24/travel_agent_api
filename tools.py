from dotenv import load_dotenv
from models import llm
from langchain_core.tools import tool
from tavily import TavilyClient
import os

load_dotenv()


tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

#MAKING THE FLIGHT SEARCH TOOL
@tool
def GetFlight(
    current_loc: str,
    destination_loc: str,
    date: str
) -> str:
    """Search for flights between two locations on a given date."""

    query = f"""
    Find flights from {current_loc} to {destination_loc}
    on {date}.

    Return:
    - Airline
    - Departure time
    - Arrival time
    - Price
    - Currency
    - Source URL

    Do not invent information.
    """

    response = tavily.search(
        query=query,
        max_results=3,
        search_depth="advanced"
    )

    results = []

    for item in response.get("results", []):
        results.append({
            "title": item.get("title"),
            "url": item.get("url"),
            "content": item.get("content", "")[:1000]
        })

    return str(results)



#MAKING THE TOOL FOR HOTELS
@tool
def GetHotels(address: str) -> str:
    """Search hotels and return concise hotel information."""

    prompt = f"""
    Find hotels in {address}.

    For each hotel, provide:
    - Hotel name
    - Star rating
    - Price per night
    - Currency
    - Source URL

    Do not invent information.
    """

    response = tavily.search(
        query=prompt,
        max_results=3,
        search_depth="advanced"
    )

    results = []

    for item in response.get("results", []):
        results.append({
            "title": item.get("title"),
            "url": item.get("url"),
            "content": item.get("content", "")[:1000]
        })

    return str(results)

#MAKING TOOL FOR SEARCH PLACES.
@tool
def GetPlaces(destination: str) -> str:
    """Find attractions and popular things to do in a destination."""

    prompt = f"""
    Find famous places to visit in {destination}.

    For each place provide:
    - Name
    - Why it is famous
    - Main activities
    - Approximate cost if available
    - Source URL

    Do not invent information.
    """

    response = tavily.search(
        query=prompt,
        max_results=4,
        search_depth="advanced"
    )

    results = []

    for item in response.get("results", []):
        results.append({
            "title": item.get("title"),
            "url": item.get("url"),
            "content": item.get("content", "")[:1000]
        })

    return str(results)


# MAKING TOOL FOR CALCULATING BUDGET
@tool
def CalculateBudget(
    flight: float,
    hotel: float,
    place_visit: float,
    food_estimate: float,
    total_budget: float
) -> dict:
    """Calculate total trip expenses and compare them with the user's budget."""

    total_cost = flight + hotel + place_visit + food_estimate
    remaining = total_budget - total_cost

    return {
        "flight": flight,
        "hotel": hotel,
        "places": place_visit,
        "food": food_estimate,
        "total_cost": total_cost,
        "total_budget": total_budget,
        "remaining": remaining,
        "within_budget": remaining >= 0
    }



# #MAKING THE TOOL FOR CREATING THE ITINERARY
# @tool
# def CreateItinerary(flight_data:str,
#                     hotel_data:str,
#                     places_to_visit:str,
#                     budget:str
#                     ) -> str:
#     """ Create a schedule for trip details."""

#     prompts = f"""
#     Create a complete travel itinerary using the information below.

#     FLIGHT DETAILS:
#     {flight_data}

#     HOTEL DETAILS:
#     {hotel_data}

#     PLACES TO VISIT:
#     {places_to_visit}

#     BUDGET DETAILS:
#     {budget}

#     Create the itinerary with:

#     1. Flight details
#        - Origin
#        - Destination
#        - Date
#        - Time
#        - Price
#        - Airline

#     2. Hotel details
#        - Hotel name
#        - Location
#        - Price per night
#        - Star rating

#     3. Day-by-day itinerary
#        - Places to visit each day
#        - Things to do
#        - Popular food
#        - Cultural experiences

#     4. Budget summary
#        - Total budget
#        - Flight cost
#        - Hotel cost
#        - Food cost
#        - Activity cost
#        - Total expenses
#        - Remaining budget

#     5. If the trip is over budget, suggest cheaper alternatives.

#     Do not invent information that is not present in the provided data.
#     """

#     response = llm.invoke(prompts)

#     return f"The necessary itinerary for the trip is{response.content}."

