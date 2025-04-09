import logging
from typing import Optional, Literal, Any
from collections.abc import Callable
import httpx
from openai.types.responses import FunctionToolParam
from openai.types import ResponsesModel
from pydantic import BaseModel, Field

from crypto_app.agents.agent import Agent
from crypto_app.agents.prompts import CMC_PROMPT_V3

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cryptocurrency
# - Categories
# - Category
# - CoinMarketCap ID Map
# - Metadata
# - Listings Latest
# - Quotes Latest

COINMARKETCAP_API_URL = "https://pro-api.coinmarketcap.com"


class CategoriesParams(BaseModel):
    start: Optional[int] = Field(
        description="""Integer >= 1; Default: 1; Optionally offset the start (1-based index) of the paginated list of items to return.""",
    )
    limit: Optional[int] = Field(
        description="""Integer [ 1 .. 5000 ]; Optionally specify the number of results to return. Use this parameter and the "start" parameter to determine your own pagination size.""",
    )
    symbol: str = Field(
        description="""Filter categories one or more comma-separated cryptocurrency symbols. Example: "BTC,ETH".""",
    )

    model_config = {
        "extra": "forbid",
    }


class CategoryParams(BaseModel):
    id: str = Field(
        description="""The Category ID. This can be found using the Categories API.""",
    )
    start: Optional[int] = Field(
        description="""Intger >= 1; Default: 1; Optionally offset the start (1-based index) of the paginated list of coins to return.""",
    )
    limit: Optional[int] = Field(
        description="""Integer [ 1 .. 1000]; Default: 100; Optionally specify the number of coins to return. Use this parameter and the "start" parameter to determine your own pagination size.""",
    )
    convert: Optional[str] = Field(
        description="""Optionally calculate market quotes in up to 120 currencies at once by passing a comma-separated list of cryptocurrency or fiat currency symbols. Each additional convert option beyond the first requires an additional call credit. Each conversion is returned in its own "quote" object.""",
    )

    model_config = {
        "extra": "forbid",
    }


class CoinMarketCapIDMapParams(BaseModel):
    listing_status: Optional[str] = Field(
        description="""Deafult: "active"; Only active cryptocurrencies are returned by default. Pass inactive to get a list of cryptocurrencies that are no longer active. Pass untracked to get a list of cryptocurrencies that are listed but do not yet meet methodology requirements to have tracked markets available. You may pass one or more comma-separated values.""",
    )
    start: Optional[int] = Field(
        description="""Integer >= 1; Default: 1; Optionally offset the start (1-based index) of the paginated list of items to return.""",
    )
    limit: Optional[int] = Field(
        description="""Integer [ 1 .. 5000 ]; Optionally specify the number of results to return. Use this parameter and the "start" parameter to determine your own pagination size.""",
    )
    sort: Optional[Literal["cmc_rank", "id"]] = Field(
        description="""Default: "id"; What field to sort the list of cryptocurrencies by.""",
    )
    symbol: Optional[str] = Field(
        description="""Optionally pass a comma-separated list of cryptocurrency symbols to return CoinMarketCap IDs for. If this option is passed, other options will be ignored.""",
    )
    aux: Optional[str] = Field(
        description="""Default: "platform,first_historical_data,last_historical_data,is_active"; Optionally specify a comma-separated list of supplemental data fields to return. Pass platform,first_historical_data,last_historical_data,is_active,status to include all auxiliary fields.""",
    )

    model_config = {
        "extra": "forbid",
    }


class MetadataParams(BaseModel):
    symbol: str = Field(
        description="""Pass one or more comma-separated cryptocurrency symbols. Example: "BTC,ETH". At least one "id" or "slug" or "symbol" is required for this request. Please note that starting in the v2 endpoint, due to the fact that a symbol is not unique, if you request by symbol each data response will contain an array of objects containing all of the coins that use each requested symbol. The v1 endpoint will still return a single object, the highest ranked coin using that symbol.""",
    )

    skip_invalid: Optional[bool] = Field(
        description="""Default: false; Pass true to relax request validation rules. When requesting records on multiple cryptocurrencies an error is returned if any invalid cryptocurrencies are requested or a cryptocurrency does not have matching records in the requested timeframe. If set to true, invalid lookups will be skipped allowing valid cryptocurrencies to still be returned.""",
    )
    aux: Optional[str] = Field(
        description="""Default: "urls,logo,description,tags,platform,date_added,notice"; Optionally specify a comma-separated list of supplemental data fields to return. Pass urls,logo,description,tags,platform,date_added,notice,status to include all auxiliary fields.""",
    )

    model_config = {
        "extra": "forbid",
    }


class ListingsLatest(BaseModel):
    start: Optional[int] = Field(
        description="""Integer >= 1; Default: 1; Optionally offset the start (1-based index) of the paginated list of items to return.""",
    )
    limit: Optional[int] = Field(
        description="""Integer [ 1 .. 5000 ]; Default: 100; Optionally specify the number of results to return. Use this parameter and the "start" parameter to determine your own pagination size.""",
    )
    price_min: Optional[float] = Field(
        description="""Number [ 0 .. 100000000000000000 ]; Optionally specify a threshold of minimum USD price to filter results by.""",
    )
    price_max: Optional[float] = Field(
        description="""Number [ 0 .. 100000000000000000 ]; Optionally specify a threshold of maximum USD price to filter results by.""",
    )
    market_cap_min: Optional[float] = Field(
        description="""Number [ 0 .. 100000000000000000 ]; Optionally specify a threshold of minimum market cap to filter results by.""",
    )
    market_cap_max: Optional[float] = Field(
        description="""Number [ 0 .. 100000000000000000 ]; Optionally specify a threshold of maximum market cap to filter results by.""",
    )
    volume_24h_min: Optional[float] = Field(
        description="""Number [ 0 .. 100000000000000000 ]; Optionally specify a threshold of minimum 24 hour USD volume to filter results by.""",
    )
    volume_24h_max: Optional[float] = Field(
        description="""Number [ 0 .. 100000000000000000 ]; Optionally specify a threshold of maximum 24 hour USD volume to filter results by.""",
    )
    circulating_supply_min: Optional[float] = Field(
        description="""Number [ 0 .. 100000000000000000 ]; Optionally specify a threshold of minimum circulating supply to filter results by.""",
    )
    circulating_supply_max: Optional[float] = Field(
        description="""Number [ 0 .. 100000000000000000 ]; Optionally specify a threshold of maximum circulating supply to filter results by.""",
    )
    percent_change_24h_min: Optional[float] = Field(
        description="""Number >= -100; Optionally specify a threshold of minimum 24 hour percent change to filter results by.""",
    )
    percent_change_24h_max: Optional[float] = Field(
        description="""Number >= -100; Optionally specify a threshold of maximum 24 hour percent change to filter results by.""",
    )
    self_reported_circulating_supply_min: Optional[float] = Field(
        description="""Number [ 0 .. 100000000000000000 ]; Optionally specify a threshold of minimum self reported circulating supply to filter results by.""",
    )
    self_reported_circulating_supply_max: Optional[float] = Field(
        description="""Number [ 0 .. 100000000000000000 ]; Optionally specify a threshold of maximum self reported circulating supply to filter results by.""",
    )
    self_reported_market_cap_min: Optional[float] = Field(
        description="""Number [ 0 .. 100000000000000000 ]; Optionally specify a threshold of minimum self reported market cap to filter results by.""",
    )
    self_reported_market_cap_max: Optional[float] = Field(
        description="""Number [ 0 .. 100000000000000000 ]; Optionally specify a threshold of maximum self reported market cap to filter results by.""",
    )
    unlocked_market_cap_min: Optional[float] = Field(
        description="""Number [ 0 .. 100000000000000000 ]; Optionally specify a threshold of minimum unlocked market cap to filter results by.""",
    )
    unlocked_market_cap_max: Optional[float] = Field(
        description="""Number [ 0 .. 100000000000000000 ]; Optionally specify a threshold of maximum unlocked market cap to filter results by.""",
    )
    unlocked_circulating_supply_min: Optional[float] = Field(
        description="""Number [ 0 .. 100000000000000000 ]; Optionally specify a threshold of minimum unlocked circulating supply to filter results by.""",
    )
    unlocked_circulating_supply_max: Optional[float] = Field(
        description="""Number [ 0 .. 100000000000000000 ]; Optionally specify a threshold of maximum unlocked circulating supply to filter results by.""",
    )
    convert: Optional[str] = Field(
        description="""Optionally calculate market quotes in up to 120 currencies at once by passing a comma-separated list of cryptocurrency or fiat currency symbols. Each additional convert option beyond the first requires an additional call credit. Each conversion is returned in its own "quote" object.""",
    )
    sort: Optional[
        Literal[
            "name",
            "symbol",
            "date_added",
            "market_cap",
            "market_cap_strict",
            "price",
            "circulating_supply",
            "total_supply",
            "max_supply",
            "num_market_pairs",
            "volume_24h",
            "percent_change_1h",
            "percent_change_24h",
            "percent_change_7d",
            "market_cap_by_total_supply_strict",
            "volume_7d",
            "volume_30d",
        ]
    ] = Field(
        description="""Default: "market_cap"; What field to sort the list of cryptocurrencies by.""",
    )
    sort_dir: Optional[Literal["asc", "desc"]] = Field(
        description="""The direction in which to order cryptocurrencies against the specified sort.""",
    )
    cryptocurrency_type: Optional[Literal["all", "coins", "tokens"]] = Field(
        description="""Default: "all"; The type of cryptocurrency to include.""",
    )
    tag: Optional[Literal["all", "defi", "filesharing"]] = Field(
        description="""Default: "all"; The tag of cryptocurrency to include.""",
    )

    model_config = {
        "extra": "forbid",
    }


class QuotesLatestParams(BaseModel):
    symbol: str = Field(
        description="""Pass one or more comma-separated cryptocurrency symbols. Example: "BTC,ETH". At least one "id" or "slug" or "symbol" is required for this request.""",
    )
    convert: Optional[str] = Field(
        description="""Optionally calculate market quotes in up to 120 currencies at once by passing a comma-separated list of cryptocurrency or fiat currency symbols. Each additional convert option beyond the first requires an additional call credit. A list of supported fiat options can be found here. Each conversion is returned in its own "quote" object.""",
    )
    skip_invalid: Optional[bool] = Field(
        description="""Default: true; Pass true to relax request validation rules. When requesting records on multiple cryptocurrencies an error is returned if no match is found for 1 or more requested cryptocurrencies. If set to true, invalid lookups will be skipped allowing valid cryptocurrencies to still be returned.""",
    )

    model_config = {
        "extra": "forbid",
    }


FUNCTIONS: list[FunctionToolParam] = [
    {
        "type": "function",
        "name": "categories",
        "strict": True,
        "parameters": CategoriesParams.model_json_schema(),
        "description": """Returns information about all coin categories available on CoinMarketCap. Includes a paginated list of cryptocurrency quotes and metadata from each category.""",
    },
    {
        "type": "function",
        "name": "category",
        "strict": True,
        "parameters": CategoryParams.model_json_schema(),
        "description": """Returns information about a single coin category available on CoinMarketCap. Includes a paginated list of the cryptocurrency quotes and metadata for the category.""",
    },
    {
        "type": "function",
        "name": "coinmarketcap_id_map",
        "strict": True,
        "parameters": CoinMarketCapIDMapParams.model_json_schema(),
        "description": """
Returns a mapping of all cryptocurrencies to unique CoinMarketCap ids. Per our Best Practices we recommend utilizing CMC ID instead of cryptocurrency symbols to securely identify cryptocurrencies with our other endpoints and in your own application logic. Each cryptocurrency returned includes typical identifiers such as name, symbol, and token_address for flexible mapping to id.
By default this endpoint returns cryptocurrencies that have actively tracked markets on supported exchanges. You may receive a map of all inactive cryptocurrencies by passing listing_status=inactive. You may also receive a map of registered cryptocurrency projects that are listed but do not yet meet methodology requirements to have tracked markets via listing_status=untracked. Please review our methodology documentation for additional details on listing states.
Cryptocurrencies returned include first_historical_data and last_historical_data timestamps to conveniently reference historical date ranges available to query with historical time-series data endpoints. You may also use the aux parameter to only include properties you require to slim down the payload if calling this endpoint frequently.
""",
    },
    {
        "type": "function",
        "name": "metadata",
        "strict": True,
        "parameters": MetadataParams.model_json_schema(),
        "description": """Returns all static metadata available for one or more cryptocurrencies. This information includes details like logo, description, official website URL, social links, and links to a cryptocurrency's technical documentation.""",
    },
    {
        "type": "function",
        "name": "listings_latest",
        "strict": True,
        "parameters": ListingsLatest.model_json_schema(),
        "description": """
Returns a paginated list of all active cryptocurrencies with latest market data. The default "market_cap" sort returns cryptocurrency in order of CoinMarketCap's market cap rank (as outlined in our methodology) but you may configure this call to order by another market ranking field. Use the "convert" option to return market values in multiple fiat and cryptocurrency conversions in the same call.
You may sort against any of the following:
market_cap: CoinMarketCap's market cap rank as outlined in our methodology.
market_cap_strict: A strict market cap sort (latest trade price x circulating supply).
name: The cryptocurrency name.
symbol: The cryptocurrency symbol.
date_added: Date cryptocurrency was added to the system.
price: latest average trade price across markets.
circulating_supply: approximate number of coins currently in circulation.
total_supply: approximate total amount of coins in existence right now (minus any coins that have been verifiably burned).
max_supply: our best approximation of the maximum amount of coins that will ever exist in the lifetime of the currency.
num_market_pairs: number of market pairs across all exchanges trading each currency.
market_cap_by_total_supply_strict: market cap by total supply.
volume_24h: rolling 24 hour adjusted trading volume.
volume_7d: rolling 24 hour adjusted trading volume.
volume_30d: rolling 24 hour adjusted trading volume.
percent_change_1h: 1 hour trading price percentage change for each currency.
percent_change_24h: 24 hour trading price percentage change for each currency.
percent_change_7d: 7 day trading price percentage change for each currency.
""",
    },
    {
        "type": "function",
        "name": "quotes_latest",
        "strict": True,
        "parameters": QuotesLatestParams.model_json_schema(),
        "description": """Returns the latest market quote for 1 or more cryptocurrencies. Use the "convert" option to return market values in multiple fiat and cryptocurrency conversions in the same call.""",
    },
]


class CoinMarketAgent(Agent):
    def __init__(
        self,
        openai_api_key: str,
        coimarketcap_api_key: str,
        model: ResponsesModel = "gpt-4o-mini",
    ):
        super().__init__(
            openai_api_key, model=model, tools=FUNCTIONS, system_prompt=CMC_PROMPT_V3
        )
        self._coimarketcap_api_key = coimarketcap_api_key

    def _categories(self, params):
        return httpx.get(
            f"{COINMARKETCAP_API_URL}/v1/cryptocurrency/categories",
            headers={
                "X-CMC_PRO_API_KEY": self._coimarketcap_api_key,
            },
            params=params,
        )

    def _category(self, params):
        return httpx.get(
            f"{COINMARKETCAP_API_URL}/v1/cryptocurrency/category",
            headers={
                "X-CMC_PRO_API_KEY": self._coimarketcap_api_key,
            },
            params=params,
        )

    def _coinmarketcap_id_map(self, params):
        return httpx.get(
            f"{COINMARKETCAP_API_URL}/v1/cryptocurrency/map",
            headers={
                "X-CMC_PRO_API_KEY": self._coimarketcap_api_key,
            },
            params=params,
        )

    def _metadata(self, params):
        return httpx.get(
            f"{COINMARKETCAP_API_URL}/v2/cryptocurrency/info",
            headers={
                "X-CMC_PRO_API_KEY": self._coimarketcap_api_key,
            },
            params=params,
        )

    def _listings_latest(self, params):
        return httpx.get(
            f"{COINMARKETCAP_API_URL}/v1/cryptocurrency/listings/latest",
            headers={
                "X-CMC_PRO_API_KEY": self._coimarketcap_api_key,
            },
            params=params,
        )

    def _quotes_latest(self, params):
        return httpx.get(
            f"{COINMARKETCAP_API_URL}/v2/cryptocurrency/quotes/latest",
            headers={ 
                'Accepts': 'application/json',
                "X-CMC_PRO_API_KEY": self._coimarketcap_api_key,
            },
            params=params,
        )

    def _call_function(self, function_name, params):
        functions: dict[str, Callable[[Any], httpx.Response]] = {
            "categories": self._categories ,
            "category": self._category,
            "coinmarketcap_id_map": self._coinmarketcap_id_map,
            "metadata": self._metadata,
            "listings_latest": self._listings_latest,
            "quotes_latest": self._quotes_latest,
        }
        if function_name not in functions:
            logger.error("function-not-found=%s", function_name)
            raise Exception(f"Function '{function_name}' does not exist")
        params = { k: v for k, v in params.items() if v is not None }
        response = functions[function_name](params)
        if response.status_code != 200:
            logger.error(
                "copinmarketcap-request function-name=%s status-code=%d",
                function_name,
                response.status_code,
            )
            raise Exception(
                f"Request to '{function_name}' failed with params '{params}'"
            )
        return response.json()
