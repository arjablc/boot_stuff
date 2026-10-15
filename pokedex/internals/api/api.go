package api

import (
	"encoding/json"
	"io"
	"log"
	"net/http"

	"github.com/arjablc/pokedex/internals/pokecache"
	"github.com/arjablc/pokedex/internals/types"
)

type ApiClient struct {
	Cache *pokecache.Cache
}

func (client *ApiClient) RequestLocationArea(url string) LocationsResponse {
	value, exists := client.Cache.Get(url)
	var body []byte
	if exists {
		body = value
	} else {
		res, err := http.Get(url)
		if err != nil {
			log.Fatal(err)
		}
		resBody, err := io.ReadAll(res.Body)
		defer res.Body.Close()
		if res.StatusCode > 299 {
			log.Fatalf("Failed with status code: %d and body %s", res.StatusCode, resBody)
		}
		client.Cache.Add(url, resBody)
		body = resBody
	}
	var result LocationsResponse
	if err := json.Unmarshal(body, &result); err != nil {
		log.Fatal("Failed to unmarshal")
	}
	return result
}

func (client *ApiClient) RequestLocationAreaInfo(areaName string) LocationAreaResponse {
	url := LocationsUrl + areaName
	value, exists := client.Cache.Get(url)
	var body []byte
	if exists {
		body = value
	} else {
		res, err := http.Get(url)
		if err != nil {
			log.Fatal(err)
		}
		resBody, err := io.ReadAll(res.Body)
		defer res.Body.Close()
		if res.StatusCode > 299 {
			log.Fatalf("Failed with status code: %d and body %s", res.StatusCode, resBody)
		}
		client.Cache.Add(url, resBody)
		body = resBody
	}
	var result LocationAreaResponse
	if err := json.Unmarshal(body, &result); err != nil {
		log.Fatal("Failed to unmarshal")
	}
	return result
}

func (client *ApiClient) RequestPokemonInfo(pokemonName string) types.PokemonRes {
	url := PokemonBaseUrl + pokemonName
	value, exists := client.Cache.Get(url)
	var body []byte
	if exists {
		body = value
	} else {
		res, err := http.Get(url)
		if err != nil {
			log.Fatal(err)
		}
		resBody, err := io.ReadAll(res.Body)
		defer res.Body.Close()
		if res.StatusCode > 299 {
			log.Fatalf("Failed with status code: %d and body %s", res.StatusCode, resBody)
		}
		client.Cache.Add(url, resBody)
		body = resBody
	}
	var result types.PokemonRes
	if err := json.Unmarshal(body, &result); err != nil {
		log.Fatal("Failed to unmarshal")
	}
	return result
}
