package main

import (
	"errors"
	"fmt"
	"math/rand"
	"os"
	"strings"

	"github.com/arjablc/pokedex/internals/api"
	"github.com/arjablc/pokedex/internals/types"
)

type cliCommand struct {
	name        string
	description string
	callback    func(*config, ...string) error
}

type config struct {
	previousUrl *string
	nextUrl     *string
	pokedex     map[string]types.PokemonRes
	areaName    *string
	apiClient   *api.ApiClient
}

func getCommandReg() map[string]cliCommand {
	commands := map[string]cliCommand{
		"help": {
			name:        "help",
			description: "Displays a help message",
			callback:    commandHelp,
		},
		"exit": {
			name:        "exit",
			description: "Exit the Pokedex",
			callback:    commandExit,
		},
		"map": {
			name:        "map",
			description: "Show the location areas or next location areas",
			callback:    commandMap,
		},
		"mapb": {
			name:        "map",
			description: "Show the previous location areas",
			callback:    commandMapb,
		},
		"explore": {
			name:        "explore <location_area>",
			description: "Explore the given area, return the pokemons found",
			callback:    commandExplore,
		},
		"catch": {
			name:        "catch <pokemon_name>",
			description: "Catch a pokemon",
			callback:    commandCatch,
		},
		"pokedex": {
			name:        "pokedex ",
			description: "Show caught pokemon",
			callback:    commandPokedex,
		},
		"inspect": {
			name:        "inspect <pokemon_name>",
			description: "Show Pokemon inof",
			callback:    commandInspect,
		},
	}
	return commands
}

func cleanInput(text string) []string {
	out := strings.ToLower(text)
	words := strings.Fields(out)
	return words
}

func commandHelp(config *config, args ...string) error {
	fmt.Println("Welcome to the Pokedex!")
	fmt.Println("Usage:")
	fmt.Println("help: Displays a help message")
	fmt.Println("exit: Exit the Pokedex")
	return nil
}

func commandExit(config *config, args ...string) error {
	fmt.Println("Closing the Pokedex... Goodbye!")
	os.Exit(0)
	return nil
}

func commandMapb(config *config, args ...string) error {
	url := config.previousUrl
	if url == nil {
		println("You're on the first page")
		return nil
	}
	locationResponse := config.apiClient.RequestLocationArea(*url)
	config.nextUrl = locationResponse.Next
	config.previousUrl = locationResponse.Previous
	for _, location := range locationResponse.Results {
		println(location.Name)
	}
	return nil
}

func commandMap(config *config, args ...string) error {
	url := config.nextUrl
	if url == nil {
		url = &api.LocationsUrl
	}
	locationResponse := config.apiClient.RequestLocationArea(*url)
	config.nextUrl = locationResponse.Next
	config.previousUrl = locationResponse.Previous
	for _, location := range locationResponse.Results {
		println(location.Name)
	}
	return nil
}

func commandExplore(config *config, args ...string) error {
	if len(args) != 1 {
		return errors.New("No location provided")
	}
	locationName := args[0]
	url := config.nextUrl
	if url == nil {
		url = &api.LocationsUrl
	}
	pokemonsResponse := config.apiClient.RequestLocationAreaInfo(locationName)
	for _, pokemon := range pokemonsResponse.PokemonEncounters {
		fmt.Println(pokemon.Pokemon.Name)
	}
	return nil
}

func commandCatch(config *config, args ...string) error {
	if len(args) != 1 {
		return errors.New("No Pokemon Name provided")
	}
	pokemonName := args[0]
	fmt.Printf("Throwing a Pokeball at %s...\n", pokemonName)
	pokemonsResponse := config.apiClient.RequestPokemonInfo(pokemonName)
	res := rand.Intn(pokemonsResponse.BaseExperience)
	if res > 40 {
		fmt.Printf("%s was caught!\n", pokemonName)
		config.pokedex[pokemonName] = pokemonsResponse
	} else {
		fmt.Printf("%s escaped!\n", pokemonName)
	}
	return nil
}

func commandPokedex(config *config, args ...string) error {
	fmt.Println("Your pokedex:")
	for key, _ := range config.pokedex {
		fmt.Println("- ", key)
	}
	return nil

}

func commandInspect(config *config, args ...string) error {
	if len(args) != 1 {
		return errors.New("No pokemon name provided")
	}
	pokemonName := args[0]
	if pokemon, ok := config.pokedex[pokemonName]; !ok {
		return errors.New("you have not caught that pokemon")
	} else {
		printPokemonData(pokemon)
	}

	return nil

}

func printPokemonData(pokemon types.PokemonRes) {
	fmt.Println("Name: ", pokemon.Name)
	fmt.Println("Height: ", pokemon.Height)
	fmt.Println("Weight: ", pokemon.Weight)
	fmt.Println("Stats:")
	for _, stat := range pokemon.Stats {
		fmt.Println("- ", stat.Stat.Name, ": ", stat.BaseStat)
	}
	fmt.Println("Types:")
	for _, pType := range pokemon.Types {
		fmt.Println("- ", pType.Type.Name)
	}
}
