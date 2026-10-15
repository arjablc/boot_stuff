package api

type LocationsResponse struct {
	Count    int            `json:"count"`
	Next     *string        `json:"next"`
	Previous *string        `json:"previous"`
	Results  []LocationArea `json:"results"`
}

type LocationArea struct {
	Name string `json:"name"`
	Url  string `json:"url"`
}

type LocationAreaResponse struct {
	EncounterMethodRates []EncounterMethodRate `json:"encounter_method_rates"`
	GameIndex            int                   `json:"game_index"`
	ID                   int                   `json:"id"`
	Location             Location              `json:"location"`
	Name                 string                `json:"name"`
	Names                []NameEntry           `json:"names"`
	PokemonEncounters    []PokemonEncounter    `json:"pokemon_encounters"`
}

type EncounterMethodRate struct {
	EncounterMethod EncounterMethod          `json:"encounter_method"`
	VersionDetails  []EncounterVersionDetail `json:"version_details"`
}

type EncounterMethod struct {
	Name string `json:"name"`
	URL  string `json:"url"`
}

type EncounterVersionDetail struct {
	Rate    int     `json:"rate"`
	Version Version `json:"version"`
}

type Version struct {
	Name string `json:"name"`
	URL  string `json:"url"`
}

type Location struct {
	Name string `json:"name"`
	URL  string `json:"url"`
}

type NameEntry struct {
	Language Language `json:"language"`
	Name     string   `json:"name"`
}

type Language struct {
	Name string `json:"name"`
	URL  string `json:"url"`
}

type PokemonEncounter struct {
	Pokemon        Pokemon                `json:"pokemon"`
	VersionDetails []PokemonVersionDetail `json:"version_details"`
}

type Pokemon struct {
	Name string `json:"name"`
	URL  string `json:"url"`
}

type PokemonVersionDetail struct {
	EncounterDetails []EncounterDetail `json:"encounter_details"`
	MaxChance        int               `json:"max_chance"`
	Version          Version           `json:"version"`
}

type EncounterDetail struct {
	Chance          int           `json:"chance"`
	ConditionValues []interface{} `json:"condition_values"`
	MaxLevel        int           `json:"max_level"`
	Method          Method        `json:"method"`
	MinLevel        int           `json:"min_level"`
}

type Method struct {
	Name string `json:"name"`
	URL  string `json:"url"`
}
